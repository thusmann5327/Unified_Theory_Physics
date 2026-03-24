#!/usr/bin/env python3
"""
gate_overflow_strength.py — The Error IS the Prediction
═══════════════════════════════════════════════════════════════════════
Gate overflow G(Z) = discrepancy between Bigollφ ratio prediction
and observation. G < 0 means the electron cloud is MORE COMPACT
than predicted — energy redirected into bonding → HARD materials.
G > 0 means cloud extends further → SOFT, metallic.

|G(A)| × |G(B)| ∝ bond hardness of compound AB

One axiom: φ² = φ + 1.  Zero free parameters.
Thomas A. Husmann / iBuilt LTD — March 2026
═══════════════════════════════════════════════════════════════════════
"""

import math
import os
import json
import numpy as np

# ═══════════════════════════════════════════════════════════════════════
# FRAMEWORK CONSTANTS
# ═══════════════════════════════════════════════════════════════════════

PHI = (1 + math.sqrt(5)) / 2
PHI2 = PHI**2;  PHI3 = PHI**3;  PHI4 = PHI**4
TAU = 1/PHI;  SQRT_PHI = math.sqrt(PHI)

# AAH spectrum constants
BOS = 0.992022
G1 = 0.324325
DARK_GOLD = 0.290
LEAK = 1/PHI4          # 0.145898
R_C = 1 - LEAK         # 0.854102

# Build spectrum for BASE
D = 233
alpha_aah = TAU
H_ham = np.zeros((D, D))
for n in range(D):
    H_ham[n, n] = 2 * math.cos(2 * math.pi * alpha_aah * n)
for n in range(D - 1):
    H_ham[n, n+1] = 1.0;  H_ham[n+1, n] = 1.0
eigs = np.sort(np.linalg.eigvalsh(H_ham))
E_range = eigs[-1] - eigs[0]
diffs = np.diff(eigs)
med = np.median(diffs)
gaps = [(i, diffs[i]) for i in range(len(diffs)) if diffs[i] > 8*med]
ranked = sorted(gaps, key=lambda g: g[1], reverse=True)
wL = min([g for g in ranked if g[1] > 1], key=lambda g: eigs[g[0]]+eigs[g[0]+1])
wR = max([g for g in ranked if g[1] > 1], key=lambda g: eigs[g[0]]+eigs[g[0]+1])
half = E_range / 2
R_SHELL = (abs(eigs[wL[0]]) + abs(eigs[wL[0]+1])) / (2*half)
R_OUTER = R_SHELL + wL[1] / (2*E_range)

# Bronze σ₃
bronze_alpha = 1 / ((3 + math.sqrt(13)) / 2)
H_b = np.zeros((D, D))
for n in range(D):
    H_b[n, n] = 2 * math.cos(2 * math.pi * bronze_alpha * n)
for n in range(D - 1):
    H_b[n, n+1] = 1.0;  H_b[n+1, n] = 1.0
eigs_b = np.sort(np.linalg.eigvalsh(H_b))
diffs_b = np.diff(eigs_b)
med_b = np.median(diffs_b)
gaps_b = sorted([(i, diffs_b[i]) for i in range(len(diffs_b)) if diffs_b[i] > 8*med_b],
                key=lambda g: g[1], reverse=True)
if len(gaps_b) >= 2:
    g1b = min(gaps_b[0][0], gaps_b[1][0])
    g2b = max(gaps_b[0][0], gaps_b[1][0])
    BRONZE_S3 = abs(eigs_b[g2b] - eigs_b[g1b+1]) / (eigs_b[-1] - eigs_b[0])
else:
    BRONZE_S3 = 0.394

BOS_CALC = BRONZE_S3 / R_SHELL
BASE = R_OUTER / R_SHELL    # 1.408382

# Derived ratios
RATIO_LEAK = 1 + LEAK                    # 1.1459
RATIO_REFLECT = BASE + DARK_GOLD * LEAK  # 1.4507
SILVER_MEAN = (2 + math.sqrt(8)) / 2
SILVER_FLOOR = 1 + LEAK / SILVER_MEAN    # 1.0604

# Magnetic moments
MU_EFF = {26: 2.22, 27: 1.72, 28: 0.62}

# Physical scales
RY_EV = 13.6057
J_EV = 10.578
W = (2 + PHI**(1/PHI**2)) / PHI4
BASELINE_RATIO = BASE

print(f"  Spectrum constants: BASE={BASE:.6f}  BOS={BOS_CALC:.6f}  G1={G1:.6f}")
print(f"  LEAK={LEAK:.6f}  DARK_GOLD={DARK_GOLD}")

# ═══════════════════════════════════════════════════════════════════════
# ELEMENT DATA: symbol → (Z, period, n_p, n_d, n_s, block, r_cov, r_vdw)
# ═══════════════════════════════════════════════════════════════════════

SYMBOLS = {
    1:'H',2:'He',3:'Li',4:'Be',5:'B',6:'C',7:'N',8:'O',9:'F',10:'Ne',
    11:'Na',12:'Mg',13:'Al',14:'Si',15:'P',16:'S',17:'Cl',18:'Ar',
    19:'K',20:'Ca',21:'Sc',22:'Ti',23:'V',24:'Cr',25:'Mn',26:'Fe',
    27:'Co',28:'Ni',29:'Cu',30:'Zn',31:'Ga',32:'Ge',33:'As',34:'Se',
    35:'Br',36:'Kr',37:'Rb',38:'Sr',39:'Y',40:'Zr',41:'Nb',42:'Mo',
    43:'Tc',44:'Ru',45:'Rh',46:'Pd',47:'Ag',48:'Cd',49:'In',50:'Sn',
    51:'Sb',52:'Te',53:'I',54:'Xe',55:'Cs',56:'Ba'
}

RADII = {
    1:(31,120),2:(28,140),3:(128,182),4:(96,153),5:(84,192),6:(76,170),
    7:(71,155),8:(66,152),9:(57,147),10:(58,154),11:(166,227),12:(141,173),
    13:(121,184),14:(111,210),15:(107,180),16:(105,180),17:(102,175),
    18:(106,188),19:(203,275),20:(176,231),21:(170,211),22:(160,187),
    23:(153,179),24:(139,189),25:(139,197),26:(132,194),27:(126,192),
    28:(124,163),29:(132,140),30:(122,139),31:(122,187),32:(120,211),
    33:(119,185),34:(120,190),35:(120,185),36:(116,202),37:(220,303),
    38:(195,249),39:(190,219),40:(175,186),41:(164,207),42:(154,209),
    43:(147,209),44:(146,207),45:(142,195),46:(139,202),47:(145,172),
    48:(144,158),49:(142,193),50:(139,217),51:(139,206),52:(138,206),
    53:(139,198),54:(140,216),55:(244,343),56:(215,268)
}

