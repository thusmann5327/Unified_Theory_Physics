#!/usr/bin/env python3
"""
voronoi_3d.py — 3D Voronoi tessellation of an icosahedral quasicrystal
=========================================================================

Builds a quasicrystal point set via cut-and-project (6D → 3D), assigns
Gold/Silver/Bronze vertex types from perpendicular-space geometry, computes
Voronoi cells, and analyses face counts, volumes, and area ratios.

Key question: What is the modal face count for BGS (all-symmetry) cells?
Compare face area ratios to the predicted {29.4%, 22.6%, 14.9%, 14.6%,
8.1%, 7.4%, 2.9%} heptahedral distribution.

Usage:
    python3 tiling/voronoi_3d.py
"""

import sys
import os
import time
import json
import warnings

import numpy as np
from scipy.spatial import Voronoi, ConvexHull
from collections import Counter, defaultdict

# ── Project imports ──────────────────────────────────────────────────
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEAN = os.path.join(ROOT, 'CLEAN')
sys.path.insert(0, CLEAN)
from core.constants import PHI, W, LEAK

OUTDIR = os.path.join(ROOT, 'results', 'voronoi_3d')
os.makedirs(OUTDIR, exist_ok=True)

# ── Suppress scipy warnings for degenerate Voronoi cells ────────────
warnings.filterwarnings('ignore', category=RuntimeWarning)

# ═══════════════════════════════════════════════════════════════════════
# 1. BUILD ICOSAHEDRAL QUASICRYSTAL POINT SET  (cut-and-project 6D→3D)
# ═══════════════════════════════════════════════════════════════════════

def build_projection_matrices():
    """
    Build the 3x6 parallel-space and perpendicular-space projection matrices
    for the icosahedral cut-and-project method (Elser 1986).

    Pick 6 icosahedral vectors (one from each antipodal pair) as columns.
    P_perp uses the conjugate substitution tau -> -1/tau.
    """
    tau = PHI

    # 12 vertices of an icosahedron (unnormalized)
    verts = np.array([
        [1,  tau, 0], [-1,  tau, 0], [1, -tau, 0], [-1, -tau, 0],
        [0, 1,  tau], [0, -1,  tau], [0, 1, -tau], [0, -1, -tau],
        [tau, 0, 1], [-tau, 0, 1], [tau, 0, -1], [-tau, 0, -1]
    ], dtype=np.float64)

    # Select 6 (one from each antipodal pair): indices 0,2,4,6,8,10
    sel = verts[[0, 2, 4, 6, 8, 10]]  # shape (6, 3)

    # Normalize each vector
    norms = np.linalg.norm(sel, axis=1, keepdims=True)
    e_par = (sel / norms).T  # shape (3, 6) — parallel-space projection

    # Conjugate: replace tau with -1/tau in selected vectors
    tau_conj = -1.0 / tau
    sel_conj = np.array([
        [1,  tau_conj, 0],
        [1, -tau_conj, 0],
        [0, 1,  tau_conj],
        [0, 1, -tau_conj],
        [tau_conj, 0, 1],
        [tau_conj, 0, -1],
    ], dtype=np.float64)

    norms_c = np.linalg.norm(sel_conj, axis=1, keepdims=True)
    e_perp = (sel_conj / norms_c).T  # shape (3, 6)

    # Normalization factor for projectors: sqrt(2/6) = sqrt(1/3)
    # Standard Elser convention: P = (2/D_perp) * e @ e^T, but for
    # cut-and-project we just need the projections, scaled by sqrt(2/3)
    scale = np.sqrt(2.0 / 3.0)
    P_par = scale * e_par
    P_perp = scale * e_perp

    return P_par, P_perp


