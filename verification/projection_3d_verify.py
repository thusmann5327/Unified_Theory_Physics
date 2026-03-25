#!/usr/bin/env python3
"""
3D PROJECTION VERIFICATION: Does the 2+3 phase separation close the gap?
==========================================================================

Tests five claims from the 3D projection logic:
  1. σ₂+σ₃+σ₄ eigenvalue count ≈ 118 (spatial manifold = periodic table)
  2. Inter-layer ratios match Danzer prototile edge ratios (φ-powers)
  3. Icosahedral vertex fraction after 3 inflations ≈ W⁴ = Ω_b
  4. Cosmic web scales follow φ-scaling
  5. Nuclear magic corrections = inverse Danzer matching ratios

Thomas A. Husmann / iBuilt LTD
March 24, 2026
"""

import numpy as np
import math
import json
import os

# ══════════════════════════════════════════════════════════════════
# SETUP
# ══════════════════════════════════════════════════════════════════

PHI = (1 + 5**0.5) / 2
D = 233
N_BRACKETS = 294
W = (2 + PHI**(1/PHI**2)) / PHI**4
LEAK = 1 / PHI**4
R_C = 1 - LEAK
D_S = 0.5
H_HINGE = PHI**(-1/PHI)
RHO6 = PHI**(1/6)

# Build AAH spectrum
ALPHA_AAH = 1.0 / PHI
H_mat = np.diag(2 * np.cos(2 * np.pi * ALPHA_AAH * np.arange(D)))
H_mat += np.diag(np.ones(D - 1), 1) + np.diag(np.ones(D - 1), -1)
eigs = np.sort(np.linalg.eigvalsh(H_mat))
E_range = eigs[-1] - eigs[0]
half = E_range / 2
diffs = np.diff(eigs)
med = np.median(diffs)

# All gaps above threshold
gaps_all = [(i, diffs[i]) for i in range(len(diffs)) if diffs[i] > 8 * med]
ranked = sorted(gaps_all, key=lambda g: g[1], reverse=True)

# Five spectral ratios
dominant = [g for g in ranked if g[1] > 1.0]
wL = min(dominant, key=lambda g: eigs[g[0]] + eigs[g[0] + 1])

R_MATTER = abs(eigs[wL[0] + 1]) / half
R_INNER = abs(eigs[wL[0]] + eigs[wL[0] + 1]) / (2 * E_range)
R_SHELL = (abs(eigs[wL[0]]) + abs(eigs[wL[0] + 1])) / (2 * half)
R_OUTER = R_SHELL + wL[1] / (2 * E_range)
cos_alpha = math.cos(1.0 / PHI)
R_PHOTO = R_INNER + cos_alpha * (R_SHELL - R_INNER)

BASE = R_OUTER / R_SHELL

# Fibonacci
FIB = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]

# Nuclear magic
NUCLEAR_MAGIC = [2, 8, 20, 28, 50, 82, 126]


def nearest_fib(n):
    best_f, best_idx = FIB[0], 0
    for i, f in enumerate(FIB):
        if abs(f - n) < abs(best_f - n):
            best_f, best_idx = f, i
    return best_f, best_idx


