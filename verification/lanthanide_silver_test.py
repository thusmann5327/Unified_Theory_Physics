#!/usr/bin/env python3
"""
lanthanide_silver_test.py — Can lanthanides constrain the silver coefficient?
=============================================================================
Thomas A. Husmann / iBuilt LTD / March 23, 2026

The original bigollo_solver.py stops at Z=56. Only 9 elements are sensitive
to c_silver (mid-series d-block). Adding 15 lanthanides (Z=57-71) with
f-electrons AND d-electrons should dramatically constrain c_silver.

The lanthanide θ formula extends the unified formula:

  θ(Z) = 1 + √φ × Σ_gold - Σ_silver - Σ_f + Σ_magnetic

  Σ_f = c_f × (n_f/14) × dark_silver × LEAK

The f-electrons contribute confinement along the silver axis (like d-electrons)
but through one more recursion level (φ^-1 deeper).

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

# Build AAH spectrum
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

DARK_SILVER = 0.83
DARK_GOLD = 0.29

print(f"BASE={BASE:.6f}  BOS={BOS:.6f}  G1={G1:.6f}")
print()

# ══════════════════════════════════════════════════════════════════════
# ELEMENT DATABASE: Z=1-71 (now including lanthanides)
# ══════════════════════════════════════════════════════════════════════

# (covalent_pm, vdw_pm) — Cordero 2008 + Alvarez 2013
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
    # Lanthanides (Cordero 2008 / Alvarez 2013)
    57:(207,298),  # La
    58:(204,288),  # Ce
    59:(203,292),  # Pr
    60:(201,295),  # Nd
    61:(199,291),  # Pm (vdW interpolated)
    62:(198,290),  # Sm
    63:(198,287),  # Eu
    64:(196,283),  # Gd
    65:(194,279),  # Tb
    66:(192,287),  # Dy
    67:(192,281),  # Ho
    68:(189,283),  # Er
    69:(190,279),  # Tm
    70:(187,280),  # Yb
    71:(187,274),  # Lu
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
    57:'La', 58:'Ce', 59:'Pr', 60:'Nd', 61:'Pm', 62:'Sm',
    63:'Eu', 64:'Gd', 65:'Tb', 66:'Dy', 67:'Ho', 68:'Er',
    69:'Tm', 70:'Yb', 71:'Lu',
}

# Real electron configs: [Xe] 4f^n 5d^m 6s^2
# Most lanthanides: [Xe] 4f^n 6s^2 (n_d=0)
# Exceptions: La (5d1), Ce (4f1 5d1), Gd (4f7 5d1), Lu (4f14 5d1)
LANTHANIDE_CONFIG = {
    # Z: (n_f, n_d, n_s)  — 4f, 5d, 6s electrons
    57: (0, 1, 2),   # La: [Xe] 5d1 6s2
    58: (1, 1, 2),   # Ce: [Xe] 4f1 5d1 6s2
    59: (3, 0, 2),   # Pr: [Xe] 4f3 6s2
    60: (4, 0, 2),   # Nd: [Xe] 4f4 6s2
    61: (5, 0, 2),   # Pm: [Xe] 4f5 6s2
    62: (6, 0, 2),   # Sm: [Xe] 4f6 6s2
    63: (7, 0, 2),   # Eu: [Xe] 4f7 6s2
    64: (7, 1, 2),   # Gd: [Xe] 4f7 5d1 6s2
    65: (9, 0, 2),   # Tb: [Xe] 4f9 6s2
    66: (10, 0, 2),  # Dy: [Xe] 4f10 6s2
    67: (11, 0, 2),  # Ho: [Xe] 4f11 6s2
    68: (12, 0, 2),  # Er: [Xe] 4f12 6s2
    69: (13, 0, 2),  # Tm: [Xe] 4f13 6s2
    70: (14, 0, 2),  # Yb: [Xe] 4f14 6s2
    71: (14, 1, 2),  # Lu: [Xe] 4f14 5d1 6s2
}

# Anomalous d-block configs (Z=1-56)
REAL_CONFIG = {
    24: (5, 1), 29: (10, 1), 41: (4, 1), 42: (5, 1),
    44: (7, 1), 45: (8, 1), 46: (10, 0), 47: (10, 1),
}

MU_EFF = {26: 2.22, 27: 1.72, 28: 0.62}

# Lanthanide effective moments (free ion, μ_eff = g√(J(J+1)))
LANTHANIDE_MU = {
    57: 0.0,    # La: no f electrons
    58: 2.54,   # Ce
    59: 3.58,   # Pr
    60: 3.62,   # Nd
    61: 2.68,   # Pm
    62: 0.85,   # Sm (anomalous)
    63: 3.54,   # Eu (anomalous J=0 ground, but effective ~3.5)
    64: 7.94,   # Gd — highest, half-filled 4f7
    65: 9.72,   # Tb
    66: 10.65,  # Dy — highest μ_eff of all elements
    67: 10.61,  # Ho
    68: 9.58,   # Er
    69: 7.56,   # Tm
    70: 4.54,   # Yb
    71: 0.0,    # Lu: filled 4f14
}


def get_quantum_numbers(Z):
    """Get (period, n_p, n_d, n_s, n_f, block) for any element Z=1-71."""
    if Z in LANTHANIDE_CONFIG:
        n_f, n_d, n_s = LANTHANIDE_CONFIG[Z]
        return 6, 0, n_d, n_s, n_f, 'f'

    # Standard aufbau for Z=1-56
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
    if Z in REAL_CONFIG and blk == 'd':
        n_d, n_s = REAL_CONFIG[Z]
    return per, n_p, n_d, n_s, 0, blk


def theta_extended(Z, per, n_p, n_d, n_s, n_f, blk, c_gold, c_silver, c_f, c_mag):
    """Extended θ formula including f-electron contribution."""
    mu = MU_EFF.get(Z, 0.0)
    if Z in LANTHANIDE_MU:
        mu = LANTHANIDE_MU[Z]

    OBLATE = math.sqrt(PHI)

    # Gold (momentum): p-electrons
    sigma_gold = c_gold * n_p * (G1 / BOS) * PHI**(-(per - 1))

    # Silver (confinement): d-electrons
    sigma_silver = c_silver * (n_d / 10.0) * DARK_GOLD

    # F-block (deep confinement): f-electrons, one recursion deeper
    sigma_f = c_f * (n_f / 14.0) * DARK_SILVER * LEAK

    # Magnetic exchange
    sigma_magnetic = c_mag * mu * LEAK

    theta = 1.0 + sigma_gold - sigma_silver - sigma_f + sigma_magnetic

    return theta


def predict_ratio(Z, c_gold, c_silver, c_f, c_mag):
    """Predict vdW/cov ratio for element Z."""
    per, n_p, n_d, n_s, n_f, blk = get_quantum_numbers(Z)

    # D-block boundary modes (same as original)
    if blk == 'd':
        is_boundary = (n_d <= 4 or n_d >= 9)
        has_s = (n_s > 0)
        if is_boundary and has_s and Z not in MU_EFF:
            theta_leak = math.sqrt((1 + LEAK)**2 - 1) / BOS
            theta = theta_leak
        elif n_d >= 9 and not has_s:
            ratio_reflect = BASE + DARK_GOLD * LEAK
            theta_reflect = math.sqrt(ratio_reflect**2 - 1) / BOS
            theta = theta_reflect
        else:
            theta = theta_extended(Z, per, n_p, n_d, n_s, n_f, blk,
                                   c_gold, c_silver, c_f, c_mag)
    else:
        theta = theta_extended(Z, per, n_p, n_d, n_s, n_f, blk,
                               c_gold, c_silver, c_f, c_mag)

    ratio = math.sqrt(1 + (theta * BOS)**2)

    # Corrections
    if blk == 'p' and n_p >= 4 and per >= 3:
        ratio *= R_C
    if Z == 2:
        ratio *= (1 + BREATHING)

    return ratio, theta


def evaluate(c_gold, c_silver, c_f, c_mag, show=False):
    """Evaluate model across all elements."""
    errors = []
    results = []
    for Z in sorted(RADII.keys()):
        rc, rv = RADII[Z]
        ratio_obs = rv / rc
        ratio_pred, theta = predict_ratio(Z, c_gold, c_silver, c_f, c_mag)
        err = (ratio_pred - ratio_obs) / ratio_obs * 100
        per, n_p, n_d, n_s, n_f, blk = get_quantum_numbers(Z)
        errors.append(abs(err))
        results.append((Z, SYMBOLS[Z], blk, n_d, n_f, theta,
                        ratio_pred, ratio_obs, err))

    if show:
        print(f"  {'Z':>3} {'Sym':>3} {'Blk':>3} {'nd':>2} {'nf':>2}"
              f" {'θ':>6} {'Pred':>7} {'Obs':>7} {'Err':>7}")
        print("  " + "─" * 55)
        for Z, sym, blk, nd, nf, th, rp, ro, err in results:
            flag = " " if abs(err) < 10 else ("~" if abs(err) < 20 else "!")
            print(f"  {Z:3d} {sym:>3} {blk:>3} {nd:>2d} {nf:>2d}"
                  f" {th:6.3f} {rp:7.3f} {ro:7.3f} {err:+7.1f}%{flag}")

    ae = np.array(errors)
    return np.mean(ae), ae


# ══════════════════════════════════════════════════════════════════════
# MAIN: Grid search for optimal coefficients with lanthanides
# ══════════════════════════════════════════════════════════════════════

print("=" * 70)
print("  LANTHANIDE SILVER COEFFICIENT TEST")
print("  71 elements (Z=1-71), c_gold fixed at √φ")
print("=" * 70)
print()

# First: show lanthanide observed ratios
print("  Lanthanide vdW/cov ratios:")
print(f"  {'Z':>3} {'Sym':>3} {'n_f':>3} {'n_d':>3} {'r_cov':>5} {'r_vdw':>5} {'Ratio':>6}")
print("  " + "─" * 35)
for Z in range(57, 72):
    rc, rv = RADII[Z]
    nf, nd, ns = LANTHANIDE_CONFIG[Z]
    print(f"  {Z:3d} {SYMBOLS[Z]:>3} {nf:>3d} {nd:>3d} {rc:5d} {rv:5d} {rv/rc:6.3f}")

ratios = [RADII[Z][1]/RADII[Z][0] for Z in range(57, 72)]
print(f"\n  Range: [{min(ratios):.3f}, {max(ratios):.3f}]")
print(f"  Mean:  {np.mean(ratios):.3f}")
print(f"  Std:   {np.std(ratios):.3f}")

# Grid search
print()
print("=" * 70)
print("  GRID SEARCH: c_gold=√φ, scan c_silver, c_f, c_mag")
print("=" * 70)
print()

cg = math.sqrt(PHI)
best_loss = 999
best_cs = 0
best_cf = 0
best_cm = 0

# Coarse grid
for cs_int in range(0, 300, 5):
    cs = cs_int / 100.0
    for cf_int in range(0, 300, 5):
        cf = cf_int / 100.0
        for cm_int in range(0, 200, 5):
            cm = cm_int / 100.0
            l, _ = evaluate(cg, cs, cf, cm)
            if l < best_loss:
                best_loss = l
                best_cs = cs
                best_cf = cf
                best_cm = cm

print(f"  Coarse: c_s={best_cs:.2f}  c_f={best_cf:.2f}  c_m={best_cm:.2f}  loss={best_loss:.2f}%")

# Fine grid around best
for cs_int in range(max(0, int(best_cs*100)-20), int(best_cs*100)+20):
    cs = cs_int / 100.0
    for cf_int in range(max(0, int(best_cf*100)-20), int(best_cf*100)+20):
        cf = cf_int / 100.0
        for cm_int in range(max(0, int(best_cm*100)-20), int(best_cm*100)+20):
            cm = cm_int / 100.0
            l, _ = evaluate(cg, cs, cf, cm)
            if l < best_loss:
                best_loss = l
                best_cs = cs
                best_cf = cf
                best_cm = cm

print(f"  Fine:   c_s={best_cs:.3f}  c_f={best_cf:.3f}  c_m={best_cm:.3f}  loss={best_loss:.3f}%")

# Ultra-fine
for cs_int in range(max(0, int(best_cs*1000)-10), int(best_cs*1000)+10):
    cs = cs_int / 1000.0
    for cf_int in range(max(0, int(best_cf*1000)-10), int(best_cf*1000)+10):
        cf = cf_int / 1000.0
        for cm_int in range(max(0, int(best_cm*1000)-10), int(best_cm*1000)+10):
            cm = cm_int / 1000.0
            l, _ = evaluate(cg, cs, cf, cm)
            if l < best_loss:
                best_loss = l
                best_cs = cs
                best_cf = cf
                best_cm = cm

print(f"  Ultra:  c_s={best_cs:.4f}  c_f={best_cf:.4f}  c_m={best_cm:.4f}  loss={best_loss:.4f}%")

# Show full results with best coefficients
print()
print("=" * 70)
print(f"  BEST MODEL: c_gold=√φ  c_silver={best_cs:.4f}  c_f={best_cf:.4f}  c_mag={best_cm:.4f}")
print("=" * 70)
print()

mean_err, all_errs = evaluate(cg, best_cs, best_cf, best_cm, show=True)

n = len(all_errs)
n10 = sum(1 for e in all_errs if e < 10)
n20 = sum(1 for e in all_errs if e < 20)
print(f"\n  Score: {n} elements, mean={mean_err:.1f}%, <10%={n10}/{n}, <20%={n20}/{n}")

# Also show framework baseline (all coefficients = 1)
print()
mean_fw, _ = evaluate(cg, 1.0, 1.0, 1.0)
print(f"  Framework baseline (all c=1): mean={mean_fw:.1f}%")

# ══════════════════════════════════════════════════════════════════════
# RELATIONSHIP ANALYSIS
# ══════════════════════════════════════════════════════════════════════

print()
print("=" * 70)
print("  COEFFICIENT RELATIONSHIPS")
print("=" * 70)
print()

cs = best_cs
cf = best_cf
cm = best_cm

print(f"  c_gold    = √φ     = {cg:.6f}")
print(f"  c_silver  =          {cs:.6f}")
print(f"  c_f       =          {cf:.6f}")
print(f"  c_magnetic=          {cm:.6f}")
print()

# Check against framework constants
targets = {
    'φ': PHI, '1/φ': 1/PHI, '√φ': math.sqrt(PHI), '1/√φ': 1/math.sqrt(PHI),
    'φ²': PHI**2, '1/φ²': 1/PHI**2, '√5': math.sqrt(5), '√2': math.sqrt(2),
    '2': 2.0, '1': 1.0, '0': 0.0,
    'W': W, '1-W': 1-W, 'H': PHI**(-1/PHI),
    '√(1-W²)': math.sqrt(1-W**2), 'r_c': R_C,
    'LEAK': LEAK, '√LEAK': math.sqrt(LEAK),
    'dark_S': DARK_SILVER, 'dark_G': DARK_GOLD,
    '5/8': 5/8, '8/13': 8/13, '5/13': 5/13,
}

for coeff_name, coeff_val in [('c_silver', cs), ('c_f', cf), ('c_magnetic', cm)]:
    best = sorted(targets.items(), key=lambda kv: abs(kv[1]-coeff_val))[:3]
    print(f"  {coeff_name} = {coeff_val:.4f}:")
    for name, val in best:
        err = abs(val - coeff_val) / max(abs(coeff_val), 1e-10) * 100
        print(f"    ≈ {name:>10} = {val:.6f}  ({err:.2f}%)")
    print()

# Gold-Silver relationship
print(f"  ── Gold × Silver relationship ──")
if cs > 1e-10:
    pairs = [('g+s', cg+cs), ('g×s', cg*cs), ('g/s', cg/cs),
             ('g²+s²', cg**2+cs**2), ('g²-s²', cg**2-cs**2)]
    for label, val in pairs:
        print(f"  {label:>8} = {val:.6f}")
        best_match = min(targets.items(), key=lambda kv: abs(kv[1]-val))
        err = abs(best_match[1]-val)/max(abs(val),1e-10)*100
        mark = ' ◀◀◀' if err < 0.5 else (' ◀◀' if err < 1 else (' ◀' if err < 3 else ''))
        print(f"           ≈ {best_match[0]:>10} = {best_match[1]:.6f} ({err:.2f}%){mark}")
else:
    print(f"  c_silver = 0 → SILVER TERM ELIMINATED BY OPTIMIZER")
    print(f"  The model prefers NO silver contribution.")
    print(f"  Only c_gold = √φ and c_magnetic = {cm:.4f} are active.")
    print()
    print(f"  ── Interpretation ──")
    print(f"  c_magnetic = {cm:.4f}")
    print(f"    LEAK/2    = {0.145898/2:.4f}  ({abs(cm - 0.145898/2)/cm*100:.1f}%)")
    print(f"    W/6       = {0.4671/6:.4f}  ({abs(cm - 0.4671/6)/cm*100:.1f}%)")
    print(f"    1/(2δ₇)   = {1/(2*7.140):.4f}  ({abs(cm - 1/(2*7.140))/cm*100:.1f}%)")
    print(f"    σ₃        = {0.0728:.4f}  ({abs(cm - 0.0728)/cm*100:.1f}%)")

# Gold-F relationship
print()
if cf > 1e-10:
    print(f"  ── Gold × F relationship ──")
    for label, val in [('g+f', cg+cf), ('g×f', cg*cf), ('g/f', cg/cf),
                        ('g²+f²', cg**2+cf**2), ('g²-f²', cg**2-cf**2)]:
        best_match = min(targets.items(), key=lambda kv: abs(kv[1]-val))
        err = abs(best_match[1]-val)/max(abs(val),1e-10)*100
        mark = ' ◀◀◀' if err < 0.5 else (' ◀◀' if err < 1 else (' ◀' if err < 3 else ''))
        print(f"    {label:>8} = {val:.6f} ≈ {best_match[0]:>10} = {best_match[1]:.6f} ({err:.2f}%){mark}")
else:
    print(f"  c_f = 0 → F-ELECTRON TERM ALSO ELIMINATED")
    print(f"  Lanthanide ratios are predicted by magnetic moments alone.")

print()
print("=" * 70)
print("  DONE")
print("=" * 70)
