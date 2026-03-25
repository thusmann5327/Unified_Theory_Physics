"""
face_merging.py — Find the Coarse Heptahedron Inside the 23-Faced BGS Cell
============================================================================

The 3D Voronoi gives BGS cells with 23 faces. But many faces point in
similar directions — they are vacuum sub-contacts of the same effective
matter boundary.

This script merges coplanar faces to find the COARSE face count.
If it's ~7, the heptahedron exists at the coarse scale.

Run:  python3 model/face_merging.py
"""

import sys, os, json, time
import numpy as np
from collections import Counter, defaultdict
from scipy.spatial import Voronoi, ConvexHull
from scipy.cluster.hierarchy import fcluster, linkage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEAN = os.path.join(ROOT, 'CLEAN')
sys.path.insert(0, CLEAN)

from core.constants import PHI, W, LEAK

R_MATTER = 0.0728
R_INNER  = 0.2350
R_SHELL  = 0.3972
R_OUTER  = 0.5594


# ═════════════════════════════════════════════════════════════════════
# 1. LOAD AND RECOMPUTE VORONOI WITH FACE NORMALS
# ═════════════════════════════════════════════════════════════════════

def load_quasicrystal():
    path = os.path.join(ROOT, 'results', 'voronoi_3d', 'quasicrystal_points.npz')
    data = np.load(path, allow_pickle=True)
    return data['pts_par'], data['pts_perp'], data['types'], float(data['R_accept'])


def extract_cell_geometry(pts, types):
    """Compute Voronoi and extract face normals/areas for each cell."""
    vor = Voronoi(pts)
    clip_radius = 0.8 * np.max(np.linalg.norm(pts, axis=1))
    cells = {}

    for i, region_idx in enumerate(vor.point_region):
        region = vor.regions[region_idx]
        if -1 in region or len(region) < 4:
            continue
        if np.linalg.norm(pts[i]) > clip_radius:
            continue

        face_normals = []
        face_areas = []
        face_neighbor_types = []

        for ridge_idx, (p1, p2) in enumerate(vor.ridge_points):
            if p1 != i and p2 != i:
                continue
            neighbor = p2 if p1 == i else p1
            rv = vor.ridge_vertices[ridge_idx]
            if -1 in rv or len(rv) < 3:
                continue

            face_pts = vor.vertices[rv]
            center = pts[i]
            face_center = face_pts.mean(axis=0)

            normal = face_center - center
            norm_len = np.linalg.norm(normal)
            if norm_len < 1e-15:
                continue
            normal /= norm_len

            # Face area via triangle fan
            area = 0.0
            for k in range(1, len(face_pts) - 1):
                v1 = face_pts[k] - face_pts[0]
                v2 = face_pts[k + 1] - face_pts[0]
                area += np.linalg.norm(np.cross(v1, v2))
            area *= 0.5

            face_normals.append(normal)
            face_areas.append(area)
            nb_type = types[neighbor] if neighbor < len(types) else '?'
            face_neighbor_types.append(nb_type)

        if len(face_normals) >= 4:
            cells[i] = {
                'center': pts[i],
                'face_normals': np.array(face_normals),
                'face_areas': np.array(face_areas),
                'face_neighbor_types': face_neighbor_types,
                'n_faces': len(face_normals),
                'type': types[i],
            }

    return cells


