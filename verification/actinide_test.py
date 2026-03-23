#!/usr/bin/env python3
"""
actinide_test.py — Extend the unified Pythagorean formula to actinides (Z=89-103)
==================================================================================
Thomas A. Husmann / iBuilt LTD / March 23, 2026

Tests whether the same formula that works for Z=3-71 extends to 5f elements.
Key difference from lanthanides: 5f electrons are more spatially extended than 4f,
so the magnetic-moment-only model may need refinement.

Actinide electron configs have more 6d involvement than lanthanide 5d:
  - Ac, Th: pure d-block (no 5f electrons)
  - Pa, U, Np, Cm: mixed 5f + 6d
  - Pu, Am, Bk-No: pure 5f
  - Lr: 5f14 7p1 (unique — no 6d)

Covalent radii: Cordero 2008 (Z=89-96), Pyykko 2009 (Z=97-103)
vdW radii: Alvarez 2013 (reliable for Th, U, Np, Pu, Am; rough for others)
Magnetic moments: g_J√(J(J+1)) from Hund's rules ground state terms

© 2026 Thomas A. Husmann / iBuilt LTD. All rights reserved.
"""

import numpy as np
import math

# ══════════════════════════════════════════════════════════════════════
# FRAMEWORK CONSTANTS (same as delta_silver_complete.py)
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

print(f"BASE={BASE:.6f}  BOS={BOS:.6f}  G1={G1:.6f}")
print(f"W/6={W/6:.6f}  LEAK={LEAK:.6f}  R_C={R_C:.6f}")
print()

# ══════════════════════════════════════════════════════════════════════
# FULL ELEMENT DATABASE: Z=3-71 (from delta_silver_complete.py)
# + Z=89-103 actinides
# ══════════════════════════════════════════════════════════════════════

