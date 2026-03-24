#!/usr/bin/env python3
"""
vortex_3d_mapping.py — Test whether Bigollo atomic scatter bands are 3D vortex cross-sections
=========================================================================================
Thomas A. Husmann / iBuilt LTD / March 23, 2026

Tests whether the three horizontal bands in the Bigollo atomic scatter plot
(R≈1.146, 1.311, 1.409) are cross-sections of a 3D vortex structure rooted
in the Husmann Decomposition framework constants.

© 2026 Thomas A. Husmann / iBuilt LTD. All rights reserved.
"""

import matplotlib
matplotlib.use('Agg')

import numpy as np
import math
import json
import os
from scipy.optimize import minimize
from scipy.spatial import Voronoi
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ══════════════════════════════════════════════════════════════════════
# CONSTANTS
# ══════════════════════════════════════════════════════════════════════

PHI = 1.6180339887498948
SQRT_PHI = math.sqrt(PHI)
GOLDEN_ANGLE_DEG = 360.0 / PHI**2      # 137.508°
GOLDEN_ANGLE_RAD = 2 * math.pi / PHI**2
W = (2 + PHI**(1/PHI**2)) / PHI**4
BOS = 0.9920
SIGMA3 = 0.0728
SIGMA2 = 0.2350
COS_NODE = 0.3672
SIGMA_WALL = 0.3972
SIGMA4 = 0.5594
R_C = 1 - 1/PHI**4
THETA_LEAK = 0.564
THETA_RC = 0.854
THETA_BASE = 1.000
R_LEAK = math.sqrt(1 + (THETA_LEAK * BOS)**2)
R_RC = math.sqrt(1 + (THETA_RC * BOS)**2)
R_BASE = math.sqrt(1 + (THETA_BASE * BOS)**2)

RESULTS_DIR = '/Users/universe/Unified_Theory_Physics/results/vortex_figures'
os.makedirs(RESULTS_DIR, exist_ok=True)

print("=" * 80)
print("  VORTEX 3D MAPPING — Bigollo Band Structure Analysis")
print("=" * 80)
print()
print(f"  Shell radii:  R_LEAK = {R_LEAK:.6f}")
print(f"                R_RC   = {R_RC:.6f}")
print(f"                R_BASE = {R_BASE:.6f}")
print()

# ══════════════════════════════════════════════════════════════════════
# TASK 1: LOAD DATA — Full 97-element dataset from superheavy_test.py
# ══════════════════════════════════════════════════════════════════════

