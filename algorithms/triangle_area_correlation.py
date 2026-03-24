#!/usr/bin/env python3
"""
triangle_area_correlation.py — Discriminant Triangle Area Correlations
======================================================================
Thomas A. Husmann / iBuilt LTD / March 23, 2026

For each element (Z=1..56), compute the area of the triangle formed by
its position on the discriminant (√5, √8, √13) triangle:

    Area = (u_silver × √8) × (u_gold × √5) / 2

Then correlate these areas with atomic properties:
  - Atomic weight, covalent radius, vdW radius
  - Electronegativity (Pauling), ionization energy
  - Electron affinity, atomic number
  - vdW/cov ratio, period, block

© 2026 Thomas A. Husmann / iBuilt LTD. All rights reserved.
"""

import numpy as np
import math

# ══════════════════════════════════════════════════════════════════════
# FRAMEWORK CONSTANTS
# ══════════════════════════════════════════════════════════════════════

PHI = (1 + 5**0.5) / 2
W = (2 + PHI**(1/PHI**2)) / PHI**4
LEAK = 1 / PHI**4

SILVER_S3 = 0.171
GOLD_S3   = 0.236
BRONZE_S3 = 0.394
S3_TOTAL  = SILVER_S3 + GOLD_S3 + BRONZE_S3

DARK_SILVER = 0.83
DARK_GOLD   = 0.29
DARK_BRONZE = 0.61

DELTA_GOLD   = 5
DELTA_SILVER = 8
DELTA_BRONZE = 13

# ══════════════════════════════════════════════════════════════════════
# ELEMENT DATA
# ══════════════════════════════════════════════════════════════════════

REAL_CONFIG = {
    24: (5, 1), 29: (10, 1), 41: (4, 1), 42: (5, 1),
    44: (7, 1), 45: (8, 1), 46: (10, 0), 47: (10, 1),
}

MU_EFF = {26: 2.22, 27: 1.72, 28: 0.62}

RADII = {
    1:(31,120), 2:(28,140), 3:(128,182), 4:(96,153), 5:(84,192),
    6:(76,170), 7:(71,155), 8:(66,152), 9:(57,147), 10:(58,154),
    11:(166,227), 12:(141,173), 13:(121,184), 14:(111,210),
    15:(107,180), 16:(105,180), 17:(102,175), 18:(106,188),
    19:(203,275), 20:(176,231), 21:(170,211), 22:(160,187),
    23:(153,179), 24:(139,189), 25:(139,197), 26:(132,194),
    27:(126,192), 28:(124,163), 29:(132,140), 30:(122,139),
    31:(122,187), 32:(120,211), 33:(119,185), 34:(120,190),
    35:(120,185), 36:(116,202), 37:(220,303), 38:(195,249),
    39:(190,219), 40:(175,186), 41:(164,207), 42:(154,209),
    43:(147,209), 44:(146,207), 45:(142,195), 46:(139,202),
    47:(145,172), 48:(144,158), 49:(142,193), 50:(139,217),
    51:(139,206), 52:(138,206), 53:(139,198), 54:(140,216),
    55:(244,343), 56:(215,268),
}

SYMBOLS = {
    1:'H', 2:'He', 3:'Li', 4:'Be', 5:'B', 6:'C', 7:'N', 8:'O',
    9:'F', 10:'Ne', 11:'Na', 12:'Mg', 13:'Al', 14:'Si', 15:'P',
    16:'S', 17:'Cl', 18:'Ar', 19:'K', 20:'Ca', 21:'Sc', 22:'Ti',
    23:'V', 24:'Cr', 25:'Mn', 26:'Fe', 27:'Co', 28:'Ni', 29:'Cu',
    30:'Zn', 31:'Ga', 32:'Ge', 33:'As', 34:'Se', 35:'Br', 36:'Kr',
    37:'Rb', 38:'Sr', 39:'Y', 40:'Zr', 41:'Nb', 42:'Mo', 43:'Tc',
    44:'Ru', 45:'Rh', 46:'Pd', 47:'Ag', 48:'Cd', 49:'In', 50:'Sn',
    51:'Sb', 52:'Te', 53:'I', 54:'Xe', 55:'Cs', 56:'Ba',
}

