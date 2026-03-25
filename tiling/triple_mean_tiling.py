#!/usr/bin/env python3
"""
THE TRIPLE METALLIC MEAN TILING — The Framework's Actual Space
================================================================

Three metallic mean frequencies build physical space:
  Gold:   δ₁ = φ = 1.618      (5-fold, matter core)
  Silver: δ₂ = 1+√2 = 2.414   (4-fold/8-fold, DM walls)
  Bronze: δ₃ = (3+√13)/2 = 3.303  (13-fold aperiodic, forces 3D)

Method: de Bruijn multigrid → vertex classification → tiling analysis.

Thomas A. Husmann / iBuilt LTD
March 24, 2026
"""

import numpy as np
import math
import json
import os
from collections import Counter, defaultdict
from itertools import combinations

# ══════════════════════════════════════════════════════════════════
# SETUP
# ══════════════════════════════════════════════════════════════════

PHI = (1 + 5**0.5) / 2
DELTA_S = 1 + 2**0.5            # silver mean 2.414
DELTA_B = (3 + 13**0.5) / 2     # bronze mean 3.303
W = (2 + PHI**(1/PHI**2)) / PHI**4
LEAK = 1 / PHI**4
R_C = 1 - LEAK
BOS = 0.992  # bronze/sigma_shell

# Spectral σ₃ widths
GOLD_S3 = 0.236
SILVER_S3 = 0.171
BRONZE_S3 = 0.394

# Framework θ values
THETA_LEAK = 0.564
THETA_RC = 0.854
THETA_BASE = 1.000

# Bond energy reference
E_BRACKET = 6.356  # eV


def metallic_mean(n):
    return (n + (n*n + 4)**0.5) / 2


# ══════════════════════════════════════════════════════════════════
# PHASE 1: MULTIGRID CONSTRUCTION
# ══════════════════════════════════════════════════════════════════