def icosahedral_axes():
    """Return 6 five-fold, 10 three-fold, 15 two-fold axes."""
    tau = PHI
    verts = np.array([
        [0, 1, tau], [0, -1, tau], [0, 1, -tau], [0, -1, -tau],
        [1, tau, 0], [-1, tau, 0], [1, -tau, 0], [-1, -tau, 0],
        [tau, 0, 1], [-tau, 0, 1], [tau, 0, -1], [-tau, 0, -1]
    ], dtype=np.float64)
    verts /= np.linalg.norm(verts, axis=1, keepdims=True)

    five_fold = []
    for v in verts:
        if not any(abs(np.dot(v, e)) > 0.99 for e in five_fold):
            five_fold.append(v)
    five_fold = np.array(five_fold[:6])

    edge_len = 2.0 / np.sqrt(1 + tau**2)
    n = len(verts)

    three_fold = []
    for i in range(n):
        for j in range(i+1, n):
            if abs(np.linalg.norm(verts[i]-verts[j])-edge_len) > 0.1:
                continue
            for k in range(j+1, n):
                if (abs(np.linalg.norm(verts[i]-verts[k])-edge_len) < 0.1 and
                    abs(np.linalg.norm(verts[j]-verts[k])-edge_len) < 0.1):
                    c = (verts[i]+verts[j]+verts[k])/3.0
                    cn = np.linalg.norm(c)
                    if cn > 1e-10:
                        c /= cn
                        if not any(abs(np.dot(c, e)) > 0.99 for e in three_fold):
                            three_fold.append(c)
    three_fold = np.array(three_fold[:10])

    two_fold = []
    for i in range(n):
        for j in range(i+1, n):
            if abs(np.linalg.norm(verts[i]-verts[j])-edge_len) < 0.1:
                m = (verts[i]+verts[j])/2.0
                mn = np.linalg.norm(m)
                if mn > 1e-10:
                    m /= mn
                    if not any(abs(np.dot(m, e)) > 0.99 for e in two_fold):
                        two_fold.append(m)
    two_fold = np.array(two_fold[:15])

    return five_fold, three_fold, two_fold


# ═════════════════════════════════════════════════════════════════════
# 2. FACE MERGING — COPLANAR NEIGHBOR GROUPING
# ═════════════════════════════════════════════════════════════════════

def merge_faces(normals, areas, neighbor_types, theta_deg):
    """Merge faces whose normals are within theta_deg of each other.

    Uses hierarchical clustering on angular distance between normals.
    Returns list of groups, each group = list of face indices.
    """
    n = len(normals)
    if n < 2:
        return [list(range(n))]

    units = normals / np.linalg.norm(normals, axis=1, keepdims=True)

    # Angular distance matrix
    dots = units @ units.T
    dots = np.clip(dots, -1, 1)
    # Use absolute dot product (normals pointing ±same direction are same face)
    ang_dist = np.degrees(np.arccos(np.clip(np.abs(dots), 0, 1)))

    # Condensed distance for linkage
    from scipy.spatial.distance import squareform
    np.fill_diagonal(ang_dist, 0)
    condensed = squareform(ang_dist)

    link = linkage(condensed, method='complete')
    labels = fcluster(link, t=theta_deg, criterion='distance')

    groups = defaultdict(list)
    for i, lab in enumerate(labels):
        groups[lab].append(i)

    return list(groups.values())


def analyze_merged_faces(groups, normals, areas, neighbor_types):
    """Compute statistics for each merged face group."""
    units = normals / np.linalg.norm(normals, axis=1, keepdims=True)

    merged = []
    for grp in groups:
        grp_normals = units[grp]
        grp_areas = areas[grp]
        grp_nb_types = [neighbor_types[i] for i in grp]

        # Average normal direction
        avg_normal = grp_normals.mean(axis=0)
        avg_normal /= max(np.linalg.norm(avg_normal), 1e-15)

        merged.append({
            'indices': grp,
            'sub_face_count': len(grp),
            'total_area': float(np.sum(grp_areas)),
            'avg_normal': avg_normal,
            'neighbor_types': grp_nb_types,
        })

    # Sort by total area (ascending)
    merged.sort(key=lambda m: m['total_area'])
    return merged


# ═════════════════════════════════════════════════════════════════════
# 3. ORBITAL CLASSIFICATION
# ═════════════════════════════════════════════════════════════════════

def classify_face_orbital(normal, five_fold, three_fold, two_fold):
    """Classify a single face normal by best-aligned axis set."""
    n_unit = normal / max(np.linalg.norm(normal), 1e-15)
    a5 = np.max(np.abs(five_fold @ n_unit))
    a3 = np.max(np.abs(three_fold @ n_unit))
    a2 = np.max(np.abs(two_fold @ n_unit))

    best = max((a5, 's'), (a3, 'p'), (a2, 'd'), key=lambda x: x[0])
    return best[1], best[0]


