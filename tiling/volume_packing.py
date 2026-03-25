"""
volume_packing.py — 3D Heptahedral Volume Packing
===================================================

Build actual convex heptahedra in 3D and pack them face-to-face.
The face-matching Monte Carlo showed all 60 orientations survive
junction rules. This script tests the GEOMETRIC constraint:
tiles cannot physically overlap in 3D space.

Method:
  1. Construct heptahedron via half-space intersection (H-rep → V-rep)
  2. Place seed at origin
  3. For each face, translate+rotate a neighbor to share that face
  4. Check overlap with ALL placed tiles using Separating Axis Theorem
  5. Count valid (non-overlapping + allowed junction) orientations
  6. Track spatial pattern of placed tiles for helix/vortex detection

Run:  python3 tiling/volume_packing.py
"""

import sys, os, math, json
import numpy as np
from collections import Counter, defaultdict
from itertools import combinations

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEAN = os.path.join(ROOT, 'CLEAN')
sys.path.insert(0, CLEAN)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.constants import PHI
from heptahedron import (
    FACE_NAMES, FACE_FORCE, FACE_COLORS,
    ALLOWED_JUNCTIONS, FORBIDDEN_JUNCTIONS,
    get_face_fractions, icosahedral_axes, select_7_normals,
    _icosahedral_rotations, _rotation_matrix,
)
from scipy.spatial import ConvexHull
from scipy.optimize import linprog


# ═════════════════════════════════════════════════════════════════
# 1. BUILD THE HEPTAHEDRON (H-rep → V-rep)
# ═════════════════════════════════════════════════════════════════

def build_heptahedron_solid(normals_dict_unused, fracs):
    """Construct a convex heptahedron as a deformed pentagonal prism.

    A pentagonal prism naturally has 7 faces (2 caps + 5 sides).
    We deform it so face areas match the target fractions.
    Face assignment: S (smallest) = top cap, BG (largest) = bottom cap,
    G, B, GS, BS, BGS = the 5 side faces in order.

    Returns dict with vertices, faces, normals, areas, centroid.
    """
    names = list(FACE_NAMES)
    target_fracs = np.array([fracs[n] for n in names])

    # Sort by target fraction to assign faces
    sorted_idx = np.argsort(target_fracs)  # smallest first
    # sorted: S(0.029), G(0.074), B(0.081), GS(0.146), BGS(0.149), BS(0.226), BG(0.294)

    # Build pentagonal prism: 5 vertices on top ring, 5 on bottom
    # Adjust ring radii and height to match face areas
    n_sides = 5
    angles = np.array([2 * math.pi * k / n_sides for k in range(n_sides)])

    # Start with unit prism, then scale
    r_top = 0.4     # smaller top cap = S face (smallest)
    r_bot = 1.2     # larger bottom cap = BG face (largest)
    height = 1.5    # prism height affects side face areas

    # Iteratively adjust
    for iteration in range(100):
        top_verts = np.column_stack([r_top * np.cos(angles),
                                      r_top * np.sin(angles),
                                      np.full(n_sides, height / 2)])
        bot_verts = np.column_stack([r_bot * np.cos(angles),
                                      r_bot * np.sin(angles),
                                      np.full(n_sides, -height / 2)])
        vertices = np.vstack([top_verts, bot_verts])

        hull = ConvexHull(vertices)

        # Compute face areas by grouping hull facets by normal direction
        # Normals: top cap ≈ (0,0,1), bottom cap ≈ (0,0,-1),
        # 5 side normals ≈ pentagonal directions
        face_groups = defaultdict(lambda: {'area': 0, 'verts': set()})

        for idx, simplex in enumerate(hull.simplices):
            eq_n = hull.equations[idx][:3]
            norm = np.linalg.norm(eq_n)
            if norm < 1e-10:
                continue
            n_unit = eq_n / norm

            p0, p1, p2 = vertices[simplex]
            area = 0.5 * np.linalg.norm(np.cross(p1 - p0, p2 - p0))

            # Classify: top, bottom, or which side
            if n_unit[2] > 0.5:
                key = 'top'
            elif n_unit[2] < -0.5:
                key = 'bottom'
            else:
                # Which side? Use azimuthal angle
                az = math.atan2(n_unit[1], n_unit[0])
                side_idx = int(round((az % (2 * math.pi)) /
                                      (2 * math.pi / n_sides))) % n_sides
                key = f'side_{side_idx}'

            face_groups[key]['area'] += area
            face_groups[key]['verts'].update(simplex.tolist())

        # Assign face names: S=top (smallest), BG=bottom (largest),
        # sides = G, B, GS, BGS, BS by area
        if len(face_groups) < 7:
            # Not enough distinct faces — adjust
            r_top *= 0.9
            r_bot *= 1.1
            continue

        total_area = sum(fg['area'] for fg in face_groups.values())
        group_keys = sorted(face_groups.keys(),
                            key=lambda k: face_groups[k]['area'])

        # Map sorted groups to sorted face names
        face_name_sorted = [names[i] for i in sorted_idx]

        face_data = {}
        normal_vecs_list = []

        for rank, gkey in enumerate(group_keys):
            fname = face_name_sorted[rank]
            fg = face_groups[gkey]
            vidx = sorted(fg['verts'])
            center = np.mean(vertices[vidx], axis=0)
            # Normal: compute from face center direction
            centroid = np.mean(vertices, axis=0)
            normal = center - centroid
            normal = normal / (np.linalg.norm(normal) + 1e-10)

            face_data[fname] = {
                'area': fg['area'],
                'fraction': fg['area'] / total_area,
                'center': center,
                'vertex_indices': vidx,
                'normal': normal,
            }
            normal_vecs_list.append(normal)

        # Check all faces present
        if len(face_data) < 7:
            r_top *= 0.9
            continue

        # Compute residual
        current_fracs = np.array([face_data[n]['fraction'] for n in names])
        residual = np.max(np.abs(current_fracs - target_fracs))
        if residual < 0.05:
            break

        # Adjust: top area ↔ r_top, bottom area ↔ r_bot, sides ↔ height
        top_target = fracs[face_name_sorted[0]]
        bot_target = fracs[face_name_sorted[-1]]
        top_frac = face_data[face_name_sorted[0]]['fraction']
        bot_frac = face_data[face_name_sorted[-1]]['fraction']

        r_top *= (1 + 0.2 * (top_target / max(top_frac, 0.01) - 1))
        r_bot *= (1 + 0.2 * (bot_target / max(bot_frac, 0.01) - 1))

    centroid = np.mean(vertices, axis=0)
    normal_vecs = np.array([face_data[n]['normal'] for n in names])

    face_data = {}
    for i, name in enumerate(names):
        vidx = sorted(face_vert_sets[i])
        center = np.mean(vertices[vidx], axis=0) if vidx else centroid
        face_data[name] = {
            'area': face_areas[i],
            'fraction': current_fracs[i],
            'center': center,
            'vertex_indices': vidx,
            'normal': normal_vecs[i],
        }

    return {
        'vertices': vertices,
        'n_vertices': len(vertices),
        'hull': hull,
        'centroid': centroid,
        'normals': normal_vecs,
        'distances': distances,
        'face_data': face_data,
        'total_area': total_area,
        'names': names,
        'iterations': iteration + 1,
    }