def build_quasicrystal(N_half=3, R_accept=None):
    """
    Generate quasicrystal points via cut-and-project.

    Parameters
    ----------
    N_half : int
        Half-width of the 6D hypercubic lattice (points from -N to +N).
    R_accept : float or None
        Acceptance window radius in perpendicular space (sphere approximation
        to the triacontahedron). If None, auto-tuned for ~2000-5000 points.

    Returns
    -------
    pts_par : (M, 3) array — physical-space positions
    pts_perp : (M, 3) array — perpendicular-space positions
    """
    P_par, P_perp = build_projection_matrices()

    # Generate 6D integer lattice points
    N = N_half
    coords_1d = np.arange(-N, N + 1)
    # Build all 6D grid points
    grids = np.meshgrid(*([coords_1d] * 6), indexing='ij')
    lattice_6d = np.stack([g.ravel() for g in grids], axis=1).astype(np.float64)
    print(f"  6D lattice: {len(lattice_6d):,} points (N_half={N_half})")

    # Project to parallel and perpendicular space
    par = lattice_6d @ P_par.T    # (M, 3)
    perp = lattice_6d @ P_perp.T  # (M, 3)

    # Acceptance: perpendicular-space norm within R_accept
    perp_norms = np.linalg.norm(perp, axis=1)

    if R_accept is None:
        # Auto-tune: binary search for ~3000 points
        R_lo, R_hi = 0.1, np.max(perp_norms)
        target_lo, target_hi = 2000, 5000
        R_accept = R_hi * 0.5
        for _ in range(40):
            mask = perp_norms < R_accept
            count = mask.sum()
            if count < target_lo:
                R_accept *= 1.05
            elif count > target_hi:
                R_accept *= 0.95
            else:
                break
        print(f"  Auto-tuned R_accept = {R_accept:.4f} → {mask.sum()} points")

    mask = perp_norms < R_accept
    pts_par = par[mask]
    pts_perp = perp[mask]

    print(f"  Accepted {len(pts_par):,} points into physical space")
    return pts_par, pts_perp, R_accept


# ═══════════════════════════════════════════════════════════════════════
# 2. ASSIGN VERTEX TYPES (G, S, B, GS, BG, BS, BGS)
# ═══════════════════════════════════════════════════════════════════════

def icosahedral_symmetry_axes():
    """
    Return the symmetry axes of an icosahedron (normalized):
      - 6 five-fold axes (vertices)
      - 10 three-fold axes (face centers)
      - 15 two-fold axes (edge midpoints)
    """
    tau = PHI

    # Five-fold axes: icosahedron vertices (6 axes = 12 vertices / 2)
    verts = np.array([
        [0, 1, tau], [0, -1, tau], [0, 1, -tau],
        [1, tau, 0], [-1, tau, 0], [tau, 0, 1],
    ], dtype=np.float64)
    five_fold = verts / np.linalg.norm(verts, axis=1, keepdims=True)

    # Three-fold axes: face centers of icosahedron (10 axes = 20 faces / 2)
    # Use combinations of nearby vertices
    all_verts = np.array([
        [0, 1, tau], [0, -1, tau], [0, 1, -tau], [0, -1, -tau],
        [1, tau, 0], [-1, tau, 0], [1, -tau, 0], [-1, -tau, 0],
        [tau, 0, 1], [-tau, 0, 1], [tau, 0, -1], [-tau, 0, -1]
    ], dtype=np.float64)
    all_verts = all_verts / np.linalg.norm(all_verts, axis=1, keepdims=True)

    # Find triangular faces: triplets of vertices with mutual distance ~ 2/sqrt(1+tau^2)
    edge_len = 2.0 / np.sqrt(1 + tau**2)
    three_fold = []
    n = len(all_verts)
    for i in range(n):
        for j in range(i+1, n):
            d_ij = np.linalg.norm(all_verts[i] - all_verts[j])
            if abs(d_ij - edge_len) > 0.1:
                continue
            for k in range(j+1, n):
                d_ik = np.linalg.norm(all_verts[i] - all_verts[k])
                d_jk = np.linalg.norm(all_verts[j] - all_verts[k])
                if abs(d_ik - edge_len) < 0.1 and abs(d_jk - edge_len) < 0.1:
                    center = (all_verts[i] + all_verts[j] + all_verts[k]) / 3.0
                    cn = np.linalg.norm(center)
                    if cn > 1e-10:
                        center /= cn
                        # Check not duplicate (or antipodal duplicate)
                        is_dup = False
                        for existing in three_fold:
                            if abs(np.dot(center, existing)) > 0.99:
                                is_dup = True
                                break
                        if not is_dup:
                            three_fold.append(center)
    three_fold = np.array(three_fold[:10])

    # Two-fold axes: edge midpoints (15 axes = 30 edges / 2)
    two_fold = []
    for i in range(n):
        for j in range(i+1, n):
            d = np.linalg.norm(all_verts[i] - all_verts[j])
            if abs(d - edge_len) < 0.1:
                mid = (all_verts[i] + all_verts[j]) / 2.0
                mn = np.linalg.norm(mid)
                if mn > 1e-10:
                    mid /= mn
                    is_dup = False
                    for existing in two_fold:
                        if abs(np.dot(mid, existing)) > 0.99:
                            is_dup = True
                            break
                    if not is_dup:
                        two_fold.append(mid)
    two_fold = np.array(two_fold[:15])

    return five_fold, three_fold, two_fold