# Atomic weights (standard)
ATOMIC_WEIGHT = {
    1:1.008, 2:4.003, 3:6.941, 4:9.012, 5:10.81, 6:12.01, 7:14.01,
    8:16.00, 9:19.00, 10:20.18, 11:22.99, 12:24.31, 13:26.98, 14:28.09,
    15:30.97, 16:32.07, 17:35.45, 18:39.95, 19:39.10, 20:40.08,
    21:44.96, 22:47.87, 23:50.94, 24:52.00, 25:54.94, 26:55.85,
    27:58.93, 28:58.69, 29:63.55, 30:65.38, 31:69.72, 32:72.63,
    33:74.92, 34:78.97, 35:79.90, 36:83.80, 37:85.47, 38:87.62,
    39:88.91, 40:91.22, 41:92.91, 42:95.95, 43:98.0, 44:101.07,
    45:102.91, 46:106.42, 47:107.87, 48:112.41, 49:114.82, 50:118.71,
    51:121.76, 52:127.60, 53:126.90, 54:131.29, 55:132.91, 56:137.33,
}

# Pauling electronegativity
ELECTRONEGATIVITY = {
    1:2.20, 2:None, 3:0.98, 4:1.57, 5:2.04, 6:2.55, 7:3.04, 8:3.44,
    9:3.98, 10:None, 11:0.93, 12:1.31, 13:1.61, 14:1.90, 15:2.19,
    16:2.58, 17:3.16, 18:None, 19:0.82, 20:1.00, 21:1.36, 22:1.54,
    23:1.63, 24:1.66, 25:1.55, 26:1.83, 27:1.88, 28:1.91, 29:1.90,
    30:1.65, 31:1.81, 32:2.01, 33:2.18, 34:2.55, 35:2.96, 36:3.00,
    37:0.82, 38:0.95, 39:1.22, 40:1.33, 41:1.60, 42:2.16, 43:1.90,
    44:2.20, 45:2.28, 46:2.20, 47:1.93, 48:1.69, 49:1.78, 50:1.96,
    51:2.05, 52:2.10, 53:2.66, 54:2.60, 55:0.79, 56:0.89,
}

# First ionization energy (eV)
IONIZATION_ENERGY = {
    1:13.598, 2:24.587, 3:5.392, 4:9.323, 5:8.298, 6:11.260,
    7:14.534, 8:13.618, 9:17.423, 10:21.565, 11:5.139, 12:7.646,
    13:5.986, 14:8.152, 15:10.487, 16:10.360, 17:12.968, 18:15.760,
    19:4.341, 20:6.113, 21:6.562, 22:6.828, 23:6.746, 24:6.767,
    25:7.434, 26:7.902, 27:7.881, 28:7.640, 29:7.726, 30:9.394,
    31:5.999, 32:7.900, 33:9.789, 34:9.752, 35:11.814, 36:14.000,
    37:4.177, 38:5.695, 39:6.217, 40:6.634, 41:6.759, 42:7.092,
    43:7.28, 44:7.361, 45:7.459, 46:8.337, 47:7.576, 48:8.994,
    49:5.786, 50:7.344, 51:8.608, 52:9.010, 53:10.451, 54:12.130,
    55:3.894, 56:5.212,
}

# Electron affinity (eV) — positive means energy released
ELECTRON_AFFINITY = {
    1:0.754, 2:0.0, 3:0.618, 4:0.0, 5:0.277, 6:1.263, 7:-0.07,
    8:1.461, 9:3.401, 10:0.0, 11:0.548, 12:0.0, 13:0.433, 14:1.390,
    15:0.746, 16:2.077, 17:3.617, 18:0.0, 19:0.501, 20:0.025,
    21:0.188, 22:0.079, 23:0.525, 24:0.676, 25:0.0, 26:0.151,
    27:0.662, 28:1.157, 29:1.236, 30:0.0, 31:0.43, 32:1.233,
    33:0.804, 34:2.021, 35:3.364, 36:0.0, 37:0.486, 38:0.048,
    39:0.307, 40:0.426, 41:0.893, 42:0.748, 43:0.55, 44:1.05,
    45:1.137, 46:0.562, 47:1.302, 48:0.0, 49:0.384, 50:1.112,
    51:1.047, 52:1.971, 53:3.059, 54:0.0, 55:0.472, 56:0.145,
}