# ═════════════════════════════════════════════════════════════════
# 2. OVERLAP DETECTION (Separating Axis Theorem)
# ═════════════════════════════════════════════════════════════════

def convex_hulls_overlap(verts_a, verts_b, margin=0.01):
    """Test if two convex polyhedra overlap using LP feasibility.

    Two convex sets intersect iff there exists a point x in both.
    We test: is there x such that A_a @ x <= b_a AND A_b @ x <= b_b?

    Uses scipy linprog to test feasibility.
    Returns True if they overlap, False if separated.
    """
    hull_a = ConvexHull(verts_a)
    hull_b = ConvexHull(verts_b)

    # Combine constraints: A_combined @ x <= b_combined
    A = np.vstack([hull_a.equations[:, :3], hull_b.equations[:, :3]])
    b = np.concatenate([-hull_a.equations[:, 3] - margin,
                        -hull_b.equations[:, 3] - margin])

    # Feasibility: minimize 0 subject to A @ x <= b
    c = np.zeros(3)
    result = linprog(c, A_ub=A, b_ub=b, method='highs',
                     options={'presolve': True})
    return result.success  # True = feasible = overlap


def quick_overlap_check(center_a, radius_a, center_b, radius_b):
    """Fast bounding sphere pre-check."""
    dist = np.linalg.norm(center_a - center_b)
    return dist < (radius_a + radius_b)


# ═════════════════════════════════════════════════════════════════
# 3. TILE PLACEMENT
# ═════════════════════════════════════════════════════════════════

def place_neighbor(hepta, face_idx, rotation_matrix):
    """Compute vertices of a neighbor tile placed at face face_idx.

    Steps:
    1. Rotate the template tile by rotation_matrix
    2. Translate so the matching face is flush with the central tile's face

    The neighbor is placed such that its touching face is coplanar
    and coincident with face face_idx of the central tile.
    """
    face_name = FACE_NAMES[face_idx]
    fd = hepta['face_data'][face_name]
    face_center = fd['center']
    face_normal = fd['normal']  # outward normal of central tile

    # Rotate the template vertices
    template_verts = hepta['vertices'].copy()
    centroid = hepta['centroid']

    # Center, rotate, then translate
    centered = template_verts - centroid
    rotated = (rotation_matrix @ centered.T).T

    # Find which face of the rotated tile should touch face_idx
    # The touching face has normal anti-parallel to face_normal
    rotated_normals = (rotation_matrix @ hepta['normals'].T).T
    dots = rotated_normals @ face_normal
    touching_face = int(np.argmin(dots))  # most anti-parallel

    # Get the center of the touching face on the rotated tile
    touching_fd = None
    touching_name = FACE_NAMES[touching_face]

    # Compute face center of the touching face on the rotated tile
    rotated_face_centers = {}
    for i, name in enumerate(FACE_NAMES):
        fdata = hepta['face_data'][name]
        if fdata['center'] is not None:
            rc = rotation_matrix @ (fdata['center'] - centroid)
            rotated_face_centers[i] = rc

    if touching_face not in rotated_face_centers:
        return None, None, None

    touching_center_local = rotated_face_centers[touching_face]

    # Translation: place the touching face center at the central face center
    # Then push outward by a small gap to avoid exact surface contact
    # The neighbor should be on the OUTSIDE of the central tile's face
    offset = face_center - touching_center_local
    # Additional push along face normal to separate the tiles
    push = face_normal * 0.02  # tiny gap

    neighbor_verts = rotated + offset + push

    return neighbor_verts, touching_face, touching_name