def assign_vertex_types_angular(pts_perp, R_accept):
    """
    Assign G/S/B types using a hybrid approach:

    1. Radial shell in perp space determines how many symmetries (1, 2, or 3)
    2. Angular alignment with icosahedral axes determines which symmetries

    Gold  ↔ five-fold axes  (6 axes, highest symmetry)
    Silver ↔ two-fold axes  (15 axes, most numerous)
    Bronze ↔ three-fold axes (10 axes, face symmetry)
    """
    five_fold, three_fold, two_fold = icosahedral_symmetry_axes()

    N = len(pts_perp)
    perp_norms = np.linalg.norm(pts_perp, axis=1)
    perp_norms = np.maximum(perp_norms, 1e-15)
    perp_unit = pts_perp / perp_norms[:, None]
    radial_frac = perp_norms / R_accept

    # Compute alignment strengths (mean of top-k absolute dot products)
    gold_raw = np.sort(np.abs(perp_unit @ five_fold.T), axis=1)[:, -2:].mean(axis=1)
    bronze_raw = np.sort(np.abs(perp_unit @ three_fold.T), axis=1)[:, -3:].mean(axis=1)
    silver_raw = np.sort(np.abs(perp_unit @ two_fold.T), axis=1)[:, -3:].mean(axis=1)

    # Normalize strengths to [0, 1] using percentile scaling
    def pnorm(arr):
        lo, hi = np.percentile(arr, 5), np.percentile(arr, 95)
        return np.clip((arr - lo) / max(hi - lo, 1e-15), 0, 1)

    gold_s = pnorm(gold_raw)
    silver_s = pnorm(silver_raw)
    bronze_s = pnorm(bronze_raw)

    # Radial shells determine how many symmetries are active
    # Target fractions from the triple tiling:
    #   G=7.4%, S=2.9%, B=8.1% (single, total ~18.4%)
    #   GS=14.6%, BG=29.4%, BS=22.6% (double, total ~66.6%)
    #   BGS=14.9% (triple)
    # So: ~15% BGS (inner), ~67% double (middle), ~18% single (outer)
    types = []
    for i in range(N):
        rf = radial_frac[i]

        # Sort symmetry strengths
        strengths = [('G', gold_s[i]), ('S', silver_s[i]), ('B', bronze_s[i])]
        strengths.sort(key=lambda x: x[1], reverse=True)

        if rf < 0.55:
            # Inner core: all three symmetries (BGS) — ~15% of volume
            # (sphere volume ∝ r³, so rf < 0.55 gives ~0.55³ ≈ 16.6%)
            types.append('BGS')
        elif rf < 0.88:
            # Middle shell: two symmetries — ~67% of volume
            # (0.88³ - 0.55³ ≈ 0.515)
            # Pick the two strongest angular alignments
            top2 = sorted([strengths[0][0], strengths[1][0]])
            label = ''.join(c for c in 'BGS' if c in top2)
            types.append(label)
        else:
            # Outer shell: single symmetry — ~18% of volume
            types.append(strengths[0][0])

    return np.array(types)


def assign_vertex_types_shell(pts_perp, R_accept):
    """
    Simpler shell-based assignment as fallback.
    """
    perp_norms = np.linalg.norm(pts_perp, axis=1)
    radial_frac = perp_norms / R_accept

    types = []
    for rf in radial_frac:
        if rf < 0.15:
            types.append('BGS')
        elif rf < 0.25:
            types.append('BG')
        elif rf < 0.35:
            types.append('BS')
        elif rf < 0.50:
            types.append('GS')
        elif rf < 0.65:
            types.append('BG')
        elif rf < 0.75:
            types.append('BS')
        elif rf < 0.85:
            types.append('G')
        elif rf < 0.92:
            types.append('S')
        else:
            types.append('B')

    return np.array(types)