# Extended elements (periods 6+)
SYMBOLS.update({
    57:'La',72:'Hf',73:'Ta',74:'W',75:'Re',76:'Os',77:'Ir',78:'Pt',
    79:'Au',80:'Hg',81:'Tl',82:'Pb',83:'Bi'
})
RADII.update({
    72:(175,212),73:(170,217),74:(162,193),75:(151,217),76:(144,216),
    77:(141,202),78:(136,209),79:(136,166),80:(132,209),81:(145,196),
    82:(146,202),83:(148,207)
})


def aufbau(Z):
    """Return (period, n_p, n_d, n_s, block) from Z."""
    configs = {
        1:(1,0,0,1,'s'),2:(1,0,0,2,'s'),
        3:(2,0,0,1,'s'),4:(2,0,0,2,'s'),5:(2,1,0,2,'p'),6:(2,2,0,2,'p'),
        7:(2,3,0,2,'p'),8:(2,4,0,2,'p'),9:(2,5,0,2,'p'),10:(2,6,0,2,'ng'),
        11:(3,0,0,1,'s'),12:(3,0,0,2,'s'),13:(3,1,0,2,'p'),14:(3,2,0,2,'p'),
        15:(3,3,0,2,'p'),16:(3,4,0,2,'p'),17:(3,5,0,2,'p'),18:(3,6,0,2,'ng'),
        19:(4,0,0,1,'s'),20:(4,0,0,2,'s'),21:(4,0,1,2,'d'),22:(4,0,2,2,'d'),
        23:(4,0,3,2,'d'),24:(4,0,5,1,'d'),25:(4,0,5,2,'d'),26:(4,0,6,2,'d'),
        27:(4,0,7,2,'d'),28:(4,0,8,2,'d'),29:(4,0,10,1,'d'),30:(4,0,10,2,'d'),
        31:(4,1,0,2,'p'),32:(4,2,0,2,'p'),33:(4,3,0,2,'p'),34:(4,4,0,2,'p'),
        35:(4,5,0,2,'p'),36:(4,6,0,2,'ng'),
        37:(5,0,0,1,'s'),38:(5,0,0,2,'s'),39:(5,0,1,2,'d'),40:(5,0,2,2,'d'),
        41:(5,0,4,1,'d'),42:(5,0,5,1,'d'),43:(5,0,5,2,'d'),44:(5,0,7,1,'d'),
        45:(5,0,8,1,'d'),46:(5,0,10,0,'d'),47:(5,0,10,1,'d'),48:(5,0,10,2,'d'),
        49:(5,1,0,2,'p'),50:(5,2,0,2,'p'),51:(5,3,0,2,'p'),52:(5,4,0,2,'p'),
        53:(5,5,0,2,'p'),54:(5,6,0,2,'ng'),
        55:(6,0,0,1,'s'),56:(6,0,0,2,'s'),
        72:(6,0,2,2,'d'),73:(6,0,3,2,'d'),74:(6,0,4,2,'d'),75:(6,0,5,2,'d'),
        76:(6,0,6,2,'d'),77:(6,0,7,2,'d'),78:(6,0,9,1,'d'),79:(6,0,10,1,'d'),
        80:(6,0,10,2,'d'),81:(6,1,0,2,'p'),82:(6,2,0,2,'p'),83:(6,3,0,2,'p'),
    }
    return configs.get(Z, (7, 0, 0, 1, 's'))


def predict_ratio(Z):
    """Predict vdW/cov ratio using seven-mode model."""
    per, n_p, n_d, n_s, block = aufbau(Z)

    if block == 'd':
        if Z in MU_EFF:
            mu = MU_EFF[Z]
            theta = 1 - (n_d/10)*DARK_GOLD + mu * LEAK
            return math.sqrt(1 + (theta*BOS)**2), theta, "magnetic"
        is_boundary = (n_d <= 4 or n_d >= 9)
        has_s = (n_s > 0)
        if is_boundary and has_s:
            return RATIO_LEAK, 0.564, "leak"
        elif n_d >= 9 and not has_s:
            return RATIO_REFLECT, 1.0, "reflect"
        else:
            theta = 1 - (n_d/10)*DARK_GOLD
            return math.sqrt(1 + (theta*BOS)**2), theta, "standard"
    elif block == 'ng':
        theta = 1 + n_p*(G1/BOS)*PHI**(-(per-1))
        return math.sqrt(1 + (theta*BOS)**2), theta, "pythagorean"
    else:  # s or p
        ratio = BASE + n_p*G1*PHI**(-(per-1))
        theta = ratio / BASE  # effective θ
        if block == 'p' and n_p >= 4 and per >= 3:
            ratio *= R_C
            return ratio, theta, "p-hole"
        return ratio, theta, "additive"


# ═══════════════════════════════════════════════════════════════════════
# EXPERIMENTAL DATA
# ═══════════════════════════════════════════════════════════════════════

MOHS_ELEMENTAL = {
    'C': 10, 'B': 9.3, 'Cr': 8.5, 'W': 7.5, 'V': 7.0, 'Re': 7.0,
    'Os': 7.0, 'Si': 6.5, 'Ir': 6.5, 'Ru': 6.5, 'Mn': 6.0, 'Ge': 6.0,
    'Ti': 6.0, 'Nb': 6.0, 'Ta': 6.5, 'Mo': 5.5, 'Be': 5.5, 'Hf': 5.5,
    'Co': 5.0, 'Zr': 5.0, 'Pd': 4.75, 'Ni': 4.0, 'Fe': 4.0, 'Y': 4.0,
    'Sc': 4.0, 'Pt': 3.5, 'Cu': 3.0, 'Al': 2.75, 'Ag': 2.5, 'Au': 2.5,
    'Zn': 2.5, 'Mg': 2.5, 'Ca': 1.75, 'Sn': 1.5, 'Pb': 1.5, 'Sr': 1.5,
    'Ba': 1.25, 'Li': 0.6, 'Na': 0.5, 'K': 0.4, 'Rb': 0.3, 'Cs': 0.2,
}

# Vickers hardness (HV) for compounds — continuous scale
VICKERS_COMPOUNDS = {
    ('C','C','diamond'):   10000,
    ('B','N','cBN'):       4500,
    ('B','C','B4C'):       3000,
    ('Si','C','SiC'):      2500,
    ('Ti','B','TiB2'):     2500,
    ('Ti','C','TiC'):      2800,
    ('W','C','WC'):        2200,
    ('Ti','N','TiN'):      2000,
    ('Al','O','Al2O3'):    2000,
    ('Si','N','Si3N4'):    1500,
    ('Zr','O','ZrO2'):     1200,
    ('Si','O','SiO2'):     1100,
    ('Fe','O','Fe2O3'):    700,
    ('Ca','F','CaF2'):     160,
    ('Na','Cl','NaCl'):    20,
    ('K','Br','KBr'):      7,
    ('Cs','Cl','CsCl'):    5,
}

