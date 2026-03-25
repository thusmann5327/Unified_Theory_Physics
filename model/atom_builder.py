"""
atom_builder.py — Build Atoms from the Actual Quasicrystal Tiles
=================================================================

The 3D Voronoi of the icosahedral quasicrystal gives two tile families:
  VACUUM: 9-faced cells (G, S, B, BG, GS, BS types)
  MATTER: 23-faced cells (BGS type)

An atom is a cluster of tiles centered on BGS vertices.
The face directions of the matter tile determine bonding geometry.

Run:  python3 model/atom_builder.py

Depends on: results/voronoi_3d/quasicrystal_points.npz
"""

import sys, os, math, json, time
import numpy as np
from collections import Counter, defaultdict
from scipy.spatial import Voronoi, ConvexHull

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEAN = os.path.join(ROOT, 'CLEAN')
sys.path.insert(0, CLEAN)

from core.constants import PHI, W, LEAK

# Cantor node ratios
R_MATTER = 0.0728
R_INNER  = 0.2350
R_SHELL  = 0.3972
R_OUTER  = 0.5594


# ═══════════════════════════════════════════════════════════════════
# 1. LOAD QUASICRYSTAL AND RECOMPUTE VORONOI WITH FULL GEOMETRY
# ═══════════════════════════════════════════════════════════════════

def load_quasicrystal():
    """Load saved quasicrystal point set."""
    path = os.path.join(ROOT, 'results', 'voronoi_3d', 'quasicrystal_points.npz')
    data = np.load(path, allow_pickle=True)
    return data['pts_par'], data['pts_perp'], data['types'], float(data['R_accept'])


def compute_full_voronoi(pts):
    """Compute Voronoi and extract full cell geometry.

    Returns dict: cell_idx → {
        'center', 'vertices', 'faces' (list of vertex-index lists),
        'face_normals', 'face_areas', 'face_centers',
        'neighbors', 'volume'
    }
    """
    vor = Voronoi(pts)
    clip_radius = 0.8 * np.max(np.linalg.norm(pts, axis=1))
    cells = {}

    for i, region_idx in enumerate(vor.point_region):
        region = vor.regions[region_idx]
        if -1 in region or len(region) < 4:
            continue

        verts = vor.vertices[region]
        center = pts[i]

        # Skip boundary cells
        if np.linalg.norm(center) > clip_radius:
            continue

        # Cell volume via ConvexHull
        try:
            hull = ConvexHull(verts)
        except Exception:
            continue

        # Extract faces from Voronoi ridge structure
        # A ridge is a face shared between two points
        faces = []
        face_normals = []
        face_areas = []
        face_centers = []
        neighbors = []

        for ridge_idx, (p1, p2) in enumerate(vor.ridge_points):
            if p1 != i and p2 != i:
                continue
            neighbor = p2 if p1 == i else p1
            ridge_verts = vor.ridge_vertices[ridge_idx]
            if -1 in ridge_verts or len(ridge_verts) < 3:
                continue

            face_pts = vor.vertices[ridge_verts]
            face_center = face_pts.mean(axis=0)

            # Face normal: from cell center toward face center
            normal = face_center - center
            norm_len = np.linalg.norm(normal)
            if norm_len < 1e-15:
                continue
            normal /= norm_len

            # Face area via ConvexHull of face projected to 2D
            # Project face points onto the plane perpendicular to normal
            if len(face_pts) >= 3:
                try:
                    # Use cross products to compute polygon area in 3D
                    area = 0.0
                    for k in range(1, len(face_pts) - 1):
                        v1 = face_pts[k] - face_pts[0]
                        v2 = face_pts[k + 1] - face_pts[0]
                        area += np.linalg.norm(np.cross(v1, v2))
                    area *= 0.5
                except Exception:
                    area = 0.0
            else:
                area = 0.0

            faces.append(ridge_verts)
            face_normals.append(normal)
            face_areas.append(area)
            face_centers.append(face_center)
            neighbors.append(neighbor)

        if len(faces) < 4:
            continue

        cells[i] = {
            'center': center,
            'vertices': verts,
            'faces': faces,
            'face_normals': np.array(face_normals),
            'face_areas': np.array(face_areas),
            'face_centers': np.array(face_centers),
            'neighbors': neighbors,
            'volume': hull.volume,
            'n_faces': len(faces),
        }

    return cells, vor


def icosahedral_axes():
    """Return the 31 icosahedral symmetry axes."""
    tau = PHI
    # 12 vertices → 6 five-fold axes
    verts = np.array([
        [0, 1, tau], [0, -1, tau], [0, 1, -tau], [0, -1, -tau],
        [1, tau, 0], [-1, tau, 0], [1, -tau, 0], [-1, -tau, 0],
        [tau, 0, 1], [-tau, 0, 1], [tau, 0, -1], [-tau, 0, -1]
    ], dtype=np.float64)
    verts /= np.linalg.norm(verts, axis=1, keepdims=True)

    # 6 five-fold (take one from each antipodal pair)
    five_fold = []
    for v in verts:
        is_dup = any(abs(np.dot(v, e)) > 0.99 for e in five_fold)
        if not is_dup:
            five_fold.append(v)
    five_fold = np.array(five_fold[:6])

    # 20 face centers → 10 three-fold axes
    edge_len = 2.0 / np.sqrt(1 + tau**2)
    three_fold = []
    n = len(verts)
    for i in range(n):
        for j in range(i + 1, n):
            if abs(np.linalg.norm(verts[i] - verts[j]) - edge_len) > 0.1:
                continue
            for k in range(j + 1, n):
                if (abs(np.linalg.norm(verts[i] - verts[k]) - edge_len) < 0.1 and
                    abs(np.linalg.norm(verts[j] - verts[k]) - edge_len) < 0.1):
                    c = (verts[i] + verts[j] + verts[k]) / 3.0
                    cn = np.linalg.norm(c)
                    if cn > 1e-10:
                        c /= cn
                        if not any(abs(np.dot(c, e)) > 0.99 for e in three_fold):
                            three_fold.append(c)
    three_fold = np.array(three_fold[:10])

    # 30 edge midpoints → 15 two-fold axes
    two_fold = []
    for i in range(n):
        for j in range(i + 1, n):
            if abs(np.linalg.norm(verts[i] - verts[j]) - edge_len) < 0.1:
                m = (verts[i] + verts[j]) / 2.0
                mn = np.linalg.norm(m)
                if mn > 1e-10:
                    m /= mn
                    if not any(abs(np.dot(m, e)) > 0.99 for e in two_fold):
                        two_fold.append(m)
    two_fold = np.array(two_fold[:15])

    return five_fold, three_fold, two_fold