# ═════════════════════════════════════════════════════════════════
# 4. MAIN PACKING ANALYSIS
# ═════════════════════════════════════════════════════════════════

def packing_analysis(hepta, rot_tables, rotations, is_allowed):
    """For each face, try all 60 orientations, check overlaps.

    Returns per-face valid counts, effective orientation set,
    and the positions of successfully placed tiles.
    """
    n_rots = len(rotations)
    central_verts = hepta['vertices']
    central_center = hepta['centroid']
    central_radius = np.max(np.linalg.norm(
        central_verts - central_center, axis=1))

    per_face_valid = {}
    per_face_details = {}
    all_valid_rots = set()
    all_valid_sigs = set()
    placed_tiles = []  # (face_idx, rot_idx, vertices, touching_name)

    for face_idx in range(7):
        face_name = FACE_NAMES[face_idx]
        valid_rots = []
        blocked_overlap = 0
        blocked_junction = 0
        blocked_geometry = 0

        for r_idx in range(n_rots):
            R = rotations[r_idx]

            # Place the neighbor
            neighbor_verts, touching_face, touching_name = \
                place_neighbor(hepta, face_idx, R)

            if neighbor_verts is None:
                blocked_geometry += 1
                continue

            # Check junction rule
            if not is_allowed(face_name, touching_name):
                blocked_junction += 1
                continue

            # Quick bounding sphere check with central tile
            neighbor_center = np.mean(neighbor_verts, axis=0)
            neighbor_radius = np.max(np.linalg.norm(
                neighbor_verts - neighbor_center, axis=1))

            # Check overlap with central tile
            if quick_overlap_check(central_center, central_radius * 0.85,
                                   neighbor_center, neighbor_radius * 0.85):
                # Detailed LP overlap check
                if convex_hulls_overlap(central_verts, neighbor_verts,
                                        margin=0.02):
                    blocked_overlap += 1
                    continue

            # Check overlap with all previously placed tiles at OTHER faces
            overlap_with_placed = False
            for _, _, placed_verts, _ in placed_tiles:
                placed_center = np.mean(placed_verts, axis=0)
                placed_radius = np.max(np.linalg.norm(
                    placed_verts - placed_center, axis=1))
                if quick_overlap_check(neighbor_center, neighbor_radius * 0.85,
                                       placed_center, placed_radius * 0.85):
                    if convex_hulls_overlap(placed_verts, neighbor_verts,
                                            margin=0.02):
                        overlap_with_placed = True
                        break

            if overlap_with_placed:
                blocked_overlap += 1
                continue

            # VALID: this orientation works at this face
            valid_rots.append(r_idx)
            all_valid_rots.add(r_idx)
            sig = rot_tables[r_idx]['sig_names']
            all_valid_sigs.add(sig)

        # Pick the first valid orientation to place for neighbor checks
        if valid_rots:
            best_r = valid_rots[0]
            R = rotations[best_r]
            nv, tf, tn = place_neighbor(hepta, face_idx, R)
            if nv is not None:
                placed_tiles.append((face_idx, best_r, nv, tn))

        per_face_valid[face_name] = len(valid_rots)
        per_face_details[face_name] = {
            'valid': len(valid_rots),
            'blocked_overlap': blocked_overlap,
            'blocked_junction': blocked_junction,
            'blocked_geometry': blocked_geometry,
            'valid_rots': valid_rots,
        }

    return {
        'per_face': per_face_valid,
        'details': per_face_details,
        'total_valid_rots': len(all_valid_rots),
        'total_valid_sigs': len(all_valid_sigs),
        'placed_tiles': placed_tiles,
    }


# ═════════════════════════════════════════════════════════════════
# 5. DIHEDRAL ANGLE ANALYSIS
# ═════════════════════════════════════════════════════════════════