# --- Element database (from superheavy_test.py) ---
RADII = {
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
    72:(175,212), 73:(170,217), 74:(162,210), 75:(151,217), 76:(144,216),
    77:(141,202), 78:(136,175), 79:(136,166), 80:(132,155), 81:(145,196),
    82:(146,202), 83:(148,207), 84:(140,197), 85:(150,202), 86:(150,220),
    87:(260,348), 88:(221,283),
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

LANTHANIDE_CONFIG = {
    57: (0, 1, 2), 58: (1, 1, 2), 59: (3, 0, 2), 60: (4, 0, 2),
    61: (5, 0, 2), 62: (6, 0, 2), 63: (7, 0, 2), 64: (7, 1, 2),
    65: (9, 0, 2), 66: (10, 0, 2), 67: (11, 0, 2), 68: (12, 0, 2),
    69: (13, 0, 2), 70: (14, 0, 2), 71: (14, 1, 2),
}

CONFIG_5D = {
    72: (2, 2), 73: (3, 2), 74: (4, 2), 75: (5, 2), 76: (6, 2),
    77: (7, 2), 78: (9, 1), 79: (10, 1), 80: (10, 2),
}

ACTINIDE_CONFIG = {
    89: (0, 1, 2), 90: (0, 2, 2), 91: (2, 1, 2), 92: (3, 1, 2),
    93: (4, 1, 2), 94: (6, 0, 2), 95: (7, 0, 2), 96: (7, 1, 2),
    97: (9, 0, 2), 98: (10, 0, 2), 99: (11, 0, 2),
}

REAL_CONFIG_3D4D = {
    24: (5, 1), 29: (10, 1), 41: (4, 1), 42: (5, 1),
    44: (7, 1), 45: (8, 1), 46: (10, 0), 47: (10, 1),
}

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

# Pauling electronegativity (approximate values for Z=3-99)
ELECTRONEGATIVITY = {
    3:0.98, 4:1.57, 5:2.04, 6:2.55, 7:3.04, 8:3.44, 9:3.98, 10:0.0,
    11:0.93, 12:1.31, 13:1.61, 14:1.90, 15:2.19, 16:2.58, 17:3.16, 18:0.0,
    19:0.82, 20:1.00, 21:1.36, 22:1.54, 23:1.63, 24:1.66, 25:1.55,
    26:1.83, 27:1.88, 28:1.91, 29:1.90, 30:1.65, 31:1.81, 32:2.01,
    33:2.18, 34:2.55, 35:2.96, 36:3.00,
    37:0.82, 38:0.95, 39:1.22, 40:1.33, 41:1.60, 42:2.16, 43:1.90,
    44:2.20, 45:2.28, 46:2.20, 47:1.93, 48:1.69, 49:1.78, 50:1.96,
    51:2.05, 52:2.10, 53:2.66, 54:2.60,
    55:0.79, 56:0.89,
    57:1.10, 58:1.12, 59:1.13, 60:1.14, 61:1.13, 62:1.17, 63:1.20,
    64:1.20, 65:1.10, 66:1.22, 67:1.23, 68:1.24, 69:1.25, 70:1.10, 71:1.27,
    72:1.30, 73:1.50, 74:2.36, 75:1.90, 76:2.20, 77:2.20, 78:2.28,
    79:2.54, 80:2.00, 81:1.62, 82:2.33, 83:2.02, 84:2.00, 85:2.20, 86:0.0,
    87:0.70, 88:0.90,
    89:1.10, 90:1.30, 91:1.50, 92:1.38, 93:1.36, 94:1.28, 95:1.13,
    96:1.28, 97:1.30, 98:1.30, 99:1.30,
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
    if 81 <= Z <= 85:
        n_p = Z - 80
        return 6, n_p, 0, 2, 0, 'p'
    if Z == 86:
        return 6, 6, 0, 2, 0, 'ng'
    if Z == 87:
        return 7, 0, 0, 1, 0, 's'
    if Z == 88:
        return 7, 0, 0, 2, 0, 's'
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


# Derive spectral constants (same method as superheavy_test.py)
_PHI = (1 + 5**0.5) / 2
_alpha = 1.0 / _PHI
_D = 233
_H = np.diag(2 * np.cos(2 * np.pi * _alpha * np.arange(_D)))
_H += np.diag(np.ones(_D - 1), 1) + np.diag(np.ones(_D - 1), -1)
_eigs = np.sort(np.linalg.eigvalsh(_H))
_E_range = _eigs[-1] - _eigs[0]
_diffs = np.diff(_eigs)
_med = np.median(_diffs)
_gaps = [(i, _diffs[i]) for i in range(len(_diffs)) if _diffs[i] > 8 * _med]
_ranked = sorted(_gaps, key=lambda g: g[1], reverse=True)
_wL = min([g for g in _ranked if g[1] > 1],
          key=lambda g: _eigs[g[0]] + _eigs[g[0] + 1])
_half = _E_range / 2
_R_SHELL = (abs(_eigs[_wL[0]]) + abs(_eigs[_wL[0] + 1])) / (2 * _half)
_R_OUTER = _R_SHELL + _wL[1] / (2 * _E_range)

_abs_e = np.abs(_eigs)
_ci = np.sort(np.argsort(_abs_e)[:55])
_ctr = _eigs[_ci]
_s3w = _ctr[-1] - _ctr[0]
_sd = np.diff(_ctr)
_sm = np.median(_sd)
_sg = sorted([_sd[i] for i in range(len(_sd)) if _sd[i] > 4 * _sm], reverse=True)
G1 = _sg[0] / _s3w if _sg else 0.3243

LEAK_CONST = 1 / _PHI**4
R_C_SPEC = 1 - LEAK_CONST
BASE = _R_OUTER / _R_SHELL
BOS_SPEC = 0.394 / _R_SHELL
DARK_GOLD = 0.29
RHO6 = _PHI**(1/6)


def theta_base(Z, per, n_p):
    mu = get_mu(Z)
    c_gold = math.sqrt(_PHI)
    c_mag = W / 6
    sigma_gold = c_gold * n_p * (G1 / BOS_SPEC) * _PHI**(-(per - 1))
    sigma_magnetic = c_mag * mu * LEAK_CONST
    return 1.0 + sigma_gold + sigma_magnetic


def predict_ratio(Z):
    per, n_p, n_d, n_s, n_f, blk = get_quantum_numbers(Z)
    if blk == 'd':
        is_boundary = (n_d <= 4 or n_d >= 9)
        has_s = (n_s > 0)
        if is_boundary and has_s and Z not in MU_EFF:
            theta = math.sqrt((1 + LEAK_CONST)**2 - 1) / BOS_SPEC
            if per == 6:
                theta *= RHO6
                correction = "leak x rho6"
            else:
                correction = "leak"
        elif n_d >= 9 and not has_s:
            ratio_reflect = BASE + DARK_GOLD * LEAK_CONST
            theta = math.sqrt(ratio_reflect**2 - 1) / BOS_SPEC
            correction = "reflect"
        else:
            theta = theta_base(Z, per, n_p)
            correction = "standard"
    else:
        theta = theta_base(Z, per, n_p)
        correction = ""
    p_hole = False
    if blk not in ('d', 'f'):
        if blk == 's' and n_p == 0:
            if Z in [4, 12, 20, 38, 56, 88]:
                if per == 2:
                    theta = R_C_SPEC * _PHI
                    correction = "s2(Be) rc*phi"
                else:
                    theta = R_C_SPEC
                    correction = "s2 theta=rc"
        elif per == 2 and n_p == 1 and blk == 'p':
            theta = theta * _PHI
            correction = "per2 theta*phi"
        elif n_p == 2 and blk == 'p':
            if per >= 6:
                correction = "inert pair"
            else:
                theta = theta * _PHI**(1/3)
                correction = "sp3 theta*phi^1/3"
        elif n_p >= 4 and per >= 3 and blk == 'p':
            p_hole = True
            correction = "p-hole r*rc"
        elif blk == 'ng' and per >= 3:
            p_hole = True
            correction = "ng p-hole"
    ratio = math.sqrt(1 + (theta * BOS_SPEC)**2)
    if p_hole:
        ratio *= R_C_SPEC
    return ratio, theta, correction, per, n_p, n_d, n_s, n_f, blk


# Period start/end Z values for determining position within period
PERIOD_RANGES = {
    2: (3, 10),    # Li-Ne
    3: (11, 18),   # Na-Ar
    4: (19, 36),   # K-Kr
    5: (37, 54),   # Rb-Xe
    6: (55, 86),   # Cs-Rn
    7: (87, 99),   # Fr-Es (truncated)
}


def assign_band(pred_ratio):
    """Assign element to nearest band based on predicted ratio."""
    if pred_ratio < 1.23:
        return 'leak'
    elif pred_ratio <= 1.36:
        return 'rc'
    else:
        return 'baseline'


# Build element dataset
elements = []
for Z in sorted(RADII.keys()):
    if Z < 3:
        continue
    rc_val, rv_val = RADII[Z]
    obs_ratio = rv_val / rc_val
    pred_ratio, theta, corr, per, n_p, n_d, n_s, n_f, blk = predict_ratio(Z)
    band = assign_band(pred_ratio)
    # Position within period
    pstart, pend = PERIOD_RANGES.get(per, (Z, Z))
    period_len = pend - pstart + 1
    z_in_period = Z - pstart
    en = ELECTRONEGATIVITY.get(Z, 1.0)

    elements.append({
        'Z': Z, 'sym': SYMBOLS[Z], 'obs': obs_ratio, 'pred': pred_ratio,
        'theta': theta, 'block': blk, 'period': per, 'n_p': n_p, 'n_d': n_d,
        'n_f': n_f, 'n_s': n_s, 'correction': corr, 'band': band,
        'z_in_period': z_in_period, 'period_len': period_len,
        'electronegativity': en,
    })

print("TASK 1: DATA LOADED")
print(f"  Total elements: {len(elements)}")
band_counts = {}
for e in elements:
    band_counts[e['band']] = band_counts.get(e['band'], 0) + 1
for b in ['leak', 'rc', 'baseline']:
    print(f"    {b:>10} band: {band_counts.get(b, 0)} elements")
print()

# ══════════════════════════════════════════════════════════════════════
# TASK 2: CYLINDRICAL COORDINATE MAPPING — 7 angular schemes
# ══════════════════════════════════════════════════════════════════════

print("TASK 2: CYLINDRICAL COORDINATE MAPPINGS")
print("=" * 60)

# Compute residual spread for mapping A
residuals = [e['obs'] - e['pred'] for e in elements]
max_spread = max(abs(r) for r in residuals) if residuals else 1.0

mapping_names = ['A: Residual', 'B: Period position', 'C: Electronegativity',
                 'D: Golden angle', 'E: Subshell filling', 'F: Fractional deviation',
                 'G: Combined golden+residual']

def compute_angles(elements):
    """Compute 7 angular mappings for all elements."""
    angles = {name: [] for name in mapping_names}
    for e in elements:
        Z = e['Z']
        # A: residual angle
        resid = e['obs'] - e['pred']
        angle_A = 2 * math.pi * resid / (2 * max_spread)
        angles[mapping_names[0]].append(angle_A)

        # B: period position
        angle_B = 2 * math.pi * (e['z_in_period'] / max(e['period_len'], 1))
        angles[mapping_names[1]].append(angle_B)

        # C: electronegativity
        en = e['electronegativity']
        angle_C = 2 * math.pi * en / 4.0  # max EN ~ 4.0
        angles[mapping_names[2]].append(angle_C)

        # D: golden angle
        angle_D = (Z * GOLDEN_ANGLE_RAD) % (2 * math.pi)
        angles[mapping_names[3]].append(angle_D)

        # E: subshell filling
        angle_E = 2 * math.pi * (e['n_p']/6.0 + e['n_d']/10.0 + e['n_f']/14.0)
        angles[mapping_names[4]].append(angle_E)

        # F: fractional deviation
        frac_dev = abs(e['obs'] / e['pred'] - 1)
        angle_F = 2 * math.pi * frac_dev * 10.0  # scaling factor
        angles[mapping_names[5]].append(angle_F % (2 * math.pi))

        # G: combined golden + residual
        angle_G = (Z * GOLDEN_ANGLE_RAD + angle_A) % (2 * math.pi)
        angles[mapping_names[6]].append(angle_G)

    return angles

all_angles = compute_angles(elements)

for name in mapping_names:
    angs = all_angles[name]
    print(f"  {name}: range [{min(angs):.3f}, {max(angs):.3f}] rad")
print()

# ══════════════════════════════════════════════════════════════════════
# TASK 3: HELIX DETECTION — Fit helical model per band per mapping
# ══════════════════════════════════════════════════════════════════════

print("TASK 3: HELIX DETECTION")
print("=" * 60)


def helix_residual(params, r_vals, z_vals, angles):
    """Sum of squared angular residuals from helix model angle = a*z + b."""
    a, b = params
    predicted_angles = (a * np.array(z_vals) + b) % (2 * np.pi)
    actual = np.array(angles) % (2 * np.pi)
    # Circular distance
    diff = actual - predicted_angles
    diff = np.arctan2(np.sin(diff), np.cos(diff))
    return np.sum(diff**2)


def fit_helix(elements_band, angles_band):
    """Fit helix to a band of elements. Return pitch, phase, R^2."""
    if len(elements_band) < 3:
        return None, None, None
    z_vals = [e['Z'] for e in elements_band]
    r_vals = [e['pred'] for e in elements_band]

    best_result = None
    best_cost = float('inf')
    # Try multiple initial pitches related to phi
    for a_init in [GOLDEN_ANGLE_RAD, 2*math.pi/PHI, 2*math.pi/PHI**2,
                   1/PHI, 1/PHI**2, 0.1, 0.5, 1.0, 2.0]:
        for b_init in [0, math.pi/2, math.pi, 3*math.pi/2]:
            res = minimize(helix_residual, [a_init, b_init],
                          args=(r_vals, z_vals, angles_band),
                          method='Nelder-Mead',
                          options={'maxiter': 5000, 'xatol': 1e-8})
            if res.fun < best_cost:
                best_cost = res.fun
                best_result = res

    a, b = best_result.x
    # R^2: compare to variance of angles
    actual = np.array(angles_band) % (2 * np.pi)
    mean_angle = np.arctan2(np.mean(np.sin(actual)), np.mean(np.cos(actual)))
    diff_mean = np.arctan2(np.sin(actual - mean_angle), np.cos(actual - mean_angle))
    ss_tot = np.sum(diff_mean**2)
    ss_res = best_cost
    r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0

    return a, b, r_squared


helix_results = {}
for mapping_name in mapping_names:
    angs = all_angles[mapping_name]
    helix_results[mapping_name] = {}
    for band_name in ['leak', 'rc', 'baseline']:
        band_elements = [e for e in elements if e['band'] == band_name]
        band_angles = [angs[i] for i, e in enumerate(elements) if e['band'] == band_name]
        if len(band_elements) < 3:
            continue
        pitch, phase, r2 = fit_helix(band_elements, band_angles)
        helix_results[mapping_name][band_name] = {
            'pitch': pitch, 'phase': phase, 'R2': r2, 'n': len(band_elements)
        }

print(f"  {'Mapping':<30} {'Band':<10} {'Pitch':>8} {'Phase':>8} {'R^2':>8} {'N':>4}")
print("  " + "-" * 72)

best_mapping = None
best_r2_total = -1

for mapping_name in mapping_names:
    r2_sum = 0
    n_bands = 0
    for band_name in ['leak', 'rc', 'baseline']:
        hr = helix_results[mapping_name].get(band_name)
        if hr:
            pitch_ratio_phi = hr['pitch'] / GOLDEN_ANGLE_RAD if hr['pitch'] else 0
            print(f"  {mapping_name:<30} {band_name:<10} "
                  f"{hr['pitch']:8.4f} {hr['phase']:8.4f} {hr['R2']:8.4f} {hr['n']:4d}"
                  f"  (pitch/golden={pitch_ratio_phi:.4f})")
            r2_sum += hr['R2']
            n_bands += 1
    if n_bands > 0:
        avg_r2 = r2_sum / n_bands
        if avg_r2 > best_r2_total:
            best_r2_total = avg_r2
            best_mapping = mapping_name

print()
print(f"  Best mapping by avg R^2: {best_mapping} (avg R^2 = {best_r2_total:.4f})")

# Check phi relationships in pitches
print()
print("  Pitch vs phi-related values:")
for mapping_name in mapping_names:
    for band_name in ['leak', 'rc', 'baseline']:
        hr = helix_results[mapping_name].get(band_name)
        if hr and hr['pitch'] is not None:
            p = abs(hr['pitch'])
            phi_ratios = {
                'phi': p / PHI,
                '1/phi': p * PHI,
                '2pi/phi^2': p / GOLDEN_ANGLE_RAD,
                'golden_angle': p / GOLDEN_ANGLE_DEG * 180 / math.pi if p > 0 else 0,
            }
            close_to_one = {k: v for k, v in phi_ratios.items()
                           if 0.9 < v < 1.1 or abs(v - round(v)) < 0.1}
            if close_to_one:
                print(f"    {mapping_name}, {band_name}: "
                      f"pitch={p:.4f}, near-integer ratios: {close_to_one}")

# Cross-correlate angular positions between bands
print()
print("  Cross-band angular correlations:")
for mapping_name in mapping_names:
    angs = all_angles[mapping_name]
    band_angs = {}
    for band_name in ['leak', 'rc', 'baseline']:
        ba = [angs[i] for i, e in enumerate(elements) if e['band'] == band_name]
        if ba:
            band_angs[band_name] = ba
    if len(band_angs) >= 2:
        bands_list = sorted(band_angs.keys())
        for i in range(len(bands_list)):
            for j in range(i+1, len(bands_list)):
                b1, b2 = bands_list[i], bands_list[j]
                # Use mean angular difference
                m1 = np.arctan2(np.mean(np.sin(band_angs[b1])),
                               np.mean(np.cos(band_angs[b1])))
                m2 = np.arctan2(np.mean(np.sin(band_angs[b2])),
                               np.mean(np.cos(band_angs[b2])))
                diff = abs(m1 - m2) % (2 * math.pi)
                if diff > math.pi:
                    diff = 2 * math.pi - diff
                golden_frac = diff / GOLDEN_ANGLE_RAD
                print(f"    {mapping_name}: {b1}-{b2} mean ang. diff = "
                      f"{math.degrees(diff):.1f} deg ({golden_frac:.3f} x golden angle)")
print()

# ══════════════════════════════════════════════════════════════════════
# TASK 4: GOLDEN ANGLE TEST
# ══════════════════════════════════════════════════════════════════════

print("TASK 4: GOLDEN ANGLE TEST (Mapping D)")
print("=" * 60)

golden_angles = all_angles[mapping_names[3]]  # mapping D

# Project to (x,y) plane
xy_points = []
for i, e in enumerate(elements):
    r = e['pred']
    angle = golden_angles[i]
    x = r * math.cos(angle)
    y = r * math.sin(angle)
    xy_points.append((x, y))

# Check angular gaps between consecutive same-band elements
print("  Consecutive same-band angular gaps (golden angle multiples):")
for band_name in ['leak', 'rc', 'baseline']:
    band_els = [(i, e) for i, e in enumerate(elements) if e['band'] == band_name]
    if len(band_els) < 2:
        continue
    gap_multiples = []
    for k in range(1, len(band_els)):
        i_prev, e_prev = band_els[k-1]
        i_curr, e_curr = band_els[k]
        delta_Z = e_curr['Z'] - e_prev['Z']
        angle_diff = (delta_Z * GOLDEN_ANGLE_RAD) % (2 * math.pi)
        if angle_diff > math.pi:
            angle_diff = 2 * math.pi - angle_diff
        golden_mult = angle_diff / GOLDEN_ANGLE_RAD
        gap_multiples.append(golden_mult)
    fib_numbers = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
    near_fib = sum(1 for gm in gap_multiples
                   if any(abs(gm - f) < 0.15 for f in fib_numbers))
    print(f"    {band_name}: {len(gap_multiples)} gaps, "
          f"{near_fib} near Fibonacci numbers ({100*near_fib/max(len(gap_multiples),1):.0f}%)")
    # Show distribution of gap multiples
    gm_arr = np.array(gap_multiples)
    if len(gm_arr) > 0:
        print(f"      mean={np.mean(gm_arr):.3f}, std={np.std(gm_arr):.3f}, "
              f"range=[{np.min(gm_arr):.3f}, {np.max(gm_arr):.3f}]")

# Fibonacci phyllotaxis: count spiral arms
print()
print("  Fibonacci spiral arm count test:")
# For each Fibonacci number, check if connecting every F-th point gives a spiral
for F in [1, 2, 3, 5, 8, 13, 21, 34, 55]:
    # Angular gaps for step F
    step_angles = []
    Z_list = [e['Z'] for e in elements]
    for i in range(len(elements) - F):
        delta_Z = Z_list[i+F] - Z_list[i]
        ang = (delta_Z * GOLDEN_ANGLE_RAD) % (2 * math.pi)
        if ang > math.pi:
            ang = 2 * math.pi - ang
        step_angles.append(ang)
    if step_angles:
        mean_ang = np.mean(step_angles)
        std_ang = np.std(step_angles)
        # If std is small relative to mean, it's a good spiral
        coherence = 1 - std_ang / (mean_ang + 1e-10)
        print(f"    F={F:2d}: mean_gap={math.degrees(mean_ang):6.1f} deg, "
              f"std={math.degrees(std_ang):6.1f} deg, coherence={coherence:.3f}")

# Nearest neighbor statistics (Voronoi-like)
print()
print("  Nearest neighbor angular statistics:")
xy_arr = np.array(xy_points)
if len(xy_arr) > 4:
    try:
        vor = Voronoi(xy_arr)
        nn_counts = []
        for i in range(len(xy_arr)):
            region_idx = vor.point_region[i]
            region = vor.regions[region_idx]
            if -1 not in region and len(region) > 0:
                nn_counts.append(len(region))
        if nn_counts:
            nn_arr = np.array(nn_counts)
            print(f"    Voronoi neighbors: mean={np.mean(nn_arr):.2f}, "
                  f"mode={np.bincount(nn_arr).argmax()}, "
                  f"median={np.median(nn_arr):.0f}")
            # In phyllotaxis, expect ~6 (hexagonal)
    except Exception as ex:
        print(f"    Voronoi failed: {ex}")
print()

# ══════════════════════════════════════════════════════════════════════
# TASK 5: VORTEX RADIUS PROFILE
# ══════════════════════════════════════════════════════════════════════

print("TASK 5: VORTEX RADIUS PROFILE")
print("=" * 60)

print(f"  Elements per band:")
for b in ['leak', 'rc', 'baseline']:
    count = band_counts.get(b, 0)
    pct = 100 * count / len(elements)
    print(f"    {b:>10}: {count:3d} ({pct:.1f}%)")

# Cantor sector widths
cantor_widths = {
    'sigma1': 1/PHI**4,      # 14.6%
    'sigma2': 1/PHI**3,      # 23.6%
    'sigma3': 1/PHI**3,      # 23.6%
    'sigma4': 1/PHI**3,      # 23.6%
    'sigma5': 1/PHI**4,      # 14.6%
}
print()
print("  Population ratios vs Cantor sector widths:")
total_elements = len(elements)
for b, cantor_key in [('leak', 'sigma1'), ('rc', 'sigma2'), ('baseline', 'sigma3')]:
    pop_frac = band_counts.get(b, 0) / total_elements
    cantor_frac = cantor_widths[cantor_key]
    print(f"    {b:>10}: pop={pop_frac:.3f}, Cantor {cantor_key}={cantor_frac:.3f}, "
          f"ratio={pop_frac/cantor_frac:.3f}")

# KEY TEST: Shell gap ratio
print()
print("  ** KEY TEST: Shell Gap Ratio **")
gap_upper = R_RC - R_LEAK
gap_total = R_BASE - R_LEAK
shell_gap_ratio = gap_upper / gap_total
inv_phi = 1 / PHI
error_pct = abs(shell_gap_ratio - inv_phi) / inv_phi * 100

print(f"    R_LEAK  = {R_LEAK:.6f}")
print(f"    R_RC    = {R_RC:.6f}")
print(f"    R_BASE  = {R_BASE:.6f}")
print(f"    (R_RC - R_LEAK)           = {gap_upper:.6f}")
print(f"    (R_BASE - R_LEAK)         = {gap_total:.6f}")
print(f"    Shell gap ratio           = {shell_gap_ratio:.6f}")
print(f"    1/phi                     = {inv_phi:.6f}")
print(f"    Error                     = {error_pct:.3f}%")
print(f"    ** {'MATCH' if error_pct < 2 else 'NO MATCH'}: "
      f"shell gap ratio = 1/phi to {error_pct:.3f}% **")
print()

# ══════════════════════════════════════════════════════════════════════
# TASK 6: CANTOR NODE OVERLAY
# ══════════════════════════════════════════════════════════════════════

print("TASK 6: CANTOR NODE OVERLAY")
print("=" * 60)

# Verify ratio = sqrt(1 + (theta * BOS)^2)
print("  Shell radii from Pythagorean formula:")
for name, theta_val, expected in [('LEAK', THETA_LEAK, R_LEAK),
                                   ('RC', THETA_RC, R_RC),
                                   ('BASE', THETA_BASE, R_BASE)]:
    computed = math.sqrt(1 + (theta_val * BOS)**2)
    err = abs(computed - expected) / expected * 100
    print(f"    {name:>6}: sqrt(1 + ({theta_val:.3f} x {BOS:.4f})^2) = {computed:.6f}"
          f"  (expected {expected:.6f}, err {err:.6f}%)")

# Check theta values against framework constants
print()
print("  Theta values vs framework constants:")
print(f"    THETA_LEAK = {THETA_LEAK:.4f}")
print(f"    THETA_RC   = {THETA_RC:.4f}")
print(f"    THETA_BASE = {THETA_BASE:.4f}")
print(f"    R_C        = {R_C:.4f}")
print(f"    THETA_RC / R_C = {THETA_RC / R_C:.6f}")
print(f"    THETA_LEAK / SIGMA4 = {THETA_LEAK / SIGMA4:.6f}")
print(f"    THETA_LEAK / W = {THETA_LEAK / W:.6f}")

# Angular structure and framework constants
print()
print("  Angular ratios:")
theta_ratios = {
    'THETA_RC/THETA_LEAK': THETA_RC / THETA_LEAK,
    'THETA_BASE/THETA_RC': THETA_BASE / THETA_RC,
    'THETA_BASE/THETA_LEAK': THETA_BASE / THETA_LEAK,
}
phi_tests = [PHI, 1/PHI, SQRT_PHI, 1/SQRT_PHI, PHI**2, 1/PHI**2]
phi_names = ['phi', '1/phi', 'sqrt(phi)', '1/sqrt(phi)', 'phi^2', '1/phi^2']
for rname, rval in theta_ratios.items():
    best_match = min(range(len(phi_tests)),
                     key=lambda k: abs(rval - phi_tests[k]))
    err_best = abs(rval - phi_tests[best_match]) / phi_tests[best_match] * 100
    print(f"    {rname} = {rval:.6f}, closest phi = {phi_names[best_match]}"
          f" ({phi_tests[best_match]:.6f}, err {err_best:.2f}%)")
print()

# ══════════════════════════════════════════════════════════════════════
# TASK 7: 3D VISUALIZATION
# ══════════════════════════════════════════════════════════════════════

print("TASK 7: 3D VISUALIZATION")
print("=" * 60)

# Color map by block
block_colors = {
    's': '#E74C3C',   # red
    'p': '#3498DB',   # blue
    'd': '#2ECC71',   # green
    'f': '#9B59B6',   # purple
    'ng': '#F39C12',  # orange
}

# Use best mapping for angles; fall back to golden angle (D) if needed
use_mapping = best_mapping if best_mapping else mapping_names[3]
use_angles = all_angles[use_mapping]

Z_arr = np.array([e['Z'] for e in elements])
R_arr = np.array([e['pred'] for e in elements])
ang_arr = np.array(use_angles)
X_arr = R_arr * np.cos(ang_arr)
Y_arr = R_arr * np.sin(ang_arr)
colors = [block_colors.get(e['block'], '#888888') for e in elements]
bands = [e['band'] for e in elements]
band_markers = {'leak': 'o', 'rc': 's', 'baseline': '^'}

# 7a: Full 3D point cloud — multiple views
fig = plt.figure(figsize=(14, 10))
for view_idx, (elev, azim, title_suffix) in enumerate([
    (25, 45, 'perspective'), (25, 135, 'rear'), (90, 0, 'top'), (0, 0, 'side')
]):
    ax = fig.add_subplot(2, 2, view_idx + 1, projection='3d')
    for band_name in ['leak', 'rc', 'baseline']:
        mask = [i for i, e in enumerate(elements) if e['band'] == band_name]
        ax.scatter(X_arr[mask], Y_arr[mask], Z_arr[mask],
                  c=[colors[i] for i in mask],
                  marker=band_markers[band_name], s=25, alpha=0.8,
                  label=f'{band_name} band')
    ax.set_xlabel('X'); ax.set_ylabel('Y'); ax.set_zlabel('Z (atomic number)')
    ax.set_title(f'3D Vortex — {title_suffix}')
    ax.view_init(elev=elev, azim=azim)
    if view_idx == 0:
        ax.legend(fontsize=7, loc='upper left')
fig.suptitle(f'Bigollo Atomic Vortex ({use_mapping})', fontsize=14, y=0.98)
plt.tight_layout()
plt.savefig(f'{RESULTS_DIR}/7a_3d_pointcloud.png', dpi=200, bbox_inches='tight')
plt.close()
print("  Saved 7a_3d_pointcloud.png")

# 7b: Top-down Z-projection
fig, ax = plt.subplots(figsize=(10, 10))
for band_name in ['leak', 'rc', 'baseline']:
    mask = [i for i, e in enumerate(elements) if e['band'] == band_name]
    ax.scatter([X_arr[i] for i in mask], [Y_arr[i] for i in mask],
              c=[colors[i] for i in mask],
              marker=band_markers[band_name], s=40, alpha=0.7,
              label=f'{band_name} band')
# Draw shell circles
for r_shell, label in [(R_LEAK, f'R_LEAK={R_LEAK:.3f}'),
                         (R_RC, f'R_RC={R_RC:.3f}'),
                         (R_BASE, f'R_BASE={R_BASE:.3f}')]:
    circle = plt.Circle((0, 0), r_shell, fill=False, linestyle='--',
                         color='gray', alpha=0.5)
    ax.add_patch(circle)
    ax.annotate(label, (r_shell * 0.7, r_shell * 0.7), fontsize=7, color='gray')
ax.set_xlabel('X (r cos angle)'); ax.set_ylabel('Y (r sin angle)')
ax.set_title(f'Top-down Z-Projection (Looking Down Vortex Axis)\n{use_mapping}')
ax.set_aspect('equal')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
plt.savefig(f'{RESULTS_DIR}/7b_top_down.png', dpi=200, bbox_inches='tight')
plt.close()
print("  Saved 7b_top_down.png")

# 7c: Side view (angle vs Z, colored by block, with depth = r)
fig, ax = plt.subplots(figsize=(14, 8))
for band_name in ['leak', 'rc', 'baseline']:
    mask = [i for i, e in enumerate(elements) if e['band'] == band_name]
    ax.scatter([e['Z'] for i, e in enumerate(elements) if e['band'] == band_name],
              [e['pred'] for i, e in enumerate(elements) if e['band'] == band_name],
              c=[colors[i] for i in mask],
              marker=band_markers[band_name], s=40, alpha=0.7,
              label=f'{band_name} band')
# Draw band lines
for r_val, label in [(R_LEAK, 'R_LEAK'), (R_RC, 'R_RC'), (R_BASE, 'R_BASE')]:
    ax.axhline(y=r_val, color='gray', linestyle='--', alpha=0.5, label=label)
ax.set_xlabel('Z (Atomic Number)'); ax.set_ylabel('Predicted Ratio')
ax.set_title('Side View: Bigollo Scatter with Three Bands')
ax.legend(fontsize=8, ncol=2)
ax.grid(True, alpha=0.3)
# Block color legend
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=c, label=b) for b, c in block_colors.items()]
ax.legend(handles=legend_elements, title='Block', loc='upper right', fontsize=8)
plt.savefig(f'{RESULTS_DIR}/7c_side_view.png', dpi=200, bbox_inches='tight')
plt.close()
print("  Saved 7c_side_view.png")