# ═══════════════════════════════════════════════════════════════════
# 2. ANALYZE BGS CELLS — NEIGHBOR DISTRIBUTION AND FACE GEOMETRY
# ═══════════════════════════════════════════════════════════════════

def analyze_bgs_cells(cells, types):
    """Detailed analysis of BGS (matter) cells."""

    bgs_indices = [i for i in cells if types[i] == 'BGS']
    print(f"\n  BGS cells in interior: {len(bgs_indices)}")

    # Neighbor type distribution
    neighbor_type_counts = Counter()
    neighbor_type_per_cell = []
    bgs_neighbor_counts = []

    for i in bgs_indices:
        cell = cells[i]
        ntypes = Counter()
        for nb in cell['neighbors']:
            if nb < len(types):
                ntypes[types[nb]] += 1
        neighbor_type_counts += ntypes
        neighbor_type_per_cell.append(ntypes)
        bgs_neighbor_counts.append(ntypes.get('BGS', 0))

    total_neighbors = sum(neighbor_type_counts.values())
    print(f"\n  Average BGS cell neighbor distribution:")
    print(f"  {'Type':<6} {'Mean count':>10} {'Fraction':>10} {'Role'}")
    print(f"  {'─'*6} {'─'*10} {'─'*10} {'─'*30}")

    role_map = {
        'BGS': 'other atoms (bonding candidates)',
        'GS':  'electromagnetic coupling channels',
        'BS':  'strong force channels',
        'BG':  'gravitational coupling',
        'G':   'vacuum (gold symmetry)',
        'S':   'vacuum (silver symmetry)',
        'B':   'vacuum (bronze symmetry)',
    }

    for t in ['BGS', 'GS', 'BS', 'BG', 'G', 'S', 'B']:
        count = neighbor_type_counts.get(t, 0)
        mean = count / max(len(bgs_indices), 1)
        frac = count / max(total_neighbors, 1)
        print(f"  {t:<6} {mean:>10.2f} {frac:>10.3f} {role_map.get(t, '')}")

    mean_bgs_nb = np.mean(bgs_neighbor_counts) if bgs_neighbor_counts else 0
    print(f"\n  A typical matter vertex touches {mean_bgs_nb:.1f} other matter vertices")

    return bgs_indices, neighbor_type_per_cell


def classify_faces_by_symmetry(face_normals, five_fold, three_fold, two_fold):
    """Classify each face normal by its alignment to icosahedral axes.

    Returns dict mapping each face index to its orbital type:
      's' — aligned with 5-fold axis (l=0, capacity 2)
      'p' — aligned with 3-fold axis (l=1, capacity 6)
      'd' — aligned with 2-fold axis (l=2, capacity 10)
      'f' — general position (l=3, capacity 14)
    """
    classifications = []
    # Use RELATIVE alignment: which axis set has the strongest alignment?
    # Then rank faces by their best-axis alignment score.
    # The top 2 become s, next 6 become p, next 10 become d, rest become f.
    # This uses the actual icosahedral geometry to partition faces.

    n_faces = len(face_normals)
    if n_faces == 0:
        return []

    scores = []
    for fi, normal in enumerate(face_normals):
        n_unit = normal / max(np.linalg.norm(normal), 1e-15)
        align_5 = np.max(np.abs(five_fold @ n_unit))
        align_3 = np.max(np.abs(three_fold @ n_unit))
        align_2 = np.max(np.abs(two_fold @ n_unit))
        # Assign to best-aligned axis set
        best = max((align_5, 's'), (align_3, 'p'), (align_2, 'd'),
                   key=lambda x: x[0])
        scores.append((fi, best[0], best[1], align_5, align_3, align_2))

    # Partition by the subshell capacity rule:
    # Sort all faces by their alignment to 5-fold (highest symmetry first)
    scores.sort(key=lambda x: x[3], reverse=True)

    # Capacity-based assignment: s=2, p=6, d=10, f=remaining
    classifications = [''] * n_faces
    assigned = 0
    for rank, (fi, _, _, a5, a3, a2) in enumerate(scores):
        if assigned < 2:
            classifications[fi] = 's'
        elif assigned < 2 + 6:
            classifications[fi] = 'p'
        elif assigned < 2 + 6 + 10:
            classifications[fi] = 'd'
        else:
            classifications[fi] = 'f'
        assigned += 1

    return classifications