def dihedral_analysis(hepta, rotations):
    """Compute dihedral angles between adjacent faces of the heptahedron,
    and between central + neighbor tiles at each face junction."""
    normals = hepta['normals']

    # Internal dihedral angles (between adjacent faces of ONE tile)
    internal = []
    for i in range(7):
        for j in range(i + 1, 7):
            cos_angle = np.dot(normals[i], normals[j])
            angle_deg = math.degrees(math.acos(np.clip(cos_angle, -1, 1)))
            internal.append({
                'faces': (FACE_NAMES[i], FACE_NAMES[j]),
                'angle': angle_deg,
                'cos': cos_angle,
            })

    internal.sort(key=lambda x: x['angle'])

    # Junction dihedral: angle between central face normal and
    # each rotated tile's touching face normal
    junction_angles = {}
    for face_idx in range(7):
        angles_for_face = []
        face_normal = normals[face_idx]
        for r_idx, R in enumerate(rotations):
            rotated_normals = (R @ normals.T).T
            # Touching face = most anti-parallel
            dots = rotated_normals @ face_normal
            touching = int(np.argmin(dots))
            # Dihedral = angle between outward normals
            cos_dih = np.dot(face_normal, rotated_normals[touching])
            angle = math.degrees(math.acos(np.clip(cos_dih, -1, 1)))
            angles_for_face.append(angle)
        junction_angles[FACE_NAMES[face_idx]] = angles_for_face

    return internal, junction_angles


# ═════════════════════════════════════════════════════════════════
# 6. SPATIAL PATTERN ANALYSIS (helix / vortex detection)
# ═════════════════════════════════════════════════════════════════

def analyze_spatial_pattern(placed_tiles, hepta):
    """Analyze the 3D positions of placed tiles for patterns.

    Check for:
    - Helical arrangement (positions follow a helix)
    - Double helix (two interleaved helices)
    - Vortex (positions spiral outward)
    - Linear chain
    - Planar arrangement
    """
    if len(placed_tiles) < 3:
        return {'pattern': 'too few tiles', 'n_placed': len(placed_tiles)}

    # Get tile centers
    centers = []
    labels = []
    for face_idx, rot_idx, verts, touching_name in placed_tiles:
        center = np.mean(verts, axis=0)
        centers.append(center)
        labels.append(FACE_NAMES[face_idx])

    centers = np.array(centers)
    # Add the central tile
    all_centers = np.vstack([hepta['centroid'].reshape(1, 3), centers])
    all_labels = ['SEED'] + labels

    n = len(all_centers)

    # ── Planarity test ──
    if n >= 4:
        centered = all_centers - np.mean(all_centers, axis=0)
        _, S, Vt = np.linalg.svd(centered)
        # If smallest singular value is << others, points are planar
        planarity = S[2] / S[0] if S[0] > 0 else 0
    else:
        planarity = 0

    # ── Helix test ──
    # Fit a helix: x = R*cos(t), y = R*sin(t), z = pitch*t
    # Try along each axis as the helix axis
    best_helix = None
    best_helix_error = float('inf')

    for axis in range(3):
        # Project onto the plane perpendicular to this axis
        other = [i for i in range(3) if i != axis]
        proj_2d = all_centers[:, other]
        z_vals = all_centers[:, axis]

        # Fit circle to 2D projection
        circle_center, circle_radius = fit_circle_2d(proj_2d)
        if circle_radius < 1e-6:
            continue

        # Compute angles around the circle
        angles = np.arctan2(proj_2d[:, 1] - circle_center[1],
                            proj_2d[:, 0] - circle_center[0])

        # Sort by angle
        order = np.argsort(angles)
        sorted_angles = angles[order]
        sorted_z = z_vals[order]

        # Check if z is monotonic with angle (helix signature)
        if len(sorted_z) >= 3:
            dz = np.diff(sorted_z)
            monotonic_frac = max(np.sum(dz > 0), np.sum(dz < 0)) / len(dz)

            # Residual from circle
            radii = np.linalg.norm(proj_2d - circle_center, axis=1)
            circle_error = np.std(radii) / circle_radius

            helix_score = monotonic_frac * (1 - circle_error)

            if helix_score > 0.5 and circle_error < best_helix_error:
                best_helix = {
                    'axis': axis,
                    'radius': circle_radius,
                    'center': circle_center,
                    'monotonic_frac': monotonic_frac,
                    'circle_error': circle_error,
                    'score': helix_score,
                    'pitch_per_turn': (np.max(sorted_z) - np.min(sorted_z))
                                       / max(1, len(sorted_z) - 1) * 2 * np.pi,
                }
                best_helix_error = circle_error

    # ── Vortex test ──
    # Check if radial distances from centroid grow with angle
    centroid = np.mean(all_centers, axis=0)
    rel = all_centers - centroid
    radial = np.linalg.norm(rel, axis=1)
    # Sort by azimuthal angle in xy-plane
    azimuth = np.arctan2(rel[:, 1], rel[:, 0])
    order = np.argsort(azimuth)
    sorted_radial = radial[order]
    if len(sorted_radial) >= 3:
        dr = np.diff(sorted_radial)
        vortex_score = np.sum(dr > 0) / len(dr)
    else:
        vortex_score = 0

    # ── Chain test ──
    # Check if points are roughly collinear
    if n >= 3:
        chain_score = 1 - planarity  # low planarity = high linearity
        # More precisely: ratio of first to second singular value
        linearity = S[0] / (S[1] + 1e-10) if len(S) >= 2 else 1
    else:
        chain_score = 0
        linearity = 0

    # ── Angular momentum / chirality ──
    # L = Σ r_i × v_i where v_i = r_{i+1} - r_i
    L = np.zeros(3)
    for i in range(n - 1):
        r = all_centers[i] - centroid
        v = all_centers[min(i + 1, n - 1)] - all_centers[i]
        L += np.cross(r, v)
    L_mag = np.linalg.norm(L)
    if L_mag > 0:
        L_unit = L / L_mag
    else:
        L_unit = np.zeros(3)

    # Determine dominant pattern
    pattern = 'amorphous'
    if best_helix and best_helix['score'] > 0.7:
        pattern = 'helical'
    elif vortex_score > 0.7:
        pattern = 'vortex'
    elif linearity > 5:
        pattern = 'linear chain'
    elif planarity < 0.1:
        pattern = 'planar'

    return {
        'pattern': pattern,
        'n_placed': n,
        'centers': all_centers.tolist(),
        'labels': all_labels,
        'planarity': planarity,
        'linearity': linearity,
        'helix': best_helix,
        'vortex_score': vortex_score,
        'angular_momentum': L.tolist(),
        'L_magnitude': L_mag,
        'L_direction': L_unit.tolist(),
        'chirality': 'right-handed' if L[2] > 0 else 'left-handed'
                     if L[2] < 0 else 'achiral',
    }