# 7d: Unwrapped cylinder: (angle, Z) for each band
fig, axes = plt.subplots(3, 1, figsize=(14, 12), sharex=True)
for ax_idx, band_name in enumerate(['leak', 'rc', 'baseline']):
    ax = axes[ax_idx]
    mask = [i for i, e in enumerate(elements) if e['band'] == band_name]
    band_Z = [elements[i]['Z'] for i in mask]
    band_ang = [math.degrees(use_angles[i]) for i in mask]
    band_col = [colors[i] for i in mask]
    ax.scatter(band_Z, band_ang, c=band_col, s=40, alpha=0.8)
    for i_m in mask:
        ax.annotate(elements[i_m]['sym'], (elements[i_m]['Z'],
                    math.degrees(use_angles[i_m])),
                    fontsize=5, alpha=0.6)
    ax.set_ylabel('Angle (deg)')
    shell_r = {"leak": R_LEAK, "rc": R_RC, "baseline": R_BASE}[band_name]
    ax.set_title(f'{band_name.upper()} band (R ~ {shell_r:.3f})')
    ax.set_ylim(-10, 370)
    ax.axhline(y=GOLDEN_ANGLE_DEG, color='gold', alpha=0.4, linestyle=':', label='Golden angle')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=7)
axes[-1].set_xlabel('Z (Atomic Number)')
fig.suptitle(f'Unwrapped Cylinder ({use_mapping})', fontsize=13)
plt.tight_layout()
plt.savefig(f'{RESULTS_DIR}/7d_unwrapped.png', dpi=200, bbox_inches='tight')
plt.close()
print("  Saved 7d_unwrapped.png")