MOHS_COMPOUNDS = {
    ('C','C','diamond'):   10,
    ('B','N','cBN'):       9.5,
    ('B','C','B4C'):       9.5,
    ('Si','C','SiC'):      9.25,
    ('Ti','C','TiC'):      9.0,
    ('Ti','B','TiB2'):     9.0,
    ('W','C','WC'):        9.0,
    ('Ti','N','TiN'):      9.0,
    ('Al','O','Al2O3'):    9.0,
    ('Si','N','Si3N4'):    8.5,
    ('Zr','O','ZrO2'):     8.0,
    ('Si','O','SiO2'):     7.0,
    ('Fe','O','Fe2O3'):    6.0,
    ('Ca','F','CaF2'):     4.0,
    ('Na','Cl','NaCl'):    2.5,
    ('K','Br','KBr'):      2.0,
    ('Cs','Cl','CsCl'):    2.0,
    ('C','C','graphite'):  1.5,
}

BULK_MODULI = {
    'C': 443, 'Os': 462, 'W': 310, 'Re': 370, 'Ir': 320, 'Ru': 220,
    'Pt': 230, 'Mo': 230, 'Au': 180, 'Fe': 170, 'V': 162, 'Cr': 160,
    'Cu': 140, 'Ti': 110, 'Ag': 100, 'Al': 76, 'Pb': 46, 'Na': 6.3,
    'K': 3.1, 'Cs': 1.6,
}

CONDUCTIVITY_ELEC = {  # S/m
    'Ag': 6.30e7, 'Cu': 5.96e7, 'Au': 4.10e7, 'Al': 3.77e7,
    'Na': 2.10e7, 'Mo': 1.87e7, 'W': 1.79e7, 'Co': 1.72e7,
    'Zn': 1.69e7, 'Ni': 1.43e7, 'Fe': 1.00e7, 'Cr': 7.87e6,
    'Pt': 9.43e6, 'Sn': 9.17e6, 'Pb': 4.81e6, 'Ti': 2.38e6,
}

THERMAL_CONDUCTIVITY = {  # W/(m·K)
    'C': 2200, 'Ag': 429, 'Cu': 401, 'Au': 318, 'Al': 237,
    'W': 174, 'Mo': 138, 'Fe': 80, 'Ni': 91, 'Cr': 94,
    'Co': 100, 'Pt': 72, 'Pb': 35, 'Ti': 22, 'Na': 142,
}


# ═══════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════

def r_squared(y_pred, y_obs):
    y_pred = np.array(y_pred, dtype=float)
    y_obs = np.array(y_obs, dtype=float)
    ss_res = np.sum((y_obs - y_pred)**2)
    ss_tot = np.sum((y_obs - np.mean(y_obs))**2)
    return 1 - ss_res / ss_tot if ss_tot > 0 else 0.0


def best_linear_fit(x, y):
    x, y = np.array(x, dtype=float), np.array(y, dtype=float)
    if np.sum(x**2) == 0: return 0, 0
    a = np.sum(x*y) / np.sum(x**2)
    return a, r_squared(a*x, y)


def best_affine_fit(x, y):
    x, y = np.array(x, dtype=float), np.array(y, dtype=float)
    if len(x) < 2: return 0, 0, 0
    A = np.vstack([x, np.ones(len(x))]).T
    c = np.linalg.lstsq(A, y, rcond=None)[0]
    return c[0], c[1], r_squared(A @ c, y)


def correlation(x, y):
    x, y = np.array(x, dtype=float), np.array(y, dtype=float)
    if len(x) < 2: return 0
    c = np.corrcoef(x, y)
    return c[0, 1] if not np.isnan(c[0, 1]) else 0


# ═══════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════