# (covalent_pm, vdw_pm)
RADII = {
    # Z=3-71: same as before
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
    57:(207,298), 58:(204,288), 59:(203,292), 60:(201,295), 61:(199,291),
    62:(198,290), 63:(198,287), 64:(196,283), 65:(194,279), 66:(192,287),
    67:(192,281), 68:(189,283), 69:(190,279), 70:(187,280), 71:(187,274),
    # Actinides: Cordero 2008 (Z=89-96) / Pyykko 2009 (Z=97-103)
    # vdW from Alvarez 2013
    89:(215,280),   # Ac — vdW rough estimate
    90:(206,293),   # Th — vdW reliable
    91:(200,288),   # Pa — vdW rough estimate
    92:(196,271),   # U  — vdW reliable
    93:(190,282),   # Np — vdW reliable
    94:(187,281),   # Pu — vdW reliable
    95:(180,283),   # Am — vdW reliable
    96:(169,305),   # Cm — vdW rough estimate
    # Bk-Es: Pyykko covalent, Alvarez vdW (rough/anomalous)
    97:(168,340),   # Bk — vdW anomalous (single structure), likely too large
    98:(168,305),   # Cf — vdW rough estimate
    99:(165,270),   # Es — vdW rough estimate
    # Fm-Lr: no vdW data, skip
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

# Actinide configs (5f, 6d, 7s)
ACTINIDE_CONFIG = {
    89: (0, 1, 2),   # Ac: [Rn] 6d1 7s2
    90: (0, 2, 2),   # Th: [Rn] 6d2 7s2
    91: (2, 1, 2),   # Pa: [Rn] 5f2 6d1 7s2
    92: (3, 1, 2),   # U:  [Rn] 5f3 6d1 7s2
    93: (4, 1, 2),   # Np: [Rn] 5f4 6d1 7s2
    94: (6, 0, 2),   # Pu: [Rn] 5f6 7s2
    95: (7, 0, 2),   # Am: [Rn] 5f7 7s2
    96: (7, 1, 2),   # Cm: [Rn] 5f7 6d1 7s2
    97: (9, 0, 2),   # Bk: [Rn] 5f9 7s2
    98: (10, 0, 2),  # Cf: [Rn] 5f10 7s2
    99: (11, 0, 2),  # Es: [Rn] 5f11 7s2
}

# Anomalous d-block configs (Z=1-56)
REAL_CONFIG = {
    24: (5, 1), 29: (10, 1), 41: (4, 1), 42: (5, 1),
    44: (7, 1), 45: (8, 1), 46: (10, 0), 47: (10, 1),
}

# Magnetic moments: d-block (Z=26-28)
MU_D = {26: 2.22, 27: 1.72, 28: 0.62}

# Lanthanide effective moments (g_J√(J(J+1)))
LANTHANIDE_MU = {
    57: 0.0, 58: 2.54, 59: 3.58, 60: 3.62, 61: 2.68,
    62: 0.85, 63: 3.54, 64: 7.94, 65: 9.72, 66: 10.65,
    67: 10.61, 68: 9.58, 69: 7.56, 70: 4.54, 71: 0.0,
}

# Actinide effective moments (g_J√(J(J+1)) from Hund's rules)
# Note: LS coupling breaks down for early actinides (Pa, U, Np)
ACTINIDE_MU = {
    89: 1.55,   # Ac: 2D_3/2
    90: 1.63,   # Th: 3F_2
    91: 4.57,   # Pa: 4K_11/2 (intermediate coupling)
    92: 4.68,   # U:  5L_6 (intermediate coupling)
    93: 3.80,   # Np: 6L_11/2 (intermediate coupling)
    94: 0.00,   # Pu: 7F_0 (J=0, Van Vleck paramagnet)
    95: 7.94,   # Am: 8S_7/2 (half-filled, like Gd)
    96: 8.57,   # Cm: 9D_2
    97: 9.72,   # Bk: 6H_15/2
    98: 8.49,   # Cf: 5I_8
    99: 7.57,   # Es: 4I_15/2
}


def get_quantum_numbers(Z):
    """Get (period, n_p, n_d, n_s, n_f, block) for Z=3-99."""
    if Z in LANTHANIDE_CONFIG:
        n_f, n_d, n_s = LANTHANIDE_CONFIG[Z]
        return 6, 0, n_d, n_s, n_f, 'f'

    if Z in ACTINIDE_CONFIG:
        n_f, n_d, n_s = ACTINIDE_CONFIG[Z]
        return 7, 0, n_d, n_s, n_f, 'f'

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
        if (last_l == 1 and filled[-1][2] == filled[-1][3]):
            blk = 'ng'
    n_d = 0 if blk in ('p', 's', 'ng') else n_d_val
    n_s = n_s_val
    if Z in REAL_CONFIG and blk == 'd':
        n_d, n_s = REAL_CONFIG[Z]
    return per, n_p, n_d, n_s, 0, blk


def get_mu(Z):
    """Get effective magnetic moment for any element."""
    if Z in MU_D:
        return MU_D[Z]
    if Z in LANTHANIDE_MU:
        return LANTHANIDE_MU[Z]
    if Z in ACTINIDE_MU:
        return ACTINIDE_MU[Z]
    return 0.0


def theta_base(Z, per, n_p, n_d, n_s, n_f, blk):
    """Base θ formula: θ = 1 + √φ × Σ_gold + (W/6) × μ_eff × LEAK"""
    mu = get_mu(Z)
    c_gold = math.sqrt(PHI)
    c_mag = W / 6

    sigma_gold = c_gold * n_p * (G1 / BOS) * PHI**(-(per - 1))
    sigma_magnetic = c_mag * mu * LEAK

    return 1.0 + sigma_gold + sigma_magnetic


def predict_ratio(Z):
    """Predict vdW/cov ratio with full δ_silver corrections."""
    per, n_p, n_d, n_s, n_f, blk = get_quantum_numbers(Z)

    # D-block boundary modes
    if blk == 'd':
        is_boundary = (n_d <= 4 or n_d >= 9)
        has_s = (n_s > 0)
        if is_boundary and has_s and Z not in MU_D:
            theta_leak = math.sqrt((1 + LEAK)**2 - 1) / BOS
            theta = theta_leak
        elif n_d >= 9 and not has_s:
            ratio_reflect = BASE + DARK_GOLD * LEAK
            theta_reflect = math.sqrt(ratio_reflect**2 - 1) / BOS
            theta = theta_reflect
        else:
            theta = theta_base(Z, per, n_p, n_d, n_s, n_f, blk)
    else:
        theta = theta_base(Z, per, n_p, n_d, n_s, n_f, blk)

    # δ_silver corrections (only for silver-vertex: n_d = n_f = 0)
    correction = ""
    p_hole = False
    if blk not in ('d', 'f'):
        if blk == 's' and n_p == 0:
            if Z in [4, 12, 20, 38, 56]:
                if per == 2:
                    theta = R_C * PHI
                    correction = "s²(Be) θ=r_c×φ"
                else:
                    theta = R_C
                    correction = "s² θ=r_c"
        elif per == 2 and n_p == 1 and blk == 'p':
            theta = theta * PHI
            correction = "per2 overflow θ×φ"
        elif n_p == 2 and blk == 'p':
            theta = theta * PHI**(1/3)
            correction = "sp³ θ×φ^(1/3)"
        elif n_p >= 4 and per >= 3 and blk == 'p':
            p_hole = True
            correction = "p-hole ratio×r_c"
        elif blk == 'ng' and per >= 3:
            p_hole = True
            correction = "ng p-hole ratio×r_c"

    ratio = math.sqrt(1 + (theta * BOS)**2)

    if p_hole:
        ratio *= R_C

    return ratio, theta, correction


# ══════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════

print("=" * 80)
print("  ACTINIDE EXTENSION TEST")
print("  Same formula as lanthanides: θ = 1 + √φ × Σ_gold + (W/6) × μ_eff × LEAK")
print("  Question: does it work for 5f electrons (more extended than 4f)?")
print("=" * 80)
print()

# ── Show actinide observed ratios ──
print("  Actinide observed data:")
print(f"  {'Z':>3} {'Sym':>3} {'n_f':>3} {'n_d':>3} {'μ_eff':>6} {'r_cov':>5} {'r_vdw':>5}"
      f" {'Ratio':>6} {'Source':>8}")
print("  " + "─" * 55)
for Z in range(89, 100):
    rc, rv = RADII[Z]
    nf, nd, ns = ACTINIDE_CONFIG[Z]
    mu = ACTINIDE_MU[Z]
    reliable = Z in [90, 92, 93, 94, 95]
    src = "Alvarez" if reliable else "rough"
    print(f"  {Z:3d} {SYMBOLS[Z]:>3} {nf:>3d} {nd:>3d} {mu:6.2f} {rc:5d} {rv:5d}"
          f" {rv/rc:6.3f} {src:>8}")

# Compare lanthanide and actinide ratio ranges
lant_ratios = [RADII[Z][1]/RADII[Z][0] for Z in range(57, 72)]
act_ratios = [RADII[Z][1]/RADII[Z][0] for Z in range(89, 100)]
print()
print(f"  Lanthanide ratios: [{min(lant_ratios):.3f}, {max(lant_ratios):.3f}], mean={np.mean(lant_ratios):.3f}")
print(f"  Actinide ratios:   [{min(act_ratios):.3f}, {max(act_ratios):.3f}], mean={np.mean(act_ratios):.3f}")

# ── Run predictions on actinides ──
print()
print("=" * 80)
print("  ACTINIDE PREDICTIONS")
print("=" * 80)
print()
print(f"  {'Z':>3} {'Sym':>3} {'n_f':>3} {'n_d':>3} {'μ':>6} {'θ':>6}"
      f" {'Pred':>7} {'Obs':>7} {'Err':>7} {'Src':>6}")
print("  " + "─" * 65)

act_errors = []
act_reliable_errors = []

for Z in range(89, 100):
    rc, rv = RADII[Z]
    ratio_obs = rv / rc
    ratio_pred, theta, corr = predict_ratio(Z)
    err = (ratio_pred - ratio_obs) / ratio_obs * 100
    nf, nd, ns = ACTINIDE_CONFIG[Z]
    mu = ACTINIDE_MU[Z]
    reliable = Z in [90, 92, 93, 94, 95]
    flag = " " if abs(err) < 10 else ("~" if abs(err) < 20 else "!")
    src = "rel" if reliable else "rough"
    print(f"  {Z:3d} {SYMBOLS[Z]:>3} {nf:>3d} {nd:>3d} {mu:6.2f} {theta:6.3f}"
          f" {ratio_pred:7.3f} {ratio_obs:7.3f} {err:+7.1f}%{flag} {src:>6}")
    act_errors.append(abs(err))
    if reliable:
        act_reliable_errors.append(abs(err))

print()
print(f"  All actinides (11): mean={np.mean(act_errors):.1f}%,"
      f" <10%={sum(1 for e in act_errors if e<10)}/11,"
      f" <20%={sum(1 for e in act_errors if e<20)}/11")
print(f"  Reliable only (5):  mean={np.mean(act_reliable_errors):.1f}%,"
      f" <10%={sum(1 for e in act_reliable_errors if e<10)}/5,"
      f" <20%={sum(1 for e in act_reliable_errors if e<20)}/5")

# ── Compare lanthanide performance ──
print()
print("=" * 80)
print("  COMPARISON: LANTHANIDES vs ACTINIDES")
print("=" * 80)
print()
print(f"  {'Z':>3} {'Sym':>3} {'n_f':>3} {'n_d':>3} {'μ':>6} {'θ':>6}"
      f" {'Pred':>7} {'Obs':>7} {'Err':>7}")
print("  " + "─" * 55)

lant_errors = []
for Z in range(57, 72):
    rc, rv = RADII[Z]
    ratio_obs = rv / rc
    ratio_pred, theta, corr = predict_ratio(Z)
    err = (ratio_pred - ratio_obs) / ratio_obs * 100
    nf, nd, ns = LANTHANIDE_CONFIG[Z]
    mu = LANTHANIDE_MU[Z]
    flag = " " if abs(err) < 10 else ("~" if abs(err) < 20 else "!")
    print(f"  {Z:3d} {SYMBOLS[Z]:>3} {nf:>3d} {nd:>3d} {mu:6.2f} {theta:6.3f}"
          f" {ratio_pred:7.3f} {ratio_obs:7.3f} {err:+7.1f}%{flag}")
    lant_errors.append(abs(err))

print()
print(f"  Lanthanides (15): mean={np.mean(lant_errors):.1f}%,"
      f" <10%={sum(1 for e in lant_errors if e<10)}/15")
print(f"  Actinides (11):   mean={np.mean(act_errors):.1f}%,"
      f" <10%={sum(1 for e in act_errors if e<10)}/11")

# ── Full periodic table summary ──
print()
print("=" * 80)
print("  FULL PERIODIC TABLE SUMMARY (Z=3-99)")
print("=" * 80)
print()

all_errors = []
blocks = {'s': [], 'p': [], 'd': [], 'f_lant': [], 'f_act': [], 'ng': []}

for Z in sorted(RADII.keys()):
    if Z < 3:
        continue
    rc, rv = RADII[Z]
    ratio_obs = rv / rc
    ratio_pred, theta, corr = predict_ratio(Z)
    err = abs((ratio_pred - ratio_obs) / ratio_obs * 100)
    all_errors.append(err)
    per, n_p, n_d, n_s, n_f, blk = get_quantum_numbers(Z)
    if blk == 'f':
        if Z >= 89:
            blocks['f_act'].append(err)
        else:
            blocks['f_lant'].append(err)
    else:
        blocks[blk].append(err)

n = len(all_errors)
n10 = sum(1 for e in all_errors if e < 10)
n20 = sum(1 for e in all_errors if e < 20)
print(f"  Total: {n} elements, mean={np.mean(all_errors):.1f}%,"
      f" <10%={n10}/{n} ({100*n10/n:.0f}%), <20%={n20}/{n} ({100*n20/n:.0f}%)")
print()
print(f"  {'Block':>12} {'N':>4} {'Mean':>7} {'<10%':>10}")
print("  " + "─" * 40)
for name, key in [('S-block', 's'), ('P-block', 'p'), ('D-block', 'd'),
                   ('F-lant', 'f_lant'), ('F-act', 'f_act'), ('Noble', 'ng')]:
    be = blocks[key]
    if not be:
        continue
    nb = len(be)
    n10b = sum(1 for e in be if e < 10)
    print(f"  {name:>12} {nb:>4} {np.mean(be):>7.1f}% {n10b:>4}/{nb} ({100*n10b/nb:.0f}%)")

# ── Key question: does the model need refinement for actinides? ──
print()
print("=" * 80)
print("  ANALYSIS: Does 5f delocalization break the model?")
print("=" * 80)
print()

# Check if actinides with n_d > 0 behave differently from those with n_d = 0
act_with_d = [(Z, abs((predict_ratio(Z)[0] - RADII[Z][1]/RADII[Z][0]) / (RADII[Z][1]/RADII[Z][0]) * 100))
              for Z in [89, 90, 91, 92, 93, 96] if Z in RADII]
act_no_d = [(Z, abs((predict_ratio(Z)[0] - RADII[Z][1]/RADII[Z][0]) / (RADII[Z][1]/RADII[Z][0]) * 100))
            for Z in [94, 95, 97, 98, 99] if Z in RADII]

print(f"  Actinides with 6d electrons (Ac,Th,Pa,U,Np,Cm):")
for Z, e in act_with_d:
    print(f"    {SYMBOLS[Z]:>3}: {e:.1f}%")
print(f"    Mean: {np.mean([e for _,e in act_with_d]):.1f}%")
print()
print(f"  Actinides without 6d (Pu,Am,Bk,Cf,Es):")
for Z, e in act_no_d:
    print(f"    {SYMBOLS[Z]:>3}: {e:.1f}%")
print(f"    Mean: {np.mean([e for _,e in act_no_d]):.1f}%")

print()
print("=" * 80)
print("  DONE")
print("=" * 80)