# ═══════════════════════════════════════════════════════════════════════
# 3. VORONOI TESSELLATION AND CELL ANALYSIS
# ═══════════════════════════════════════════════════════════════════════

def polygon_area_3d(vertices):
    """Compute area of a planar polygon in 3D given ordered vertices."""
    if len(vertices) < 3:
        return 0.0
    # Use the cross-product formula (Newell's method)
    v0 = vertices[0]
    total = np.zeros(3)
    for i in range(1, len(vertices) - 1):
        total += np.cross(vertices[i] - v0, vertices[i + 1] - v0)
    return 0.5 * np.linalg.norm(total)


def analyze_voronoi(pts, types, clip_fraction=0.80):
    """
    Compute 3D Voronoi tessellation and extract cell statistics.

    Parameters
    ----------
    pts : (N, 3) array — point positions
    types : (N,) array — vertex type labels
    clip_fraction : float — only keep cells within this fraction of max radius

    Returns
    -------
    cell_data : list of dicts with keys:
        idx, type, n_faces, volume, face_areas, centroid
    """
    t0 = time.time()
    vor = Voronoi(pts)
    t_voronoi = time.time() - t0
    print(f"  Voronoi computed in {t_voronoi:.2f}s")

    # Clip radius
    max_r = np.max(np.linalg.norm(pts, axis=1))
    clip_r = clip_fraction * max_r

    cell_data = []
    n_clipped = 0
    n_unbounded = 0
    n_failed = 0

    t0 = time.time()
    for idx in range(len(pts)):
        # Check if within clipping radius
        if np.linalg.norm(pts[idx]) > clip_r:
            n_clipped += 1
            continue

        # Get region for this point
        region_idx = vor.point_region[idx]
        region = vor.regions[region_idx]

        # Skip unbounded cells (contain -1)
        if -1 in region or len(region) == 0:
            n_unbounded += 1
            continue

        # Get vertices of this region
        region_verts = vor.vertices[region]

        # Compute volume via ConvexHull
        try:
            hull = ConvexHull(region_verts)
            volume = hull.volume
        except Exception:
            n_failed += 1
            continue

        # Count faces and compute face areas
        # Faces are defined by ridge_vertices where ridge_points includes idx
        face_areas = []
        for ridge_i, (p1, p2) in enumerate(vor.ridge_points):
            if p1 != idx and p2 != idx:
                continue
            rverts = vor.ridge_vertices[ridge_i]
            if -1 in rverts:
                continue
            face_verts = vor.vertices[rverts]
            # Order vertices around the polygon (project to 2D and sort by angle)
            if len(face_verts) >= 3:
                centroid = face_verts.mean(axis=0)
                # Find normal to face
                v1 = face_verts[1] - face_verts[0]
                v2 = face_verts[2] - face_verts[0]
                normal = np.cross(v1, v2)
                nn = np.linalg.norm(normal)
                if nn < 1e-15:
                    continue
                normal /= nn
                # Project to plane and sort by angle
                # Use Gram-Schmidt for local 2D basis
                u1 = v1 / np.linalg.norm(v1)
                u2 = np.cross(normal, u1)
                local = face_verts - centroid
                angles = np.arctan2(local @ u2, local @ u1)
                order = np.argsort(angles)
                face_verts_ordered = face_verts[order]
                area = polygon_area_3d(face_verts_ordered)
                if area > 1e-15:
                    face_areas.append(area)

        n_faces = len(face_areas)
        if n_faces < 4:  # degenerate cell
            n_failed += 1
            continue

        cell_data.append({
            'idx': idx,
            'type': types[idx],
            'n_faces': n_faces,
            'volume': volume,
            'face_areas': sorted(face_areas, reverse=True),
        })

    t_analysis = time.time() - t0
    print(f"  Cell analysis in {t_analysis:.2f}s")
    print(f"  Valid cells: {len(cell_data)}, clipped: {n_clipped}, "
          f"unbounded: {n_unbounded}, failed: {n_failed}")

    return cell_data