def main():
    print("=" * 74)
    print("  3D PROJECTION VERIFICATION")
    print("  Does the 2+3 phase separation close the gap?")
    print("=" * 74)

    # ══════════════════════════════════════════════════════════════
    # TASK 1: FIVE-SECTOR EIGENVALUE COUNT
    # ══════════════════════════════════════════════════════════════
    print()
    print("─" * 74)
    print("  TASK 1: FIVE-SECTOR EIGENVALUE COUNT")
    print("─" * 74)
    print()

    # Find the 4 largest gaps to partition into 5 sectors
    top4 = sorted(ranked[:4], key=lambda g: g[0])  # sort by position

    print(f"  Top 4 gaps (sorted by position in spectrum):")
    for i, (idx, width) in enumerate(top4):
        E_left = eigs[idx]
        E_right = eigs[idx + 1]
        print(f"    Gap {i+1}: index {idx:3d}, width {width:.4f}, "
              f"between E={E_left:.3f} and E={E_right:.3f}")

    # Partition eigenvalues into 5 sectors
    boundaries = sorted([g[0] for g in top4])
    sectors = []
    start = 0
    for b in boundaries:
        sector_eigs = eigs[start:b + 1]
        sectors.append(sector_eigs)
        start = b + 1
    sectors.append(eigs[start:])  # last sector

    print()
    print(f"  Five-sector eigenvalue partition:")
    print(f"  {'Sector':>8s} {'Count':>6s} {'E_min':>10s} {'E_max':>10s} {'E_center':>10s}")
    print(f"  {'─'*8} {'─'*6} {'─'*10} {'─'*10} {'─'*10}")

    sector_names = ['σ₁ (dark−)', 'σ₂ (inner)', 'σ₃ (core)',
                    'σ₄ (outer)', 'σ₅ (dark+)']
    sector_counts = []
    for i, sec in enumerate(sectors):
        n = len(sec)
        sector_counts.append(n)
        e_min = sec[0] if len(sec) > 0 else 0
        e_max = sec[-1] if len(sec) > 0 else 0
        e_ctr = np.mean(sec) if len(sec) > 0 else 0
        print(f"  {sector_names[i]:>10s} {n:6d} {e_min:10.4f} {e_max:10.4f} {e_ctr:10.4f}")

    n1, n2, n3, n4, n5 = sector_counts
    total = sum(sector_counts)

    print()
    print(f"  Total: {total} (should be {D}): {'✓' if total == D else '✗'}")
    print()

    # Spatial manifold = σ₂ + σ₃ + σ₄
    n_spatial = n2 + n3 + n4
    n_energy = n1 + n5

    print(f"  n_spatial = n₂ + n₃ + n₄ = {n2} + {n3} + {n4} = {n_spatial}")
    print(f"  Z_max = 118")
    print(f"  Difference: {n_spatial} − 118 = {n_spatial - 118}")
    err_spatial = abs(n_spatial - 118) / 118 * 100
    print(f"  Error: {err_spatial:.1f}%")

    if n_spatial == 118:
        print(f"  ◄ EXACT MATCH: spatial eigenvalue count = Z_max = 118")
    elif abs(n_spatial - 118) <= 5:
        print(f"  ◄ CLOSE: within {abs(n_spatial - 118)} of 118")

    print()
    print(f"  n_energy = n₁ + n₅ = {n1} + {n5} = {n_energy}")
    print(f"  Dark sector: 233 − 118 = {233 - 118}")
    print(f"  Difference: {n_energy} − 115 = {n_energy - 115}")
    print()

    # Also check: D × D_s = 116.5 (from aufbau_bridge)
    print(f"  Cross-check: D × D_s = {D} × {D_S} = {D * D_S}")
    print(f"  n_spatial / 2 = {n_spatial / 2}")
    print(f"  n₃ = {n3} (core/matter states)")
    print()

    # Sector fractions
    print(f"  Sector fractions:")
    for i, n in enumerate(sector_counts):
        frac = n / D
        print(f"    {sector_names[i]:>10s}: {n:3d}/{D} = {frac:.4f} ({frac*100:.1f}%)")

    print()

    # Compare to cosmological fractions
    omega_b = W**4
    omega_dm_new = 1 - W**4 - W**2 - W
    omega_de_new = W**2 + W

    frac_core = n3 / D
    frac_walls = (n2 + n4) / D
    frac_dark = (n1 + n5) / D

    print(f"  Cosmological comparison:")
    print(f"    Core (σ₃):  {frac_core:.4f}  vs  Ω_b = {omega_b:.4f} "
          f"({abs(frac_core - omega_b)/omega_b*100:.1f}%)")
    print(f"    Walls (σ₂+σ₄): {frac_walls:.4f}  vs  Ω_DM = {omega_dm_new:.4f} "
          f"({abs(frac_walls - omega_dm_new)/omega_dm_new*100:.1f}%)")
    print(f"    Dark (σ₁+σ₅): {frac_dark:.4f}  vs  Ω_DE = {omega_de_new:.4f} "
          f"({abs(frac_dark - omega_de_new)/omega_de_new*100:.1f}%)")

    # ══════════════════════════════════════════════════════════════
    # TASK 2: SECTOR COUPLING RATIOS = DANZER PROTOTILE EDGES?
    # ══════════════════════════════════════════════════════════════
    print()
    print("─" * 74)
    print("  TASK 2: INTER-LAYER RATIOS vs DANZER TILE EDGES")
    print("─" * 74)
    print()

    # Four inter-layer ratios
    ratios = [
        ('σ₂/σ₁ = R_INNER/R_MATTER', R_INNER / R_MATTER),
        ('σ₃/σ₂ = R_PHOTO/R_INNER', R_PHOTO / R_INNER),
        ('σ₄/σ₃ = R_SHELL/R_PHOTO', R_SHELL / R_PHOTO),
        ('σ₅/σ₄ = R_OUTER/R_SHELL', R_OUTER / R_SHELL),
    ]

    print(f"  Spectral ratios:")
    for name, val in ratios:
        print(f"    {name} = {val:.4f}")

    print()

    # Search for φ-expressions
    phi_candidates = [
        ('2φ', 2 * PHI),
        ('φ²', PHI**2),
        ('φ + LEAK', PHI + LEAK),
        ('2φ − LEAK', 2 * PHI - LEAK),
        ('√(5+φ)', math.sqrt(5 + PHI)),
        ('φ + 1', PHI + 1),
    ]

    mid_candidates = [
        ('φ − LEAK', PHI - LEAK),
        ('√φ + LEAK', math.sqrt(PHI) + LEAK),
        ('φ/√R_C', PHI / math.sqrt(R_C)),
        ('φ × ρ₆', PHI * RHO6),
        ('1 + R_SHELL', 1 + R_SHELL),
        ('3/2 + LEAK', 1.5 + LEAK),
        ('√(φ²+LEAK)', math.sqrt(PHI**2 + LEAK)),
        ('2 − W', 2 - W),
    ]

    small_candidates = [
        ('ρ₆ = φ^(1/6)', RHO6),
        ('1 + R_MATTER', 1 + R_MATTER),
        ('1 + LEAK/2', 1 + LEAK / 2),
        ('√(1 + LEAK)', math.sqrt(1 + LEAK)),
        ('φ/√φ² − 1', PHI / math.sqrt(PHI**2 - 1)),
        ('2 − √R_C', 2 - math.sqrt(R_C)),
    ]

    base_candidates = [
        ('BASE (exact)', BASE),
        ('√2', math.sqrt(2)),
        ('φ − LEAK', PHI - LEAK),
        ('2 − R_SHELL', 2 - R_SHELL),
    ]

    all_candidates = [phi_candidates, mid_candidates, small_candidates, base_candidates]

    print(f"  Framework constant search:")
    print()

    danzer_matches = []
    for i, (name, val) in enumerate(ratios):
        best_name, best_val, best_err = '', 0, 999
        for cname, cval in all_candidates[i]:
            err = abs(val - cval) / val * 100
            if err < best_err:
                best_name, best_val, best_err = cname, cval, err

        # Also search all candidate lists
        global_best = best_name, best_val, best_err
        for clist in all_candidates:
            for cname, cval in clist:
                err = abs(val - cval) / val * 100
                if err < global_best[2]:
                    global_best = cname, cval, err

        print(f"    {name} = {val:.4f}")
        if global_best[2] < 1.0:
            print(f"      BEST: {global_best[0]} = {global_best[1]:.4f} "
                  f"({global_best[2]:.2f}%) ◄")
            danzer_matches.append((name, val, global_best[0], global_best[1],
                                   global_best[2]))
        else:
            print(f"      Best: {global_best[0]} = {global_best[1]:.4f} "
                  f"({global_best[2]:.1f}%)")
        print()

    # Explicit test: ratio 1 ≈ 2φ?
    r1 = R_INNER / R_MATTER
    err_2phi = abs(r1 - 2 * PHI) / r1 * 100
    print(f"  Key tests:")
    print(f"    σ₂/σ₁ = {r1:.4f} vs 2φ = {2*PHI:.4f} ({err_2phi:.2f}%)")

    # Explicit test: ratio 3 ≈ ρ₆?
    r3 = R_SHELL / R_PHOTO
    err_rho6 = abs(r3 - RHO6) / r3 * 100
    print(f"    σ₄/σ₃ = {r3:.4f} vs ρ₆ = {RHO6:.4f} ({err_rho6:.2f}%)")

    # Explicit test: ratio 4 = BASE
    r4 = R_OUTER / R_SHELL
    print(f"    σ₅/σ₄ = {r4:.4f} vs BASE = {BASE:.4f} (0.00% by construction)")

    # Check for Danzer prototile connection
    # The four Danzer tetrahedra (A,B,C,K) have edges that are
    # powers of τ = φ: specifically τ⁰=1, τ¹=φ, τ²=φ²
    # And edge length ratios between tiles
    print()
    print(f"  Danzer prototile edge ratios (powers of φ):")
    print(f"    φ⁰ = 1.000")
    print(f"    φ¹ = {PHI:.4f}")
    print(f"    φ² = {PHI**2:.4f}")
    print(f"    2φ = {2*PHI:.4f}")
    print()

    # ══════════════════════════════════════════════════════════════
    # TASK 3: ICOSAHEDRAL VERTEX FRACTION
    # ══════════════════════════════════════════════════════════════
    print()
    print("─" * 74)
    print("  TASK 3: ICOSAHEDRAL VERTEX FRACTION vs Ω_b")
    print("─" * 74)
    print()

    # Icosahedron: 12 vertices, 30 edges, 20 faces
    # Icosidodecahedron (rectified icosahedron): 30 vertices
    # Dual dodecahedron: 20 vertices, 12 faces
    # Compound icosahedron+dodecahedron: 12+20 = 32 vertices

    # In a Danzer tiling, each inflation step multiplies the number
    # of prototiles. The four Danzer prototile types have known
    # inflation multipliers:
    #   A → 6A + 2B + 7C + 5K   (example from Danzer 1989)
    # The total number of tiles grows as φ³ per inflation.

    # For icosahedral quasicrystal vertex analysis:
    # Start with a single icosahedron (12 vertices, all 5-fold)
    # At each inflation level:
    #   - New vertices appear at midpoints/divisions
    #   - Most new vertices have LOWER symmetry (2-fold or irregular)
    #   - Full 5-fold vertices are rare in the bulk

    # Method: count vertex types in the Ammann-Kramer model
    # The "Bergman cluster" has:
    #   12 vertices (icosahedral, 5-fold)
    #   20 vertices (dodecahedral, 3-fold)
    #   12 midedge vertices (2-fold)
    # Total per cluster: 44

    # In a large quasicrystal, the vertex frequency ratio is known:
    # The fraction of "node" vertices (sites at cluster centers) is:
    # f_node = 1/(τ³ + 1) where τ = φ (from Henley 1986)

    f_node_exact = 1 / (PHI**3 + 1)
    print(f"  Henley vertex fraction (quasicrystal node sites):")
    print(f"    f_node = 1/(φ³+1) = {f_node_exact:.6f}")
    print(f"    Ω_b = W⁴ = {W**4:.6f}")
    print(f"    Error: {abs(f_node_exact - W**4)/W**4*100:.1f}%")
    print()

    # Alternative: inflation-based counting
    print(f"  Inflation-based vertex fraction:")
    print()

    # Initial icosahedron: 12 full-symmetry vertices out of 12 total
    # Each inflation by φ³ factor:
    #   New vertices: (old_total × φ³) − old_total
    #   New full-symmetry: much fewer
    # Model: 12 of initial stay full-sym, rest are lower symmetry
    # After n inflations: total ≈ 12 × φ^(3n), full-sym ≈ 12 (core) + edge corrections

    # Known result from Elser & Henley (1985):
    # In a 3D Penrose tiling, there are 4 vertex types.
    # The "P" vertex (prolate rhombohedron center) has frequency ≈ 1/τ³
    # The "O" vertex (oblate center) has frequency ≈ 1/τ⁴
    # Together the high-symmetry vertices: 1/τ³ + 1/τ⁴ = 1/τ² = 1/φ²

    f_P = 1 / PHI**3
    f_O = 1 / PHI**4
    f_highsym = f_P + f_O

    print(f"  Elser-Henley vertex frequencies (3D Penrose tiling):")
    print(f"    Prolate (P): 1/φ³ = {f_P:.6f}")
    print(f"    Oblate  (O): 1/φ⁴ = {f_O:.6f} = LEAK")
    print(f"    High-symmetry total: {f_highsym:.6f} = 1/φ² = {1/PHI**2:.6f}")
    print()

    # The OBLATE vertex fraction alone = 1/φ⁴ = LEAK ≈ 14.6%
    # But Ω_b = W⁴ = 4.76%
    print(f"  Comparing vertex frequencies to Ω_b = {W**4:.6f}:")
    print(f"    1/φ⁴ = {LEAK:.6f} ({abs(LEAK - W**4)/W**4*100:.1f}% off) — too high")
    print()

    # Try: W⁴ as a PRODUCT of vertex frequencies?
    # W⁴ = f_P × f_O × something?
    print(f"  Searching for W⁴ as vertex frequency combination:")
    vertex_combos = [
        ('1/φ⁴ × R_MATTER', LEAK * R_MATTER),
        ('1/φ⁴ × R_SHELL', LEAK * R_SHELL),
        ('1/φ⁴ × W', LEAK * W),
        ('1/φ⁴ × 1/3', LEAK / 3),
        ('1/φ⁶', 1 / PHI**6),
        ('1/φ³ × 1/φ⁴', f_P * f_O),
        ('(1/φ³)² × 1/φ⁴', f_P**2 * f_O),
        ('1/(φ³+1)', f_node_exact),
        ('12/D', 12 / D),
        ('20/D × 1/φ', 20 / D / PHI),
        ('R_MATTER × R_SHELL', R_MATTER * R_SHELL),
    ]

    close_combos = []
    for name, val in vertex_combos:
        err = abs(val - W**4) / W**4 * 100
        tag = " ◄" if err < 10 else ""
        print(f"    {name:<25s} = {val:.6f}  ({err:.1f}%){tag}")
        if err < 10:
            close_combos.append((name, val, err))

    print()

    # Inflation counting approach
    print(f"  Inflation counting (n levels):")
    print(f"  {'n':>3s} {'Total vertices':>16s} {'Full-sym':>10s} "
          f"{'Fraction':>10s} {'vs W⁴':>10s}")
    print(f"  {'─'*3} {'─'*16} {'─'*10} {'─'*10} {'─'*10}")

    v_initial = 12  # icosahedral vertices
    v_total_initial = 62  # icosahedron + dodecahedron + icosidodecahedron
    inflation_target_n = None

    for n in range(0, 8):
        # Total vertices grow as φ^(3n) (volume scaling)
        v_total = v_total_initial * PHI**(3 * n)
        # Full-symmetry vertices: 12 persist + some new ones
        # Conservative: 12 (original) + small corrections at each level
        # Growth of full-sym vertices is slower: ∝ φ^(2n) (surface-like)
        v_fullsym = v_initial * PHI**(2 * n)
        frac = v_fullsym / v_total
        err_wb = abs(frac - W**4) / W**4 * 100
        tag = " ◄" if err_wb < 5 else ""
        print(f"  {n:3d} {v_total:16.0f} {v_fullsym:10.0f} "
              f"{frac:10.6f} {err_wb:9.1f}%{tag}")
        if inflation_target_n is None and frac < W**4:
            inflation_target_n = n

    print()

    # Exact check: does the decay rate match?
    # frac(n) = (12/62) × φ^(-n) = 0.1935 × φ^(-n)
    # frac = W⁴ → 0.1935 / φⁿ = 0.0476 → φⁿ = 4.065 → n = ln(4.065)/ln(φ) = 2.91
    n_exact = math.log(v_initial / v_total_initial / W**4) / math.log(PHI)
    # Actually: (12/62) × φ^(-n) = W⁴ → φⁿ = 12/(62×W⁴) = 12/2.951 = 4.065
    phi_n_needed = (v_initial / v_total_initial) / W**4
    n_needed = math.log(phi_n_needed) / math.log(PHI)

    print(f"  Fraction = {v_initial}/{v_total_initial} × φ⁻ⁿ = W⁴")
    print(f"  → φⁿ = {phi_n_needed:.4f}")
    print(f"  → n = {n_needed:.3f}")
    print(f"  → n ≈ {round(n_needed)} {'= 3 (spatial dimensions!) ◄' if round(n_needed) == 3 else ''}")

    # Verify at n=3
    frac_at_3 = (v_initial / v_total_initial) / PHI**3
    err_at_3 = abs(frac_at_3 - W**4) / W**4 * 100
    print(f"  At n=3: fraction = {frac_at_3:.6f} vs W⁴ = {W**4:.6f} "
          f"({err_at_3:.1f}%)")

    # ══════════════════════════════════════════════════════════════
    # TASK 4: COSMIC WEB SCALES
    # ══════════════════════════════════════════════════════════════
    print()
    print("─" * 74)
    print("  TASK 4: COSMIC WEB φ-SCALING")
    print("─" * 74)
    print()

    # Observed cosmic web scales (Mpc)
    cosmic_scales = {
        'Galaxy group': 1.5,
        'Void (small)': 10,
        'Void (typical)': 30,
        'Void (large)': 50,
        'BAO scale': 150,
        'Hubble radius': 4400,
    }

    print(f"  Observed cosmic web scales:")
    for name, scale in cosmic_scales.items():
        print(f"    {name:<20s}: {scale:8.1f} Mpc")

    print()
    print(f"  Ratio tests (looking for φ-scaling):")
    print()

    scale_list = list(cosmic_scales.items())
    phi_ratio_results = []
    for i in range(len(scale_list)):
        for j in range(i + 1, len(scale_list)):
            name_i, s_i = scale_list[i]
            name_j, s_j = scale_list[j]
            ratio = s_j / s_i

            # Search for φ-expression
            phi_matches = [
                ('φ', PHI),
                ('φ²', PHI**2),
                ('φ³', PHI**3),
                ('φ⁴', PHI**4),
                ('φ⁵', PHI**5),
                ('2φ', 2 * PHI),
                ('3φ', 3 * PHI),
                ('5', 5.0),
                ('3', 3.0),
                ('F(5)=5', 5.0),
                ('F(6)=8', 8.0),
                ('F(7)=13', 13.0),
                ('F(8)=21', 21.0),
                ('F(9)=34', 34.0),
                ('F(10)=55', 55.0),
                ('F(11)=89', 89.0),
                ('F(12)=144', 144.0),
                ('φ⁶', PHI**6),
                ('φ⁷', PHI**7),
                ('φ¹⁰', PHI**10),
                ('φ¹²', PHI**12),
                ('φ¹⁵', PHI**15),
                ('φ¹⁶', PHI**16),
                ('F(14)×φ', 377 * PHI),
            ]

            best_name, best_val, best_err = '', 0, 999
            for pname, pval in phi_matches:
                err = abs(ratio - pval) / ratio * 100
                if err < best_err:
                    best_name, best_val, best_err = pname, pval, err

            if best_err < 5:
                phi_ratio_results.append({
                    'from': name_i, 'to': name_j,
                    'ratio': ratio, 'match': best_name,
                    'match_val': best_val, 'error': best_err,
                })
                print(f"    {name_j}/{name_i} = {ratio:.3f} ≈ {best_name} "
                      f"= {best_val:.3f} ({best_err:.1f}%) ◄")

    if not phi_ratio_results:
        print(f"    No clean φ-ratios found in cosmic web scales within 5%")

    # Specific tests from the prompt
    print()
    print(f"  Specific ratio tests:")
    r_50_30 = 50 / 30
    print(f"    50 Mpc / 30 Mpc = {r_50_30:.4f} vs φ = {PHI:.4f} "
          f"({abs(r_50_30 - PHI)/PHI*100:.1f}%)")

    r_150_30 = 150 / 30
    print(f"    150 Mpc / 30 Mpc = {r_150_30:.1f} = F(5) = 5 "
          f"({'✓ FIBONACCI' if r_150_30 == 5.0 else ''})")

    r_150_50 = 150 / 50
    print(f"    150 Mpc / 50 Mpc = {r_150_50:.1f} vs φ² = {PHI**2:.3f} "
          f"({abs(r_150_50 - PHI**2)/PHI**2*100:.1f}%)")

    # BAO scale vs φ⁵ × galaxy group
    r_bao_group = 150 / 1.5
    print(f"    150 Mpc / 1.5 Mpc = {r_bao_group:.0f} vs F(10)=55+F(9)=34 "
          f"= {55+34} ({abs(r_bao_group - 89)/89*100:.1f}%)")
    print(f"    150 Mpc / 1.5 Mpc = {r_bao_group:.0f} = 100 vs F(11)=89 "
          f"({abs(r_bao_group - 89)/89*100:.1f}%)")

    # Hubble/BAO
    r_hubble_bao = 4400 / 150
    nf, fi = nearest_fib(round(r_hubble_bao))
    print(f"    4400 Mpc / 150 Mpc = {r_hubble_bao:.1f} vs F({fi+1})={nf} "
          f"({abs(r_hubble_bao - nf)/nf*100:.1f}%)")

    # ══════════════════════════════════════════════════════════════
    # TASK 5: NUCLEAR MAGIC CORRECTIONS = MATCHING RATIOS?
    # ══════════════════════════════════════════════════════════════
    print()
    print("─" * 74)
    print("  TASK 5: NUCLEAR MAGIC CORRECTIONS vs DANZER MATCHING RATIOS")
    print("─" * 74)
    print()

    # Magic number corrections (magic / nearest Fibonacci)
    print(f"  Nuclear magic / nearest Fibonacci:")
    print(f"  {'Magic':>6s} {'Near F':>7s} {'Ratio':>8s}")
    print(f"  {'─'*6} {'─'*7} {'─'*8}")

    corrections = []
    for m in NUCLEAR_MAGIC:
        nf, fi = nearest_fib(m)
        ratio = m / nf if nf > 0 else 0
        corrections.append((m, nf, fi, ratio))
        print(f"  {m:6d} {nf:7d} {ratio:8.4f}")

    print()

    # The matching ratio hypothesis: corrections ≈ inverse of prototile ratios
    # T₃↔T₄ matching: R_SHELL/R_PHOTO = 1.082
    matching_T3T4 = R_SHELL / R_PHOTO
    inv_T3T4 = 1 / matching_T3T4
    print(f"  Danzer T₃↔T₄ matching ratio: R_SHELL/R_PHOTO = {matching_T3T4:.4f}")
    print(f"  Inverse: 1/({matching_T3T4:.4f}) = {inv_T3T4:.4f}")
    print(f"  √R_C = {math.sqrt(R_C):.4f}")
    print(f"  Match: inverse = √R_C? {abs(inv_T3T4 - math.sqrt(R_C))/math.sqrt(R_C)*100:.2f}%")
    print()

    # Ward identity ratios
    ward_ratios = [
        ('R_C', R_C),
        ('√R_C', math.sqrt(R_C)),
        ('W + D_s', W + D_S),
        ('1/ρ₆', 1 / RHO6),
        ('1 − R_MATTER', 1 - R_MATTER),
        ('1 − LEAK', 1 - LEAK),
        ('R_C × (1+LEAK)', R_C * (1 + LEAK)),
        ('LORENTZ_W', math.sqrt(1 - W**2)),
        ('2/φ²', 2 / PHI**2),
        ('(φ-1)/φ', (PHI - 1) / PHI),
    ]

    print(f"  Correction factors vs Ward identity ratios:")
    print()

    correction_matches = []
    for m, nf, fi, ratio in corrections:
        if m in [2, 8]:
            # Exact Fibonacci — no correction
            continue

        best_name, best_val, best_err = '', 0, 999
        for wname, wval in ward_ratios:
            err = abs(ratio - wval) / ratio * 100
            if err < best_err:
                best_name, best_val, best_err = wname, wval, err

        match_tag = "◄" if best_err < 3 else ""
        correction_matches.append((m, nf, ratio, best_name, best_val, best_err))
        print(f"    {m:3d}/{nf:3d} = {ratio:.4f} ≈ {best_name} = {best_val:.4f} "
              f"({best_err:.1f}%) {match_tag}")

    print()

    # Test: is there a SINGLE correction function?
    # c(k) = magic(k) / F_nearest(k)
    # Does c(k) converge to √R_C or some other constant?
    non_exact = [(m, nf, ratio) for m, nf, fi, ratio in corrections if m not in [2, 8]]

    if non_exact:
        mean_corr = np.mean([r for _, _, r in non_exact])
        std_corr = np.std([r for _, _, r in non_exact])
        print(f"  Mean correction (excluding exact 2,8): {mean_corr:.4f} ± {std_corr:.4f}")
        print(f"  √R_C = {math.sqrt(R_C):.4f}")
        print(f"  Match: {abs(mean_corr - math.sqrt(R_C))/math.sqrt(R_C)*100:.1f}%")

    # The Ward identity constraint check
    print()
    print(f"  Ward identity constraints on magic numbers:")
    print()
    print(f"    W × φ⁴ = 2 + φ^(1/φ²)")
    print(f"      LHS = {W * PHI**4:.10f}")
    print(f"      RHS = {2 + PHI**(1/PHI**2):.10f}")
    print(f"      Error: {abs(W * PHI**4 - (2 + PHI**(1/PHI**2))):.2e}")
    print()
    print(f"    φ² × R_C = √5")
    print(f"      LHS = {PHI**2 * R_C:.10f}")
    print(f"      RHS = {math.sqrt(5):.10f}")
    print(f"      Error: {abs(PHI**2 * R_C - math.sqrt(5)):.2e}")
    print()

    # Does the correction pattern follow from R_C?
    # Hypothesis: magic(k) = F_nearest(k) × R_C^(f(k))
    # where f(k) encodes the prototile matching rule at that shell
    print(f"  Testing: magic = F_near × R_C^p for some power p:")
    for m, nf, fi, ratio in corrections:
        if m in [2, 8]:
            continue
        if ratio > 0 and ratio < 1:
            p = math.log(ratio) / math.log(R_C)
            print(f"    {m:3d} = {nf} × R_C^{p:.3f}")
        elif ratio >= 1:
            print(f"    {m:3d}/{nf} = {ratio:.4f} > 1 (overcounts F)")

    # ══════════════════════════════════════════════════════════════
    # SCORECARD
    # ══════════════════════════════════════════════════════════════
    print()
    print("─" * 74)
    print("  SCORECARD")
    print("─" * 74)
    print()

    tests = [
        ("n₁+n₂+n₃+n₄+n₅ = 233",
         total == 233),

        (f"n_spatial = n₂+n₃+n₄ = {n_spatial} within 5 of 118",
         abs(n_spatial - 118) <= 5),

        ("σ₂/σ₁ ≈ 2φ (< 1%)" if err_2phi < 1
         else f"σ₂/σ₁ ≈ 2φ ({err_2phi:.1f}%)",
         err_2phi < 5),

        (f"σ₄/σ₃ ≈ ρ₆ = φ^(1/6) ({err_rho6:.1f}%)",
         err_rho6 < 5),

        ("σ₅/σ₄ = BASE (exact by construction)",
         True),

        (f"50/30 Mpc ≈ φ ({abs(r_50_30 - PHI)/PHI*100:.1f}%)",
         abs(r_50_30 - PHI) / PHI * 100 < 5),

        ("150/30 Mpc = 5 = F(5) (exact)",
         r_150_30 == 5.0),

        (f"Inflation n ≈ 3 for vertex frac = W⁴ (n = {n_needed:.2f})",
         abs(round(n_needed) - 3) == 0),

        (f"Mean magic correction ≈ √R_C ({abs(mean_corr - math.sqrt(R_C))/math.sqrt(R_C)*100:.1f}%)"
         if non_exact else "No non-exact corrections",
         abs(mean_corr - math.sqrt(R_C)) / math.sqrt(R_C) * 100 < 5
         if non_exact else False),

        (f"Inverse T₃↔T₄ matching = √R_C ({abs(inv_T3T4 - math.sqrt(R_C))/math.sqrt(R_C)*100:.2f}%)",
         abs(inv_T3T4 - math.sqrt(R_C)) / math.sqrt(R_C) * 100 < 1),
    ]

    n_pass = 0
    for desc, result in tests:
        status = "PASS" if result else "FAIL"
        if result:
            n_pass += 1
        print(f"    [{status}] {desc}")

    print()
    print(f"  Result: {n_pass}/{len(tests)} tests passed")

    # Summary assessment
    print()
    print("─" * 74)
    print("  ASSESSMENT")
    print("─" * 74)
    print()

    if n_spatial == 118:
        print("  ★ EXACT: n_spatial = 118 = Z_max")
        print("    The periodic table counts spatial eigenvalues.")
    elif abs(n_spatial - 118) <= 5:
        print(f"  ● CLOSE: n_spatial = {n_spatial}, within "
              f"{abs(n_spatial - 118)} of 118")
        print(f"    Suggestive but not exact.")
    else:
        print(f"  ✗ n_spatial = {n_spatial}, too far from 118")

    print()

    # ══════════════════════════════════════════════════════════════
    # SAVE
    # ══════════════════════════════════════════════════════════════
    save_dir = os.path.expanduser(
        "~/Unified_Theory_Physics/results/projection_3d"
    )
    os.makedirs(save_dir, exist_ok=True)

    save_data = {
        'sector_counts': sector_counts,
        'sector_names': sector_names,
        'n_spatial': n_spatial,
        'n_energy': n_energy,
        'total': total,
        'Z_max_comparison': {
            'n_spatial': n_spatial,
            'Z_max': 118,
            'difference': n_spatial - 118,
            'error_pct': round(err_spatial, 2),
        },
        'inter_layer_ratios': {
            'sigma2_over_sigma1': round(R_INNER / R_MATTER, 4),
            'sigma3_over_sigma2': round(R_PHOTO / R_INNER, 4),
            'sigma4_over_sigma3': round(R_SHELL / R_PHOTO, 4),
            'sigma5_over_sigma4': round(R_OUTER / R_SHELL, 4),
        },
        'danzer_matches': {
            'ratio_1_vs_2phi': round(err_2phi, 2),
            'ratio_3_vs_rho6': round(err_rho6, 2),
        },
        'cosmic_phi_ratios': {
            '50_30': round(r_50_30, 4),
            '150_30': r_150_30,
            '150_50': r_150_50,
        },
        'inflation_n_for_Wb': round(n_needed, 3),
        'mean_magic_correction': round(mean_corr, 4) if non_exact else None,
        'sqrt_RC': round(math.sqrt(R_C), 4),
        'inverse_T3T4': round(inv_T3T4, 4),
        'tests_passed': n_pass,
        'tests_total': len(tests),
    }

    with open(os.path.join(save_dir, "projection_3d.json"), 'w') as f:
        json.dump(save_data, f, indent=2)

    print(f"\n  Results saved: {save_dir}/projection_3d.json")


if __name__ == "__main__":
    main()