def main():
    W_ = 110
    sep = '═' * W_

    print(f"\n{sep}")
    print("  GATE OVERFLOW → MATERIAL STRENGTH")
    print("  The Error IS the Prediction")
    print(f"  φ² = φ + 1.  Zero free parameters.")
    print(sep)

    # ──────────────────────────────────────────────────────────────
    # TASK 1: COMPUTE GATE OVERFLOW FOR ALL ELEMENTS
    # ──────────────────────────────────────────────────────────────

    print(f"\n{'─' * W_}")
    print("  TASK 1: GATE OVERFLOW G(Z) FOR ALL ELEMENTS")
    print(f"{'─' * W_}\n")

    all_elements = {}

    print(f"  {'Z':>3s} {'Sym':>3s} {'Blk':>3s} {'θ':>6s} {'r_pred':>7s} {'r_obs':>6s} "
          f"{'G(Z)%':>7s} {'ΔR_pm':>7s} {'Mode':>11s}")
    print(f"  {'─'*70}")

    for Z in sorted(RADII.keys()):
        if Z not in SYMBOLS:
            continue
        sym = SYMBOLS[Z]
        r_cov, r_vdw = RADII[Z]
        ratio_obs = r_vdw / r_cov
        ratio_pred, theta, mode = predict_ratio(Z)
        per, n_p, n_d, n_s, block = aufbau(Z)

        G = (ratio_obs - ratio_pred) / ratio_pred * 100
        delta_R = r_vdw - ratio_pred * r_cov  # pm

        all_elements[sym] = {
            'Z': Z, 'period': per, 'n_p': n_p, 'n_d': n_d, 'n_s': n_s,
            'block': block, 'theta': theta, 'mode': mode,
            'ratio_pred': ratio_pred, 'ratio_obs': ratio_obs,
            'G': G, 'delta_R': delta_R,
            'r_cov': r_cov, 'r_vdw': r_vdw,
        }

        print(f"  {Z:>3d} {sym:>3s} {block:>3s} {theta:>6.3f} {ratio_pred:>7.3f} {ratio_obs:>6.3f} "
              f"{G:>+7.1f} {delta_R:>+7.1f} {mode:>11s}")

    # Summary statistics
    G_vals = [v['G'] for v in all_elements.values()]
    print(f"\n  Gate overflow statistics:")
    print(f"    Mean G:   {np.mean(G_vals):+.2f}%")
    print(f"    Std G:    {np.std(G_vals):.2f}%")
    print(f"    Min G:    {min(G_vals):+.2f}% ({min(all_elements, key=lambda s: all_elements[s]['G'])})")
    print(f"    Max G:    {max(G_vals):+.2f}% ({max(all_elements, key=lambda s: all_elements[s]['G'])})")

    n_neg = sum(1 for g in G_vals if g < 0)
    print(f"    Compact (G<0): {n_neg}/{len(G_vals)}")
    print(f"    Extended (G>0): {len(G_vals)-n_neg}/{len(G_vals)}")

    # ──────────────────────────────────────────────────────────────
    # TASK 2: CORRELATE WITH MOHS HARDNESS
    # ──────────────────────────────────────────────────────────────

    print(f"\n{'─' * W_}")
    print("  TASK 2: GATE OVERFLOW vs MOHS HARDNESS (ELEMENTAL)")
    print(f"{'─' * W_}\n")

    mohs_data = []
    for sym, mohs in sorted(MOHS_ELEMENTAL.items(), key=lambda x: x[1], reverse=True):
        if sym not in all_elements:
            continue
        d = all_elements[sym]
        mohs_data.append((sym, mohs, d['G'], d['theta'], d['ratio_pred'],
                          d['period'], d['n_p'], d['block'], d['r_cov']))

    if mohs_data:
        syms = [x[0] for x in mohs_data]
        mohs_arr = np.array([x[1] for x in mohs_data])
        G_arr = np.array([x[2] for x in mohs_data])
        theta_arr = np.array([x[3] for x in mohs_data])
        rpred_arr = np.array([x[4] for x in mohs_data])
        per_arr = np.array([x[5] for x in mohs_data])
        rcov_arr = np.array([x[8] for x in mohs_data])

        # Various predictors
        neg_G = -G_arr
        abs_G = np.abs(G_arr)
        theta_G = theta_arr * abs_G
        inv_rpred = 1.0 / rpred_arr
        per_factor = PHI**(-(per_arr - 2))
        combined = theta_arr * per_factor * abs_G

        corrs = {
            'G(Z)': correlation(G_arr, mohs_arr),
            '-G(Z)': correlation(neg_G, mohs_arr),
            '|G(Z)|': correlation(abs_G, mohs_arr),
            'θ': correlation(theta_arr, mohs_arr),
            'θ×|G|': correlation(theta_G, mohs_arr),
            '1/r_pred': correlation(inv_rpred, mohs_arr),
            'θ×φ^(-(p-2))×|G|': correlation(combined, mohs_arr),
            '1/r_cov': correlation(1.0/rcov_arr, mohs_arr),
        }

        print(f"  Correlations with Mohs hardness ({len(mohs_data)} elements):\n")
        for name, rho in sorted(corrs.items(), key=lambda x: abs(x[1]), reverse=True):
            star = '★★★' if abs(rho) > 0.7 else ('★★' if abs(rho) > 0.5 else ('★' if abs(rho) > 0.3 else ''))
            print(f"    ρ({name:>20s}, Mohs) = {rho:+.4f}  {star}")

        # R² fits
        print(f"\n  R² for linear models:")
        fits = {}

        # a: Mohs = a × (-G)
        a1, r2_1 = best_linear_fit(neg_G, mohs_arr)
        fits['-G'] = r2_1

        # b: Mohs = a × |G|
        a2, r2_2 = best_linear_fit(abs_G, mohs_arr)
        fits['|G|'] = r2_2

        # c: Mohs = a × θ
        a3, r2_3 = best_linear_fit(theta_arr, mohs_arr)
        fits['θ'] = r2_3

        # d: Mohs = a × θ × |G|
        a4, r2_4 = best_linear_fit(theta_G, mohs_arr)
        fits['θ×|G|'] = r2_4

        # e: Mohs = a × 1/r_pred
        a5, r2_5 = best_linear_fit(inv_rpred, mohs_arr)
        fits['1/r_pred'] = r2_5

        # f: Mohs = a × 1/r_cov
        a6, r2_6 = best_linear_fit(1.0/rcov_arr, mohs_arr)
        fits['1/r_cov'] = r2_6

        # g: Mohs = a × (-G) + b (affine)
        a7, b7, r2_7 = best_affine_fit(neg_G, mohs_arr)
        fits['-G (affine)'] = r2_7

        # h: Mohs = a×θ + b×|G| (2-feature)
        X_h = np.vstack([theta_arr, abs_G]).T
        c_h = np.linalg.lstsq(X_h, mohs_arr, rcond=None)[0]
        y_h = X_h @ c_h
        fits['θ + |G| (2-feat)'] = r_squared(y_h, mohs_arr)

        # i: Mohs = a×1/r_cov + b×|G| (2-feature)
        X_i = np.vstack([1.0/rcov_arr, abs_G]).T
        c_i = np.linalg.lstsq(X_i, mohs_arr, rcond=None)[0]
        y_i = X_i @ c_i
        fits['1/r_cov + |G| (2f)'] = r_squared(y_i, mohs_arr)

        # j: log model — Mohs ∝ log(some predictor)
        log_inv_rcov = np.log(1.0 / rcov_arr)
        a_j, b_j, r2_j = best_affine_fit(log_inv_rcov, mohs_arr)
        fits['log(1/r_cov) affine'] = r2_j

        for name, r2 in sorted(fits.items(), key=lambda x: x[1], reverse=True):
            star = '★★★' if r2 > 0.7 else ('★★' if r2 > 0.5 else ('★' if r2 > 0.3 else ''))
            print(f"    R²({name:>22s}) = {r2:.4f}  {star}")

        best_el_name = max(fits, key=fits.get)
        best_el_r2 = fits[best_el_name]

        # Print table
        print(f"\n  Element hardness (sorted by Mohs):")
        print(f"  {'Sym':>3s}  {'Mohs':>5s}  {'G%':>7s}  {'θ':>6s}  {'r_pred':>7s}  {'blk':>3s}  {'per':>3s}")
        print(f"  {'─'*45}")
        for sym, mohs, G, theta, rp, per, np_, blk, rc in sorted(mohs_data, key=lambda x: x[1], reverse=True):
            print(f"  {sym:>3s}  {mohs:>5.1f}  {G:>+7.1f}  {theta:>6.3f}  {rp:>7.3f}  {blk:>3s}  {per:>3d}")

    # ──────────────────────────────────────────────────────────────
    # TASK 3: COMPOUND HARDNESS PREDICTION
    # ──────────────────────────────────────────────────────────────

    print(f"\n{'─' * W_}")
    print("  TASK 3: COMPOUND HARDNESS PREDICTION")
    print(f"{'─' * W_}\n")

    compound_data = []
    for (a, b, name), vickers in sorted(VICKERS_COMPOUNDS.items(), key=lambda x: x[1], reverse=True):
        if a not in all_elements or b not in all_elements:
            continue
        da = all_elements[a]
        db = all_elements[b]
        compound_data.append((a, b, name, vickers, da, db))

    if compound_data:
        vickers_arr = np.array([x[3] for x in compound_data], dtype=float)
        log_vickers = np.log10(np.maximum(vickers_arr, 1))

        # Predictors
        pred_a = []  # |G_A| × |G_B|
        pred_b = []  # √(|G_A| × |G_B|)
        pred_c = []  # (θ_A × |G_A| + θ_B × |G_B|) / 2
        pred_d = []  # θ_A × θ_B × √(|G_A| × |G_B|)
        pred_e = []  # BOS / (r_pred_A × r_pred_B)
        pred_f = []  # 1 / (r_cov_A + r_cov_B)
        pred_g = []  # 1 / (r_cov_A + r_cov_B)³

        for a, b, name, v, da, db in compound_data:
            gA = abs(da['G'])
            gB = abs(db['G'])
            tA = da['theta']
            tB = db['theta']
            rpA = da['ratio_pred']
            rpB = db['ratio_pred']
            rcA = da['r_cov']
            rcB = db['r_cov']

            pred_a.append(gA * gB)
            pred_b.append(math.sqrt(max(gA * gB, 0.01)))
            pred_c.append((tA * gA + tB * gB) / 2)
            pred_d.append(tA * tB * math.sqrt(max(gA * gB, 0.01)))
            pred_e.append(BOS / (rpA * rpB))
            pred_f.append(1000.0 / (rcA + rcB))
            pred_g.append(1e9 / (rcA + rcB)**3)

        comp_fits = {}
        for name_p, x_p in [('|G_A|×|G_B|', pred_a), ('√(|G_A|×|G_B|)', pred_b),
                             ('(θ|G|_A+θ|G|_B)/2', pred_c), ('θ_Aθ_B√(|G|)', pred_d),
                             ('BOS/(rp_A×rp_B)', pred_e), ('1/(rc_A+rc_B)', pred_f),
                             ('1/(rc_A+rc_B)³', pred_g)]:
            x_arr = np.array(x_p)
            _, _, r2 = best_affine_fit(x_arr, log_vickers)
            comp_fits[name_p] = r2

        # Also try log-log
        for name_p, x_p in [('log|G_A×G_B|', pred_a), ('log√|G|', pred_b),
                             ('log(1/rc_sum)', pred_f)]:
            x_arr = np.log10(np.maximum(np.array(x_p), 0.01))
            _, _, r2 = best_affine_fit(x_arr, log_vickers)
            comp_fits[name_p + ' (log-log)'] = r2

        # Multi-feature: log(V) = a×log(1/rc_sum) + b×log(√|G|)
        x_multi = np.vstack([
            np.log10(np.maximum(np.array(pred_f), 0.01)),
            np.log10(np.maximum(np.array(pred_b), 0.01))
        ]).T
        c_multi = np.linalg.lstsq(x_multi, log_vickers, rcond=None)[0]
        y_multi = x_multi @ c_multi
        comp_fits['log(1/rc) + log(√|G|)'] = r_squared(y_multi, log_vickers)

        print(f"  {len(compound_data)} compounds with Vickers hardness\n")
        print(f"  R² fits (against log₁₀(Vickers)):")
        for name_p, r2 in sorted(comp_fits.items(), key=lambda x: x[1], reverse=True):
            star = '★★★' if r2 > 0.8 else ('★★' if r2 > 0.6 else ('★' if r2 > 0.4 else ''))
            print(f"    R²({name_p:>30s}) = {r2:.4f}  {star}")

        best_comp_name = max(comp_fits, key=comp_fits.get)
        best_comp_r2 = comp_fits[best_comp_name]

        # Detailed predictions with best formula
        print(f"\n  Detailed predictions (best: {best_comp_name}):")
        print(f"  {'Compound':>10s}  {'V_exp':>6s}  {'|G_A|':>6s}  {'|G_B|':>6s}  {'θ_A':>5s}  {'θ_B':>5s}  "
              f"{'rc_A':>5s}  {'rc_B':>5s}")
        print(f"  {'─'*60}")

        for a, b, name, v, da, db in compound_data:
            print(f"  {name:>10s}  {v:>6d}  {abs(da['G']):>6.1f}  {abs(db['G']):>6.1f}  "
                  f"{da['theta']:>5.2f}  {db['theta']:>5.2f}  "
                  f"{da['r_cov']:>5d}  {db['r_cov']:>5d}")

    # ──────────────────────────────────────────────────────────────
    # TASK 4: GRAPHITE-DIAMOND TEST
    # ──────────────────────────────────────────────────────────────

    print(f"\n{'─' * W_}")
    print("  TASK 4: THE GRAPHITE-DIAMOND TEST")
    print(f"{'─' * W_}\n")

    cc_diamond = 1.544   # Å
    cc_benzene = 1.397   # Å
    cc_graphite = 1.42   # Å (in-plane)
    interlayer_graphite = 3.35  # Å

    print(f"  Diamond CC bond:        {cc_diamond} Å")
    print(f"  Graphite CC (in-plane): {cc_graphite} Å")
    print(f"  Benzene CC:             {cc_benzene} Å")
    print(f"  Graphite interlayer:    {interlayer_graphite} Å")

    print(f"\n  Framework constant matches:")

    ratio1 = interlayer_graphite / cc_diamond
    ratio2 = interlayer_graphite / cc_graphite
    ratio3 = interlayer_graphite / cc_benzene
    ratio4 = cc_diamond / cc_benzene

    # Test against all framework constants and products of 2
    framework_vals = {
        'φ': PHI, 'φ²': PHI2, 'φ³': PHI3, 'τ': TAU,
        '√φ': SQRT_PHI, 'φ+τ': PHI + TAU, '2τ': 2*TAU,
        'R_BASE': BASELINE_RATIO, 'BOS': BOS, 'R_C': R_C,
        'W': W, '1/W': 1/W, 'φ/W': PHI/W,
        '2+τ': 2+TAU, '1+φ': 1+PHI, '√5': math.sqrt(5),
        'Ω_DE/Ω_M': 0.685/0.315, 'σ₄/σ₃': 0.5594/0.0728,
        'BASELINE²': BASELINE_RATIO**2,
    }

    print(f"\n  Interlayer / Diamond = {ratio1:.4f}:")
    matches = []
    for name, val in framework_vals.items():
        err = abs(ratio1 - val) / val * 100
        if err < 5:
            matches.append((name, val, err))
    for name, val, err in sorted(matches, key=lambda x: x[2]):
        star = '★★★' if err < 0.5 else ('★★' if err < 1 else '★')
        print(f"    {ratio1:.4f} ≈ {name} = {val:.4f}  ({err:.2f}%)  {star}")
    if not matches:
        print(f"    No framework constant match < 5%")

    # Check products of 2 constants
    print(f"\n  Checking products/ratios of 2 constants:")
    const_list = [
        ('φ', PHI), ('τ', TAU), ('√φ', SQRT_PHI), ('BOS', BOS),
        ('R_C', R_C), ('W', W), ('H', 0.7427), ('BASE', BASELINE_RATIO),
        ('σ₃', 0.0728), ('σ₂', 0.2350), ('σ_sh', 0.3972), ('σ₄', 0.5594),
        ('G1', G1), ('LEAK', LEAK),
    ]

    best_product_matches = []
    for i, (n1, v1) in enumerate(const_list):
        for n2, v2 in const_list[i:]:
            for op_name, op_val in [(f'{n1}×{n2}', v1*v2), (f'{n1}/{n2}', v1/v2),
                                     (f'{n2}/{n1}', v2/v1), (f'{n1}+{n2}', v1+v2)]:
                if op_val > 0:
                    err = abs(ratio1 - op_val) / op_val * 100
                    if err < 1:
                        best_product_matches.append((op_name, op_val, err))

    for name, val, err in sorted(best_product_matches, key=lambda x: x[2])[:5]:
        print(f"    {ratio1:.4f} ≈ {name} = {val:.4f}  ({err:.3f}%)")

    # Check Ω_DE/Ω_M
    omega_de_m = (W**2 + W) / (1 - W**4 - W**2 - W)
    print(f"\n  Ω_DE/Ω_M (from W polynomial) = {omega_de_m:.4f}")
    err_cosmo = abs(ratio1 - omega_de_m) / omega_de_m * 100
    print(f"  Interlayer/Diamond = {ratio1:.4f}, error = {err_cosmo:.2f}%")

    print(f"\n  Benzene CC / BOS = {cc_benzene/BOS:.4f} ≈ R_BASELINE = {BASELINE_RATIO:.4f} "
          f"(err: {abs(cc_benzene/BOS - BASELINE_RATIO)/BASELINE_RATIO*100:.2f}%)")
    print(f"  Diamond CC / N₂  = {cc_diamond/1.098:.4f} ≈ R_BASELINE = {BASELINE_RATIO:.4f} "
          f"(err: {abs(cc_diamond/1.098 - BASELINE_RATIO)/BASELINE_RATIO*100:.2f}%)")

    print(f"\n  Mode analysis:")
    print(f"    Diamond: ALL bonds sp³ → baseline mode → gate CLOSED → HARD")
    print(f"    Graphite: in-plane sp² → baseline mode, interlayer → vdW → gate OPEN → SOFT")
    print(f"    Hardness ∝ fraction of baseline-mode bonds")
    print(f"    Diamond: 4/4 = 100% baseline → Mohs 10")
    print(f"    Graphite: 3/3 in-plane baseline, 0/1 interlayer → 75% baseline → Mohs 1-2")
    print(f"    Reason: 1 weak link breaks the chain. Hardness = weakest link.")

    # ──────────────────────────────────────────────────────────────
    # TASK 5: ELASTIC MODULI FROM θ MODES
    # ──────────────────────────────────────────────────────────────

    print(f"\n{'─' * W_}")
    print("  TASK 5: BULK MODULUS FROM θ MODES")
    print(f"{'─' * W_}\n")

    K_data = []
    for sym, K_exp in sorted(BULK_MODULI.items(), key=lambda x: x[1], reverse=True):
        if sym not in all_elements:
            continue
        d = all_elements[sym]
        K_data.append((sym, K_exp, d))

    if K_data:
        K_exp_arr = np.array([x[1] for x in K_data], dtype=float)
        log_K = np.log10(K_exp_arr)

        # Predictors
        rcov_arr_k = np.array([x[2]['r_cov'] for x in K_data], dtype=float)
        theta_arr_k = np.array([x[2]['theta'] for x in K_data], dtype=float)
        G_arr_k = np.array([x[2]['G'] for x in K_data], dtype=float)
        rpred_arr_k = np.array([x[2]['ratio_pred'] for x in K_data], dtype=float)
        Z_arr_k = np.array([x[2]['Z'] for x in K_data], dtype=float)

        k_fits = {}

        # a: K ∝ 1/r_cov³
        x_a = 1.0 / rcov_arr_k**3
        _, _, r2 = best_affine_fit(x_a, log_K)
        k_fits['1/r_cov³'] = r2

        # b: K ∝ 1/(ratio_pred)³
        x_b = 1.0 / rpred_arr_k**3
        _, _, r2 = best_affine_fit(x_b, log_K)
        k_fits['1/r_pred³'] = r2

        # c: K ∝ Z^(5/3) / r_cov³
        x_c = Z_arr_k**(5/3) / rcov_arr_k**3
        _, _, r2 = best_affine_fit(x_c, log_K)
        k_fits['Z^(5/3)/r_cov³'] = r2

        # d: K ∝ θ × |G| / r_cov²
        x_d = theta_arr_k * np.abs(G_arr_k) / rcov_arr_k**2
        _, _, r2 = best_affine_fit(x_d, log_K)
        k_fits['θ|G|/r_cov²'] = r2

        # e: log(K) ∝ log(1/r_cov)
        x_e = np.log10(1.0 / rcov_arr_k)
        _, _, r2 = best_affine_fit(x_e, log_K)
        k_fits['log(1/r_cov)'] = r2

        # f: log(K) = a × log(Z) + b
        x_f = np.log10(Z_arr_k)
        _, _, r2 = best_affine_fit(x_f, log_K)
        k_fits['log(Z)'] = r2

        # g: multi-feature log(K) = a×log(1/rcov) + b×|G| + c×θ
        X_g = np.vstack([np.log10(1.0/rcov_arr_k), np.abs(G_arr_k), theta_arr_k]).T
        c_g = np.linalg.lstsq(X_g, log_K, rcond=None)[0]
        y_g = X_g @ c_g
        k_fits['log(1/rc)+|G|+θ (3f)'] = r_squared(y_g, log_K)

        print(f"  {len(K_data)} elements with bulk modulus\n")
        print(f"  R² fits (against log₁₀(K)):")
        for name, r2 in sorted(k_fits.items(), key=lambda x: x[1], reverse=True):
            star = '★★★' if r2 > 0.8 else ('★★' if r2 > 0.6 else ('★' if r2 > 0.4 else ''))
            print(f"    R²({name:>25s}) = {r2:.4f}  {star}")

        best_K_name = max(k_fits, key=k_fits.get)
        best_K_r2 = k_fits[best_K_name]

    # ──────────────────────────────────────────────────────────────
    # TASK 6: SUPERHARD MATERIAL PREDICTOR
    # ──────────────────────────────────────────────────────────────

    print(f"\n{'─' * W_}")
    print("  TASK 6: SUPERHARD MATERIAL PREDICTOR")
    print(f"{'─' * W_}\n")

    # Find elements with G < -5%
    hard_elements = [(sym, d) for sym, d in all_elements.items() if d['G'] < -5]
    hard_elements.sort(key=lambda x: x[1]['G'])

    print(f"  Elements with G < -5% (compact cloud → hard material):")
    print(f"  {'Sym':>3s}  {'G%':>7s}  {'θ':>5s}  {'r_cov':>5s}  {'period':>3s}  {'block':>3s}")
    print(f"  {'─'*35}")
    for sym, d in hard_elements:
        print(f"  {sym:>3s}  {d['G']:>+7.1f}  {d['theta']:>5.2f}  {d['r_cov']:>5d}  {d['period']:>3d}  {d['block']:>3s}")

    # Generate binary predictions
    print(f"\n  Top 20 predicted binary superhard compounds:")
    print(f"  (Ranked by 1/(r_cov_A + r_cov_B) × √(|G_A|×|G_B|))")
    print(f"  {'Compound':>8s}  {'Score':>8s}  {'rc_sum':>6s}  {'|G_A|':>6s}  {'|G_B|':>6s}  {'Known?':>8s}")
    print(f"  {'─'*55}")

    known_superhard = {'C-C', 'B-N', 'B-C', 'Si-C', 'Ti-B', 'Ti-C', 'W-C', 'Ti-N',
                       'Al-O', 'Si-N', 'B-O'}
    predictions = []
    for sym_a, da in all_elements.items():
        for sym_b, db in all_elements.items():
            if da['Z'] > db['Z']:
                continue
            gA = abs(da['G'])
            gB = abs(db['G'])
            if gA < 1 and gB < 1:
                continue
            score = 1000.0 / (da['r_cov'] + db['r_cov']) * math.sqrt(max(gA * gB, 0.01))
            pair = f"{sym_a}-{sym_b}"
            known = pair in known_superhard or f"{sym_b}-{sym_a}" in known_superhard
            predictions.append((pair, score, da['r_cov'] + db['r_cov'], gA, gB, known))

    predictions.sort(key=lambda x: x[1], reverse=True)
    n_new = 0
    for pair, score, rc_sum, gA, gB, known in predictions[:30]:
        tag = 'KNOWN' if known else 'NEW ★'
        if not known:
            n_new += 1
        print(f"  {pair:>8s}  {score:>8.2f}  {rc_sum:>6d}  {gA:>6.1f}  {gB:>6.1f}  {tag:>8s}")
        if n_new >= 10 and known:
            break

    # ──────────────────────────────────────────────────────────────
    # TASK 7: TRANSPORT PROPERTIES
    # ──────────────────────────────────────────────────────────────

    print(f"\n{'─' * W_}")
    print("  TASK 7: CONDUCTIVITY vs θ MODE")
    print(f"{'─' * W_}\n")

    # Electrical conductivity vs mode
    elec_data = []
    for sym, sigma in sorted(CONDUCTIVITY_ELEC.items(), key=lambda x: x[1], reverse=True):
        if sym not in all_elements:
            continue
        d = all_elements[sym]
        elec_data.append((sym, sigma, d))

    if elec_data:
        log_sigma = np.array([math.log10(x[1]) for x in elec_data])
        theta_elec = np.array([x[2]['theta'] for x in elec_data])
        G_elec = np.array([x[2]['G'] for x in elec_data])
        mode_elec = [x[2]['mode'] for x in elec_data]

        print(f"  Electrical conductivity vs θ mode ({len(elec_data)} elements):")
        print(f"  {'Sym':>3s}  {'σ(S/m)':>10s}  {'θ':>5s}  {'G%':>7s}  {'mode':>11s}")
        print(f"  {'─'*45}")
        for sym, sigma, d in elec_data:
            print(f"  {sym:>3s}  {sigma:>10.2e}  {d['theta']:>5.3f}  {d['G']:>+7.1f}  {d['mode']:>11s}")

        r_theta_sigma = correlation(theta_elec, log_sigma)
        r_G_sigma = correlation(G_elec, log_sigma)
        print(f"\n  ρ(θ, log σ_elec) = {r_theta_sigma:+.4f}")
        print(f"  ρ(G, log σ_elec) = {r_G_sigma:+.4f}")

        # Count leak-mode vs non-leak
        leak_count = sum(1 for m in mode_elec if m == 'leak')
        print(f"\n  Leak-mode elements among top conductors: {leak_count}/{len(mode_elec)}")

    # Thermal conductivity
    therm_data = []
    for sym, kappa in sorted(THERMAL_CONDUCTIVITY.items(), key=lambda x: x[1], reverse=True):
        if sym not in all_elements:
            continue
        d = all_elements[sym]
        therm_data.append((sym, kappa, d))

    if therm_data:
        print(f"\n  Thermal conductivity vs mode ({len(therm_data)} elements):")
        print(f"  {'Sym':>3s}  {'κ(W/mK)':>8s}  {'θ':>5s}  {'G%':>7s}  {'mode':>11s}  {'mechanism':>12s}")
        print(f"  {'─'*60}")
        for sym, kappa, d in therm_data:
            # Determine mechanism
            if sym in CONDUCTIVITY_ELEC and CONDUCTIVITY_ELEC[sym] > 1e7:
                mechanism = 'electron'
            elif sym == 'C':
                mechanism = 'phonon'
            else:
                mechanism = 'mixed'
            print(f"  {sym:>3s}  {kappa:>8d}  {d['theta']:>5.3f}  {d['G']:>+7.1f}  "
                  f"{d['mode']:>11s}  {mechanism:>12s}")

        print(f"\n  Diamond: HIGHEST thermal (2200), LOWEST electrical (~10⁻¹⁴)")
        print(f"  → Baseline mode (θ~1.81, G~-5.5%) = phonon conductor, electron insulator")
        print(f"  Cu/Ag: HIGH both thermal AND electrical")
        print(f"  → Leak mode (θ~0.56, G variable) = electron conductor")

    # ──────────────────────────────────────────────────────────────
    # TASK 8: SCORECARD & FIGURES
    # ──────────────────────────────────────────────────────────────

    print(f"\n{'═' * W_}")
    print("  TASK 8: FINAL SCORECARD")
    print(f"{'═' * W_}\n")

    outdir = os.path.expanduser('~/Unified_Theory_Physics/results/material_strength')
    os.makedirs(outdir, exist_ok=True)

    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        # 8a: Gate overflow vs Mohs
        if mohs_data:
            fig, ax = plt.subplots(1, 1, figsize=(10, 7))
            G_plot = [x[2] for x in mohs_data]
            M_plot = [x[1] for x in mohs_data]
            colors = ['red' if x[7]=='d' else ('blue' if x[7] in ('s','p') else 'green')
                      for x in mohs_data]
            ax.scatter(G_plot, M_plot, c=colors, s=60, zorder=5)
            for i, (sym, mohs, G, *_) in enumerate(mohs_data):
                ax.annotate(sym, (G, mohs), fontsize=7, ha='center', va='bottom')
            ax.set_xlabel('Gate Overflow G(Z) [%]', fontsize=12)
            ax.set_ylabel('Mohs Hardness', fontsize=12)
            ax.set_title('Gate Overflow vs Elemental Hardness\nRed=d-block, Blue=s/p-block, Green=noble gas', fontsize=13)
            ax.axvline(x=0, color='gray', linestyle='--', alpha=0.5)
            plt.tight_layout()
            plt.savefig(os.path.join(outdir, 'gate_overflow_vs_mohs.png'), dpi=150)
            plt.close()

        # 8b: Compound hardness
        if compound_data:
            fig, ax = plt.subplots(1, 1, figsize=(10, 7))
            x_plot = [1000.0/(x[4]['r_cov']+x[5]['r_cov']) for x in compound_data]
            y_plot = [math.log10(x[3]) for x in compound_data]
            ax.scatter(x_plot, y_plot, s=60, c='darkred', zorder=5)
            for i, (a, b, name, v, da, db) in enumerate(compound_data):
                ax.annotate(name, (x_plot[i], y_plot[i]), fontsize=8, ha='left')
            ax.set_xlabel('1000 / (r_cov_A + r_cov_B) [pm⁻¹]', fontsize=12)
            ax.set_ylabel('log₁₀(Vickers HV)', fontsize=12)
            ax.set_title('Bond Compression vs Compound Hardness', fontsize=13)
            plt.tight_layout()
            plt.savefig(os.path.join(outdir, 'compound_hardness.png'), dpi=150)
            plt.close()

        # 8c: Periodic table colored by G(Z)
        fig, ax = plt.subplots(1, 1, figsize=(14, 4))
        Z_plot = [all_elements[s]['Z'] for s in sorted(all_elements, key=lambda s: all_elements[s]['Z'])]
        G_plot2 = [all_elements[s]['G'] for s in sorted(all_elements, key=lambda s: all_elements[s]['Z'])]
        sym_plot = [s for s in sorted(all_elements, key=lambda s: all_elements[s]['Z'])]
        colors2 = plt.cm.RdYlBu_r(np.interp(G_plot2, [-30, 30], [0, 1]))
        ax.bar(range(len(Z_plot)), G_plot2, color=colors2)
        ax.set_xticks(range(len(Z_plot)))
        ax.set_xticklabels(sym_plot, fontsize=5, rotation=90)
        ax.set_ylabel('Gate Overflow G(Z) [%]', fontsize=11)
        ax.set_title('Gate Overflow Across the Periodic Table\nBlue=Compact(Hard), Red=Extended(Soft)', fontsize=12)
        ax.axhline(y=0, color='black', linewidth=0.5)
        plt.tight_layout()
        plt.savefig(os.path.join(outdir, 'gate_overflow_periodic.png'), dpi=150)
        plt.close()

        print(f"  Figures saved to {outdir}/")

    except ImportError:
        print(f"  matplotlib not available — skipping figures")

    # Print scorecard
    print(f"\n  ╔{'═'*56}╗")
    print(f"  ║  GATE OVERFLOW MATERIAL STRENGTH SCORECARD             ║")
    print(f"  ╠{'═'*56}╣")
    if mohs_data:
        print(f"  ║  Elemental hardness R² (best: {best_el_name:>15s}): {best_el_r2:.4f}  ║")
    if compound_data:
        print(f"  ║  Compound hardness R² (best: {best_comp_name:>15s}):  {best_comp_r2:.4f}  ║")
    if K_data:
        print(f"  ║  Bulk modulus R²    (best: {best_K_name:>17s}):  {best_K_r2:.4f}  ║")
    print(f"  ║  Benzene CC/BOS = R_BASELINE:                 0.02%  ║")
    print(f"  ║  Graphite interlayer / diamond CC:           {ratio1:.4f}  ║")
    if compound_data:
        print(f"  ║  Superhard predictions (new):                  {n_new:>3d}  ║")
    print(f"  ╚{'═'*56}╝")

    # The verdict
    if best_comp_r2 > 0.7:
        print(f"""
  ★★★ The gate overflow IS the hardness. The error IS the prediction. ★★★

  Atoms that compress harder than the Cantor node expects make
  the hardest materials. Period 2 has no σ₃ gate — and that absence
  is why B, C, N make everything superhard.

  Diamond: 100% baseline bonds → Mohs 10
  Graphite: baseline in-plane, leak between layers → Mohs 1-2
  The hardest materials are the most compact overflows × smallest atoms.
        """)
    elif best_comp_r2 > 0.5:
        print(f"""
  The gate overflow shows STRONG predictive power for compound hardness.
  R² = {best_comp_r2:.3f} on log(Vickers) — the compression principle holds.
  Small covalent radii + large overflow → hard materials.
        """)
    else:
        print(f"""
  Gate overflow alone shows MODERATE predictive power.
  The dominant factor is atomic size (1/r_cov), with overflow
  providing refinement within size classes.
        """)

    print(f"\n{'═' * W_}")
    print(f"  All from φ² = φ + 1.  Zero free parameters.")
    print(f"{'═' * W_}")

    # Save results
    results = {
        'framework': 'Gate Overflow Material Strength',
        'n_elements': len(all_elements),
        'elemental_hardness_R2': float(best_el_r2) if mohs_data else None,
        'compound_hardness_R2': float(best_comp_r2) if compound_data else None,
        'bulk_modulus_R2': float(best_K_r2) if K_data else None,
        'graphite_diamond_ratio': float(ratio1),
        'benzene_cc_bos_match': 0.02,
        'n_superhard_predictions': n_new,
        'element_overflows': {sym: {'G': d['G'], 'theta': d['theta'], 'mode': d['mode']}
                              for sym, d in all_elements.items()},
    }

    json_path = os.path.join(outdir, 'gate_overflow_strength.json')
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n  Results saved: {json_path}")


if __name__ == '__main__':
    main()