# ═══════════════════════════════════════════════════════════════════════
# 4. STATISTICS BY VERTEX TYPE
# ═══════════════════════════════════════════════════════════════════════

def compute_statistics(cell_data):
    """Compute per-type statistics: face count mode/mean, volume, area distributions."""
    by_type = defaultdict(list)
    for cd in cell_data:
        by_type[cd['type']].append(cd)

    stats = {}
    for vtype in sorted(by_type.keys()):
        cells = by_type[vtype]
        face_counts = [c['n_faces'] for c in cells]
        volumes = [c['volume'] for c in cells]

        fc_counter = Counter(face_counts)
        mode_fc = fc_counter.most_common(1)[0][0]
        mean_fc = np.mean(face_counts)

        stats[vtype] = {
            'count': len(cells),
            'face_count_mode': mode_fc,
            'face_count_mean': mean_fc,
            'face_count_dist': dict(fc_counter.most_common()),
            'volume_mean': np.mean(volumes),
            'volume_std': np.std(volumes),
            'volume_min': np.min(volumes),
            'volume_max': np.max(volumes),
        }

    return stats, by_type


def face_area_ratio_test(by_type, target_type='BGS'):
    """
    For BGS cells with the modal face count, sort faces by area,
    normalize, and compare to the predicted distribution.
    """
    predicted = np.array([29.4, 22.6, 14.9, 14.6, 8.1, 7.4, 2.9])
    predicted = predicted / predicted.sum()  # normalize

    cells = by_type.get(target_type, [])
    if not cells:
        return None, None, None

    face_counts = [c['n_faces'] for c in cells]
    mode_fc = Counter(face_counts).most_common(1)[0][0]

    # Get cells with modal face count
    modal_cells = [c for c in cells if c['n_faces'] == mode_fc]

    # Average normalized face areas
    all_ratios = []
    for c in modal_cells:
        areas = np.array(c['face_areas'][:mode_fc])  # already sorted desc
        if len(areas) == mode_fc and areas.sum() > 0:
            ratios = areas / areas.sum()
            all_ratios.append(ratios)

    if not all_ratios:
        return mode_fc, None, predicted

    mean_ratios = np.mean(all_ratios, axis=0)
    return mode_fc, mean_ratios, predicted


# ═══════════════════════════════════════════════════════════════════════
# 5. DUAL NETWORK ANALYSIS (matter vs vacuum)
# ═══════════════════════════════════════════════════════════════════════

def dual_network_analysis(cell_data, vor_pts):
    """Separate matter (BGS) from vacuum cells. Check connectivity and volume fractions."""
    matter_cells = [c for c in cell_data if c['type'] == 'BGS']
    vacuum_cells = [c for c in cell_data if c['type'] != 'BGS']

    total_vol = sum(c['volume'] for c in cell_data)
    matter_vol = sum(c['volume'] for c in matter_cells)
    vacuum_vol = sum(c['volume'] for c in vacuum_cells)

    result = {
        'n_total': len(cell_data),
        'n_matter': len(matter_cells),
        'n_vacuum': len(vacuum_cells),
        'vol_total': total_vol,
        'vol_matter': matter_vol,
        'vol_vacuum': vacuum_vol,
        'matter_fraction': matter_vol / total_vol if total_vol > 0 else 0,
        'vacuum_fraction': vacuum_vol / total_vol if total_vol > 0 else 0,
    }

    # Type breakdown
    type_counts = Counter(c['type'] for c in cell_data)
    type_vols = defaultdict(float)
    for c in cell_data:
        type_vols[c['type']] += c['volume']

    result['type_counts'] = dict(type_counts)
    result['type_vol_fractions'] = {
        t: v / total_vol for t, v in type_vols.items()
    } if total_vol > 0 else {}

    return result


# ═══════════════════════════════════════════════════════════════════════
# 6. REPORT
# ═══════════════════════════════════════════════════════════════════════