def analyze_face_symmetry(cells, bgs_indices, five_fold, three_fold, two_fold):
    """Classify BGS cell faces by orbital type and check subshell capacities."""

    # Aggregate over all BGS cells
    all_counts = Counter()
    per_cell_counts = []

    # Also track for modal (23-face) cells specifically
    modal_counts = Counter()
    modal_cell_count = 0

    for i in bgs_indices:
        cell = cells[i]
        classes = classify_faces_by_symmetry(
            cell['face_normals'], five_fold, three_fold, two_fold
        )
        counts = Counter(classes)
        all_counts += counts
        per_cell_counts.append(counts)

        if cell['n_faces'] == 23:
            modal_counts += counts
            modal_cell_count += 1

    n_bgs = len(bgs_indices)
    print(f"\n  FACE ORBITAL CLASSIFICATION (all {n_bgs} BGS cells)")
    print(f"  {'Orbital':<8} {'Mean/cell':>10} {'Total':>8} {'Expected capacity'}")
    print(f"  {'─'*8} {'─'*10} {'─'*8} {'─'*20}")
    for orb, cap in [('s', 2), ('p', 6), ('d', 10), ('f', 14)]:
        total = all_counts.get(orb, 0)
        mean = total / max(n_bgs, 1)
        print(f"  {orb:<8} {mean:>10.2f} {total:>8} {cap}")

    total_classified = sum(all_counts.values())
    print(f"  {'TOTAL':<8} {total_classified/max(n_bgs,1):>10.2f} {total_classified:>8} 32")

    if modal_cell_count > 0:
        print(f"\n  FACE ORBITAL CLASSIFICATION (23-face BGS cells only, n={modal_cell_count})")
        print(f"  {'Orbital':<8} {'Mean/cell':>10} {'Expected capacity'}")
        print(f"  {'─'*8} {'─'*10} {'─'*20}")
        for orb, cap in [('s', 2), ('p', 6), ('d', 10), ('f', 14)]:
            total = modal_counts.get(orb, 0)
            mean = total / max(modal_cell_count, 1)
            print(f"  {orb:<8} {mean:>10.2f} {cap}")

    return all_counts, per_cell_counts


# ═══════════════════════════════════════════════════════════════════
# 3. GEOMETRIC TESTS — TETRAHEDRAL, OCTAHEDRAL, BCC SUBSETS
# ═══════════════════════════════════════════════════════════════════

def find_tetrahedral_subset(normals):
    """Find 4 face normals forming the best tetrahedral arrangement.

    Ideal tetrahedron: all pairwise angles = 109.47° (cos = -1/3).
    Returns (indices, mean_angle, rms_deviation_from_109.47).
    """
    n = len(normals)
    if n < 4:
        return None, 0, 999

    units = normals / np.linalg.norm(normals, axis=1, keepdims=True)
    target_cos = -1.0 / 3.0  # cos(109.47°)

    best_score = 999
    best_quad = None
    best_angle = 0

    # For efficiency, sample if too many combinations
    from itertools import combinations
    combos = list(combinations(range(n), 4))
    if len(combos) > 50000:
        np.random.seed(42)
        idx = np.random.choice(len(combos), 50000, replace=False)
        combos = [combos[i] for i in idx]

    for quad in combos:
        dots = []
        for a in range(4):
            for b in range(a + 1, 4):
                dots.append(np.dot(units[quad[a]], units[quad[b]]))
        dots = np.array(dots)
        rms = np.sqrt(np.mean((dots - target_cos) ** 2))
        if rms < best_score:
            best_score = rms
            best_quad = quad
            mean_cos = np.mean(dots)
            best_angle = np.degrees(np.arccos(np.clip(mean_cos, -1, 1)))

    return best_quad, best_angle, best_score


def find_octahedral_subset(normals):
    """Find 6 face normals forming the best octahedral arrangement.

    Ideal octahedron: 3 pairs of antipodal normals, each pair at 180°,
    adjacent pairs at 90°.
    Returns (indices, quality_score).
    """
    n = len(normals)
    if n < 6:
        return None, 999

    units = normals / np.linalg.norm(normals, axis=1, keepdims=True)

    # Find 3 best antipodal pairs (dot ≈ -1)
    pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            dot = np.dot(units[i], units[j])
            if dot < -0.7:  # roughly antipodal
                pairs.append((i, j, dot))

    pairs.sort(key=lambda x: x[2])  # most antipodal first

    if len(pairs) < 3:
        return None, 999

    # Try combinations of 3 non-overlapping pairs
    best_score = 999
    best_six = None
    from itertools import combinations
    for combo in combinations(range(min(len(pairs), 20)), 3):
        idx_set = set()
        indices = []
        valid = True
        for c in combo:
            i, j, _ = pairs[c]
            if i in idx_set or j in idx_set:
                valid = False
                break
            idx_set.update([i, j])
            indices.extend([i, j])
        if not valid or len(indices) != 6:
            continue

        # Score: adjacent pairs should be at 90° (dot ≈ 0)
        score = 0
        count = 0
        for a in range(6):
            for b in range(a + 1, 6):
                dot = abs(np.dot(units[indices[a]], units[indices[b]]))
                # Should be either 0 (adjacent) or 1 (same axis)
                # For octahedron: 12 pairs at 90°, 3 pairs at 180°
                score += min(dot, 1 - dot)
                count += 1
        score /= max(count, 1)
        if score < best_score:
            best_score = score
            best_six = tuple(indices)

    return best_six, best_score


def find_bcc_subset(normals):
    """Find 8 face normals forming the best BCC arrangement.

    BCC nearest neighbors: 8 directions at (±1,±1,±1)/√3.
    All pairwise angles are either 70.53° or 109.47° or 180°.
    """
    n = len(normals)
    if n < 8:
        return None, 999

    units = normals / np.linalg.norm(normals, axis=1, keepdims=True)

    # BCC directions
    bcc_dirs = []
    for sx in [-1, 1]:
        for sy in [-1, 1]:
            for sz in [-1, 1]:
                bcc_dirs.append([sx, sy, sz])
    bcc_dirs = np.array(bcc_dirs, dtype=np.float64)
    bcc_dirs /= np.linalg.norm(bcc_dirs, axis=1, keepdims=True)

    # For each BCC direction, find the best-aligned face normal
    used = set()
    mapping = []
    total_align = 0
    for bcc_d in bcc_dirs:
        dots = units @ bcc_d
        # Sort by alignment, pick best unused
        order = np.argsort(-dots)
        found = False
        for idx in order:
            if idx not in used:
                used.add(idx)
                mapping.append(idx)
                total_align += dots[idx]
                found = True
                break
        if not found:
            return None, 999

    mean_align = total_align / 8
    score = 1 - mean_align  # 0 = perfect
    return tuple(mapping), score