def fit_circle_2d(points):
    """Fit a circle to 2D points using algebraic fit."""
    if len(points) < 3:
        return np.mean(points, axis=0), 0

    x, y = points[:, 0], points[:, 1]
    A = np.column_stack([2 * x, 2 * y, np.ones(len(x))])
    b = x**2 + y**2
    try:
        result = np.linalg.lstsq(A, b, rcond=None)
        params = result[0]
        cx, cy = params[0], params[1]
        r = math.sqrt(params[2] + cx**2 + cy**2)
        return np.array([cx, cy]), r
    except Exception:
        return np.mean(points, axis=0), 0


# ═════════════════════════════════════════════════════════════════
# 7. MULTI-LAYER PACKING
# ═════════════════════════════════════════════════════════════════

def grow_packed_tiling(hepta, rot_tables, rotations, is_allowed,
                       max_tiles=30, rng=None):
    """Grow a tiling with volume overlap checking.

    BFS: seed → layer 1 (up to 7 neighbors) → layer 2 → ...
    At each step, try random orientations and keep non-overlapping ones.
    """
    if rng is None:
        rng = np.random.RandomState(42)

    central_verts = hepta['vertices']

    # Each placed tile: (id, vertices, centroid, radius, rot_idx, face_name)
    placed = [{
        'id': 0,
        'verts': central_verts,
        'center': hepta['centroid'],
        'radius': np.max(np.linalg.norm(
            central_verts - hepta['centroid'], axis=1)),
        'rot_idx': 0,
        'parent_face': None,
        'layer': 0,
        'sig': rot_tables[0]['sig_names'],
    }]

    frontier = [0]  # indices into placed
    sigs_used = {rot_tables[0]['sig_names']}
    tile_id = 1

    for layer in range(1, 6):
        new_frontier = []
        for parent_idx in frontier:
            parent = placed[parent_idx]
            parent_verts = parent['verts']
            parent_center = parent['center']

            # Try each face
            for face_idx in range(7):
                if tile_id >= max_tiles:
                    break

                face_name = FACE_NAMES[face_idx]

                # Shuffle orientations for randomness
                rot_order = rng.permutation(len(rotations))
                placed_this = False

                for r_idx in rot_order:
                    R = rotations[int(r_idx)]

                    # Place relative to parent
                    nv, tf, tn = place_neighbor_at(
                        hepta, parent_verts, parent_center,
                        face_idx, R)

                    if nv is None:
                        continue

                    # Junction check
                    if not is_allowed(face_name, tn):
                        continue

                    # Overlap check with ALL placed tiles
                    nc = np.mean(nv, axis=0)
                    nr = np.max(np.linalg.norm(nv - nc, axis=1))
                    overlap = False

                    for p in placed:
                        if not quick_overlap_check(nc, nr * 0.85,
                                                    p['center'],
                                                    p['radius'] * 0.85):
                            continue
                        if convex_hulls_overlap(p['verts'], nv, margin=0.01):
                            overlap = True
                            break

                    if overlap:
                        continue

                    # Place it!
                    sig = rot_tables[int(r_idx)]['sig_names']
                    placed.append({
                        'id': tile_id,
                        'verts': nv,
                        'center': nc,
                        'radius': nr,
                        'rot_idx': int(r_idx),
                        'parent_face': face_name,
                        'layer': layer,
                        'sig': sig,
                    })
                    sigs_used.add(sig)
                    new_frontier.append(tile_id)
                    tile_id += 1
                    placed_this = True
                    break  # one tile per face per parent

            if tile_id >= max_tiles:
                break

        frontier = new_frontier
        if not frontier:
            break

    return placed, sigs_used