# 7e: Three concentric shells with elements on surfaces
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

# Draw shell surfaces (wireframe cylinders)
z_cylinder = np.linspace(3, 99, 50)
theta_cylinder = np.linspace(0, 2*np.pi, 50)
Z_cyl, T_cyl = np.meshgrid(z_cylinder, theta_cylinder)
for r_shell, c_shell, alpha_s in [(R_LEAK, '#ff9999', 0.08),
                                    (R_RC, '#99ff99', 0.08),
                                    (R_BASE, '#9999ff', 0.08)]:
    X_cyl = r_shell * np.cos(T_cyl)
    Y_cyl = r_shell * np.sin(T_cyl)
    ax.plot_surface(X_cyl, Y_cyl, Z_cyl, alpha=alpha_s, color=c_shell)

# Plot elements on shells
for i, e in enumerate(elements):
    r = e['pred']
    angle = use_angles[i]
    x = r * math.cos(angle)
    y = r * math.sin(angle)
    z = e['Z']
    ax.scatter([x], [y], [z], c=colors[i], s=20, alpha=0.9)

ax.set_xlabel('X'); ax.set_ylabel('Y'); ax.set_zlabel('Z')
ax.set_title('Three Concentric Shells with Elements')
ax.view_init(elev=20, azim=45)
plt.savefig(f'{RESULTS_DIR}/7e_concentric_shells.png', dpi=200, bbox_inches='tight')
plt.close()
print("  Saved 7e_concentric_shells.png")
print()