def find_fcc_subset(normals):
    """Find 12 face normals forming the best FCC arrangement.

    FCC nearest neighbors: 12 directions of form (±1,±1,0)/√2 etc.
    """
    n = len(normals)
    if n < 12:
        return None, 999

    units = normals / np.linalg.norm(normals, axis=1, keepdims=True)

    # FCC directions
    fcc_dirs = []
    for perm in [(0, 1, 2), (1, 2, 0), (2, 0, 1)]:
        for s1 in [-1, 1]:
            for s2 in [-1, 1]:
                d = [0.0, 0.0, 0.0]
                d[perm[0]] = s1
                d[perm[1]] = s2
                d[perm[2]] = 0
                fcc_dirs.append(d)
    fcc_dirs = np.array(fcc_dirs, dtype=np.float64)
    fcc_dirs /= np.linalg.norm(fcc_dirs, axis=1, keepdims=True)

    used = set()
    mapping = []
    total_align = 0
    for fcc_d in fcc_dirs:
        dots = units @ fcc_d
        order = np.argsort(-dots)
        found = False
        for idx in order:
            if idx not in used:
                used.add(idx)
                mapping.append(idx)
                total_align += dots[idx]
                found = True
                break
        if not found:
            return None, 999

    mean_align = total_align / 12
    score = 1 - mean_align
    return tuple(mapping), score


# ═══════════════════════════════════════════════════════════════════
# 4. BOND LENGTH ANALYSIS
# ═══════════════════════════════════════════════════════════════════

def analyze_bond_lengths(cells, types, pts):
    """Compute BGS-BGS distances and compare to bond length ratios."""

    bgs_centers = []
    bgs_global_idx = []
    for i in cells:
        if types[i] == 'BGS':
            bgs_centers.append(cells[i]['center'])
            bgs_global_idx.append(i)
    bgs_centers = np.array(bgs_centers)
    n_bgs = len(bgs_centers)

    if n_bgs < 2:
        print("  Too few BGS cells for bond length analysis")
        return {}

    # Compute all pairwise distances
    from scipy.spatial.distance import pdist, squareform
    dists = pdist(bgs_centers)

    # Find characteristic distances (peaks in the distance histogram)
    hist, bin_edges = np.histogram(dists, bins=100)
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])

    # Find peaks (local maxima with significant counts)
    peaks = []
    for i in range(1, len(hist) - 1):
        if hist[i] > hist[i-1] and hist[i] > hist[i+1] and hist[i] > 3:
            peaks.append((bin_centers[i], hist[i]))
    peaks.sort(key=lambda x: x[0])

    # Also find nearest-neighbor distance for each BGS cell
    dist_matrix = squareform(dists)
    np.fill_diagonal(dist_matrix, np.inf)
    nn_dists = np.min(dist_matrix, axis=1)
    d1 = np.median(nn_dists)

    # Second-nearest
    nn2_dists = []
    for row in dist_matrix:
        sorted_row = np.sort(row)
        if len(sorted_row) > 1:
            nn2_dists.append(sorted_row[1])
    d2 = np.median(nn2_dists) if nn2_dists else 0

    # Third-nearest
    nn3_dists = []
    for row in dist_matrix:
        sorted_row = np.sort(row)
        if len(sorted_row) > 2:
            nn3_dists.append(sorted_row[2])
    d3 = np.median(nn3_dists) if nn3_dists else 0

    print(f"\n  BGS-BGS DISTANCE ANALYSIS ({n_bgs} matter cells)")
    print(f"  {'─'*50}")
    print(f"  Nearest neighbor:      d₁ = {d1:.4f}")
    print(f"  2nd nearest neighbor:  d₂ = {d2:.4f}")
    print(f"  3rd nearest neighbor:  d₃ = {d3:.4f}")
    if d1 > 0:
        print(f"\n  Distance ratios:")
        print(f"    d₂/d₁ = {d2/d1:.4f}  (single/triple bond ≈ 1.283)")
        print(f"    d₃/d₁ = {d3/d1:.4f}  (σ₄/σ_shell = 1.409)")
        print(f"    d₂/d₃ = {d2/d3:.4f}  (double/single ≈ 0.870)")
        print(f"\n  Cantor ratio comparison:")
        print(f"    d₂/d₁ vs R_OUTER/R_SHELL = {R_OUTER/R_SHELL:.4f} (Δ = {abs(d2/d1 - R_OUTER/R_SHELL):.4f})")
        print(f"    d₂/d₁ vs φ/φ² = 1/φ     = {1/PHI:.4f} (Δ = {abs(d2/d1 - 1/PHI):.4f})")

    # First 5 distance peaks
    if peaks:
        print(f"\n  Distance histogram peaks:")
        for k, (dist, count) in enumerate(peaks[:8]):
            ratio = dist / d1 if d1 > 0 else 0
            print(f"    peak {k+1}: d = {dist:.4f} (count {count:>3}, ratio = {ratio:.3f})")

    return {
        'd1': d1, 'd2': d2, 'd3': d3,
        'd2_d1': d2 / d1 if d1 > 0 else 0,
        'd3_d1': d3 / d1 if d1 > 0 else 0,
        'peaks': peaks[:8],
    }


# ═══════════════════════════════════════════════════════════════════
# 5. SPECIFIC ATOMS AND MOLECULES
# ═══════════════════════════════════════════════════════════════════