def aufbau(Z):
    sub = []
    for n in range(1, 8):
        for l in range(n):
            sub.append((n, l, 2 * (2 * l + 1)))
    sub.sort(key=lambda s: (s[0] + s[1], s[0]))

    rem = Z
    filled = []
    for n, l, cap in sub:
        if rem <= 0:
            break
        e = min(rem, cap)
        filled.append((n, l, e, cap))
        rem -= e

    per = max(n for n, l, e, c in filled)
    n_p = sum(e for n, l, e, c in filled if n == per and l == 1)
    n_d_val = sum(e for n, l, e, c in filled if l == 2 and n == per - 1)
    n_s_val = sum(e for n, l, e, c in filled if n == per and l == 0)
    last_l = filled[-1][1]
    blk = {0: 's', 1: 'p', 2: 'd', 3: 'f'}.get(last_l, '?')

    se = {}
    sm2 = {}
    for n, l, e, cap in filled:
        se[n] = se.get(n, 0) + e
        sm2[n] = sm2.get(n, 0) + cap
    if se.get(per, 0) == sm2.get(per, 0):
        if Z == 2 or (last_l == 1 and filled[-1][2] == filled[-1][3]):
            blk = 'ng'
            if Z == 2:
                n_p = 0

    n_d = 0 if blk in ('p', 's', 'ng') else n_d_val
    n_s = n_s_val
    if Z in REAL_CONFIG and blk == 'd':
        n_d, n_s = REAL_CONFIG[Z]

    return per, n_p, n_d, n_s, blk


def barycentric_coords(Z, per, n_p, n_d, n_s, blk):
    u_s_base = SILVER_S3 / S3_TOTAL
    u_g_base = GOLD_S3 / S3_TOTAL
    u_b_base = BRONZE_S3 / S3_TOTAL

    silver_mod = (n_d / 10.0) * DARK_SILVER if n_d > 0 else 0.0
    gold_mod = (n_p / 6.0) * (1 - DARK_GOLD) * PHI**(-(per - 1)) if n_p > 0 else 0.0
    bronze_mod = (per - 1) / 6.0 * DARK_BRONZE * 0.1

    u_s = u_s_base + silver_mod
    u_g = u_g_base + gold_mod
    u_b = u_b_base + bronze_mod

    total = u_s + u_g + u_b
    u_s /= total
    u_g /= total
    u_b /= total

    return u_s, u_g, u_b


def triangle_area(u_s, u_g):
    """
    Area of the triangle formed by the element's position on the
    discriminant triangle: (u_silver × √8) × (u_gold × √5) / 2.

    The projections onto the silver (mass) and gold (momentum) legs
    give the physical coordinates on the (√5, √8, √13) triangle.
    """
    s_proj = u_s * math.sqrt(DELTA_SILVER)   # silver → mass axis
    g_proj = u_g * math.sqrt(DELTA_GOLD)     # gold → momentum axis
    return s_proj * g_proj / 2.0


def pearson_r(x, y):
    """Compute Pearson correlation coefficient."""
    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)
    mask = np.isfinite(x) & np.isfinite(y)
    x, y = x[mask], y[mask]
    if len(x) < 3:
        return float('nan'), 0
    r = np.corrcoef(x, y)[0, 1]
    n = len(x)
    return r, n


