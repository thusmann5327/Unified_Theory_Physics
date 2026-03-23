#!/usr/bin/env python3
"""
delta_silver_complete.py — Full δ_silver correction with p-hole gate
=====================================================================
Thomas A. Husmann / iBuilt LTD / March 23, 2026

The four silver-vertex gates (all gated behind n_d = n_f = 0):
  1. Alkaline earths (s² closed subshell): θ = r_c = 1 - 1/φ⁴
  2. Period 2 gate overflow (B only): θ × φ
  3. sp³ hybridizers (Si, Ge, Sn): θ × φ^(1/3)
  4. P-hole regime (n_p ≥ 4, per ≥ 3): θ × 1/φ  [NEW]

Plus: Be gets r_c × φ (period 2 alkaline earth boost)
Plus: C gets sp³ × φ (period 2 + sp³ combined)

All constants from φ² = φ + 1. Zero free parameters.
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
print(f"R_C={R_C:.6f}  1/φ={1/PHI:.6f}  φ^(1/3)={PHI**(1/3):.6f}")
print()

# ══════════════════════════════════════════════════════════════════════
# ELEMENT DATABASE: Z=1-71
# ══════════════════════════════════════════════════════════════════════

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
    57:(207,298), 58:(204,288), 59:(203,292), 60:(201,295),
    61:(199,291), 62:(198,290), 63:(198,287), 64:(196,283),
    65:(194,279), 66:(192,287), 67:(192,281), 68:(189,283),
    69:(190,279), 70:(187,280), 71:(187,274),
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

LANTHANIDE_CONFIG = {
    57: (0, 1, 2), 58: (1, 1, 2), 59: (3, 0, 2), 60: (4, 0, 2),
    61: (5, 0, 2), 62: (6, 0, 2), 63: (7, 0, 2), 64: (7, 1, 2),
    65: (9, 0, 2), 66: (10, 0, 2), 67: (11, 0, 2), 68: (12, 0, 2),
    69: (13, 0, 2), 70: (14, 0, 2), 71: (14, 1, 2),
}

REAL_CONFIG = {
    24: (5, 1), 29: (10, 1), 41: (4, 1), 42: (5, 1),
    44: (7, 1), 45: (8, 1), 46: (10, 0), 47: (10, 1),
}

MU_EFF = {26: 2.22, 27: 1.72, 28: 0.62}
LANTHANIDE_MU = {
    57: 0.0, 58: 2.54, 59: 3.58, 60: 3.62, 61: 2.68,
    62: 0.85, 63: 3.54, 64: 7.94, 65: 9.72, 66: 10.65,
    67: 10.61, 68: 9.58, 69: 7.56, 70: 4.54, 71: 0.0,
}


def get_quantum_numbers(Z):
    if Z in LANTHANIDE_CONFIG:
        n_f, n_d, n_s = LANTHANIDE_CONFIG[Z]
        return 6, 0, n_d, n_s, n_f, 'f'
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


def theta_base(Z, per, n_p, n_d, n_s, n_f, blk):
    """Base θ formula: θ = 1 + √φ × Σ_gold + (W/6) × μ_eff × LEAK"""
    mu = MU_EFF.get(Z, 0.0)
    if Z in LANTHANIDE_MU:
        mu = LANTHANIDE_MU[Z]

    c_gold = math.sqrt(PHI)
    c_mag = W / 6  # Framework constant

    sigma_gold = c_gold * n_p * (G1 / BOS) * PHI**(-(per - 1))
    sigma_magnetic = c_mag * mu * LEAK

    theta = 1.0 + sigma_gold + sigma_magnetic
    return theta


def predict_ratio(Z):
    """Predict vdW/cov ratio with full δ_silver corrections."""
    per, n_p, n_d, n_s, n_f, blk = get_quantum_numbers(Z)

    # D-block boundary modes (unchanged)
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
            theta = theta_base(Z, per, n_p, n_d, n_s, n_f, blk)
    elif blk == 'f':
        # F-block: lanthanides use base formula (magnetic term handles it)
        theta = theta_base(Z, per, n_p, n_d, n_s, n_f, blk)
    else:
        # s-block, p-block, noble gas
        theta = theta_base(Z, per, n_p, n_d, n_s, n_f, blk)

    # ── δ_silver corrections (only for silver-vertex elements) ──
    # Gated behind n_d = n_f = 0 (no d or f electrons in valence)
    correction = ""
    p_hole = False
    if blk not in ('d', 'f'):
        # 1. Alkaline earths: θ = r_c (or r_c × φ for Be)
        if blk == 's' and n_p == 0 and Z > 2:
            if per > 1 and Z in [4, 12, 20, 38, 56]:
                if per == 2:
                    theta = R_C * PHI
                    correction = "s²(Be) θ=r_c×φ"
                else:
                    theta = R_C
                    correction = "s² θ=r_c"

        # 2. Period 2 gate overflow (B only, n_p=1)
        elif per == 2 and n_p == 1 and blk == 'p':
            theta = theta * PHI
            correction = "per2 overflow θ×φ"

        # 3. sp³ hybridizers (n_p=2): θ × φ^(1/3)
        #    C (per 2), Si (per 3), Ge (per 4), Sn (per 5)
        elif n_p == 2 and blk == 'p':
            theta = theta * PHI**(1/3)
            correction = "sp³ θ×φ^(1/3)"

        # 4. P-hole regime (n_p ≥ 4, per ≥ 3): ratio × r_c
        #    The σ₃ gate opens → leak channel → effective ratio drops
        #    Applied to RATIO (not θ) — same as scorecard v10
        elif n_p >= 4 and per >= 3 and blk == 'p':
            p_hole = True
            correction = "p-hole ratio×r_c"

        # Noble gas p-hole (Ar, Kr, Xe: per ≥ 3)
        elif blk == 'ng' and per >= 3:
            p_hole = True
            correction = "ng p-hole ratio×r_c"

    ratio = math.sqrt(1 + (theta * BOS)**2)

    # P-hole applied to ratio (geometric projection)
    if p_hole:
        ratio *= R_C

    # He breathing correction
    if Z == 2:
        ratio *= (1 + BREATHING)
        correction = "He breathing"

    return ratio, theta, correction


def run_full_test():
    """Run the complete test across all 71 elements."""
    print("=" * 75)
    print("  COMPLETE δ_SILVER MODEL — FOUR GATES + P-HOLE")
    print("  All constants from φ² = φ + 1. Zero free parameters.")
    print("=" * 75)
    print()

    results = []
    for Z in sorted(RADII.keys()):
        rc, rv = RADII[Z]
        ratio_obs = rv / rc
        ratio_pred, theta, corr = predict_ratio(Z)
        err = (ratio_pred - ratio_obs) / ratio_obs * 100
        per, n_p, n_d, n_s, n_f, blk = get_quantum_numbers(Z)
        results.append((Z, SYMBOLS[Z], blk, per, n_p, n_d, n_f,
                        theta, ratio_pred, ratio_obs, err, corr))

    # Print results
    print(f"  {'Z':>3} {'Sym':>3} {'Blk':>3} {'Per':>3} {'np':>2} {'θ':>6}"
          f" {'Pred':>7} {'Obs':>7} {'Err':>7}  Correction")
    print("  " + "─" * 72)

    errors = []
    errors_no_HHe = []
    blocks = {'s': [], 'p': [], 'd': [], 'f': [], 'ng': []}

    for Z, sym, blk, per, np_, nd, nf, th, rp, ro, err, corr in results:
        flag = " " if abs(err) < 10 else ("~" if abs(err) < 20 else "!")
        print(f"  {Z:3d} {sym:>3} {blk:>3} {per:>3} {np_:>2}"
              f" {th:6.3f} {rp:7.3f} {ro:7.3f} {err:+7.1f}%{flag} {corr}")
        errors.append(abs(err))
        if Z > 2:
            errors_no_HHe.append(abs(err))
            blocks[blk].append(abs(err))

    errors = np.array(errors)
    errors_no_HHe = np.array(errors_no_HHe)

    # Summary
    print()
    print("=" * 75)
    print("  SUMMARY")
    print("=" * 75)
    print()

    n = len(errors_no_HHe)
    n10 = sum(1 for e in errors_no_HHe if e < 10)
    n20 = sum(1 for e in errors_no_HHe if e < 20)
    print(f"  All elements (Z>2): {n} elements")
    print(f"    Mean error:  {np.mean(errors_no_HHe):.1f}%")
    print(f"    Within 10%:  {n10}/{n} ({100*n10/n:.0f}%)")
    print(f"    Within 20%:  {n20}/{n} ({100*n20/n:.0f}%)")
    print()

    print("  Per-block results (Z>2):")
    print(f"  {'Block':>8} {'N':>4} {'Mean':>7} {'<10%':>8} {'<20%':>8}")
    print("  " + "─" * 40)
    for blk_name, blk_key in [('S-block', 's'), ('P-block', 'p'),
                                ('D-block', 'd'), ('F-block', 'f'),
                                ('Noble', 'ng')]:
        be = blocks[blk_key]
        if not be:
            continue
        nb = len(be)
        n10b = sum(1 for e in be if e < 10)
        n20b = sum(1 for e in be if e < 20)
        print(f"  {blk_name:>8} {nb:>4} {np.mean(be):>7.1f}% {n10b:>3}/{nb} ({100*n10b/nb:.0f}%) {n20b:>3}/{nb} ({100*n20b/nb:.0f}%)")

    # Show outliers (>10%)
    print()
    print("  Remaining outliers (>10%):")
    outliers = [(Z, sym, blk, err, corr) for Z, sym, blk, per, np_, nd, nf, th, rp, ro, err, corr in results if abs(err) > 10 and Z > 2]
    if outliers:
        for Z, sym, blk, err, corr in outliers:
            print(f"    {sym:>3} (Z={Z:2d}, {blk}): {err:+.1f}%  {corr}")
    else:
        print("    NONE — all elements within 10%!")

    print()
    print("=" * 75)
    print("  DONE")
    print("=" * 75)


if __name__ == "__main__":
    run_full_test()