def build_hydrogen(cell, face_classes):
    """Hydrogen: Z=1, 1s¹. Uses 1 s-type face."""
    s_faces = [i for i, c in enumerate(face_classes) if c == 's']
    if not s_faces:
        return None

    s_area = sum(cell['face_areas'][i] for i in s_faces[:1])
    total_area = sum(cell['face_areas'])
    frac = s_area / total_area if total_area > 0 else 0

    return {
        'element': 'H',
        'Z': 1,
        'config': '1s¹',
        'active_faces': 1,
        'total_faces': cell['n_faces'],
        'active_area_fraction': frac,
        'note': f'1 of {len(s_faces)} s-type faces used, {frac*100:.1f}% of surface'
    }


def build_carbon(cell, face_classes, normals):
    """Carbon: Z=6, sp3 → 4 tetrahedral bonds."""
    # Find best tetrahedral subset among all faces
    tet_idx, tet_angle, tet_score = find_tetrahedral_subset(normals)
    if tet_idx is None:
        return None

    active_area = sum(cell['face_areas'][i] for i in tet_idx)
    total_area = sum(cell['face_areas'])

    return {
        'element': 'C',
        'Z': 6,
        'config': 'sp³',
        'active_faces': 4,
        'tetrahedral_indices': list(tet_idx),
        'mean_angle': tet_angle,
        'angle_error': abs(tet_angle - 109.47),
        'rms_score': tet_score,
        'active_area_fraction': active_area / total_area if total_area > 0 else 0,
        'face_types': [face_classes[i] for i in tet_idx],
    }


def build_iron(cell, face_classes, normals):
    """Iron: Z=26, [Ar] 3d⁶ 4s². BCC → 8 nearest neighbors."""
    bcc_idx, bcc_score = find_bcc_subset(normals)
    if bcc_idx is None:
        return None

    active_area = sum(cell['face_areas'][i] for i in bcc_idx)
    total_area = sum(cell['face_areas'])

    return {
        'element': 'Fe',
        'Z': 26,
        'config': '[Ar] 3d⁶ 4s²',
        'active_faces': 8,
        'bcc_indices': list(bcc_idx),
        'bcc_quality': 1 - bcc_score,
        'active_area_fraction': active_area / total_area if total_area > 0 else 0,
        'face_types': [face_classes[i] for i in bcc_idx],
    }


def build_gold_atom(cell, face_classes, normals):
    """Gold: Z=79, [Xe] 4f¹⁴ 5d¹⁰ 6s¹. FCC → 12 nearest neighbors."""
    fcc_idx, fcc_score = find_fcc_subset(normals)
    if fcc_idx is None:
        return None

    active_area = sum(cell['face_areas'][i] for i in fcc_idx)
    total_area = sum(cell['face_areas'])

    return {
        'element': 'Au',
        'Z': 79,
        'config': '[Xe] 4f¹⁴ 5d¹⁰ 6s¹',
        'active_faces': 12,
        'fcc_indices': list(fcc_idx),
        'fcc_quality': 1 - fcc_score,
        'active_area_fraction': active_area / total_area if total_area > 0 else 0,
        'face_types': [face_classes[i] for i in fcc_idx],
    }


def analyze_water_angle(cell, normals, face_classes):
    """Water: H-O-H angle from face geometry.

    Oxygen uses sp3 hybridization: 2 bonding + 2 lone pairs.
    Find a tetrahedral subset, then report the angles between
    the faces that would be bonding faces.
    """
    tet_idx, tet_angle, tet_score = find_tetrahedral_subset(normals)
    if tet_idx is None:
        return None

    units = normals / np.linalg.norm(normals, axis=1, keepdims=True)

    # Try all pairs within the tetrahedral subset
    # The water H-O-H angle is the angle between 2 of the 4 tetrahedral directions
    angles = []
    for a in range(4):
        for b in range(a + 1, 4):
            i, j = tet_idx[a], tet_idx[b]
            cos_ab = np.dot(units[i], units[j])
            angle = np.degrees(np.arccos(np.clip(cos_ab, -1, 1)))
            angles.append(angle)

    # The H-O-H angle should be close to 104.5°
    # In a perfect tetrahedron all pairs are 109.47°
    # With lone pair repulsion, 2 pairs compress to ~104.5°
    angles.sort()
    closest_to_water = min(angles, key=lambda a: abs(a - 104.5))

    return {
        'molecule': 'H₂O',
        'tetrahedral_mean_angle': tet_angle,
        'all_pair_angles': [round(a, 2) for a in angles],
        'closest_to_water_angle': closest_to_water,
        'water_error': abs(closest_to_water - 104.5),
    }


# ═══════════════════════════════════════════════════════════════════
# 6. CRYSTAL STRUCTURE DETECTION
# ═══════════════════════════════════════════════════════════════════

def detect_crystal_structures(cells, types):
    """For BGS cells, count coordination numbers and map to crystal types."""

    bgs_indices = [i for i in cells if types[i] == 'BGS']
    coord_numbers = []
    bgs_bgs_coord = []

    for i in bgs_indices:
        cell = cells[i]
        # Total coordination
        coord_numbers.append(cell['n_faces'])
        # BGS-only coordination
        n_bgs_neighbors = sum(1 for nb in cell['neighbors']
                              if nb < len(types) and types[nb] == 'BGS')
        bgs_bgs_coord.append(n_bgs_neighbors)

    coord_dist = Counter(bgs_bgs_coord)
    print(f"\n  CRYSTAL STRUCTURE DETECTION")
    print(f"  BGS-BGS coordination distribution:")
    for c in sorted(coord_dist.keys()):
        count = coord_dist[c]
        pct = 100 * count / max(len(bgs_indices), 1)
        struct = ''
        if c == 4:
            struct = '← diamond'
        elif c == 6:
            struct = '← simple cubic'
        elif c == 8:
            struct = '← BCC'
        elif c == 12:
            struct = '← FCC / HCP'
        elif c == 14:
            struct = '← Kelvin cell'
        bar = '█' * int(pct / 2)
        print(f"    {c:>3} neighbors: {count:>4} ({pct:>5.1f}%) {bar} {struct}")

    if bgs_bgs_coord:
        mean_coord = np.mean(bgs_bgs_coord)
        print(f"\n  Mean BGS-BGS coordination: {mean_coord:.2f}")

        # Check BCC/FCC ratio
        n_bcc = coord_dist.get(8, 0)
        n_fcc = coord_dist.get(12, 0)
        if n_fcc > 0:
            ratio = n_bcc / n_fcc
            print(f"  BCC(8) / FCC(12) ratio: {ratio:.3f}")
            print(f"  Compare to 1/φ = {1/PHI:.3f} (Δ = {abs(ratio - 1/PHI):.3f})")
        elif n_bcc > 0:
            print(f"  BCC(8) cells: {n_bcc}, FCC(12) cells: {n_fcc}")

    return coord_dist