def main():
    print("=" * 90)
    print("  DISCRIMINANT TRIANGLE AREA ANALYSIS")
    print("  Area = (u_silver × √8) × (u_gold × √5) / 2")
    print("  Correlation with atomic properties")
    print("=" * 90)
    print()

    # Compute areas for all elements
    elements = []
    for Z in sorted(RADII.keys()):
        per, n_p, n_d, n_s, blk = aufbau(Z)
        u_s, u_g, u_b = barycentric_coords(Z, per, n_p, n_d, n_s, blk)
        area = triangle_area(u_s, u_g)
        rc, rv = RADII[Z]

        elements.append({
            'Z': Z,
            'sym': SYMBOLS[Z],
            'per': per,
            'blk': blk,
            'n_p': n_p,
            'n_d': n_d,
            'u_s': u_s,
            'u_g': u_g,
            'u_b': u_b,
            'area': area,
            'r_cov': rc,
            'r_vdw': rv,
            'ratio': rv / rc,
            'weight': ATOMIC_WEIGHT.get(Z),
            'EN': ELECTRONEGATIVITY.get(Z),
            'IE': IONIZATION_ENERGY.get(Z),
            'EA': ELECTRON_AFFINITY.get(Z),
        })

    # ── Display all elements ──────────────────────────────────────
    print(f"  {'Z':>3} {'Sym':>3} {'Blk':>3} {'Per':>3} {'n_d':>2} {'n_p':>2}"
          f" {'u_s':>6} {'u_g':>6} {'u_b':>6} {'Area':>8}"
          f" {'r_cov':>5} {'r_vdw':>5} {'Ratio':>6}")
    print("  " + "─" * 85)

    for e in elements:
        print(f"  {e['Z']:3d} {e['sym']:>3} {e['blk']:>3} {e['per']:>3d}"
              f" {e['n_d']:>2d} {e['n_p']:>2d}"
              f" {e['u_s']:6.4f} {e['u_g']:6.4f} {e['u_b']:6.4f}"
              f" {e['area']:8.5f}"
              f" {e['r_cov']:5d} {e['r_vdw']:5d} {e['ratio']:6.3f}")

    # ── Area statistics ───────────────────────────────────────────
    areas = [e['area'] for e in elements]
    print()
    print(f"  Area statistics:")
    print(f"    Min:    {min(areas):.5f}  ({elements[np.argmin(areas)]['sym']})")
    print(f"    Max:    {max(areas):.5f}  ({elements[np.argmax(areas)]['sym']})")
    print(f"    Mean:   {np.mean(areas):.5f}")
    print(f"    Median: {np.median(areas):.5f}")
    print(f"    Std:    {np.std(areas):.5f}")

    # ── Area by block ─────────────────────────────────────────────
    print()
    print(f"  Area by block:")
    for blk_name in ['s', 'p', 'd', 'ng']:
        block_areas = [e['area'] for e in elements if e['blk'] == blk_name]
        if block_areas:
            label = {'s': 'S-block', 'p': 'P-block', 'd': 'D-block', 'ng': 'Noble'}[blk_name]
            print(f"    {label:>8}: n={len(block_areas):2d}  "
                  f"mean={np.mean(block_areas):.5f}  "
                  f"range=[{min(block_areas):.5f}, {max(block_areas):.5f}]")

    # ── Correlations ──────────────────────────────────────────────
    print()
    print("=" * 90)
    print("  CORRELATION ANALYSIS: Area vs Atomic Properties")
    print("=" * 90)
    print()

    area_arr = [e['area'] for e in elements]

    properties = [
        ('Atomic number Z',        [float(e['Z']) for e in elements]),
        ('Atomic weight',          [e['weight'] for e in elements]),
        ('Period',                 [float(e['per']) for e in elements]),
        ('Covalent radius (pm)',   [float(e['r_cov']) for e in elements]),
        ('vdW radius (pm)',        [float(e['r_vdw']) for e in elements]),
        ('vdW/cov ratio',          [e['ratio'] for e in elements]),
        ('Electronegativity',      [e['EN'] if e['EN'] is not None else float('nan') for e in elements]),
        ('Ionization energy (eV)', [e['IE'] for e in elements]),
        ('Electron affinity (eV)', [e['EA'] for e in elements]),
        ('n_d (d-electrons)',      [float(e['n_d']) for e in elements]),
        ('n_p (p-electrons)',      [float(e['n_p']) for e in elements]),
    ]

    print(f"  {'Property':>30}  {'Pearson r':>10}  {'N':>4}  {'Strength':>12}")
    print("  " + "─" * 65)

    correlations = []
    for name, values in properties:
        r, n = pearson_r(area_arr, values)
        strength = "STRONG" if abs(r) > 0.7 else ("moderate" if abs(r) > 0.4 else "weak")
        print(f"  {name:>30}  {r:+10.4f}  {n:4d}  {strength:>12}")
        correlations.append((name, r, n))

    # ── Per-block correlations ────────────────────────────────────
    print()
    print("  Per-block correlations (Area vs key properties):")
    for blk_name in ['s', 'p', 'd', 'ng']:
        block_el = [e for e in elements if e['blk'] == blk_name]
        if len(block_el) < 3:
            continue
        label = {'s': 'S-block', 'p': 'P-block', 'd': 'D-block', 'ng': 'Noble'}[blk_name]
        print(f"\n  --- {label} (n={len(block_el)}) ---")

        block_areas = [e['area'] for e in block_el]
        block_props = [
            ('IE (eV)',    [e['IE'] for e in block_el]),
            ('EN',         [e['EN'] if e['EN'] is not None else float('nan') for e in block_el]),
            ('r_cov (pm)', [float(e['r_cov']) for e in block_el]),
            ('ratio',      [e['ratio'] for e in block_el]),
            ('Z',          [float(e['Z']) for e in block_el]),
        ]

        for pname, pvals in block_props:
            r, n = pearson_r(block_areas, pvals)
            if n >= 3:
                strength = "STRONG" if abs(r) > 0.7 else ("moderate" if abs(r) > 0.4 else "weak")
                print(f"    {pname:>12}: r = {r:+.4f} (n={n}) {strength}")

    # ── φ-ratio analysis ──────────────────────────────────────────
    print()
    print("=" * 90)
    print("  φ-RATIO ANALYSIS: Do areas relate to framework constants?")
    print("=" * 90)
    print()

    # Check if area ratios between blocks match φ-ratios
    s_areas = [e['area'] for e in elements if e['blk'] == 's']
    p_areas = [e['area'] for e in elements if e['blk'] == 'p']
    d_areas = [e['area'] for e in elements if e['blk'] == 'd']
    ng_areas = [e['area'] for e in elements if e['blk'] == 'ng']

    mean_s = np.mean(s_areas)
    mean_p = np.mean(p_areas)
    mean_d = np.mean(d_areas)
    mean_ng = np.mean(ng_areas)

    print(f"  Block mean areas:")
    print(f"    S-block:  {mean_s:.6f}")
    print(f"    P-block:  {mean_p:.6f}")
    print(f"    D-block:  {mean_d:.6f}")
    print(f"    Noble:    {mean_ng:.6f}")
    print()

    # Ratios between block means
    ratios_to_check = [
        ('D-block / S-block', mean_d / mean_s),
        ('D-block / P-block', mean_d / mean_p),
        ('P-block / S-block', mean_p / mean_s),
        ('Noble / S-block',   mean_ng / mean_s),
        ('Noble / P-block',   mean_ng / mean_p),
        ('D-block / Noble',   mean_d / mean_ng),
    ]

    phi_targets = {
        'φ': PHI, '1/φ': 1/PHI, 'φ²': PHI**2, '1/φ²': 1/PHI**2,
        '√φ': math.sqrt(PHI), '1/√φ': 1/math.sqrt(PHI),
        'W': W, '1-W': 1-W, 'r_c': 1-1/PHI**4,
        'H': PHI**(-1/PHI), '2': 2.0, '3': 3.0,
    }

    print(f"  Block mean area ratios vs φ-constants:")
    for label, ratio in ratios_to_check:
        best = min(phi_targets.items(), key=lambda kv: abs(kv[1] - ratio))
        err = abs(best[1] - ratio) / ratio * 100
        print(f"    {label:>25} = {ratio:.4f}  ≈ {best[0]} = {best[1]:.4f} ({err:.1f}%)")

    # ── Sorted by area ────────────────────────────────────────────
    print()
    print("=" * 90)
    print("  ELEMENTS SORTED BY DISCRIMINANT TRIANGLE AREA")
    print("=" * 90)
    print()

    sorted_el = sorted(elements, key=lambda e: e['area'])

    print(f"  {'Rank':>4} {'Z':>3} {'Sym':>3} {'Blk':>3} {'Area':>8}"
          f" {'IE':>7} {'EN':>5} {'r_cov':>5} {'Ratio':>6}")
    print("  " + "─" * 55)

    for i, e in enumerate(sorted_el):
        en_str = f"{e['EN']:5.2f}" if e['EN'] is not None else "  ---"
        print(f"  {i+1:4d} {e['Z']:3d} {e['sym']:>3} {e['blk']:>3} {e['area']:8.5f}"
              f" {e['IE']:7.2f} {en_str} {e['r_cov']:5d} {e['ratio']:6.3f}")

    # ── Special: area × φ⁴ and other products ────────────────────
    print()
    print("=" * 90)
    print("  AREA × φ⁴ — LOOKING FOR UNIVERSAL PATTERNS")
    print("=" * 90)
    print()

    print(f"  {'Z':>3} {'Sym':>3} {'Blk':>3} {'Area':>8} {'A×φ⁴':>8}"
          f" {'A×φ²':>8} {'A×2':>8} {'A/W':>8}")
    print("  " + "─" * 60)

    for e in elements:
        a = e['area']
        print(f"  {e['Z']:3d} {e['sym']:>3} {e['blk']:>3} {a:8.5f}"
              f" {a*PHI**4:8.4f} {a*PHI**2:8.4f}"
              f" {a*2:8.5f} {a/W:8.5f}")

    # ── Check if area relates to the boundary law ─────────────────
    print()
    print("=" * 90)
    print("  BOUNDARY LAW CONNECTION")
    print("=" * 90)
    print()

    # The s-block baseline area (no d or p modifications)
    u_s_base = SILVER_S3 / S3_TOTAL
    u_g_base = GOLD_S3 / S3_TOTAL
    base_area = triangle_area(u_s_base, u_g_base)
    print(f"  Baseline area (no modulation): {base_area:.6f}")
    print(f"  2/φ⁴ = {2/PHI**4:.6f}")
    print(f"  3/φ³ = {3/PHI**3:.6f}")
    print(f"  W = {W:.6f}")
    print(f"  Base area / W = {base_area/W:.6f}")
    print(f"  Base area × φ⁴ = {base_area*PHI**4:.6f}")
    print(f"  Base area × 2 = {base_area*2:.6f}")
    print(f"  √(base_area) = {math.sqrt(base_area):.6f}")
    print(f"  Base area / (√5 × √8 / 2) = {base_area / (math.sqrt(5)*math.sqrt(8)/2):.6f}")
    print(f"    = u_s_base × u_g_base = {u_s_base * u_g_base:.6f}")

    # Check: does area partition the boundary law?
    sum_areas = sum(e['area'] for e in elements)
    print(f"\n  Sum of all areas = {sum_areas:.4f}")
    print(f"  Mean area × 56 = {np.mean(areas)*56:.4f}")
    print(f"  Sum / 56 = {sum_areas/56:.6f} (= mean area)")

    # ── Striking patterns ─────────────────────────────────────────
    print()
    print("=" * 90)
    print("  NOTABLE PATTERNS")
    print("=" * 90)
    print()

    # Elements with highest and lowest areas
    sorted_by_area = sorted(elements, key=lambda e: e['area'])
    print("  TOP 5 (largest area — most d-electron confinement):")
    for e in sorted_by_area[-5:]:
        print(f"    {e['sym']:>3} (Z={e['Z']:2d}) area={e['area']:.5f}  n_d={e['n_d']}  blk={e['blk']}")

    print("\n  BOTTOM 5 (smallest area — most p-electron momentum):")
    for e in sorted_by_area[:5]:
        print(f"    {e['sym']:>3} (Z={e['Z']:2d}) area={e['area']:.5f}  n_p={e['n_p']}  blk={e['blk']}")

    # Check: d-block area vs n_d
    d_el = [e for e in elements if e['blk'] == 'd']
    if d_el:
        d_areas = [e['area'] for e in d_el]
        d_nd = [float(e['n_d']) for e in d_el]
        r_nd, n_nd = pearson_r(d_areas, d_nd)
        print(f"\n  D-block: Area vs n_d correlation: r = {r_nd:+.4f} (n={n_nd})")
        print("  → d-electrons INCREASE silver weight → INCREASE area")

    # Check: p-block area vs n_p
    p_el = [e for e in elements if e['blk'] == 'p']
    if p_el:
        p_areas = [e['area'] for e in p_el]
        p_np = [float(e['n_p']) for e in p_el]
        r_np, n_np = pearson_r(p_areas, p_np)
        print(f"\n  P-block: Area vs n_p correlation: r = {r_np:+.4f} (n={n_np})")
        print("  → p-electrons increase gold weight but also normalize → complex effect")

    # ── Final: area as predictor of vdW/cov ratio ─────────────────
    print()
    print("=" * 90)
    print("  CAN AREA PREDICT vdW/cov RATIO?")
    print("=" * 90)
    print()

    r_all, n_all = pearson_r(area_arr, [e['ratio'] for e in elements])
    print(f"  Overall: r(Area, vdW/cov) = {r_all:+.4f} (n={n_all})")

    # Linear regression
    x = np.array(area_arr)
    y = np.array([e['ratio'] for e in elements])
    slope, intercept = np.polyfit(x, y, 1)
    y_pred = slope * x + intercept
    residuals = y - y_pred
    rmse = np.sqrt(np.mean(residuals**2))
    print(f"  Linear fit: ratio = {slope:.2f} × area + {intercept:.3f}")
    print(f"  RMSE = {rmse:.3f} ({rmse/np.mean(y)*100:.1f}% of mean ratio)")

    print()
    print("=" * 90)
    print("  ANALYSIS COMPLETE")
    print("=" * 90)


if __name__ == "__main__":
    main()