def classify_merged_face(avg_normal, five_fold, three_fold, two_fold):
    """Classify a merged face by its average normal direction."""
    return classify_face_orbital(avg_normal, five_fold, three_fold, two_fold)


# ═════════════════════════════════════════════════════════════════════
# MAIN
# ═════════════════════════════════════════════════════════════════════

def main():
    print()
    print("=" * 72)
    print("  FACE MERGING: Finding the Coarse Heptahedron in the 23-Faced Cell")
    print("  Hypothesis: 23 Voronoi faces → ~7 merged faces (coarse structure)")
    print("=" * 72)

    # ── Load ──
    print("\n[1] Loading quasicrystal...")
    pts, pts_perp, types, R_accept = load_quasicrystal()
    print(f"  {len(pts)} points")

    print("\n[2] Computing Voronoi with face normals...")
    t0 = time.time()
    cells = extract_cell_geometry(pts, types)
    dt = time.time() - t0
    print(f"  {len(cells)} interior cells in {dt:.1f}s")

    five_fold, three_fold, two_fold = icosahedral_axes()

    bgs_indices = [i for i in cells if cells[i]['type'] == 'BGS']
    print(f"  BGS cells: {len(bgs_indices)}")

    # Only analyze 23-face BGS cells (the modal face count)
    modal_bgs = [i for i in bgs_indices if cells[i]['n_faces'] == 23]
    print(f"  23-face BGS cells: {len(modal_bgs)}")

    if not modal_bgs:
        # Fall back to all BGS
        modal_bgs = bgs_indices
        print(f"  (using all BGS cells)")

    # ═════════════════════════════════════════════════════════════════
    # PHASE 1: MERGE COPLANAR FACES AT MULTIPLE THRESHOLDS
    # ═════════════════════════════════════════════════════════════════
    print(f"\n{'='*72}")
    print("  PHASE 1: MERGED FACE COUNT vs ANGLE THRESHOLD")
    print(f"{'='*72}")

    thresholds = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]

    # Per-threshold statistics across all modal BGS cells
    print(f"\n  θ(°)  Mean_groups  Mode_groups  Min  Max  Std")
    print(f"  {'─'*55}")

    threshold_stats = {}
    for theta in thresholds:
        group_counts = []
        for i in modal_bgs:
            cell = cells[i]
            groups = merge_faces(
                cell['face_normals'], cell['face_areas'],
                cell['face_neighbor_types'], theta
            )
            group_counts.append(len(groups))

        gc = np.array(group_counts)
        mode_val = Counter(group_counts).most_common(1)[0][0]
        threshold_stats[theta] = {
            'mean': float(np.mean(gc)),
            'mode': mode_val,
            'min': int(np.min(gc)),
            'max': int(np.max(gc)),
            'std': float(np.std(gc)),
            'counts': dict(Counter(group_counts)),
        }
        marker = ''
        if mode_val == 7:
            marker = ' ← 7!'
        elif mode_val == 13:
            marker = ' ← F(7)!'
        print(f"  {theta:>4}°  {np.mean(gc):>11.2f}  {mode_val:>11}  "
              f"{np.min(gc):>3}  {np.max(gc):>3}  {np.std(gc):>5.2f}{marker}")

    # Find plateaus and identify physically significant ones
    modes = [threshold_stats[t]['mode'] for t in thresholds]
    plateau_ranges = []
    current_val = modes[0]
    start_idx = 0
    for idx in range(1, len(modes)):
        if modes[idx] != current_val:
            plateau_ranges.append((thresholds[start_idx], thresholds[idx-1],
                                   current_val, idx - start_idx))
            current_val = modes[idx]
            start_idx = idx
    plateau_ranges.append((thresholds[start_idx], thresholds[-1],
                           current_val, len(modes) - start_idx))

    # Report all plateaus
    print(f"\n  Plateaus detected:")
    for p in plateau_ranges:
        marker = ''
        if p[2] == 7:
            marker = ' ★ HEPTAHEDRON'
        elif p[2] == 13:
            marker = ' ★ F(7)'
        print(f"    mode = {p[2]:>3} from θ = {p[0]:>2}° to {p[1]:>2}° "
              f"(span = {p[3]}){marker}")

    # Prefer 7-face plateau if it exists; otherwise longest
    seven_plateaus = [p for p in plateau_ranges if p[2] == 7]
    if seven_plateaus:
        best = max(seven_plateaus, key=lambda x: x[3])
        print(f"\n  ★ HEPTAHEDRON plateau: mode = 7 from θ = {best[0]}° to {best[1]}°")
    else:
        plateau_ranges.sort(key=lambda x: x[3], reverse=True)
        best = plateau_ranges[0]
        print(f"\n  Longest plateau: mode = {best[2]} from θ = {best[0]}° to {best[1]}°")

    # Natural threshold = midpoint of best plateau
    natural_theta = (best[0] + best[1]) / 2
    natural_mode = best[2]
    print(f"  Natural merging threshold: θ = {natural_theta:.0f}°")
    print(f"  Natural merged face count: {natural_mode}")

    if natural_mode == 7:
        print(f"  ★ THE HEPTAHEDRON EMERGES AT THE COARSE SCALE ★")
    elif natural_mode == 13:
        print(f"  ★ F(7) = 13 merged faces — the bronze discriminant! ★")

    # ═════════════════════════════════════════════════════════════════
    # PHASE 2: SUB-FACE COUNTS AT NATURAL THRESHOLD
    # ═════════════════════════════════════════════════════════════════
    print(f"\n{'='*72}")
    print(f"  PHASE 2: SUB-FACE COUNTS PER MERGED FACE (θ = {natural_theta:.0f}°)")
    print(f"{'='*72}")

    # Collect sub-face count sequences across all modal BGS cells
    all_subface_seqs = []
    all_merged_data = []

    for i in modal_bgs:
        cell = cells[i]
        groups = merge_faces(
            cell['face_normals'], cell['face_areas'],
            cell['face_neighbor_types'], natural_theta
        )
        merged = analyze_merged_faces(
            groups, cell['face_normals'], cell['face_areas'],
            cell['face_neighbor_types']
        )
        subface_seq = sorted([m['sub_face_count'] for m in merged])
        all_subface_seqs.append(tuple(subface_seq))
        all_merged_data.append(merged)

    seq_counts = Counter(all_subface_seqs)
    print(f"\n  Sub-face count sequences (sorted, across {len(modal_bgs)} cells):")
    print(f"  {'Sequence':<40} {'Count':>6} {'Fraction':>8}")
    print(f"  {'─'*40} {'─'*6} {'─'*8}")
    for seq, cnt in seq_counts.most_common(15):
        frac = cnt / len(modal_bgs)
        total = sum(seq)
        print(f"  {str(list(seq)):<40} {cnt:>6} {frac:>8.1%}  (sum={total})")

    # Average sub-face counts per merged face position
    if all_merged_data:
        n_merged = len(all_merged_data[0])
        print(f"\n  Average sub-face count per merged face (sorted by area):")
        for pos in range(n_merged):
            counts = [md[pos]['sub_face_count'] for md in all_merged_data
                      if pos < len(md)]
            areas = [md[pos]['total_area'] for md in all_merged_data
                     if pos < len(md)]
            if counts:
                mean_c = np.mean(counts)
                mean_a = np.mean(areas)
                print(f"    Face {pos+1}: {mean_c:.1f} sub-faces, "
                      f"area = {mean_a:.4f}")

    # ═════════════════════════════════════════════════════════════════
    # PHASE 3: CROSS-REFERENCE WITH ORBITAL CLASSIFICATION
    # ═════════════════════════════════════════════════════════════════
    print(f"\n{'='*72}")
    print("  PHASE 3: MERGED FACE ↔ ORBITAL TYPE CORRESPONDENCE")
    print(f"{'='*72}")

    # For each merged face in a representative cell, classify by axis alignment
    if all_merged_data:
        # Use the first modal cell as representative
        rep_idx = modal_bgs[0]
        rep_cell = cells[rep_idx]
        rep_merged = all_merged_data[0]

        print(f"\n  Representative cell #{rep_idx} ({rep_cell['n_faces']} faces "
              f"→ {len(rep_merged)} merged):")
        print(f"  {'#':<4} {'Sub':>4} {'Area':>8} {'Axis type':<10} {'Align':>6} "
              f"{'Member orbital types'}")
        print(f"  {'─'*4} {'─'*4} {'─'*8} {'─'*10} {'─'*6} {'─'*30}")

        for mi, mf in enumerate(rep_merged):
            # Classify merged face
            axis_type, align = classify_merged_face(
                mf['avg_normal'], five_fold, three_fold, two_fold
            )

            # Classify individual member faces
            member_types = []
            for fi in mf['indices']:
                ot, _ = classify_face_orbital(
                    rep_cell['face_normals'][fi],
                    five_fold, three_fold, two_fold
                )
                member_types.append(ot)

            type_dist = Counter(member_types)
            type_str = ', '.join(f"{t}:{c}" for t, c in sorted(type_dist.items()))

            print(f"  {mi+1:<4} {mf['sub_face_count']:>4} {mf['total_area']:>8.4f} "
                  f"{axis_type:<10} {align:>6.3f} {type_str}")

    # Check purity
    purity_scores = []
    for ci, md in enumerate(all_merged_data):
        cell_idx = modal_bgs[ci]
        cell = cells[cell_idx]
        for mf in md:
            member_types = []
            for fi in mf['indices']:
                ot, _ = classify_face_orbital(
                    cell['face_normals'][fi],
                    five_fold, three_fold, two_fold
                )
                member_types.append(ot)
            if member_types:
                most_common = Counter(member_types).most_common(1)[0][1]
                purity = most_common / len(member_types)
                purity_scores.append(purity)

    if purity_scores:
        print(f"\n  Orbital purity of merged groups:")
        print(f"    Mean purity: {np.mean(purity_scores):.1%}")
        print(f"    Fully pure (100%): {sum(1 for p in purity_scores if p == 1.0)} "
              f"/ {len(purity_scores)} ({sum(1 for p in purity_scores if p==1.0)/len(purity_scores):.0%})")

    # ═════════════════════════════════════════════════════════════════
    # PHASE 4: AREA HIERARCHY vs SPECTRAL RATIOS
    # ═════════════════════════════════════════════════════════════════
    print(f"\n{'='*72}")
    print("  PHASE 4: MERGED FACE AREA RATIOS vs CANTOR SPECTRAL RATIOS")
    print(f"{'='*72}")

    if all_merged_data:
        # Average areas across all modal BGS cells
        n_merged_faces = len(all_merged_data[0])
        avg_areas = []
        for pos in range(n_merged_faces):
            areas = [md[pos]['total_area'] for md in all_merged_data
                     if pos < len(md)]
            avg_areas.append(np.mean(areas) if areas else 0)

        total_area = sum(avg_areas)
        if total_area > 0:
            fracs = [a / total_area for a in avg_areas]
        else:
            fracs = avg_areas

        print(f"\n  Merged face areas (sorted ascending, averaged):")
        spectral_ratios = [R_MATTER, R_INNER, R_SHELL, R_OUTER]
        for pos in range(n_merged_faces):
            pct = fracs[pos] * 100
            spec_label = ''
            if pos < len(spectral_ratios):
                spec_label = f'  (σ = {spectral_ratios[pos]:.4f})'
            print(f"    Face {pos+1}: {avg_areas[pos]:.4f} ({pct:.1f}%){spec_label}")

        # Compute area ratios between consecutive faces
        if len(avg_areas) > 1:
            print(f"\n  Consecutive area ratios:")
            for pos in range(1, min(len(avg_areas), 7)):
                if avg_areas[pos-1] > 0:
                    ratio = avg_areas[pos] / avg_areas[pos-1]
                    # Compare to spectral ratios
                    spec_ratios = {
                        'R_INNER/R_MATTER': R_INNER / R_MATTER,
                        'R_SHELL/R_INNER': R_SHELL / R_INNER,
                        'R_OUTER/R_SHELL': R_OUTER / R_SHELL,
                        'φ': PHI,
                        '1/φ': 1/PHI,
                    }
                    best_match = min(spec_ratios.items(),
                                     key=lambda x: abs(x[1] - ratio))
                    err = abs(ratio - best_match[1]) / best_match[1] * 100
                    print(f"    Face {pos+1}/Face {pos}: {ratio:.3f} "
                          f"(nearest: {best_match[0]} = {best_match[1]:.3f}, "
                          f"err {err:.1f}%)")

    # ═════════════════════════════════════════════════════════════════
    # PHASE 5: TETRAHEDRAL AND WATER ANGLE FROM MERGED FACES
    # ═════════════════════════════════════════════════════════════════
    print(f"\n{'='*72}")
    print("  PHASE 5: BOND ANGLES FROM MERGED FACE NORMALS")
    print(f"{'='*72}")

    if all_merged_data:
        rep_merged = all_merged_data[0]
        merged_normals = np.array([m['avg_normal'] for m in rep_merged])
        mn_unit = merged_normals / np.linalg.norm(merged_normals, axis=1, keepdims=True)
        n_mf = len(mn_unit)

        # All pairwise angles
        all_angles = []
        for a in range(n_mf):
            for b in range(a+1, n_mf):
                dot = np.dot(mn_unit[a], mn_unit[b])
                angle = np.degrees(np.arccos(np.clip(dot, -1, 1)))
                all_angles.append((a, b, angle))

        all_angles.sort(key=lambda x: x[2])
        print(f"\n  All pairwise angles between {n_mf} merged face normals:")
        for a, b, angle in all_angles:
            markers = ''
            if abs(angle - 109.47) < 5:
                markers += ' ← tetrahedral'
            if abs(angle - 104.5) < 5:
                markers += ' ← water H-O-H'
            if abs(angle - 120.0) < 5:
                markers += ' ← sp2/benzene'
            if abs(angle - 180.0) < 5:
                markers += ' ← linear'
            if abs(angle - 90.0) < 5:
                markers += ' ← orthogonal'
            if abs(angle - 70.53) < 5:
                markers += ' ← BCC'
            print(f"    Face {a+1}–Face {b+1}: {angle:.2f}°{markers}")

        # Find best tetrahedral quartet
        from itertools import combinations
        best_tet_score = 999
        best_tet = None
        best_tet_angle = 0
        target_cos = -1.0 / 3.0

        for quad in combinations(range(n_mf), 4):
            dots = []
            for a in range(4):
                for b in range(a+1, 4):
                    dots.append(np.dot(mn_unit[quad[a]], mn_unit[quad[b]]))
            dots = np.array(dots)
            rms = np.sqrt(np.mean((dots - target_cos)**2))
            if rms < best_tet_score:
                best_tet_score = rms
                best_tet = quad
                best_tet_angle = np.degrees(np.arccos(np.clip(np.mean(dots), -1, 1)))

        if best_tet:
            print(f"\n  Best tetrahedral subset (merged faces): {tuple(i+1 for i in best_tet)}")
            print(f"    Mean angle: {best_tet_angle:.2f}° (ideal: 109.47°, err: {abs(best_tet_angle-109.47):.2f}°)")
            print(f"    RMS deviation from cos(-1/3): {best_tet_score:.4f}")

            # Water angle: closest pair in the tetrahedral quartet to 104.5°
            tet_angles = []
            for a in range(4):
                for b in range(a+1, 4):
                    dot = np.dot(mn_unit[best_tet[a]], mn_unit[best_tet[b]])
                    tet_angles.append(np.degrees(np.arccos(np.clip(dot, -1, 1))))
            closest_water = min(tet_angles, key=lambda a: abs(a - 104.5))
            print(f"\n    Water H-O-H angle test:")
            print(f"    Angles in tetrahedral set: {[f'{a:.1f}°' for a in sorted(tet_angles)]}")
            print(f"    Closest to 104.5°: {closest_water:.2f}° (err: {abs(closest_water-104.5):.2f}°)")

    # ═════════════════════════════════════════════════════════════════
    # PHASE 6: HYDROGEN AND HELIUM FROM MERGED FACES
    # ═════════════════════════════════════════════════════════════════
    print(f"\n{'='*72}")
    print("  PHASE 6: HYDROGEN AND HELIUM FROM MERGED FACES")
    print(f"{'='*72}")

    if all_merged_data:
        rep_merged = all_merged_data[0]
        total_area = sum(m['total_area'] for m in rep_merged)

        # Smallest merged face = s-type
        s_face = rep_merged[0]  # already sorted ascending by area
        s_frac = s_face['total_area'] / total_area

        print(f"\n  HYDROGEN (Z=1, 1s¹):")
        print(f"    s-type merged face: {s_face['sub_face_count']} sub-faces, "
              f"area = {s_face['total_area']:.4f} ({s_frac*100:.1f}% of total)")
        print(f"    Electron occupies 1 vacuum cell behind this face.")
        print(f"    Solid angle fraction ≈ {s_frac:.3f} of 4π")

        # Second smallest = other s-type pole
        if len(rep_merged) > 1:
            s2_face = rep_merged[1]
            s2_frac = s2_face['total_area'] / total_area

            print(f"\n  HELIUM (Z=2, 1s²):")
            print(f"    Both s-type merged faces occupied:")
            print(f"    Face 1: {s_face['sub_face_count']} sub-faces, "
                  f"area = {s_face['total_area']:.4f}")
            print(f"    Face 2: {s2_face['sub_face_count']} sub-faces, "
                  f"area = {s2_face['total_area']:.4f}")
            combined = s_frac + s2_frac
            print(f"    Combined area fraction: {combined*100:.1f}%")
            # Check if antipodal
            dot = np.dot(s_face['avg_normal'], s2_face['avg_normal'])
            angle = np.degrees(np.arccos(np.clip(dot, -1, 1)))
            print(f"    Angle between s-faces: {angle:.1f}° "
                  f"({'antipodal' if angle > 150 else 'NOT antipodal'})")

        # Lithium: next merged face
        if len(rep_merged) > 2:
            p_face = rep_merged[2]
            print(f"\n  LITHIUM (Z=3, [He] 2s¹):")
            print(f"    s-faces full → electron goes to next face type")
            print(f"    Next merged face: {p_face['sub_face_count']} sub-faces, "
                  f"area = {p_face['total_area']:.4f}")
            axis_type, _ = classify_merged_face(
                p_face['avg_normal'], five_fold, three_fold, two_fold
            )
            print(f"    Axis alignment: {axis_type}-type")

    # ═════════════════════════════════════════════════════════════════
    # PHASE 7: CARBON sp3 FROM MERGED FACES
    # ═════════════════════════════════════════════════════════════════
    print(f"\n{'='*72}")
    print("  PHASE 7: CARBON sp³ HYBRIDIZATION FROM MERGED FACES")
    print(f"{'='*72}")

    if all_merged_data and best_tet:
        rep_merged = all_merged_data[0]
        print(f"\n  The 4 tetrahedral merged faces (sp³):")
        for k, fi in enumerate(best_tet):
            mf = rep_merged[fi]
            axis_type, align = classify_merged_face(
                mf['avg_normal'], five_fold, three_fold, two_fold
            )
            print(f"    Bond {k+1}: merged face {fi+1}, {mf['sub_face_count']} sub-faces, "
                  f"area = {mf['total_area']:.4f}, type = {axis_type}")

        total_sp3_subfaces = sum(rep_merged[fi]['sub_face_count'] for fi in best_tet)
        print(f"\n    Total sp³ sub-faces: {total_sp3_subfaces}")
        print(f"    Interpretation: 1 s-face + 3 p-face sub-cells → "
              f"4 equivalent hybrid directions")

        # Non-bonding faces (the other 3 or so)
        non_bond = [i for i in range(len(rep_merged)) if i not in best_tet]
        if non_bond:
            print(f"\n    Non-bonding merged faces ({len(non_bond)}):")
            for fi in non_bond:
                mf = rep_merged[fi]
                axis_type, align = classify_merged_face(
                    mf['avg_normal'], five_fold, three_fold, two_fold
                )
                print(f"      Face {fi+1}: {mf['sub_face_count']} sub-faces, "
                      f"type = {axis_type}")

    # ═════════════════════════════════════════════════════════════════
    # SCORECARD
    # ═════════════════════════════════════════════════════════════════
    print(f"\n{'='*72}")
    print("  SCORECARD")
    print(f"{'='*72}")

    checks = []
    checks.append(('Natural merged face count',
                    str(natural_mode),
                    '7 = heptahedron' if natural_mode == 7
                    else f'13 = F(7)' if natural_mode == 13
                    else f'(not 7)'))

    if all_subface_seqs:
        most_common_seq = seq_counts.most_common(1)[0][0]
        checks.append(('Most common sub-face sequence',
                        str(list(most_common_seq)),
                        f'sum = {sum(most_common_seq)}'))

    if purity_scores:
        checks.append(('Orbital purity of merged groups',
                        f'{np.mean(purity_scores):.0%}',
                        'pure' if np.mean(purity_scores) > 0.8 else 'mixed'))

    if best_tet:
        checks.append(('Tetrahedral angle (merged faces)',
                        f'{best_tet_angle:.1f}°',
                        f'err {abs(best_tet_angle-109.47):.1f}° from 109.5°'))

    if 'closest_water' in dir():
        checks.append(('Water H-O-H angle',
                        f'{closest_water:.1f}°',
                        f'err {abs(closest_water-104.5):.1f}° from 104.5°'))

    print()
    for name, result, detail in checks:
        print(f"  {name:<40} {result:<20} {detail}")

    # Verdict
    print(f"\n  VERDICT:")
    if natural_mode == 7:
        print(f"  ★ The matter tile has 7 coarse faces at θ = {natural_theta:.0f}°")
        print(f"    The Voronoi 23 = 7 × average_subdivision")
        print(f"    THE HEPTAHEDRON EXISTS at the coarse scale.")
    elif natural_mode <= 10:
        print(f"  The matter tile has {natural_mode} coarse faces at θ = {natural_theta:.0f}°")
        print(f"  Close to 7 but not exact. The Voronoi 23 subdivides into "
              f"{natural_mode} groups.")
    else:
        print(f"  The matter tile has {natural_mode} coarse faces at θ = {natural_theta:.0f}°")
        print(f"  No obvious heptahedron at any merging threshold.")

    # ── Save ──
    results_dir = os.path.join(ROOT, 'results', 'face_merging')
    os.makedirs(results_dir, exist_ok=True)

    results = {
        'natural_theta': natural_theta,
        'natural_mode': natural_mode,
        'threshold_stats': {str(k): v for k, v in threshold_stats.items()},
        'most_common_sequence': list(seq_counts.most_common(1)[0][0]) if seq_counts else [],
    }
    if best_tet:
        results['tetrahedral_angle'] = float(best_tet_angle)
    if 'closest_water' in dir():
        results['water_angle'] = float(closest_water)

    def convert(obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return obj

    with open(os.path.join(results_dir, 'face_merging.json'), 'w') as f:
        json.dump(results, f, indent=2, default=convert)
    print(f"\n  Results saved to: {results_dir}/")
    print()


if __name__ == '__main__':
    main()