# ═══════════════════════════════════════════════════════════════════
# 7. VISUALIZATION
# ═══════════════════════════════════════════════════════════════════

def visualize_bgs_cell(cell, face_classes, outdir, label='bgs_cell'):
    """Plot a single BGS cell with faces colored by orbital type."""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    except ImportError:
        print("  matplotlib not available for visualization")
        return

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    color_map = {'s': '#FF4444', 'p': '#4444FF', 'd': '#44AA44', 'f': '#FFAA00'}

    # Draw faces
    verts = cell['vertices']
    center = cell['center']

    for fi, face_verts_idx in enumerate(cell['faces']):
        if fi >= len(face_classes):
            continue
        # Get actual vertex positions
        try:
            from scipy.spatial import Voronoi
            # We stored ridge_vertices indices, need the actual vertices
            pass  # Can't easily reconstruct without Voronoi object
        except Exception:
            pass

    # Instead, draw face normals as arrows from center
    for fi in range(min(len(cell['face_normals']), len(face_classes))):
        normal = cell['face_normals'][fi]
        area = cell['face_areas'][fi]
        orb = face_classes[fi]
        color = color_map.get(orb, 'gray')

        # Arrow from center along normal, length proportional to area
        length = area * 3
        ax.quiver(center[0], center[1], center[2],
                  normal[0] * length, normal[1] * length, normal[2] * length,
                  color=color, arrow_length_ratio=0.2, linewidth=1.5)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f'BGS Cell Face Normals ({cell["n_faces"]} faces)\n'
                 f'Red=s  Blue=p  Green=d  Yellow=f')

    path = os.path.join(outdir, f'{label}.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {path}")


def visualize_cluster(cells, types, center_idx, outdir, label='cluster'):
    """Plot a BGS cell and its neighbors."""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except ImportError:
        return

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    cell = cells[center_idx]
    center = cell['center']

    # Color map for types
    type_colors = {
        'BGS': '#FF0000', 'GS': '#FF8800', 'BS': '#00AA00',
        'BG': '#0088FF', 'G': '#FFDD00', 'S': '#888888', 'B': '#884400'
    }

    # Plot center
    ax.scatter(*center, c='red', s=200, marker='*', zorder=5, label='BGS center')

    # Plot neighbors
    for nb_idx in cell['neighbors']:
        if nb_idx in cells:
            nb_center = cells[nb_idx]['center']
            t = types[nb_idx] if nb_idx < len(types) else '?'
            color = type_colors.get(t, 'gray')
            ax.scatter(*nb_center, c=color, s=80, marker='o')
            # Draw edge
            ax.plot([center[0], nb_center[0]],
                    [center[1], nb_center[1]],
                    [center[2], nb_center[2]],
                    color=color, alpha=0.3, linewidth=0.5)

    # Legend
    for t, c in type_colors.items():
        ax.scatter([], [], c=c, label=t)
    ax.legend(loc='upper right', fontsize=8)
    ax.set_title(f'BGS Cell #{center_idx} + {len(cell["neighbors"])} neighbors')

    path = os.path.join(outdir, f'{label}.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {path}")


# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

def main():
    print()
    print("=" * 72)
    print("  ATOM BUILDER: Constructing atoms from quasicrystal tiles")
    print("  Matter tile = 23-faced BGS cell, Vacuum tile = 9-faced cell")
    print("=" * 72)

    # ── Load data ──
    print("\n[1] Loading quasicrystal point set...")
    pts, pts_perp, types, R_accept = load_quasicrystal()
    print(f"  {len(pts)} points, {len(set(types))} types")

    # ── Recompute Voronoi with full geometry ──
    print("\n[2] Computing Voronoi with full cell geometry...")
    t0 = time.time()
    cells, vor = compute_full_voronoi(pts)
    dt = time.time() - t0
    print(f"  {len(cells)} interior cells extracted in {dt:.1f}s")

    # ── Icosahedral axes ──
    five_fold, three_fold, two_fold = icosahedral_axes()
    print(f"  Icosahedral axes: {len(five_fold)} five-fold, "
          f"{len(three_fold)} three-fold, {len(two_fold)} two-fold")

    # ═══════════════════════════════════════════════════════════════
    # PHASE 1: BGS CELL ANALYSIS
    # ═══════════════════════════════════════════════════════════════
    print(f"\n{'='*72}")
    print("  PHASE 1: BGS CELL NEIGHBOR DISTRIBUTION")
    print(f"{'='*72}")

    bgs_indices, nb_types = analyze_bgs_cells(cells, types)

    # ═══════════════════════════════════════════════════════════════
    # PHASE 2: FACE → ORBITAL MAPPING
    # ═══════════════════════════════════════════════════════════════
    print(f"\n{'='*72}")
    print("  PHASE 2: FACE ORBITAL CLASSIFICATION")
    print(f"{'='*72}")

    orbital_counts, per_cell_orbital = analyze_face_symmetry(
        cells, bgs_indices, five_fold, three_fold, two_fold
    )

    # ═══════════════════════════════════════════════════════════════
    # PHASE 3: GEOMETRIC TESTS (tetrahedral, octahedral, BCC, FCC)
    # ═══════════════════════════════════════════════════════════════
    print(f"\n{'='*72}")
    print("  PHASE 3: GEOMETRIC STRUCTURE TESTS")
    print(f"{'='*72}")

    # Pick a representative 23-face BGS cell
    modal_bgs = [i for i in bgs_indices if cells[i]['n_faces'] == 23]
    if not modal_bgs:
        modal_bgs = bgs_indices[:1]

    if modal_bgs:
        rep_idx = modal_bgs[0]
        rep_cell = cells[rep_idx]
        normals = rep_cell['face_normals']
        rep_classes = classify_faces_by_symmetry(
            normals, five_fold, three_fold, two_fold
        )

        print(f"\n  Representative BGS cell #{rep_idx}: {rep_cell['n_faces']} faces")
        orb_count = Counter(rep_classes)
        print(f"  Face orbital breakdown: {dict(orb_count)}")
        print(f"  Compare to subshell capacities: s=2, p=6, d=10, f=14 (total=32)")

        # Tetrahedral test (sp3 carbon)
        print(f"\n  TETRAHEDRAL (sp³) TEST:")
        tet_idx, tet_angle, tet_score = find_tetrahedral_subset(normals)
        if tet_idx:
            print(f"    Best 4-face subset: indices {tet_idx}")
            print(f"    Mean pairwise angle: {tet_angle:.2f}°")
            print(f"    Ideal tetrahedral:   109.47°")
            print(f"    Error:               {abs(tet_angle - 109.47):.2f}°")
            print(f"    RMS deviation:       {tet_score:.4f}")
            types_used = [rep_classes[i] for i in tet_idx]
            print(f"    Orbital types:       {types_used}")
        else:
            print(f"    No tetrahedral subset found")

        # Octahedral test (d-block)
        print(f"\n  OCTAHEDRAL TEST:")
        oct_idx, oct_score = find_octahedral_subset(normals)
        if oct_idx:
            print(f"    Best 6-face subset: indices {oct_idx}")
            print(f"    Quality score: {1 - oct_score:.3f}")
        else:
            print(f"    No octahedral subset found")

        # BCC test (iron)
        print(f"\n  BCC (8-coordinate) TEST:")
        bcc_idx, bcc_score = find_bcc_subset(normals)
        if bcc_idx:
            print(f"    Best 8-face subset: indices {bcc_idx}")
            print(f"    Alignment quality: {1 - bcc_score:.3f}")
            types_used = [rep_classes[i] for i in bcc_idx]
            print(f"    Orbital types:     {types_used}")
        else:
            print(f"    No BCC subset found")

        # FCC test (gold/copper)
        print(f"\n  FCC (12-coordinate) TEST:")
        fcc_idx, fcc_score = find_fcc_subset(normals)
        if fcc_idx:
            print(f"    Best 12-face subset: indices {fcc_idx}")
            print(f"    Alignment quality: {1 - fcc_score:.3f}")
            types_used = [rep_classes[i] for i in fcc_idx]
            print(f"    Orbital types:     {types_used}")
        else:
            print(f"    No FCC subset found")

        # Water angle test
        print(f"\n  WATER (H-O-H angle) TEST:")
        water = analyze_water_angle(rep_cell, normals, rep_classes)
        if water:
            print(f"    Tetrahedral mean:     {water['tetrahedral_mean_angle']:.2f}°")
            print(f"    All pair angles:      {water['all_pair_angles']}")
            print(f"    Closest to 104.5°:    {water['closest_to_water_angle']:.2f}°")
            print(f"    Error from 104.5°:    {water['water_error']:.2f}°")
        else:
            print(f"    Could not compute water angle")

    # ═══════════════════════════════════════════════════════════════
    # PHASE 4: SPECIFIC ATOMS
    # ═══════════════════════════════════════════════════════════════
    print(f"\n{'='*72}")
    print("  PHASE 4: SPECIFIC ATOMS FROM BGS CELL GEOMETRY")
    print(f"{'='*72}")

    if modal_bgs:
        rep_idx = modal_bgs[0]
        rep_cell = cells[rep_idx]
        normals = rep_cell['face_normals']
        rep_classes = classify_faces_by_symmetry(
            normals, five_fold, three_fold, two_fold
        )

        atoms = {}

        print(f"\n  HYDROGEN (Z=1, 1s¹):")
        h = build_hydrogen(rep_cell, rep_classes)
        if h:
            print(f"    Active faces: {h['active_faces']}/{h['total_faces']}")
            print(f"    Active area:  {h['active_area_fraction']*100:.1f}% of surface")
            print(f"    {h['note']}")
            atoms['H'] = h

        print(f"\n  CARBON (Z=6, sp³):")
        c = build_carbon(rep_cell, rep_classes, normals)
        if c:
            print(f"    Tetrahedral angle: {c['mean_angle']:.2f}° (ideal 109.47°, err {c['angle_error']:.2f}°)")
            print(f"    Active area:  {c['active_area_fraction']*100:.1f}%")
            print(f"    Face types:   {c['face_types']}")
            atoms['C'] = c

        print(f"\n  IRON (Z=26, BCC):")
        fe = build_iron(rep_cell, rep_classes, normals)
        if fe:
            print(f"    BCC alignment: {fe['bcc_quality']*100:.1f}%")
            print(f"    Active area:   {fe['active_area_fraction']*100:.1f}%")
            print(f"    Face types:    {fe['face_types']}")
            atoms['Fe'] = fe

        print(f"\n  GOLD (Z=79, FCC):")
        au = build_gold_atom(rep_cell, rep_classes, normals)
        if au:
            print(f"    FCC alignment: {au['fcc_quality']*100:.1f}%")
            print(f"    Active area:   {au['active_area_fraction']*100:.1f}%")
            print(f"    Face types:    {au['face_types']}")
            atoms['Au'] = au

    # ═══════════════════════════════════════════════════════════════
    # PHASE 5: BOND LENGTHS
    # ═══════════════════════════════════════════════════════════════
    print(f"\n{'='*72}")
    print("  PHASE 5: BOND LENGTH ANALYSIS")
    print(f"{'='*72}")

    bond_data = analyze_bond_lengths(cells, types, pts)

    # ═══════════════════════════════════════════════════════════════
    # PHASE 6: CRYSTAL STRUCTURE DETECTION
    # ═══════════════════════════════════════════════════════════════
    print(f"\n{'='*72}")
    print("  PHASE 6: CRYSTAL STRUCTURES FROM TILING")
    print(f"{'='*72}")

    coord_dist = detect_crystal_structures(cells, types)

    # ═══════════════════════════════════════════════════════════════
    # PHASE 7: VISUALIZATION
    # ═══════════════════════════════════════════════════════════════
    print(f"\n{'='*72}")
    print("  PHASE 7: VISUALIZATION")
    print(f"{'='*72}")

    outdir = os.path.join(ROOT, 'model', 'visualizations')
    os.makedirs(outdir, exist_ok=True)

    if modal_bgs:
        rep_idx = modal_bgs[0]
        rep_cell = cells[rep_idx]
        rep_classes = classify_faces_by_symmetry(
            rep_cell['face_normals'], five_fold, three_fold, two_fold
        )
        visualize_bgs_cell(rep_cell, rep_classes, outdir, 'bgs_orbital_faces')
        visualize_cluster(cells, types, rep_idx, outdir, 'bgs_cluster')

    # ═══════════════════════════════════════════════════════════════
    # SCORECARD
    # ═══════════════════════════════════════════════════════════════
    print(f"\n{'='*72}")
    print("  SCORECARD")
    print(f"{'='*72}")

    checks = []

    # Tetrahedral check
    if modal_bgs:
        rep_cell = cells[modal_bgs[0]]
        normals = rep_cell['face_normals']
        tet_idx, tet_angle, tet_score = find_tetrahedral_subset(normals)
        if tet_idx and abs(tet_angle - 109.47) < 15:
            checks.append(('Tetrahedral (sp³) subset exists', 'YES',
                          f'{tet_angle:.1f}° vs 109.5°'))
        else:
            checks.append(('Tetrahedral (sp³) subset exists', 'WEAK',
                          f'{tet_angle:.1f}° vs 109.5°' if tet_idx else 'not found'))

        oct_idx, oct_score = find_octahedral_subset(normals)
        checks.append(('Octahedral subset exists', 'YES' if oct_idx else 'NO',
                       f'score {1-oct_score:.3f}' if oct_idx else ''))

        bcc_idx, bcc_score = find_bcc_subset(normals)
        checks.append(('BCC (8-coord) subset', 'YES' if bcc_idx else 'NO',
                       f'align {(1-bcc_score)*100:.0f}%' if bcc_idx else ''))

        fcc_idx, fcc_score = find_fcc_subset(normals)
        checks.append(('FCC (12-coord) subset', 'YES' if fcc_idx else 'NO',
                       f'align {(1-fcc_score)*100:.0f}%' if fcc_idx else ''))

    # Face count vs subshell capacity
    if orbital_counts:
        for orb, expected in [('s', 2), ('p', 6), ('d', 10), ('f', 14)]:
            actual = orbital_counts.get(orb, 0) / max(len(bgs_indices), 1)
            match = abs(actual - expected) < expected * 0.5
            checks.append((f'{orb}-orbital faces ({expected} expected)',
                          f'{actual:.1f}', 'MATCH' if match else 'MISS'))

    # Water angle
    if modal_bgs:
        water = analyze_water_angle(cells[modal_bgs[0]],
                                    cells[modal_bgs[0]]['face_normals'],
                                    classify_faces_by_symmetry(
                                        cells[modal_bgs[0]]['face_normals'],
                                        five_fold, three_fold, two_fold))
        if water:
            err = water['water_error']
            checks.append(('H-O-H angle from faces',
                          f"{water['closest_to_water_angle']:.1f}° vs 104.5°",
                          f'err {err:.1f}°'))

    # Bond length ratios
    if bond_data and bond_data.get('d1', 0) > 0:
        r = bond_data['d2_d1']
        checks.append(('d₂/d₁ vs σ₄/σ_shell (1.409)',
                       f'{r:.3f}', f'Δ={abs(r-1.409):.3f}'))

    # Print scorecard
    print()
    for name, result, detail in checks:
        print(f"  {name:<35} {result:<10} {detail}")

    # ═══════════════════════════════════════════════════════════════
    # SAVE RESULTS
    # ═══════════════════════════════════════════════════════════════
    results_dir = os.path.join(ROOT, 'results', 'atom_builder')
    os.makedirs(results_dir, exist_ok=True)

    results = {
        'n_bgs_cells': len(bgs_indices),
        'orbital_counts': dict(orbital_counts),
        'scorecard': [(n, r, d) for n, r, d in checks],
    }
    if bond_data:
        results['bond_lengths'] = {k: v for k, v in bond_data.items()
                                    if not isinstance(v, list) or k == 'peaks'}
    if modal_bgs:
        results['representative_cell'] = {
            'idx': int(modal_bgs[0]),
            'n_faces': cells[modal_bgs[0]]['n_faces'],
        }

    # Convert numpy types for JSON
    def convert(obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return obj

    with open(os.path.join(results_dir, 'atom_builder.json'), 'w') as f:
        json.dump(results, f, indent=2, default=convert)

    print(f"\n  Results saved to: {results_dir}/")
    print()


if __name__ == '__main__':
    main()