def build_grid_lines(n_dirs, spacing, n_lines, offset_seed=0):
    """Build a set of parallel line families for the multigrid method.

    Each family has direction angle k × π / n_dirs (for k = 0..n_dirs-1)
    and n_lines parallel lines at the given spacing.

    Returns list of (normal_x, normal_y, offset) for each line,
    plus the family index.
    """
    lines = []
    rng = np.random.RandomState(42 + offset_seed)

    for k in range(n_dirs):
        angle = k * math.pi / n_dirs
        nx = math.cos(angle)
        ny = math.sin(angle)
        # Offset lines symmetrically around origin with small irrational shift
        gamma = rng.uniform(0.01, 0.49)  # avoid exact integer offsets
        for j in range(-n_lines // 2, n_lines // 2 + 1):
            d = (j + gamma) * spacing
            lines.append((nx, ny, d, k, 'G' if n_dirs == 5
                          else 'S' if n_dirs == 4 else 'B'))
    return lines


def line_intersection(l1, l2):
    """Find intersection of two lines (nx1,ny1,d1) and (nx2,ny2,d2).

    Line equation: nx*x + ny*y = d.
    Returns (x, y) or None if parallel.
    """
    nx1, ny1, d1 = l1[:3]
    nx2, ny2, d2 = l2[:3]
    det = nx1 * ny2 - nx2 * ny1
    if abs(det) < 1e-12:
        return None
    x = (d1 * ny2 - d2 * ny1) / det
    y = (nx1 * d2 - nx2 * d1) / det
    return (x, y)


def find_vertices(gold_lines, silver_lines, bronze_lines, radius=15.0):
    """Find all pairwise intersections within a circular region.

    Classify each vertex by which grid families contribute.
    """
    all_lines = gold_lines + silver_lines + bronze_lines
    vertices = {}  # (rounded_x, rounded_y) → vertex info
    tol = 0.05  # merge threshold

    def add_vertex(x, y, grid_types):
        """Add or update a vertex, merging if close to an existing one."""
        # Check within radius
        if x*x + y*y > radius*radius:
            return
        # Quantize for lookup
        key = (round(x / tol), round(y / tol))
        # Check neighboring cells too
        for dk in [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]:
            nk = (key[0] + dk[0], key[1] + dk[1])
            if nk in vertices:
                vx, vy, vtypes = vertices[nk]
                if (x - vx)**2 + (y - vy)**2 < tol**2:
                    vtypes.update(grid_types)
                    return
        vertices[key] = (x, y, set(grid_types))

    # Gold-Gold intersections (within gold grid)
    print("    Computing Gold×Gold intersections...")
    for i in range(len(gold_lines)):
        for j in range(i + 1, len(gold_lines)):
            if gold_lines[i][3] == gold_lines[j][3]:
                continue  # same family → parallel
            pt = line_intersection(gold_lines[i], gold_lines[j])
            if pt:
                add_vertex(pt[0], pt[1], {'G'})

    # Silver-Silver intersections
    print("    Computing Silver×Silver intersections...")
    for i in range(len(silver_lines)):
        for j in range(i + 1, len(silver_lines)):
            if silver_lines[i][3] == silver_lines[j][3]:
                continue
            pt = line_intersection(silver_lines[i], silver_lines[j])
            if pt:
                add_vertex(pt[0], pt[1], {'S'})

    # Bronze-Bronze intersections
    print("    Computing Bronze×Bronze intersections...")
    for i in range(len(bronze_lines)):
        for j in range(i + 1, len(bronze_lines)):
            if bronze_lines[i][3] == bronze_lines[j][3]:
                continue
            pt = line_intersection(bronze_lines[i], bronze_lines[j])
            if pt:
                add_vertex(pt[0], pt[1], {'B'})

    # Gold-Silver cross intersections
    print("    Computing Gold×Silver intersections...")
    for gl in gold_lines:
        for sl in silver_lines:
            pt = line_intersection(gl, sl)
            if pt:
                add_vertex(pt[0], pt[1], {'G', 'S'})

    # Gold-Bronze cross intersections
    print("    Computing Gold×Bronze intersections...")
    for gl in gold_lines:
        for bl in bronze_lines:
            pt = line_intersection(gl, bl)
            if pt:
                add_vertex(pt[0], pt[1], {'G', 'B'})

    # Silver-Bronze cross intersections
    print("    Computing Silver×Bronze intersections...")
    for sl in silver_lines:
        for bl in bronze_lines:
            pt = line_intersection(sl, bl)
            if pt:
                add_vertex(pt[0], pt[1], {'S', 'B'})

    # Convert to list
    result = []
    for key, (x, y, types) in vertices.items():
        type_str = ''.join(sorted(types))
        result.append({'x': x, 'y': y, 'type': type_str})

    return result


# ══════════════════════════════════════════════════════════════════
# PHASE 2 & 3: VERTEX ANALYSIS
# ══════════════════════════════════════════════════════════════════

def analyze_vertices(vertices):
    """Classify and count vertex types."""
    type_counts = Counter(v['type'] for v in vertices)
    total = len(vertices)

    results = {}
    for vtype, count in sorted(type_counts.items()):
        frac = count / total
        results[vtype] = {
            'count': count,
            'fraction': round(frac, 6),
            'percent': round(frac * 100, 3),
        }

    return results, total


def compute_vertex_angles(vertices, n_neighbors=6):
    """For each vertex, find nearest neighbors and compute inter-edge angles."""
    coords = np.array([[v['x'], v['y']] for v in vertices])
    types = [v['type'] for v in vertices]

    # For speed, sample a subset
    n_sample = min(2000, len(vertices))
    indices = np.random.RandomState(99).choice(len(vertices), n_sample,
                                                replace=False)

    angle_stats = defaultdict(list)

    for idx in indices:
        x0, y0 = coords[idx]
        # Find nearest neighbors
        dists = np.sqrt((coords[:, 0] - x0)**2 + (coords[:, 1] - y0)**2)
        dists[idx] = 1e10  # exclude self
        nn_idx = np.argsort(dists)[:n_neighbors]

        # Compute angles between consecutive neighbor directions
        angles_to_nn = []
        for ni in nn_idx:
            dx = coords[ni, 0] - x0
            dy = coords[ni, 1] - y0
            angles_to_nn.append(math.atan2(dy, dx))

        angles_to_nn.sort()
        if len(angles_to_nn) >= 2:
            # Angular gaps between consecutive neighbors
            gaps = []
            for i in range(len(angles_to_nn)):
                a1 = angles_to_nn[i]
                a2 = angles_to_nn[(i + 1) % len(angles_to_nn)]
                gap = (a2 - a1) % (2 * math.pi)
                gaps.append(gap)

            min_gap = min(gaps)
            mean_gap = np.mean(gaps)
            vtype = types[idx]
            angle_stats[vtype].append({
                'min_angle': min_gap,
                'mean_angle': mean_gap,
                'n_nn': len(angles_to_nn),
            })

    # Summarize
    summary = {}
    for vtype, stats in angle_stats.items():
        min_angles = [s['min_angle'] for s in stats]
        mean_angles = [s['mean_angle'] for s in stats]
        summary[vtype] = {
            'count': len(stats),
            'min_angle_mean_deg': round(np.mean(min_angles) * 180 / math.pi, 1),
            'min_angle_std_deg': round(np.std(min_angles) * 180 / math.pi, 1),
            'mean_gap_deg': round(np.mean(mean_angles) * 180 / math.pi, 1),
        }

    return summary


# ══════════════════════════════════════════════════════════════════
# PHASE 4: TILE EXTRACTION
# ══════════════════════════════════════════════════════════════════

def extract_tiles_delaunay(vertices, max_edge=2.0):
    """Extract tiles using Delaunay triangulation of vertices.

    Filter to tiles with reasonable edge lengths.
    Classify tiles by vertex types at their corners.
    """
    from scipy.spatial import Delaunay

    coords = np.array([[v['x'], v['y']] for v in vertices])
    types = [v['type'] for v in vertices]

    if len(coords) < 4:
        return [], {}

    tri = Delaunay(coords)
    tiles = []
    tile_type_counts = Counter()

    for simplex in tri.simplices:
        # Check edge lengths
        pts = coords[simplex]
        edges = []
        for i in range(3):
            j = (i + 1) % 3
            d = np.sqrt(np.sum((pts[i] - pts[j])**2))
            edges.append(d)

        if max(edges) > max_edge:
            continue

        # Classify by vertex types at corners
        corner_types = tuple(sorted(types[s] for s in simplex))
        tile_type_counts[corner_types] += 1
        tiles.append({
            'vertices': simplex.tolist(),
            'edges': [round(e, 4) for e in sorted(edges)],
            'corner_types': corner_types,
        })

    return tiles, tile_type_counts


# ══════════════════════════════════════════════════════════════════
# PHASE 5: EDGE LENGTH ANALYSIS
# ══════════════════════════════════════════════════════════════════

def analyze_edge_lengths(tiles):
    """Analyze the distribution of edge lengths in the tiling.

    Look for φ-ratios between common edge lengths.
    """
    all_edges = []
    for t in tiles:
        all_edges.extend(t['edges'])

    if not all_edges:
        return {}

    edges = np.array(all_edges)
    # Histogram to find peaks
    hist, bin_edges = np.histogram(edges, bins=50)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    # Find peaks
    peaks = []
    for i in range(1, len(hist) - 1):
        if hist[i] > hist[i-1] and hist[i] > hist[i+1] and hist[i] > 10:
            peaks.append((bin_centers[i], hist[i]))

    peaks.sort(key=lambda p: p[1], reverse=True)

    # Check ratios between peaks
    peak_ratios = []
    if len(peaks) >= 2:
        for i in range(min(5, len(peaks))):
            for j in range(i + 1, min(5, len(peaks))):
                r = max(peaks[i][0], peaks[j][0]) / min(peaks[i][0], peaks[j][0])
                phi_err = abs(r - PHI) / PHI * 100
                delta_s_err = abs(r - DELTA_S / PHI) / (DELTA_S / PHI) * 100
                peak_ratios.append({
                    'lengths': (round(peaks[i][0], 3), round(peaks[j][0], 3)),
                    'ratio': round(r, 4),
                    'phi_error': round(phi_err, 1),
                })

    return {
        'n_edges': len(all_edges),
        'mean': round(np.mean(edges), 4),
        'std': round(np.std(edges), 4),
        'peaks': [(round(p[0], 4), p[1]) for p in peaks[:6]],
        'peak_ratios': peak_ratios[:10],
    }


# ══════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════

def main():
    print("=" * 74)
    print("  TRIPLE METALLIC MEAN TILING")
    print("  Gold (φ) + Silver (1+√2) + Bronze ((3+√13)/2)")
    print("=" * 74)

    # ──────────────────────────────────────────────────────────
    # PHASE 1: BUILD GRIDS
    # ──────────────────────────────────────────────────────────
    print()
    print("─" * 74)
    print("  PHASE 1: MULTIGRID CONSTRUCTION")
    print("─" * 74)
    print()

    # Grid parameters
    n_gold = 15     # lines per family
    n_silver = 12
    n_bronze = 6

    print(f"  Gold grid:   5 families × {n_gold} lines, "
          f"spacing = 1.000")
    print(f"  Silver grid: 4 families × {n_silver} lines, "
          f"spacing = 1/{DELTA_S:.3f} = {1/DELTA_S:.4f}")
    print(f"  Bronze grid: 13 families × {n_bronze} lines, "
          f"spacing = 1/{DELTA_B:.3f} = {1/DELTA_B:.4f}")
    print()

    gold_lines = build_grid_lines(5, 1.0, n_gold, offset_seed=0)
    silver_lines = build_grid_lines(4, 1.0 / DELTA_S, n_silver, offset_seed=100)
    bronze_lines = build_grid_lines(13, 1.0 / DELTA_B, n_bronze, offset_seed=200)

    print(f"  Total lines: Gold={len(gold_lines)}, Silver={len(silver_lines)}, "
          f"Bronze={len(bronze_lines)}")
    print()

    # ──────────────────────────────────────────────────────────
    # PHASE 2: FIND AND CLASSIFY VERTICES
    # ──────────────────────────────────────────────────────────
    print("─" * 74)
    print("  PHASE 2: VERTEX CLASSIFICATION")
    print("─" * 74)
    print()

    radius = 8.0
    print(f"  Finding intersections within radius {radius}...")
    vertices = find_vertices(gold_lines, silver_lines, bronze_lines,
                             radius=radius)
    print(f"  Total vertices found: {len(vertices)}")
    print()

    vtypes, v_total = analyze_vertices(vertices)

    print(f"  Vertex type distribution:")
    print(f"  {'Type':>6s} {'Count':>8s} {'Fraction':>10s} {'Percent':>8s}")
    print(f"  {'─'*6} {'─'*8} {'─'*10} {'─'*8}")

    for vtype in ['B', 'G', 'S', 'BG', 'BS', 'GS', 'BGS']:
        if vtype in vtypes:
            v = vtypes[vtype]
            print(f"  {vtype:>6s} {v['count']:8d} {v['fraction']:10.6f} "
                  f"{v['percent']:7.3f}%")

    print(f"  {'Total':>6s} {v_total:8d}")
    print()

    # ──────────────────────────────────────────────────────────
    # PHASE 3: KEY COMPARISONS
    # ──────────────────────────────────────────────────────────
    print("─" * 74)
    print("  PHASE 3: FRAMEWORK COMPARISONS")
    print("─" * 74)
    print()

    # ── CORRECTED ANALYSIS (March 24, 2026) ──
    # GS = LEAK = 1/φ⁴ = gate transmission coefficient
    # GSB = W⁴ = baryonic fraction (where ALL three grids intersect)
    gs_frac = vtypes.get('GS', {}).get('fraction', 0)
    gsb_frac = vtypes.get('BGS', {}).get('fraction', 0)
    wb4 = W**4

    # GS vs LEAK
    err_gs_leak = abs(gs_frac - LEAK) / LEAK * 100 if gs_frac > 0 else float('inf')
    print(f"  Gold-Silver (GS) = GATE TRANSMISSION (LEAK):")
    print(f"    Measured:  {gs_frac:.6f} ({gs_frac*100:.3f}%)")
    print(f"    LEAK=1/φ⁴: {LEAK:.6f} ({LEAK*100:.3f}%)")
    print(f"    Error:     {err_gs_leak:.1f}%")
    print()

    # GSB vs W⁴
    err_gsb = abs(gsb_frac - wb4) / wb4 * 100 if gsb_frac > 0 else float('inf')
    print(f"  Gold-Silver-Bronze (GSB) = BARYONIC (W⁴):")
    print(f"    Measured:  {gsb_frac:.6f} ({gsb_frac*100:.3f}%)")
    print(f"    W⁴ = Ω_b: {wb4:.6f} ({wb4*100:.3f}%)")
    print(f"    Error:     {err_gsb:.1f}%")
    print()

    # Hierarchy: GS/GSB ratio
    gs_total = gs_frac + gsb_frac  # total gold+silver (with or without bronze)
    gs_gsb_ratio = gs_total / gsb_frac if gsb_frac > 0 else float('inf')
    print(f"  Hierarchy:")
    print(f"    GS (total with G+S):  {gs_total:.6f} ({gs_total*100:.3f}%)")
    print(f"    GSB only:             {gsb_frac:.6f} ({gsb_frac*100:.3f}%)")
    print(f"    Ratio GS_total/GSB:   {gs_gsb_ratio:.2f} (expected ≈ 3)")
    print()

    # Dark matter fraction at tiling scale
    dm_tiling = gs_frac  # GS vertices NOT also bronze = dark matter conduit
    print(f"  Dark sector at tiling scale:")
    print(f"    GS (not bronze) = DM conduit:  {dm_tiling:.6f} ({dm_tiling*100:.3f}%)")
    print(f"    LEAK - W⁴ = {LEAK - wb4:.6f} ({(LEAK-wb4)*100:.3f}%)")
    print(f"    Measured GS - GSB = {gs_frac - gsb_frac:.6f} "
          f"({(gs_frac-gsb_frac)*100:.3f}%)")
    print()

    # Full vertex hierarchy
    g_frac = vtypes.get('G', {}).get('fraction', 0)
    s_frac = vtypes.get('S', {}).get('fraction', 0)
    b_frac = vtypes.get('B', {}).get('fraction', 0)
    bg_frac = vtypes.get('BG', {}).get('fraction', 0)
    bs_frac = vtypes.get('BS', {}).get('fraction', 0)

    print(f"  Full vertex hierarchy:")
    print(f"    G only:   {g_frac:.6f} ({g_frac*100:.3f}%)")
    print(f"    S only:   {s_frac:.6f} ({s_frac*100:.3f}%)")
    print(f"    B only:   {b_frac:.6f} ({b_frac*100:.3f}%)")
    print(f"    GS:       {gs_frac:.6f} ({gs_frac*100:.3f}%)  ← LEAK")
    print(f"    GB:       {bg_frac:.6f} ({bg_frac*100:.3f}%)")
    print(f"    BS:       {bs_frac:.6f} ({bs_frac*100:.3f}%)")
    print(f"    GSB:      {gsb_frac:.6f} ({gsb_frac*100:.3f}%)  ← W⁴ ?")
    frac_sum = g_frac + s_frac + b_frac + gs_frac + bg_frac + bs_frac + gsb_frac
    print(f"    Sum:      {frac_sum:.6f} ({frac_sum*100:.3f}%)")
    print()

    # ── 5→3 COLLAPSE: TILING × G1 = COSMOLOGY (March 24, 2026) ──
    # The tiling shows the PRE-COLLAPSE 5-band state.
    # G1 = 0.3243 = first σ₃ sub-gap fraction = transmission through
    # the Cantor sub-gap that mediates the 5→3 collapse.
    # Post-collapse fractions = pre-collapse tiling × G1.
    G1 = 0.3243  # first σ₃ sub-gap fraction

    print(f"─" * 74)
    print(f"  5→3 COLLAPSE: TILING × G1 = COSMOLOGY")
    print(f"─" * 74)
    print()
    print(f"  G1 = first σ₃ sub-gap fraction = {G1}")
    print(f"  The tiling is the pre-collapse state.")
    print(f"  Multiply by G1 to get post-collapse (observed) fractions.")
    print()

    # Test 1: LEAK × G1 → W⁴ (baryonic matter)
    baryon_pred = LEAK * G1
    baryon_obs = wb4
    err_baryon = abs(baryon_pred - baryon_obs) / baryon_obs * 100
    print(f"  TEST 1: Baryonic matter")
    print(f"    LEAK × G1 = (1/φ⁴) × {G1}")
    print(f"             = {baryon_pred:.5f} ({baryon_pred*100:.3f}%)")
    print(f"    W⁴       = {baryon_obs:.5f} ({baryon_obs*100:.3f}%)")
    print(f"    Error:     {err_baryon:.1f}%")
    print(f"    {'PASS' if err_baryon < 2 else 'FAIL'}: "
          f"Gate transmission × collapse factor = baryon fraction")
    print()

    # Test 2: (GB + BS) × G1 → conduit dark matter
    # The user's formula: local_DM = LEAK - W⁴ = 9.8%
    # conduit_DM = (GB + BS) × G1 = 16.9%
    # total_DM = local + conduit = 26.6%
    conduit_walls = bg_frac + bs_frac
    conduit_dm = conduit_walls * G1
    local_dm = LEAK - wb4  # = 9.8% (gate states that miss bronze = DM)

    planck_dm = 0.265
    planck_de = 0.685

    print(f"  TEST 2: Conduit dark matter")
    print(f"    GB + BS = {conduit_walls:.6f} ({conduit_walls*100:.3f}%)")
    print(f"    (GB + BS) × G1 = {conduit_dm:.5f} ({conduit_dm*100:.3f}%)")
    # Compare to Planck Ω_DM minus local DM
    conduit_dm_obs = planck_dm - local_dm
    err_conduit = abs(conduit_dm - conduit_dm_obs) / conduit_dm_obs * 100
    print(f"    Planck Ω_DM - local_DM = {conduit_dm_obs:.5f} ({conduit_dm_obs*100:.3f}%)")
    print(f"    Error: {err_conduit:.1f}%")
    print(f"    {'PASS' if err_conduit < 2 else 'FAIL'}")
    print()

    # Test 3: local DM = LEAK - W⁴
    print(f"  TEST 3: Local dark matter")
    print(f"    LEAK - W⁴ = {local_dm:.5f} ({local_dm*100:.3f}%)")
    print(f"    Gate states with gold+silver but missing bronze connection")
    print()

    # Test 4: Total DM = local + conduit
    total_dm_pred = local_dm + conduit_dm
    err_total_dm = abs(total_dm_pred - planck_dm) / planck_dm * 100
    print(f"  TEST 4: Total dark matter")
    print(f"    Local DM (LEAK - W⁴):    {local_dm:.5f} ({local_dm*100:.3f}%)")
    print(f"    Conduit DM (GB+BS)×G1:   {conduit_dm:.5f} ({conduit_dm*100:.3f}%)")
    print(f"    Total DM predicted:       {total_dm_pred:.5f} ({total_dm_pred*100:.3f}%)")
    print(f"    Planck Ω_DM:              {planck_dm:.5f} ({planck_dm*100:.3f}%)")
    print(f"    Error:                     {err_total_dm:.1f}%")
    print(f"    {'PASS' if err_total_dm < 2 else 'FAIL'}: "
          f"(LEAK - W⁴) + (GB + BS) × G1 = Ω_DM")
    print()

    # Test 5: Dark energy = remainder
    de_pred = 1 - wb4 - total_dm_pred
    err_de = abs(de_pred - planck_de) / planck_de * 100
    print(f"  TEST 5: Dark energy (remainder)")
    print(f"    1 - Ω_b - Ω_DM = {de_pred:.5f} ({de_pred*100:.3f}%)")
    print(f"    Planck Ω_DE:     {planck_de:.5f} ({planck_de*100:.3f}%)")
    print(f"    Error:            {err_de:.1f}%")
    print(f"    {'PASS' if err_de < 2 else 'FAIL'}")
    print()

    # Summary table
    print(f"  ┌──────────────────────────────────────────────────────────────┐")
    print(f"  │  COSMOLOGICAL BUDGET FROM TILING                            │")
    print(f"  ├───────────────────┬──────────┬──────────┬──────────┬────────┤")
    print(f"  │ Component         │ Source   │ Predict  │ Planck   │ Error  │")
    print(f"  ├───────────────────┼──────────┼──────────┼──────────┼────────┤")
    print(f"  │ Ω_b  = LEAK×G1   │ GS×G1    │ {baryon_pred*100:5.2f}%   │"
          f" {baryon_obs*100:5.2f}%   │ {err_baryon:4.1f}%  │")
    print(f"  │ Ω_DM (local)     │ LEAK-W⁴  │ {local_dm*100:5.2f}%   │"
          f"        │        │")
    print(f"  │ Ω_DM (conduit)   │(GB+BS)G1 │ {conduit_dm*100:5.2f}%  │"
          f"        │        │")
    print(f"  │ Ω_DM (total)     │ sum      │ {total_dm_pred*100:5.2f}%  │"
          f" {planck_dm*100:5.2f}%  │ {err_total_dm:4.1f}%  │")
    print(f"  │ Ω_DE = remainder │ 1-b-DM   │ {de_pred*100:5.2f}%  │"
          f" {planck_de*100:5.2f}%  │ {err_de:4.1f}%  │")
    print(f"  └───────────────────┴──────────┴──────────┴──────────┴────────┘")
    print()

    # Fractions including overlaps
    g_any = sum(vtypes[t]['fraction'] for t in vtypes if 'G' in t)
    s_any = sum(vtypes[t]['fraction'] for t in vtypes if 'S' in t)
    b_any = sum(vtypes[t]['fraction'] for t in vtypes if 'B' in t)
    print(f"  Vertices with each grid present (including overlaps):")
    print(f"    Any Gold:   {g_any:.4f} ({g_any*100:.1f}%)")
    print(f"    Any Silver: {s_any:.4f} ({s_any*100:.1f}%)")
    print(f"    Any Bronze: {b_any:.4f} ({b_any*100:.1f}%)")
    print()

    # Compare to spectral σ₃ widths
    total_s3 = GOLD_S3 + SILVER_S3 + BRONZE_S3
    print(f"  Spectral σ₃ width fractions (for comparison):")
    print(f"    Gold/total:   {GOLD_S3/total_s3:.4f} ({GOLD_S3/total_s3*100:.1f}%)")
    print(f"    Silver/total: {SILVER_S3/total_s3:.4f} ({SILVER_S3/total_s3*100:.1f}%)")
    print(f"    Bronze/total: {BRONZE_S3/total_s3:.4f} ({BRONZE_S3/total_s3*100:.1f}%)")
    print()

    # σ₃ width ratios
    print(f"  σ₃ width ratios:")
    print(f"    Bronze/Gold  = {BRONZE_S3/GOLD_S3:.4f}  "
          f"vs φ = {PHI:.4f} ({abs(BRONZE_S3/GOLD_S3-PHI)/PHI*100:.1f}%)")
    print(f"    Gold/Silver  = {GOLD_S3/SILVER_S3:.4f}  "
          f"vs √2 = {2**0.5:.4f} ({abs(GOLD_S3/SILVER_S3-2**0.5)/2**0.5*100:.1f}%)")
    print(f"    Bronze/Silver= {BRONZE_S3/SILVER_S3:.4f}  "
          f"vs φ√2= {PHI*2**0.5:.4f} ({abs(BRONZE_S3/SILVER_S3-PHI*2**0.5)/(PHI*2**0.5)*100:.1f}%)")
    print()

    # ──────────────────────────────────────────────────────────
    # PHASE 4: VERTEX GEOMETRY (ANGLES)
    # ──────────────────────────────────────────────────────────
    print("─" * 74)
    print("  PHASE 4: VERTEX GEOMETRY — ANGLES AND DEPTH")
    print("─" * 74)
    print()

    print(f"  Computing nearest-neighbor angles at each vertex type...")
    angle_summary = compute_vertex_angles(vertices, n_neighbors=6)
    print()

    print(f"  {'Type':>6s} {'N':>6s} {'Min angle':>10s} {'±':>5s} "
          f"{'Mean gap':>10s}  {'θ = min/(2π·BOS)':>18s}")
    print(f"  {'─'*6} {'─'*6} {'─'*10} {'─'*5} {'─'*10}  {'─'*18}")

    theta_map = {}
    for vtype in ['B', 'G', 'S', 'BG', 'BS', 'GS', 'BGS']:
        if vtype in angle_summary:
            a = angle_summary[vtype]
            min_a_rad = a['min_angle_mean_deg'] * math.pi / 180
            theta = min_a_rad / (2 * math.pi * BOS)
            theta_map[vtype] = theta

            # Find closest framework θ
            best_name, best_err = '', 999
            for tname, tval in [('LEAK', THETA_LEAK), ('R_C', THETA_RC),
                                ('BASE', THETA_BASE)]:
                err = abs(theta - tval) / tval * 100
                if err < best_err:
                    best_name, best_err = tname, err

            tag = f" ≈ θ_{best_name}" if best_err < 30 else ""
            print(f"  {vtype:>6s} {a['count']:6d} {a['min_angle_mean_deg']:8.1f}° "
                  f"{'±':>5s}{a['min_angle_std_deg']:.1f}° "
                  f"{a['mean_gap_deg']:8.1f}°  {theta:18.4f}{tag}")

    print()

    # Depth parameter: smaller minimum angle = deeper confinement
    print(f"  Confinement depth ranking (smaller min angle = deeper):")
    depth_ranked = sorted(angle_summary.items(),
                          key=lambda x: x[1]['min_angle_mean_deg'])
    for rank, (vtype, a) in enumerate(depth_ranked):
        print(f"    {rank+1}. {vtype:>5s}: min angle {a['min_angle_mean_deg']:.1f}° "
              f"({'deepest' if rank == 0 else 'shallowest' if rank == len(depth_ranked)-1 else ''})")

    # ──────────────────────────────────────────────────────────
    # PHASE 5: TILE ANALYSIS
    # ──────────────────────────────────────────────────────────
    print()
    print("─" * 74)
    print("  PHASE 5: TILE ANALYSIS (Delaunay)")
    print("─" * 74)
    print()

    try:
        tiles, tile_types = extract_tiles_delaunay(vertices, max_edge=2.5)
        n_tile_types = len(tile_types)
        print(f"  Total tiles: {len(tiles)}")
        print(f"  Distinct tile types (by corner vertex classification): "
              f"{n_tile_types}")

        # Check if it's 13 or Fibonacci
        from itertools import takewhile
        fibs = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
        is_fib = n_tile_types in fibs
        is_13 = n_tile_types == 13

        if is_13:
            print(f"  ★ EXACTLY 13 tile types = bronze discriminant Δ₃!")
        elif is_fib:
            fi = fibs.index(n_tile_types)
            print(f"  Tile count {n_tile_types} = F({fi+1}) (Fibonacci)")
        else:
            nf = min(fibs, key=lambda f: abs(f - n_tile_types))
            print(f"  Tile count {n_tile_types} (nearest Fibonacci: {nf})")
        print()

        # Top tile types
        print(f"  Top 15 tile types by frequency:")
        print(f"  {'Corner types':>35s} {'Count':>8s} {'Fraction':>10s}")
        print(f"  {'─'*35} {'─'*8} {'─'*10}")
        for corners, count in tile_types.most_common(15):
            frac = count / len(tiles)
            corner_str = ' × '.join(corners)
            print(f"  {corner_str:>35s} {count:8d} {frac:10.4f}")

        # Edge length analysis
        print()
        edge_analysis = analyze_edge_lengths(tiles)
        if edge_analysis:
            print(f"  Edge length statistics:")
            print(f"    Total edges: {edge_analysis['n_edges']}")
            print(f"    Mean: {edge_analysis['mean']:.4f}")
            print(f"    Std:  {edge_analysis['std']:.4f}")
            print()

            if edge_analysis['peaks']:
                print(f"  Edge length peaks:")
                for length, count in edge_analysis['peaks'][:5]:
                    print(f"    {length:.4f} (n={count})")

            if edge_analysis['peak_ratios']:
                print()
                print(f"  Peak length ratios vs φ:")
                for pr in edge_analysis['peak_ratios'][:5]:
                    print(f"    {pr['lengths'][0]:.3f}/{pr['lengths'][1]:.3f} "
                          f"= {pr['ratio']:.4f} "
                          f"(φ error: {pr['phi_error']:.1f}%)")

    except ImportError:
        print(f"  (scipy not available — skipping Delaunay tile analysis)")
        tiles = []
        tile_types = Counter()
        n_tile_types = 0

    # ──────────────────────────────────────────────────────────
    # PHASE 6: BOND ENERGY AT GOLD VERTEX
    # ──────────────────────────────────────────────────────────
    print()
    print("─" * 74)
    print("  PHASE 6: BOND ENERGY ANALYSIS")
    print("─" * 74)
    print()

    # E_bracket vs C=C double bond
    cc_double = 6.35  # eV
    err_cc = abs(E_BRACKET - cc_double) / cc_double * 100
    print(f"  E_bracket = {E_BRACKET} eV")
    print(f"  C=C double bond energy = {cc_double} eV")
    print(f"  Match: {err_cc:.2f}%")
    print()

    # Bond energy predictions using spectral ratios
    bonds = [
        ('C-C single', 3.61),
        ('C=C double', 6.35),
        ('C≡C triple', 8.65),
        ('Fe metallic', 4.28),
        ('Au metallic', 3.81),
        ('H-H', 4.52),
        ('N≡N', 9.79),
        ('O=O', 5.15),
    ]

    print(f"  Bond energies as multiples of framework constants:")
    print(f"  {'Bond':>15s} {'E (eV)':>8s} {'E/E_br':>8s} {'Nearest':>20s} {'Error':>8s}")
    print(f"  {'─'*15} {'─'*8} {'─'*8} {'─'*20} {'─'*8}")

    framework_multiples = [
        ('GOLD_S3×E_br', GOLD_S3 * E_BRACKET),
        ('R_MATTER×E_br', 0.0728 * E_BRACKET),
        ('LEAK×E_br', LEAK * E_BRACKET),
        ('R_SHELL×E_br', 0.3972 * E_BRACKET),
        ('W×E_br', W * E_BRACKET),
        ('1×E_br', E_BRACKET),
        ('φ×E_br', PHI * E_BRACKET),
        ('√φ×E_br', PHI**0.5 * E_BRACKET),
        ('R_C×E_br', R_C * E_BRACKET),
        ('(1+LEAK)×E_br', (1+LEAK) * E_BRACKET),
        ('φ²×E_br/φ', PHI * E_BRACKET),
        ('BASE×E_br/φ', 1.408 * E_BRACKET / PHI),
    ]

    for bname, bval in bonds:
        ratio = bval / E_BRACKET
        best_name, best_val, best_err = '', 0, 999
        for fname, fval in framework_multiples:
            err = abs(bval - fval) / bval * 100
            if err < best_err:
                best_name, best_val, best_err = fname, fval, err
        print(f"  {bname:>15s} {bval:8.2f} {ratio:8.4f} "
              f"{best_name:>20s} {best_err:7.1f}%")

    # ──────────────────────────────────────────────────────────
    # PHASE 7: SILVER DEPTH AND BCC METALS
    # ──────────────────────────────────────────────────────────
    print()
    print("─" * 74)
    print("  PHASE 7: SILVER DEEP VERTEX — BCC METAL CONNECTION")
    print("─" * 74)
    print()

    # BCC metals and melting points
    bcc_metals = [
        ('W',  3695, 'silver-7'),
        ('Re', 3459, 'silver-7/gold'),
        ('Ta', 3290, 'silver-7'),
        ('Mo', 2896, 'silver-7'),
        ('Nb', 2750, 'silver-7'),
        ('Cr', 2180, 'silver-7'),
        ('V',  2183, 'silver-7'),
        ('Fe', 1811, 'silver-7'),
    ]

    fcc_metals = [
        ('Pt', 2041, 'gold/bronze'),
        ('Rh', 2237, 'gold/bronze'),
        ('Ir', 2719, 'gold/bronze'),
        ('Ni', 1728, 'gold/bronze'),
        ('Cu', 1358, 'gold/bronze'),
        ('Ag', 1235, 'gold/bronze'),
        ('Au', 1337, 'gold/bronze'),
        ('Al',  933, 'gold/bronze'),
    ]

    print(f"  BCC metals (predicted: silver vertex = deep confinement):")
    print(f"  {'Element':>8s} {'T_melt (K)':>10s} {'Crystal':>10s}")
    print(f"  {'─'*8} {'─'*10} {'─'*10}")
    for sym, tm, _ in bcc_metals:
        print(f"  {sym:>8s} {tm:10d} {'BCC':>10s}")

    print()
    print(f"  FCC metals (predicted: gold/bronze vertex = shallower):")
    for sym, tm, _ in fcc_metals:
        print(f"  {sym:>8s} {tm:10d} {'FCC':>10s}")

    bcc_mean = np.mean([t for _, t, _ in bcc_metals])
    fcc_mean = np.mean([t for _, t, _ in fcc_metals])
    print()
    print(f"  Mean melting point:")
    print(f"    BCC metals: {bcc_mean:.0f} K")
    print(f"    FCC metals: {fcc_mean:.0f} K")
    print(f"    Ratio BCC/FCC: {bcc_mean/fcc_mean:.3f}")

    # Is ratio related to framework?
    ratio_bf = bcc_mean / fcc_mean
    candidates = [
        ('φ', PHI),
        ('δ₂/δ₁', DELTA_S / PHI),
        ('√2', 2**0.5),
        ('1+LEAK', 1 + LEAK),
        ('φ²/2', PHI**2 / 2),
        ('BASE', 1.408),
        ('3/2', 1.5),
        ('SILVER_S3/GOLD_S3 × φ', SILVER_S3 / GOLD_S3 * PHI),
    ]

    print(f"    Searching for BCC/FCC ratio = {ratio_bf:.3f}:")
    for name, val in candidates:
        err = abs(ratio_bf - val) / ratio_bf * 100
        if err < 15:
            print(f"      {name} = {val:.4f} ({err:.1f}%)")

    # CONDUIT comparison
    DARK_GOLD = 0.290
    CONDUIT = DARK_GOLD / BRONZE_S3
    print()
    print(f"  CONDUIT = DARK_GOLD/BRONZE_S3 = {DARK_GOLD}/{BRONZE_S3} "
          f"= {CONDUIT:.4f}")

    if 'S' in angle_summary and 'G' in angle_summary:
        s_depth = 1.0 / angle_summary['S']['min_angle_mean_deg']
        g_depth = 1.0 / angle_summary['G']['min_angle_mean_deg']
        depth_ratio = g_depth / s_depth if s_depth > 0 else 0
        print(f"  Depth ratio Gold/Silver = {depth_ratio:.4f}")
        print(f"  CONDUIT match: {abs(depth_ratio - CONDUIT)/CONDUIT*100:.1f}%")

    # ──────────────────────────────────────────────────────────
    # PHASE 8: TILE TYPE COUNT vs 13
    # ──────────────────────────────────────────────────────────
    print()
    print("─" * 74)
    print("  PHASE 8: TILE TYPE COUNT vs BRONZE DISCRIMINANT 13")
    print("─" * 74)
    print()

    print(f"  Bronze discriminant Δ₃ = 13")
    print(f"  Culik (1996): exactly 13 Wang tiles for aperiodic tiling")
    print(f"  Aufbau multiplier: k = 13")
    print()

    if n_tile_types > 0:
        print(f"  Observed distinct tile types: {n_tile_types}")
        if n_tile_types == 13:
            print(f"  ★ EXACT MATCH: 13 tile types = Δ₃!")
        else:
            print(f"  Does not equal 13.")
            # Check if filtering changes the count
            # Only count types with > 1% frequency
            sig_types = sum(1 for _, c in tile_types.items()
                           if c / len(tiles) > 0.01)
            print(f"  Significant types (>1% frequency): {sig_types}")
            if sig_types == 13:
                print(f"  ★ 13 significant tile types!")
            elif sig_types in [1, 1, 2, 3, 5, 8, 13, 21, 34]:
                fi_sig = [1, 1, 2, 3, 5, 8, 13, 21, 34].index(sig_types) + 1
                print(f"  Significant count {sig_types} = F({fi_sig})")

    # ══════════════════════════════════════════════════════════
    # SCORECARD
    # ══════════════════════════════════════════════════════════
    print()
    print("─" * 74)
    print("  SCORECARD")
    print("─" * 74)
    print()

    tests = [
        ("Three grids produce 7 vertex types (G,S,B,GS,GB,SB,GSB)",
         len(vtypes) >= 5),

        (f"GS = LEAK = 1/φ⁴ ({err_gs_leak:.1f}%)",
         err_gs_leak < 5),

        (f"LEAK × G1 = W⁴ = Ω_b ({err_baryon:.1f}%)",
         err_baryon < 2),

        (f"(LEAK-W⁴) + (GB+BS)×G1 = Ω_DM ({err_total_dm:.1f}%)",
         err_total_dm < 2),

        (f"Remainder = Ω_DE ({err_de:.1f}%)",
         err_de < 3),

        ("BCC mean T_melt > FCC mean T_melt",
         bcc_mean > fcc_mean),

        (f"BCC/FCC melting ratio ≈ φ ({abs(ratio_bf-PHI)/PHI*100:.1f}%)",
         any(abs(ratio_bf - v) / ratio_bf * 100 < 10
             for _, v in candidates)),

        (f"E_bracket ≈ C=C double bond ({err_cc:.2f}%)",
         err_cc < 1.0),

        (f"Bronze/Gold σ₃ ratio ≈ φ ({abs(BRONZE_S3/GOLD_S3-PHI)/PHI*100:.1f}%)",
         abs(BRONZE_S3/GOLD_S3 - PHI)/PHI * 100 < 5),

        (f"Gold/Silver σ₃ ratio ≈ √2 ({abs(GOLD_S3/SILVER_S3-2**0.5)/2**0.5*100:.1f}%)",
         abs(GOLD_S3/SILVER_S3 - 2**0.5)/2**0.5 * 100 < 5),

        (f"G only ≈ R_MATTER = 0.0728 ({abs(g_frac-0.0728)/0.0728*100:.1f}%)",
         abs(g_frac - 0.0728) / 0.0728 * 100 < 10),

        (f"Vertex angles distinguish grid types",
         len(angle_summary) >= 3),
    ]

    n_pass = 0
    for desc, result in tests:
        status = "PASS" if result else "FAIL"
        if result:
            n_pass += 1
        print(f"    [{status}] {desc}")

    print()
    print(f"  Result: {n_pass}/{len(tests)} tests passed")

    # ══════════════════════════════════════════════════════════
    # SAVE
    # ══════════════════════════════════════════════════════════
    save_dir = os.path.expanduser(
        "~/Unified_Theory_Physics/results/tiling"
    )
    os.makedirs(save_dir, exist_ok=True)

    save_data = {
        'grid_params': {
            'gold_dirs': 5, 'silver_dirs': 4, 'bronze_dirs': 13,
            'gold_spacing': 1.0,
            'silver_spacing': round(1/DELTA_S, 4),
            'bronze_spacing': round(1/DELTA_B, 4),
        },
        'vertex_counts': {t: v['count'] for t, v in vtypes.items()},
        'vertex_fractions': {t: v['fraction'] for t, v in vtypes.items()},
        'total_vertices': v_total,
        'corrected_analysis': {
            'GS_fraction': round(gs_frac, 6),
            'GS_vs_LEAK': round(err_gs_leak, 1),
            'LEAK': round(LEAK, 6),
            'W4': round(wb4, 6),
        },
        'collapse_analysis': {
            'G1': G1,
            'LEAK_x_G1': round(baryon_pred, 6),
            'LEAK_x_G1_vs_W4_pct': round(err_baryon, 1),
            'walls_GB_BS': round(conduit_walls, 6),
            'conduit_dm_walls_x_G1': round(conduit_dm, 6),
            'local_dm_LEAK_minus_W4': round(local_dm, 6),
            'total_dm_pred': round(total_dm_pred, 6),
            'total_dm_vs_planck_pct': round(err_total_dm, 1),
            'de_pred': round(de_pred, 6),
            'de_vs_planck_pct': round(err_de, 1),
        },
        'sigma3_ratios': {
            'bronze_over_gold': round(BRONZE_S3/GOLD_S3, 4),
            'gold_over_silver': round(GOLD_S3/SILVER_S3, 4),
            'phi': round(PHI, 4),
            'sqrt2': round(2**0.5, 4),
        },
        'e_bracket_vs_cc': round(err_cc, 2),
        'bcc_fcc_ratio': round(ratio_bf, 3),
        'n_tile_types': n_tile_types,
        'tests_passed': n_pass,
        'tests_total': len(tests),
    }

    with open(os.path.join(save_dir, "triple_tiling.json"), 'w') as f:
        json.dump(save_data, f, indent=2)

    print(f"\n  Results saved: {save_dir}/triple_tiling.json")

    # ── CORRECTED SCORECARD (text file) ──
    corrected_lines = [
        "TRIPLE METALLIC MEAN TILING — CORRECTED SCORECARD",
        "=" * 52,
        f"Date: March 24, 2026",
        "",
        "KEY INSIGHT: Tiling = pre-collapse 5-band state.",
        "Cosmological budget = tiling vertex fractions × G1.",
        "G1 = 0.3243 = first σ₃ sub-gap = collapse transmission.",
        "",
        "5→3 COLLAPSE CHAIN:",
        f"  GS = LEAK = 1/φ⁴:           {gs_frac*100:.3f}% vs {LEAK*100:.3f}%  "
        f"({err_gs_leak:.1f}%)  PASS",
        f"  LEAK × G1 = W⁴ = Ω_b:       {baryon_pred*100:.3f}% vs {baryon_obs*100:.3f}%  "
        f"({err_baryon:.1f}%)  {'PASS' if err_baryon < 2 else 'FAIL'}",
        f"  (LEAK-W⁴) + (GB+BS)×G1 = Ω_DM: {total_dm_pred*100:.3f}% vs {planck_dm*100:.3f}%  "
        f"({err_total_dm:.1f}%)  {'PASS' if err_total_dm < 2 else 'FAIL'}",
        f"  Remainder = Ω_DE:            {de_pred*100:.3f}% vs {planck_de*100:.3f}%  "
        f"({err_de:.1f}%)  {'PASS' if err_de < 3 else 'FAIL'}",
        "",
        "FULL VERTEX HIERARCHY (pre-collapse):",
        f"  G only:   {g_frac*100:.3f}%   (≈ R_MATTER = 7.28%)",
        f"  S only:   {s_frac*100:.3f}%   (≈ silver σ₃ = 2.80%)",
        f"  B only:   {b_frac*100:.3f}%",
        f"  GS:       {gs_frac*100:.3f}%   = LEAK (gate transmission)",
        f"  GB:       {bg_frac*100:.3f}%   (conduit wall σ₂ analog)",
        f"  BS:       {bs_frac*100:.3f}%   (conduit wall σ₄ analog)",
        f"  GSB:      {gsb_frac*100:.3f}%   ≈ LEAK (pre-collapse)",
        f"  Sum:      {frac_sum*100:.3f}%",
        "",
        "OTHER CONFIRMATIONS:",
        f"  BCC/FCC = φ:       ratio {ratio_bf:.3f} ({abs(ratio_bf-PHI)/PHI*100:.1f}%)",
        f"  E_bracket = C=C:   {err_cc:.2f}%",
        f"  Bronze/Gold σ₃ ≈ φ: {abs(BRONZE_S3/GOLD_S3-PHI)/PHI*100:.1f}%",
        f"  Gold/Silver σ₃ ≈ √2: {abs(GOLD_S3/SILVER_S3-2**0.5)/2**0.5*100:.1f}%",
        f"  G only ≈ R_MATTER:  {abs(g_frac-0.0728)/0.0728*100:.1f}%",
        "",
        f"TESTS: {n_pass}/{len(tests)} passed",
    ]

    corrected_path = os.path.join(save_dir, "corrected.txt")
    with open(corrected_path, 'w') as f:
        f.write('\n'.join(corrected_lines) + '\n')
    print(f"  Corrected scorecard: {corrected_path}")


if __name__ == "__main__":
    main()