def place_neighbor_at(hepta, parent_verts, parent_center,
                      face_idx, rotation_matrix):
    """Place a neighbor relative to a specific parent tile."""
    normals = hepta['normals']
    template = hepta['vertices']
    template_centroid = hepta['centroid']

    face_normal = normals[face_idx]

    # Face center of the parent tile at face_idx
    # (approximate: centroid + normal * distance)
    fd = hepta['face_data'][FACE_NAMES[face_idx]]
    if fd['center'] is None:
        return None, None, None

    # Parent face center in world coordinates
    face_center_local = fd['center'] - template_centroid
    parent_face_center = parent_center + face_center_local

    # Rotate template
    centered = template - template_centroid
    rotated = (rotation_matrix @ centered.T).T

    # Find touching face
    rotated_normals = (rotation_matrix @ normals.T).T
    dots = rotated_normals @ face_normal
    touching_face = int(np.argmin(dots))
    touching_name = FACE_NAMES[touching_face]

    # Touching face center on rotated tile
    touching_fd = hepta['face_data'][FACE_NAMES[touching_face]]
    if touching_fd['center'] is None:
        return None, None, None
    touching_center_local = rotation_matrix @ (touching_fd['center'] -
                                                template_centroid)

    # Translation
    offset = parent_face_center - touching_center_local
    push = face_normal * 0.02
    neighbor_verts = rotated + offset + push

    return neighbor_verts, touching_face, touching_name


# ═════════════════════════════════════════════════════════════════
# MAIN
# ═════════════════════════════════════════════════════════════════