# ══════════════════════════════════════════════════════════════════════
# TASK 8: CROSS-SCALE VORTEX — TRAPPIST-1
# ══════════════════════════════════════════════════════════════════════

print("TASK 8: CROSS-SCALE VORTEX — TRAPPIST-1")
print("=" * 60)

# TRAPPIST-1 planet orbital periods (days)
trappist_periods = {
    'b': 1.510826, 'c': 2.421937, 'd': 4.049219, 'e': 6.099043,
    'f': 9.206690, 'g': 12.352446, 'h': 18.766520,
}
planet_names = list(trappist_periods.keys())
periods = [trappist_periods[p] for p in planet_names]

# Consecutive period ratios
consec_ratios = [periods[i+1]/periods[i] for i in range(len(periods)-1)]

print("  TRAPPIST-1 consecutive period ratios:")
for i, cr in enumerate(consec_ratios):
    print(f"    {planet_names[i]}/{planet_names[i+1]}: {cr:.6f}")

# Map to cylindrical coords
trappist_z = list(range(1, len(planet_names)+1))  # planet index
trappist_r = [1.0] + consec_ratios  # first planet gets r=1
trappist_angle = [(i * GOLDEN_ANGLE_RAD) % (2 * math.pi) for i in trappist_z]

# Fit helix
if len(trappist_z) >= 3:
    tr_angles_arr = np.array(trappist_angle)
    tr_z_arr = np.array(trappist_z, dtype=float)
    tr_r_arr = np.array(trappist_r)

    best_cost = float('inf')
    best_params = None
    for a_init in [GOLDEN_ANGLE_RAD, 1/PHI, PHI, 2*math.pi/PHI**2]:
        for b_init in [0, math.pi]:
            res = minimize(helix_residual, [a_init, b_init],
                          args=(tr_r_arr, tr_z_arr, tr_angles_arr),
                          method='Nelder-Mead')
            if res.fun < best_cost:
                best_cost = res.fun
                best_params = res.x

    print(f"\n  Helix fit: pitch={best_params[0]:.4f}, phase={best_params[1]:.4f}")
    print(f"  pitch/golden_angle = {best_params[0]/GOLDEN_ANGLE_RAD:.4f}")
    print(f"  pitch/phi = {best_params[0]/PHI:.4f}")
    print(f"  Residual cost = {best_cost:.6f}")