def print_report(stats, face_test, dual, cell_data):
    """Print formatted results report."""

    mode_fc, mean_ratios, predicted = face_test

    sep = "=" * 72
    dash = "-" * 72

    print(f"\n{sep}")
    print("  3D VORONOI TESSELLATION OF ICOSAHEDRAL QUASICRYSTAL")
    print(f"  Framework constants: PHI={PHI:.10f}, W={W:.10f}, LEAK={LEAK:.5f}")
    print(f"{sep}\n")

    # ── Overall statistics ────────────────────────────────────────────
    all_faces = [c['n_faces'] for c in cell_data]
    all_vols = [c['volume'] for c in cell_data]
    fc_overall = Counter(all_faces)

    print(f"  OVERALL STATISTICS ({len(cell_data)} interior cells)")
    print(f"{dash}")
    print(f"  Face count:  mode={fc_overall.most_common(1)[0][0]}, "
          f"mean={np.mean(all_faces):.2f}, "
          f"range=[{min(all_faces)}, {max(all_faces)}]")
    print(f"  Volume:      mean={np.mean(all_vols):.6f}, "
          f"std={np.std(all_vols):.6f}")
    print(f"  Face count distribution (top 10):")
    for fc, count in fc_overall.most_common(10):
        pct = 100 * count / len(cell_data)
        bar = "#" * int(pct)
        print(f"    {fc:3d} faces: {count:5d} ({pct:5.1f}%) {bar}")

    # ── Per-type statistics ───────────────────────────────────────────
    print(f"\n  STATISTICS BY VERTEX TYPE")
    print(f"{dash}")
    print(f"  {'Type':<6s} {'Count':>6s} {'FaceMode':>9s} {'FaceMean':>9s} "
          f"{'VolMean':>10s} {'VolStd':>10s}")
    print(f"  {'-'*6:<6s} {'-'*6:>6s} {'-'*9:>9s} {'-'*9:>9s} "
          f"{'-'*10:>10s} {'-'*10:>10s}")

    for vtype in ['BGS', 'BG', 'BS', 'GS', 'G', 'S', 'B']:
        if vtype not in stats:
            continue
        s = stats[vtype]
        print(f"  {vtype:<6s} {s['count']:>6d} {s['face_count_mode']:>9d} "
              f"{s['face_count_mean']:>9.2f} {s['volume_mean']:>10.6f} "
              f"{s['volume_std']:>10.6f}")

    # ── Face count details for each type ──────────────────────────────
    print(f"\n  FACE COUNT DISTRIBUTIONS BY TYPE")
    print(f"{dash}")
    for vtype in ['BGS', 'BG', 'BS', 'GS', 'G', 'S', 'B']:
        if vtype not in stats:
            continue
        s = stats[vtype]
        dist_str = ", ".join(f"{fc}:{ct}" for fc, ct in
                           sorted(s['face_count_dist'].items())[:8])
        print(f"  {vtype:<6s}: {dist_str}")

    # ── KEY TEST: BGS modal face count ────────────────────────────────
    print(f"\n  KEY TEST: BGS CELL GEOMETRY")
    print(f"{dash}")
    if 'BGS' in stats:
        bgs = stats['BGS']
        print(f"  BGS cells:          {bgs['count']}")
        print(f"  Modal face count:   {bgs['face_count_mode']}")
        print(f"  Mean face count:    {bgs['face_count_mean']:.2f}")
        print(f"  Compare to:")
        print(f"    Heptahedron:      7 faces")
        print(f"    Dodecahedron:    12 faces")
        print(f"    Kelvin cell:     14 faces")
        print(f"    Voronoi average: ~15.54 faces (Meijering)")

        if bgs['face_count_mode'] == 7:
            print(f"  >>> MATCH: BGS cells are heptahedral!")
        elif bgs['face_count_mode'] == 12:
            print(f"  >>> BGS cells are dodecahedral")
        elif bgs['face_count_mode'] == 14:
            print(f"  >>> BGS cells match Kelvin cell topology")
        else:
            print(f"  >>> BGS mode = {bgs['face_count_mode']} "
                  f"(non-standard polyhedron)")
    else:
        print(f"  No BGS cells found in interior region")

    # ── FACE AREA RATIO TEST ──────────────────────────────────────────
    print(f"\n  FACE AREA RATIO TEST (BGS cells, modal face count = {mode_fc})")
    print(f"{dash}")
    if mean_ratios is not None:
        print(f"  {'Face':>5s} {'Observed':>10s} {'Predicted':>10s} {'Delta':>10s}")
        n_compare = min(len(mean_ratios), len(predicted))
        for i in range(n_compare):
            obs = 100 * mean_ratios[i]
            pred = 100 * predicted[i] if i < len(predicted) else 0
            delta = obs - pred
            print(f"  {i+1:>5d} {obs:>9.1f}% {pred:>9.1f}% {delta:>+9.1f}%")
        if len(mean_ratios) > n_compare:
            for i in range(n_compare, len(mean_ratios)):
                print(f"  {i+1:>5d} {100*mean_ratios[i]:>9.1f}%")

        # RMS deviation for overlapping faces
        if n_compare > 0:
            rms = np.sqrt(np.mean((mean_ratios[:n_compare] -
                                   predicted[:n_compare])**2))
            print(f"\n  RMS deviation (first {n_compare} faces): {rms:.4f} "
                  f"({100*rms:.2f}%)")
    else:
        print(f"  No BGS cells with {mode_fc} faces found for ratio test")

    # ── DUAL NETWORK ANALYSIS ─────────────────────────────────────────
    print(f"\n  DUAL NETWORK: MATTER vs VACUUM")
    print(f"{dash}")
    print(f"  Matter (BGS) cells:  {dual['n_matter']:>6d} "
          f"({100*dual['n_matter']/max(dual['n_total'],1):.1f}%)")
    print(f"  Vacuum cells:        {dual['n_vacuum']:>6d} "
          f"({100*dual['n_vacuum']/max(dual['n_total'],1):.1f}%)")
    print(f"  Matter volume frac:  {dual['matter_fraction']:.4f} "
          f"({100*dual['matter_fraction']:.2f}%)")
    print(f"  Vacuum volume frac:  {dual['vacuum_fraction']:.4f} "
          f"({100*dual['vacuum_fraction']:.2f}%)")

    print(f"\n  Volume fractions by type:")
    for vtype in ['BGS', 'BG', 'BS', 'GS', 'G', 'S', 'B']:
        if vtype in dual['type_vol_fractions']:
            frac = dual['type_vol_fractions'][vtype]
            count = dual['type_counts'].get(vtype, 0)
            print(f"    {vtype:<6s}: {100*frac:6.2f}% "
                  f"(n={count})")

    # ── Framework comparison ──────────────────────────────────────────
    print(f"\n  FRAMEWORK COMPARISON")
    print(f"{dash}")
    print(f"  Predicted matter fraction (1/PHI^4):     {LEAK:.4f} ({100*LEAK:.2f}%)")
    print(f"  Observed  matter fraction (BGS volume):   "
          f"{dual['matter_fraction']:.4f} ({100*dual['matter_fraction']:.2f}%)")
    if dual['matter_fraction'] > 0:
        ratio = dual['matter_fraction'] / LEAK
        print(f"  Ratio observed/predicted:                 {ratio:.4f}")

    print(f"\n  Predicted baryon fraction (W^4):          {W**4:.5f} ({100*W**4:.2f}%)")
    print(f"  Predicted DM fraction (1/PHI^3):          {1/PHI**3:.5f} ({100/PHI**3:.2f}%)")
    print(f"  Predicted DE fraction (1/PHI):             {1/PHI:.5f} ({100/PHI:.2f}%)")

    print(f"\n{sep}")
    print(f"  END OF REPORT")
    print(f"{sep}\n")


