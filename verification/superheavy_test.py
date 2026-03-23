#!/usr/bin/env python3
"""
superheavy_test.py — Full periodic table Z=3-99 with relativistic gate
=====================================================================
Thomas A. Husmann / iBuilt LTD / March 23, 2026

Five δ_silver gates (all gated behind n_d = n_f = 0, silver vertex):
  1. Alkaline earths (s²): θ = r_c (Be: r_c × φ)
  2. Period 2 gate overflow (B): θ × φ
  3. sp³ hybridizers (n_p=2, per<6): θ × φ^(1/3)
  4. P-hole (n_p ≥ 4, per ≥ 3): ratio × r_c
  5. Period-6 relativistic (ρ₆ = φ^(1/6)):
     - 5d leak: θ_leak × ρ₆ (expanded 5d orbitals)
     - Inert pair (per≥6, n_p=2): skip sp³ (6s² stabilized)

Plus full periodic table scorecard Z=3-99 (97 elements).

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
R_C = 1 - LEAK
BREATHING = 1 - math.sqrt(1 - W**2)

alpha = 1.0 / PHI
D = 233
H = np.diag(2 * np.cos(2 * np.pi * alpha * np.arange(D)))
H += np.diag(np.ones(D - 1), 1) + np.diag(np.ones(D - 1), -1)
eigs = np.sort(np.linalg.eigvalsh(H))
E_range = eigs[-1] - eigs[0]
diffs = np.diff(eigs)
med = np.median(diffs)
gaps = [(i, diffs[i]) for i in range(len(diffs)) if diffs[i] > 8 * med]
ranked = sorted(gaps, key=lambda g: g[1], reverse=True)
wL = min([g for g in ranked if g[1] > 1],
         key=lambda g: eigs[g[0]] + eigs[g[0] + 1])
half = E_range / 2
R_SHELL = (abs(eigs[wL[0]]) + abs(eigs[wL[0] + 1])) / (2 * half)
R_OUTER = R_SHELL + wL[1] / (2 * E_range)

abs_e = np.abs(eigs)
ci = np.sort(np.argsort(abs_e)[:55])
ctr = eigs[ci]
s3w = ctr[-1] - ctr[0]
sd = np.diff(ctr)
sm = np.median(sd)
sg = sorted([sd[i] for i in range(len(sd)) if sd[i] > 4 * sm], reverse=True)
G1 = sg[0] / s3w if sg else 0.3243

BASE = R_OUTER / R_SHELL
BOS = 0.394 / R_SHELL
DARK_GOLD = 0.29
RHO6 = PHI**(1/6)  # 1.0835 — period-6 relativistic multiplier

# ══════════════════════════════════════════════════════════════════════
# COMPLETE ELEMENT DATABASE: Z=3-99
# ══════════════════════════════════════════════════════════════════════

RADII = {
    # Z=3-71 (existing)
    3:(128,182), 4:(96,153), 5:(84,192), 6:(76,170), 7:(71,155),
    8:(66,152), 9:(57,147), 10:(58,154), 11:(166,227), 12:(141,173),
    13:(121,184), 14:(111,210), 15:(107,180), 16:(105,180), 17:(102,175),
    18:(106,188), 19:(203,275), 20:(176,231), 21:(170,211), 22:(160,187),
    23:(153,179), 24:(139,189), 25:(139,197), 26:(132,194), 27:(126,192),
    28:(124,163), 29:(132,140), 30:(122,139), 31:(122,187), 32:(120,211),
    33:(119,185), 34:(120,190), 35:(120,185), 36:(116,202), 37:(220,303),
    38:(195,249), 39:(190,219), 40:(175,186), 41:(164,207), 42:(154,209),
    43:(147,209), 44:(146,207), 45:(142,195), 46:(139,202), 47:(145,172),
    48:(144,158), 49:(142,193), 50:(139,217), 51:(139,206), 52:(138,206),
    53:(139,198), 54:(140,216), 55:(244,343), 56:(215,268),
    # Lanthanides
    57:(207,298), 58:(204,288), 59:(203,292), 60:(201,295), 61:(199,291),
    62:(198,290), 63:(198,287), 64:(196,283), 65:(194,279), 66:(192,287),
    67:(192,281), 68:(189,283), 69:(190,279), 70:(187,280), 71:(187,274),
    # Z=72-88 (NEW)
    72:(175,212),  # Hf: 5d2 6s2
    73:(170,217),  # Ta: 5d3 6s2
    74:(162,210),  # W:  5d4 6s2
    75:(151,217),  # Re: 5d5 6s2
    76:(144,216),  # Os: 5d6 6s2
    77:(141,202),  # Ir: 5d7 6s2
    78:(136,175),  # Pt: 5d9 6s1 (anomalous)
    79:(136,166),  # Au: 5d10 6s1 (anomalous)
    80:(132,155),  # Hg: 5d10 6s2
    81:(145,196),  # Tl: 6p1
    82:(146,202),  # Pb: 6p2
    83:(148,207),  # Bi: 6p3
    84:(140,197),  # Po: 6p4 (radioactive)
    85:(150,202),  # At: 6p5 (very radioactive)
    86:(150,220),  # Rn: 6p6
    87:(260,348),  # Fr: 7s1 (very radioactive)
    88:(221,283),  # Ra: 7s2
    # Actinides (reliable + rough)
    89:(215,280), 90:(206,293), 91:(200,288), 92:(196,271), 93:(190,282),
    94:(187,281), 95:(180,283), 96:(169,305), 97:(168,340), 98:(168,305),
    99:(165,270),
}

SYMBOLS = {
    3:'Li', 4:'Be', 5:'B', 6:'C', 7:'N', 8:'O', 9:'F', 10:'Ne',
    11:'Na', 12:'Mg', 13:'Al', 14:'Si', 15:'P', 16:'S', 17:'Cl',
    18:'Ar', 19:'K', 20:'Ca', 21:'Sc', 22:'Ti', 23:'V', 24:'Cr',
    25:'Mn', 26:'Fe', 27:'Co', 28:'Ni', 29:'Cu', 30:'Zn', 31:'Ga',
    32:'Ge', 33:'As', 34:'Se', 35:'Br', 36:'Kr', 37:'Rb', 38:'Sr',
    39:'Y', 40:'Zr', 41:'Nb', 42:'Mo', 43:'Tc', 44:'Ru', 45:'Rh',
    46:'Pd', 47:'Ag', 48:'Cd', 49:'In', 50:'Sn', 51:'Sb', 52:'Te',
    53:'I', 54:'Xe', 55:'Cs', 56:'Ba',
    57:'La', 58:'Ce', 59:'Pr', 60:'Nd', 61:'Pm', 62:'Sm',
    63:'Eu', 64:'Gd', 65:'Tb', 66:'Dy', 67:'Ho', 68:'Er',
    69:'Tm', 70:'Yb', 71:'Lu',
    72:'Hf', 73:'Ta', 74:'W', 75:'Re', 76:'Os', 77:'Ir',
    78:'Pt', 79:'Au', 80:'Hg', 81:'Tl', 82:'Pb', 83:'Bi',
    84:'Po', 85:'At', 86:'Rn', 87:'Fr', 88:'Ra',
    89:'Ac', 90:'Th', 91:'Pa', 92:'U', 93:'Np', 94:'Pu', 95:'Am',
    96:'Cm', 97:'Bk', 98:'Cf', 99:'Es',
}

# Lanthanide configs (4f, 5d, 6s)
LANTHANIDE_CONFIG = {
    57: (0, 1, 2), 58: (1, 1, 2), 59: (3, 0, 2), 60: (4, 0, 2),
    61: (5, 0, 2), 62: (6, 0, 2), 63: (7, 0, 2), 64: (7, 1, 2),
    65: (9, 0, 2), 66: (10, 0, 2), 67: (11, 0, 2), 68: (12, 0, 2),
    69: (13, 0, 2), 70: (14, 0, 2), 71: (14, 1, 2),
}

# 5d transition metals: (n_d, n_s) — real configs
CONFIG_5D = {
    72: (2, 2),   # Hf: [Xe]4f14 5d2 6s2
    73: (3, 2),   # Ta: [Xe]4f14 5d3 6s2
    74: (4, 2),   # W:  [Xe]4f14 5d4 6s2
    75: (5, 2),   # Re: [Xe]4f14 5d5 6s2
    76: (6, 2),   # Os: [Xe]4f14 5d6 6s2
    77: (7, 2),   # Ir: [Xe]4f14 5d7 6s2
    78: (9, 1),   # Pt: [Xe]4f14 5d9 6s1 (anomalous!)
    79: (10, 1),  # Au: [Xe]4f14 5d10 6s1 (anomalous!)
    80: (10, 2),  # Hg: [Xe]4f14 5d10 6s2
}

# Actinide configs (5f, 6d, 7s)
ACTINIDE_CONFIG = {
    89: (0, 1, 2), 90: (0, 2, 2), 91: (2, 1, 2), 92: (3, 1, 2),
    93: (4, 1, 2), 94: (6, 0, 2), 95: (7, 0, 2), 96: (7, 1, 2),
    97: (9, 0, 2), 98: (10, 0, 2), 99: (11, 0, 2),
}

# Anomalous d-block configs for 3d and 4d
REAL_CONFIG_3D4D = {
    24: (5, 1), 29: (10, 1), 41: (4, 1), 42: (5, 1),
    44: (7, 1), 45: (8, 1), 46: (10, 0), 47: (10, 1),
}

# Magnetic moments
MU_EFF = {26: 2.22, 27: 1.72, 28: 0.62}
LANTHANIDE_MU = {
    57: 0.0, 58: 2.54, 59: 3.58, 60: 3.62, 61: 2.68,
    62: 0.85, 63: 3.54, 64: 7.94, 65: 9.72, 66: 10.65,
    67: 10.61, 68: 9.58, 69: 7.56, 70: 4.54, 71: 0.0,
}
ACTINIDE_MU = {
    89: 1.55, 90: 1.63, 91: 4.57, 92: 4.68, 93: 3.80,
    94: 0.00, 95: 7.94, 96: 8.57, 97: 9.72, 98: 8.49, 99: 7.57,
}


def get_quantum_numbers(Z):
    """Get (period, n_p, n_d, n_s, n_f, block) for Z=3-99."""
    if Z in LANTHANIDE_CONFIG:
        n_f, n_d, n_s = LANTHANIDE_CONFIG[Z]
        return 6, 0, n_d, n_s, n_f, 'f'

    if Z in ACTINIDE_CONFIG:
        n_f, n_d, n_s = ACTINIDE_CONFIG[Z]
        return 7, 0, n_d, n_s, n_f, 'f'

    if Z in CONFIG_5D:
        n_d, n_s = CONFIG_5D[Z]
        return 6, 0, n_d, n_s, 0, 'd'

    # 6p block
    if 81 <= Z <= 85:
        n_p = Z - 80
        return 6, n_p, 0, 2, 0, 'p'
    if Z == 86:  # Rn
        return 6, 6, 0, 2, 0, 'ng'

    # Period 7 s-block
    if Z == 87:  # Fr
        return 7, 0, 0, 1, 0, 's'
    if Z == 88:  # Ra
        return 7, 0, 0, 2, 0, 's'

    # Standard aufbau for Z=3-56
    sub = []
    for n in range(1, 8):
        for l in range(n):
            sub.append((n, l, 2 * (2 * l + 1)))
    sub.sort(key=lambda s: (s[0] + s[1], s[0]))
    rem = Z; filled = []
    for n, l, cap in sub:
        if rem <= 0: break
        e = min(rem, cap); filled.append((n, l, e, cap)); rem -= e
    per = max(n for n, l, e, c in filled)
    n_p = sum(e for n, l, e, c in filled if n == per and l == 1)
    n_d_val = sum(e for n, l, e, c in filled if l == 2 and n == per - 1)
    n_s_val = sum(e for n, l, e, c in filled if n == per and l == 0)
    last_l = filled[-1][1]
    blk = {0: 's', 1: 'p', 2: 'd', 3: 'f'}.get(last_l, '?')
    se = {}; sm2 = {}
    for n, l, e, cap in filled:
        se[n] = se.get(n, 0) + e; sm2[n] = sm2.get(n, 0) + cap
    if se.get(per, 0) == sm2.get(per, 0):
        if Z == 2 or (last_l == 1 and filled[-1][2] == filled[-1][3]):
            blk = 'ng'
            if Z == 2: n_p = 0
    n_d = 0 if blk in ('p', 's', 'ng') else n_d_val
    n_s = n_s_val
    if Z in REAL_CONFIG_3D4D and blk == 'd':
        n_d, n_s = REAL_CONFIG_3D4D[Z]
    return per, n_p, n_d, n_s, 0, blk


def get_mu(Z):
    if Z in MU_EFF: return MU_EFF[Z]
    if Z in LANTHANIDE_MU: return LANTHANIDE_MU[Z]
    if Z in ACTINIDE_MU: return ACTINIDE_MU[Z]
    return 0.0


def theta_base(Z, per, n_p):
    """Base θ = 1 + √φ × Σ_gold + (W/6) × μ × LEAK"""
    mu = get_mu(Z)
    c_gold = math.sqrt(PHI)
    c_mag = W / 6
    sigma_gold = c_gold * n_p * (G1 / BOS) * PHI**(-(per - 1))
    sigma_magnetic = c_mag * mu * LEAK
    return 1.0 + sigma_gold + sigma_magnetic


def predict_ratio(Z):
    """Predict vdW/cov ratio with full corrections including ρ₆ gate."""
    per, n_p, n_d, n_s, n_f, blk = get_quantum_numbers(Z)

    # D-block boundary modes
    if blk == 'd':
        is_boundary = (n_d <= 4 or n_d >= 9)
        has_s = (n_s > 0)
        if is_boundary and has_s and Z not in MU_EFF:
            theta = math.sqrt((1 + LEAK)**2 - 1) / BOS
            # Gate 5a: Period-6 relativistic expansion of 5d orbitals
            if per == 6:
                theta *= RHO6
                correction = "leak ×ρ₆"
            else:
                correction = "leak"
        elif n_d >= 9 and not has_s:
            ratio_reflect = BASE + DARK_GOLD * LEAK
            theta = math.sqrt(ratio_reflect**2 - 1) / BOS
            correction = "reflect"
        else:
            theta = theta_base(Z, per, n_p)
            correction = "standard"
    else:
        theta = theta_base(Z, per, n_p)
        correction = ""

    # δ_silver corrections
    p_hole = False
    if blk not in ('d', 'f'):
        if blk == 's' and n_p == 0:
            if Z in [4, 12, 20, 38, 56, 88]:  # Added Ra
                if per == 2:
                    theta = R_C * PHI
                    correction = "s²(Be) r_c×φ"
                else:
                    theta = R_C
                    correction = "s² θ=r_c"
        elif per == 2 and n_p == 1 and blk == 'p':
            theta = theta * PHI
            correction = "per2 θ×φ"
        elif n_p == 2 and blk == 'p':
            # Gate 5b: Inert pair suppression — per≥6 skips sp³
            if per >= 6:
                correction = "inert pair"
            else:
                theta = theta * PHI**(1/3)
                correction = "sp³ θ×φ^⅓"
        elif n_p >= 4 and per >= 3 and blk == 'p':
            p_hole = True
            correction = "p-hole r×r_c"
        elif blk == 'ng' and per >= 3:
            p_hole = True
            correction = "ng p-hole"

    ratio = math.sqrt(1 + (theta * BOS)**2)
    if p_hole:
        ratio *= R_C

    return ratio, theta, correction, per, n_p, n_d, n_s, n_f, blk


# ══════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════

print("=" * 80)
print("  SUPERHEAVY EXTENSION: Z=72-88 (5d metals + 6p + period 7 s-block)")
print("  Plus full periodic table scorecard Z=3-99")
print("=" * 80)
print()

# ── Z=72-88 predictions ──
print("  NEW ELEMENTS (Z=72-88):")
print(f"  {'Z':>3} {'Sym':>3} {'Blk':>3} {'Per':>3} {'nd/np':>5} {'θ':>6}"
      f" {'Pred':>7} {'Obs':>7} {'Err':>7}  Gate")
print("  " + "─" * 72)

new_errors = []
for Z in range(72, 89):
    rc, rv = RADII[Z]
    ratio_obs = rv / rc
    ratio_pred, theta, corr, per, n_p, n_d, n_s, n_f, blk = predict_ratio(Z)
    err = (ratio_pred - ratio_obs) / ratio_obs * 100
    flag = " " if abs(err) < 10 else ("~" if abs(err) < 20 else "!")
    ndnp = n_d if blk == 'd' else n_p
    print(f"  {Z:3d} {SYMBOLS[Z]:>3} {blk:>3} {per:>3} {ndnp:>5}"
          f" {theta:6.3f} {ratio_pred:7.3f} {ratio_obs:7.3f} {err:+7.1f}%{flag} {corr}")
    new_errors.append(abs(err))

n = len(new_errors)
n10 = sum(1 for e in new_errors if e < 10)
n20 = sum(1 for e in new_errors if e < 20)
print()
print(f"  Z=72-88: {n} elements, mean={np.mean(new_errors):.1f}%,"
      f" <10%={n10}/{n}, <20%={n20}/{n}")

# ── Compare 5d with 3d and 4d ──
print()
print("=" * 80)
print("  5d vs 3d vs 4d COMPARISON (analogous positions)")
print("=" * 80)
print()
print(f"  {'n_d':>3} {'3d':>6} {'err':>6} {'4d':>6} {'err':>6} {'5d':>6} {'err':>6}")
print("  " + "─" * 45)

# Map: n_d -> (3d_Z, 4d_Z, 5d_Z)
d_map = {
    1: (21, 39, None),    # Sc, Y (no 5d1 separate element, Lu/Lr don't count)
    2: (22, 40, 72),      # Ti, Zr, Hf
    3: (23, 41, 73),      # V, Nb, Ta
    4: (24, None, 74),    # Cr(5,1), W(4,2) — different configs
    5: (25, 42, 75),      # Mn, Mo, Re
    6: (26, None, 76),    # Fe, Os
    7: (27, None, 77),    # Co, Ir
    8: (28, None, None),  # Ni
    9: (None, 78, None),  # (Pt is 9,1)
    10: (29, 47, 79),     # Cu(10,1), Ag(10,1), Au(10,1)
}

for nd in [2, 3, 5, 10]:
    z3, z4, z5 = d_map.get(nd, (None, None, None))
    row = f"  {nd:>3}"
    for z in [z3, z4, z5]:
        if z and z in RADII:
            rc, rv = RADII[z]
            rp, _, _, _, _, _, _, _, _ = predict_ratio(z)
            e = (rp - rv/rc) / (rv/rc) * 100
            row += f" {SYMBOLS[z]:>6} {e:+5.1f}%"
        else:
            row += f" {'—':>6} {'—':>6}"
    print(row)

# ── FULL PERIODIC TABLE SCORECARD ──
print()
print("=" * 80)
print("  FULL PERIODIC TABLE: Z=3-99 (97 elements)")
print("=" * 80)
print()

all_errors = []
blocks = {'s': [], 'p': [], 'd_3d': [], 'd_4d': [], 'd_5d': [],
          'f_lant': [], 'f_act': [], 'ng': []}
outliers = []

for Z in sorted(RADII.keys()):
    if Z < 3:
        continue
    rc, rv = RADII[Z]
    ratio_obs = rv / rc
    ratio_pred, theta, corr, per, n_p, n_d, n_s, n_f, blk = predict_ratio(Z)
    err = (ratio_pred - ratio_obs) / ratio_obs * 100
    aerr = abs(err)
    all_errors.append(aerr)

    if blk == 'd':
        if per == 4: blocks['d_3d'].append(aerr)
        elif per == 5: blocks['d_4d'].append(aerr)
        elif per == 6: blocks['d_5d'].append(aerr)
    elif blk == 'f':
        if Z <= 71: blocks['f_lant'].append(aerr)
        else: blocks['f_act'].append(aerr)
    else:
        blocks[blk].append(aerr)

    if aerr > 10:
        outliers.append((Z, SYMBOLS[Z], blk, per, err, corr))

n = len(all_errors)
n10 = sum(1 for e in all_errors if e < 10)
n20 = sum(1 for e in all_errors if e < 20)
print(f"  Total: {n} elements")
print(f"  Mean error:  {np.mean(all_errors):.1f}%")
print(f"  Within 10%:  {n10}/{n} ({100*n10/n:.0f}%)")
print(f"  Within 20%:  {n20}/{n} ({100*n20/n:.0f}%)")
print()

print(f"  {'Block':>12} {'N':>4} {'Mean':>7} {'<10%':>12} {'<20%':>12}")
print("  " + "─" * 52)
for name, key in [('S-block', 's'), ('P-block', 'p'),
                   ('D-3d (per4)', 'd_3d'), ('D-4d (per5)', 'd_4d'),
                   ('D-5d (per6)', 'd_5d'),
                   ('F-lanthanide', 'f_lant'), ('F-actinide', 'f_act'),
                   ('Noble gas', 'ng')]:
    be = blocks[key]
    if not be: continue
    nb = len(be)
    n10b = sum(1 for e in be if e < 10)
    n20b = sum(1 for e in be if e < 20)
    print(f"  {name:>12} {nb:>4} {np.mean(be):>7.1f}%"
          f" {n10b:>4}/{nb} ({100*n10b/nb:3.0f}%)"
          f" {n20b:>4}/{nb} ({100*n20b/nb:3.0f}%)")

if outliers:
    print()
    print(f"  Outliers (>10%):")
    for Z, sym, blk, per, err, corr in outliers:
        reliable = ""
        if Z >= 96: reliable = " [rough vdW]"
        print(f"    {sym:>3} (Z={Z:2d}, {blk}, per={per}): {err:+.1f}%  {corr}{reliable}")

# ── Excluding rough actinide data ──
print()
reliable_errors = []
for Z in sorted(RADII.keys()):
    if Z < 3: continue
    if Z in [96, 97, 98, 99]: continue  # Rough actinide vdW
    if Z in [84, 85, 87]: continue  # Very radioactive, limited data
    rc, rv = RADII[Z]
    ratio_obs = rv / rc
    ratio_pred, _, _, _, _, _, _, _, _ = predict_ratio(Z)
    err = abs((ratio_pred - ratio_obs) / ratio_obs * 100)
    reliable_errors.append(err)

n = len(reliable_errors)
n10 = sum(1 for e in reliable_errors if e < 10)
n20 = sum(1 for e in reliable_errors if e < 20)
print(f"  RELIABLE DATA ONLY (excl rough actinides + Po/At/Fr):")
print(f"  {n} elements, mean={np.mean(reliable_errors):.1f}%,"
      f" <10%={n10}/{n} ({100*n10/n:.0f}%),"
      f" <20%={n20}/{n} ({100*n20/n:.0f}%)")

print()
print("=" * 80)
print("  DONE")
print("=" * 80)