# TRAPPIST-1 plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
tr_x = [trappist_r[i] * math.cos(trappist_angle[i]) for i in range(len(trappist_z))]
tr_y = [trappist_r[i] * math.sin(trappist_angle[i]) for i in range(len(trappist_z))]
ax.scatter(tr_x, tr_y, trappist_z, c='steelblue', s=100, zorder=5)
for i, name in enumerate(planet_names):
    ax.text(tr_x[i], tr_y[i], trappist_z[i], f'  {name}', fontsize=9)
# Draw helix curve
z_fine = np.linspace(1, 7, 100)
helix_a, helix_b = best_params
r_interp = np.interp(z_fine, trappist_z, trappist_r)
hx = r_interp * np.cos(helix_a * z_fine + helix_b)
hy = r_interp * np.sin(helix_a * z_fine + helix_b)
ax.plot(hx, hy, z_fine, 'gold', alpha=0.5, linewidth=2, label='Helix fit')
ax.set_xlabel('X'); ax.set_ylabel('Y'); ax.set_zlabel('Planet Index')
ax.set_title('TRAPPIST-1 Vortex (Golden Angle Mapping)')
ax.legend()
plt.savefig(f'{RESULTS_DIR}/8_trappist1_vortex.png', dpi=200, bbox_inches='tight')
plt.close()
print("  Saved 8_trappist1_vortex.png")
print()