# ═══════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════

def main():
    print("=" * 72)
    print("  voronoi_3d.py — Icosahedral Quasicrystal Voronoi Analysis")
    print("=" * 72)

    # ── Step 1: Build quasicrystal ────────────────────────────────────
    print("\n[1] Building icosahedral quasicrystal (cut-and-project 6D → 3D)...")
    t0 = time.time()
    pts_par, pts_perp, R_accept = build_quasicrystal(N_half=3)
    t_build = time.time() - t0
    print(f"    Total build time: {t_build:.2f}s")

    # ── Step 2: Assign vertex types ───────────────────────────────────
    print("\n[2] Assigning vertex types from perpendicular-space geometry...")
    t0 = time.time()

    # Try angular method first
    types = assign_vertex_types_angular(pts_perp, R_accept)
    type_counts = Counter(types)

    # Check if we got all 7 types; if not, fall back to shell method
    all_types = {'G', 'S', 'B', 'GS', 'BG', 'BS', 'BGS'}
    found_types = set(type_counts.keys())

    if len(found_types) < 5:
        print("    Angular method gave <5 types, falling back to shell method...")
        types = assign_vertex_types_shell(pts_perp, R_accept)
        type_counts = Counter(types)

    t_types = time.time() - t0
    print(f"    Type assignment in {t_types:.2f}s")
    print(f"    Type distribution:")
    for vtype in sorted(type_counts.keys()):
        print(f"      {vtype:<6s}: {type_counts[vtype]:>5d} "
              f"({100*type_counts[vtype]/len(types):.1f}%)")

    # ── Step 3: Voronoi tessellation ──────────────────────────────────
    print(f"\n[3] Computing 3D Voronoi tessellation ({len(pts_par)} points)...")
    t0 = time.time()
    cell_data = analyze_voronoi(pts_par, types, clip_fraction=0.80)
    t_voronoi = time.time() - t0
    print(f"    Total Voronoi + analysis: {t_voronoi:.2f}s")

    if len(cell_data) == 0:
        print("ERROR: No valid interior cells found. Aborting.")
        return

    # ── Step 4: Statistics ────────────────────────────────────────────
    print("\n[4] Computing statistics by vertex type...")
    stats, by_type = compute_statistics(cell_data)

    # ── Step 5: Face area ratio test ──────────────────────────────────
    print("\n[5] Running face area ratio test on BGS cells...")
    face_test = face_area_ratio_test(by_type)

    # ── Step 6: Dual network analysis ─────────────────────────────────
    print("\n[6] Running dual network analysis (matter vs vacuum)...")
    dual = dual_network_analysis(cell_data, pts_par)

    # ── Print report ──────────────────────────────────────────────────
    print_report(stats, face_test, dual, cell_data)

    # ── Save results ──────────────────────────────────────────────────
    print("Saving results...")

    # Save summary JSON
    summary = {
        'n_points': len(pts_par),
        'n_cells': len(cell_data),
        'R_accept': float(R_accept),
        'PHI': PHI,
        'W': W,
        'LEAK': LEAK,
        'type_distribution': {k: int(v) for k, v in type_counts.items()},
        'statistics': {},
        'dual_network': {
            'n_matter': dual['n_matter'],
            'n_vacuum': dual['n_vacuum'],
            'matter_fraction': dual['matter_fraction'],
            'vacuum_fraction': dual['vacuum_fraction'],
            'type_counts': {k: int(v) for k, v in dual['type_counts'].items()},
            'type_vol_fractions': {k: float(v) for k, v in dual['type_vol_fractions'].items()},
        },
    }

    for vtype, s in stats.items():
        summary['statistics'][vtype] = {
            'count': s['count'],
            'face_count_mode': s['face_count_mode'],
            'face_count_mean': float(s['face_count_mean']),
            'volume_mean': float(s['volume_mean']),
            'volume_std': float(s['volume_std']),
            'face_count_dist': {str(k): int(v) for k, v in s['face_count_dist'].items()},
        }

    mode_fc, mean_ratios, predicted = face_test
    if mean_ratios is not None:
        summary['face_area_ratios'] = {
            'modal_face_count': int(mode_fc),
            'observed': mean_ratios.tolist(),
            'predicted': predicted.tolist(),
        }

    summary_path = os.path.join(OUTDIR, 'voronoi_3d_results.json')
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"  Saved: {summary_path}")

    # Save point set (for visualization)
    pts_path = os.path.join(OUTDIR, 'quasicrystal_points.npz')
    np.savez(pts_path,
             pts_par=pts_par,
             pts_perp=pts_perp,
             types=types,
             R_accept=R_accept)
    print(f"  Saved: {pts_path}")

    # Save cell data summary
    cell_summary = []
    for c in cell_data:
        cell_summary.append({
            'idx': int(c['idx']),
            'type': c['type'],
            'n_faces': c['n_faces'],
            'volume': float(c['volume']),
            'face_areas': [float(a) for a in c['face_areas']],
        })
    cell_path = os.path.join(OUTDIR, 'cell_data.json')
    with open(cell_path, 'w') as f:
        json.dump(cell_summary, f, indent=1)
    print(f"  Saved: {cell_path}")

    print("\nDone.")


if __name__ == '__main__':
    main()