def main():
    print()
    print("  ╔═══════════════════════════════════════════════════════════════╗")
    print("  ║  3D VOLUME PACKING: Heptahedral Tiling with Overlap Check   ║")
    print("  ║  The REAL geometric constraint: tiles can't overlap.        ║")
    print("  ╚═══════════════════════════════════════════════════════════════╝")

    # ── Setup ──
    print("\n  Building tiling and heptahedron...")
    fracs, total = get_face_fractions()
    axes = icosahedral_axes()

    # Use well-separated normals for valid 3D construction
    normals, normal_array_raw = select_7_spread_normals(axes)
    rotations = _icosahedral_rotations()
    rot_tables = []
    normal_array = np.array([normals[n] for n in FACE_NAMES])
    for R in rotations:
        rotated = (R @ normal_array.T).T
        sig = []
        anti_map = {}
        for i in range(7):
            dots = np.abs(normal_array @ rotated[i])
            sig.append(int(np.argmax(dots)))
            dots2 = rotated @ normal_array[i]
            j = int(np.argmin(dots2))
            if dots2[j] < -0.3:
                anti_map[i] = (j, sig[-1])
        rot_tables.append({
            'sig_names': tuple(FACE_NAMES[s] for s in sig),
            'anti_map': anti_map,
        })

    print(f"  Constructing convex heptahedron...")
    hepta = build_heptahedron_solid(normals, fracs)
    print(f"  Heptahedron: {hepta['n_vertices']} vertices, "
          f"area = {hepta['total_area']:.3f}")

    print(f"\n  Face areas (achieved vs target):")
    print(f"  {'Face':<6} {'Area':>8} {'Frac':>8} {'Target':>8} {'Δ':>8}")
    print(f"  {'─'*6} {'─'*8} {'─'*8} {'─'*8} {'─'*8}")
    for name in FACE_NAMES:
        fd = hepta['face_data'][name]
        delta = (fd['fraction'] - fracs[name]) / fracs[name] * 100
        print(f"  {name:<6} {fd['area']:>8.3f} {fd['fraction']:>8.4f} "
              f"{fracs[name]:>8.4f} {delta:>+7.1f}%")

    # ── Dihedral angles ──
    print(f"\n{'='*70}")
    print("  DIHEDRAL ANGLES")
    print(f"{'='*70}")

    internal, junction_angles = dihedral_analysis(hepta, rotations)
    print(f"\n  Internal dihedral angles (face-face within one tile):")
    print(f"  {'Pair':<12} {'Angle':>8}")
    print(f"  {'─'*12} {'─'*8}")
    for d in internal[:10]:
        print(f"  {d['faces'][0]+'↔'+d['faces'][1]:<12} {d['angle']:>7.1f}°")
    print(f"  ... ({len(internal)} total pairs)")

    min_dih = min(d['angle'] for d in internal)
    max_dih = max(d['angle'] for d in internal)
    mean_dih = np.mean([d['angle'] for d in internal])
    print(f"\n  Min: {min_dih:.1f}°  Max: {max_dih:.1f}°  Mean: {mean_dih:.1f}°")

    # ── Junction check ──
    def is_allowed(a, b):
        pair, rev = (a, b), (b, a)
        return pair in ALLOWED_JUNCTIONS or rev in ALLOWED_JUNCTIONS

    # ── Single-layer volume packing ──
    print(f"\n{'='*70}")
    print("  SINGLE-LAYER VOLUME PACKING (seed + 7 neighbors)")
    print(f"{'='*70}")
    print(f"\n  Testing all 60 orientations at each face with overlap check...")

    result = packing_analysis(hepta, rot_tables, rotations, is_allowed)

    print(f"\n  {'Face':<6} {'Valid':>6} {'Overlap':>8} {'Junction':>9} "
          f"{'Geom':>6}")
    print(f"  {'─'*6} {'─'*6} {'─'*8} {'─'*9} {'─'*6}")
    for name in FACE_NAMES:
        d = result['details'][name]
        print(f"  {name:<6} {d['valid']:>6} {d['blocked_overlap']:>8} "
              f"{d['blocked_junction']:>9} {d['blocked_geometry']:>6}")

    eff_rots = result['total_valid_rots']
    eff_sigs = result['total_valid_sigs']
    print(f"\n  Total valid rotation indices: {eff_rots} (of 60)")
    print(f"  Total valid signatures:       {eff_sigs}")

    fibs = [1, 2, 3, 5, 8, 13, 21, 34, 55]
    nearest = min(fibs, key=lambda f: abs(eff_sigs - f))
    print(f"  Nearest Fibonacci: {nearest} (off by {eff_sigs - nearest:+d})")
    if eff_sigs == 13:
        print(f"\n  ★ VOLUME PACKING → 13 = F(7) ★")
        print(f"  The bronze discriminant constrains 3D SPACE, not 2D faces.")

    # ── Spatial pattern ──
    print(f"\n{'='*70}")
    print("  SPATIAL PATTERN OF PLACED TILES")
    print(f"{'='*70}")

    spatial = analyze_spatial_pattern(result['placed_tiles'], hepta)
    print(f"\n  Tiles placed: {spatial['n_placed']}")
    print(f"  Dominant pattern: {spatial['pattern']}")
    print(f"  Planarity (0=planar, 1=3D): {spatial['planarity']:.4f}")
    print(f"  Linearity (SVD ratio): {spatial['linearity']:.2f}")
    print(f"  Vortex score: {spatial['vortex_score']:.3f}")
    print(f"  Angular momentum: [{spatial['angular_momentum'][0]:.3f}, "
          f"{spatial['angular_momentum'][1]:.3f}, "
          f"{spatial['angular_momentum'][2]:.3f}]")
    print(f"  |L| = {spatial['L_magnitude']:.3f}")
    print(f"  Chirality: {spatial['chirality']}")

    if spatial['helix']:
        h = spatial['helix']
        ax_name = ['X', 'Y', 'Z'][h['axis']]
        print(f"\n  Helix detected:")
        print(f"    Axis: {ax_name}")
        print(f"    Radius: {h['radius']:.3f}")
        print(f"    Pitch/turn: {h['pitch_per_turn']:.3f}")
        print(f"    Monotonic fraction: {h['monotonic_frac']:.3f}")
        print(f"    Circle fit error: {h['circle_error']:.4f}")
        print(f"    Score: {h['score']:.3f}")

    # ── Multi-layer packed growth ──
    print(f"\n{'='*70}")
    print("  MULTI-LAYER PACKED GROWTH (with overlap checking)")
    print(f"{'='*70}")

    for max_t in [15, 25, 40]:
        print(f"\n  Growing up to {max_t} tiles (5 random seeds)...")
        all_sigs = set()
        for seed in range(5):
            rng = np.random.RandomState(seed * 17 + 3)
            placed, sigs = grow_packed_tiling(
                hepta, rot_tables, rotations, is_allowed,
                max_tiles=max_t, rng=rng)
            all_sigs |= sigs
            print(f"    Seed {seed}: {len(placed)} tiles, "
                  f"{len(sigs)} orientations")

        print(f"    Union across seeds: {len(all_sigs)} orientations")

    # ── Largest run with pattern analysis ──
    print(f"\n{'='*70}")
    print("  DETAILED GROWTH: 40 tiles, pattern analysis")
    print(f"{'='*70}")

    rng = np.random.RandomState(42)
    placed_full, sigs_full = grow_packed_tiling(
        hepta, rot_tables, rotations, is_allowed,
        max_tiles=40, rng=rng)

    print(f"\n  Tiles placed: {len(placed_full)}")
    print(f"  Distinct orientations: {len(sigs_full)}")
    nearest_f = min(fibs, key=lambda f: abs(len(sigs_full) - f))
    print(f"  Nearest Fibonacci: {nearest_f} "
          f"(off by {len(sigs_full) - nearest_f:+d})")

    # Layer census
    layer_counts = Counter(p['layer'] for p in placed_full)
    print(f"\n  Tiles per layer:")
    for l in sorted(layer_counts.keys()):
        print(f"    Layer {l}: {layer_counts[l]} tiles")

    # Spatial pattern of full growth
    fake_placed = [(p['rot_idx'], p['rot_idx'], p['verts'],
                     p.get('parent_face', 'SEED'))
                    for p in placed_full[1:]]
    spatial_full = analyze_spatial_pattern(fake_placed, hepta)
    print(f"\n  Spatial pattern: {spatial_full['pattern']}")
    print(f"  Planarity: {spatial_full['planarity']:.4f}")
    print(f"  Linearity: {spatial_full['linearity']:.2f}")
    print(f"  Vortex score: {spatial_full['vortex_score']:.3f}")
    print(f"  |L| = {spatial_full['L_magnitude']:.3f}")
    print(f"  Chirality: {spatial_full['chirality']}")

    if spatial_full['helix']:
        h = spatial_full['helix']
        ax_name = ['X', 'Y', 'Z'][h['axis']]
        print(f"\n  HELIX:")
        print(f"    Axis: {ax_name}, R={h['radius']:.3f}, "
              f"pitch={h['pitch_per_turn']:.3f}")
        print(f"    Score: {h['score']:.3f}")

    # ── Angular distribution ──
    centers = np.array([p['center'] for p in placed_full])
    origin = centers[0]
    rel = centers[1:] - origin
    r_vals = np.linalg.norm(rel, axis=1)
    theta = np.arctan2(rel[:, 1], rel[:, 0])
    phi = np.arccos(np.clip(rel[:, 2] / (r_vals + 1e-10), -1, 1))

    theta_sorted = np.sort(theta)
    if len(theta_sorted) > 2:
        dtheta = np.diff(theta_sorted)
        mean_dtheta = np.mean(dtheta)
        golden_angle = 2 * math.pi / PHI**2  # 137.5°
        print(f"\n  Angular spacing analysis:")
        print(f"    Mean Δθ (azimuthal): {math.degrees(mean_dtheta):.1f}°")
        print(f"    Golden angle: {math.degrees(golden_angle):.1f}°")
        print(f"    Ratio: {mean_dtheta / golden_angle:.3f}")

    # ── Save results ──
    outdir = os.path.join(ROOT, 'results', 'heptahedron', 'packing')
    os.makedirs(outdir, exist_ok=True)

    results = {
        'heptahedron': {
            'n_vertices': hepta['n_vertices'],
            'total_area': hepta['total_area'],
            'face_fractions': {n: hepta['face_data'][n]['fraction']
                               for n in FACE_NAMES},
        },
        'single_layer': {
            'per_face_valid': result['per_face'],
            'effective_rotations': eff_rots,
            'effective_signatures': eff_sigs,
        },
        'dihedral_angles': {
            'min': min_dih, 'max': max_dih, 'mean': mean_dih,
        },
        'spatial_pattern_single': {
            'pattern': spatial['pattern'],
            'planarity': spatial['planarity'],
            'chirality': spatial['chirality'],
            'L_magnitude': spatial['L_magnitude'],
        },
        'multi_layer': {
            'tiles_placed': len(placed_full),
            'orientations': len(sigs_full),
            'pattern': spatial_full['pattern'],
            'chirality': spatial_full['chirality'],
        },
    }

    with open(os.path.join(outdir, 'packing_results.json'), 'w') as f:
        json.dump(results, f, indent=2, default=str)

    # Text report
    with open(os.path.join(outdir, 'packing_report.txt'), 'w') as f:
        f.write("3D VOLUME PACKING: Heptahedral Tiling Analysis\n")
        f.write("=" * 55 + "\n\n")
        f.write(f"Heptahedron: {hepta['n_vertices']} vertices\n\n")

        f.write("SINGLE-LAYER (seed + 7 neighbors):\n")
        for name in FACE_NAMES:
            d = result['details'][name]
            f.write(f"  {name:<6} {d['valid']:>3} valid, "
                    f"{d['blocked_overlap']:>3} overlap-blocked, "
                    f"{d['blocked_junction']:>3} junction-blocked\n")
        f.write(f"\nEffective orientations: {eff_sigs}\n")
        f.write(f"Nearest Fibonacci: {nearest}\n\n")

        f.write("SPATIAL PATTERN:\n")
        f.write(f"  Single layer: {spatial['pattern']}\n")
        f.write(f"  Multi layer:  {spatial_full['pattern']}\n")
        f.write(f"  Chirality:    {spatial_full['chirality']}\n")
        f.write(f"  |L|:          {spatial_full['L_magnitude']:.3f}\n")
        if spatial_full['helix']:
            h = spatial_full['helix']
            f.write(f"  Helix axis:   {'XYZ'[h['axis']]}\n")
            f.write(f"  Helix radius: {h['radius']:.3f}\n")
            f.write(f"  Helix score:  {h['score']:.3f}\n")

    print(f"\n  Results saved to: {outdir}/")

    # ── Final verdict ──
    print(f"\n{'='*70}")
    print("  VERDICT")
    print(f"{'='*70}")

    if eff_sigs == 13:
        print(f"\n  13 from volume packing, not face matching.")
        print(f"  The bronze discriminant constrains 3D SPACE, not 2D faces.")
        print(f"  You can't prove 3 dimensions with a 2D rule.")
    elif eff_sigs < 60:
        print(f"\n  Volume packing reduces 60 → {eff_sigs}")
        print(f"  (face matching alone gives 60)")
    else:
        print(f"\n  Volume packing gives {eff_sigs} (same as face matching)")

    if spatial_full['pattern'] == 'helical':
        print(f"\n  ★ HELICAL PATTERN DETECTED ★")
        print(f"  The tiles naturally form a helix in 3D!")
        print(f"  Chirality: {spatial_full['chirality']}")
    elif spatial_full['vortex_score'] > 0.6:
        print(f"\n  ★ VORTEX TENDENCY DETECTED ★")
        print(f"  Score: {spatial_full['vortex_score']:.3f}")

    print()


if __name__ == '__main__':
    main()