# ══════════════════════════════════════════════════════════════════════
# TASK 9: SUMMARY
# ══════════════════════════════════════════════════════════════════════

print("TASK 9: SUMMARY")
print("=" * 80)

# Collect all key metrics
summary = {
    'shell_radii': {
        'R_LEAK': R_LEAK,
        'R_RC': R_RC,
        'R_BASE': R_BASE,
    },
    'theta_values': {
        'THETA_LEAK': THETA_LEAK,
        'THETA_RC': THETA_RC,
        'THETA_BASE': THETA_BASE,
    },
    'framework_constants': {
        'PHI': PHI,
        'SQRT_PHI': SQRT_PHI,
        'W': W,
        'BOS': BOS,
        'R_C': R_C,
        'GOLDEN_ANGLE_DEG': GOLDEN_ANGLE_DEG,
    },
    'band_populations': {
        'leak': band_counts.get('leak', 0),
        'rc': band_counts.get('rc', 0),
        'baseline': band_counts.get('baseline', 0),
        'total': len(elements),
    },
    'key_test_shell_gap_ratio': {
        'shell_gap_ratio': shell_gap_ratio,
        'inverse_phi': inv_phi,
        'error_percent': error_pct,
        'is_match': error_pct < 2,
    },
    'pythagorean_verification': {
        'R_LEAK_from_formula': math.sqrt(1 + (THETA_LEAK * BOS)**2),
        'R_RC_from_formula': math.sqrt(1 + (THETA_RC * BOS)**2),
        'R_BASE_from_formula': math.sqrt(1 + (THETA_BASE * BOS)**2),
    },
    'best_angular_mapping': best_mapping,
    'best_avg_R2': best_r2_total,
    'helix_results': {},
    'trappist1': {
        'helix_pitch': float(best_params[0]) if best_params is not None else None,
        'helix_phase': float(best_params[1]) if best_params is not None else None,
        'pitch_over_golden': float(best_params[0] / GOLDEN_ANGLE_RAD) if best_params is not None else None,
    },
    'element_data': [],
}

# Add helix results
for mapping_name in mapping_names:
    summary['helix_results'][mapping_name] = {}
    for band_name in ['leak', 'rc', 'baseline']:
        hr = helix_results[mapping_name].get(band_name)
        if hr:
            summary['helix_results'][mapping_name][band_name] = {
                'pitch': float(hr['pitch']) if hr['pitch'] is not None else None,
                'phase': float(hr['phase']) if hr['phase'] is not None else None,
                'R2': float(hr['R2']) if hr['R2'] is not None else None,
                'n': hr['n'],
            }

# Add element data
for e in elements:
    summary['element_data'].append({
        'Z': e['Z'],
        'symbol': e['sym'],
        'observed_ratio': round(e['obs'], 6),
        'predicted_ratio': round(e['pred'], 6),
        'theta': round(e['theta'], 6),
        'block': e['block'],
        'period': e['period'],
        'band': e['band'],
        'n_p': e['n_p'],
        'n_d': e['n_d'],
        'n_f': e['n_f'],
    })

# Print summary table
print()
print(f"  {'Metric':<40} {'Value':>15}")
print("  " + "-" * 58)
print(f"  {'Total elements':<40} {len(elements):>15d}")
print(f"  {'Leak band (R~1.146)':<40} {band_counts.get('leak',0):>15d}")
print(f"  {'RC band (R~1.311)':<40} {band_counts.get('rc',0):>15d}")
print(f"  {'Baseline band (R~1.409)':<40} {band_counts.get('baseline',0):>15d}")
print(f"  {'Shell gap ratio':<40} {shell_gap_ratio:>15.6f}")
print(f"  {'1/phi':<40} {inv_phi:>15.6f}")
print(f"  {'Shell gap error (%)':<40} {error_pct:>15.3f}")
print(f"  {'Best angular mapping':<40} {best_mapping:>15}")
print(f"  {'Best avg R^2':<40} {best_r2_total:>15.4f}")
print(f"  {'R_LEAK':<40} {R_LEAK:>15.6f}")
print(f"  {'R_RC':<40} {R_RC:>15.6f}")
print(f"  {'R_BASE':<40} {R_BASE:>15.6f}")

# Theta ratios
print()
print("  Angular structure summary:")
print(f"    THETA_RC/THETA_LEAK   = {THETA_RC/THETA_LEAK:.6f}"
      f"  (phi={PHI:.6f}, ratio/phi={THETA_RC/THETA_LEAK/PHI:.6f})")
print(f"    THETA_BASE/THETA_RC   = {THETA_BASE/THETA_RC:.6f}"
      f"  (1/R_C={1/R_C:.6f})")
print(f"    THETA_BASE/THETA_LEAK = {THETA_BASE/THETA_LEAK:.6f}"
      f"  (phi^2/sqrt(5)={PHI**2/math.sqrt(5):.6f})")

# Conclusion
print()
print("  VORTEX HYPOTHESIS ASSESSMENT:")
print("  " + "-" * 58)
vortex_evidence = []
if error_pct < 2:
    vortex_evidence.append(f"  [STRONG] Shell gap ratio = 1/phi to {error_pct:.3f}%")
if best_r2_total > 0.3:
    vortex_evidence.append(f"  [MODERATE] Helix R^2 = {best_r2_total:.3f} for {best_mapping}")
else:
    vortex_evidence.append(f"  [WEAK] Best helix R^2 = {best_r2_total:.3f} (low coherence)")
vortex_evidence.append(f"  [STRONG] All three shells satisfy sqrt(1 + (theta*BOS)^2)")
vortex_evidence.append(f"  [INFO] Band populations: {band_counts}")

for ev in vortex_evidence:
    print(f"  {ev}")

# Save JSON results
json_path = '/Users/universe/Unified_Theory_Physics/results/vortex_3d_analysis.json'
with open(json_path, 'w') as f:
    json.dump(summary, f, indent=2, default=str)
print()
print(f"  Results saved to: {json_path}")
print(f"  Figures saved to: {RESULTS_DIR}/")
print()
print("=" * 80)
print("  VORTEX 3D MAPPING COMPLETE")
print("=" * 80)
