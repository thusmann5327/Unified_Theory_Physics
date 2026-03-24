#!/usr/bin/env python3
"""
vortex_explorer.py — What coordinate system reveals the vortex?
═══════════════════════════════════════════════════════════════
The original Bigollo diagram uses:
  x = ratio × cos(Z × golden_angle)
  y = ratio × sin(Z × golden_angle)
  z = Z (atomic number — sequential, not physical)

Problem: Z is just counting. It doesn't encode a property.
Question: What if we replace Z with something that correlates
to a physical property? Does a tighter vortex emerge?

Candidates for the vertical axis:
  1. Electronegativity (EN)     — smoothly varies across periods
  2. r_norm (Fibonacci remainder) — position within Fibonacci shell
  3. 1/r_cov                    — inverse size (compactness)
  4. Gate overflow G             — how far cloud extends past prediction
  5. Period + fractional position — encodes shell structure
  6. Ionization energy proxy     — θ × Ry / r_cov

Candidates for the radius:
  1. predicted ratio (current)
  2. 1/r_cov (smaller atoms → larger radius)
  3. EN (more reactive → further out)
  4. θ (mode parameter)
  5. observed ratio (let the data speak)

We test all combinations and measure vortex coherence by:
  - Helix R² (how well angle = a×z + b fits)
  - Radial variance within bands (tighter = better)
  - Nearest-neighbor angular order (spiral vs random)

Thomas A. Husmann / iBuilt LTD — March 2026
═══════════════════════════════════════════════════════════════
"""

import matplotlib
matplotlib.use('Agg')

import numpy as np
import math
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ═══════════════════════════════════════════════════════════════
# FRAMEWORK CONSTANTS
# ═══════════════════════════════════════════════════════════════

PHI = (1 + math.sqrt(5)) / 2
PHI2 = PHI**2; PHI3 = PHI**3; PHI4 = PHI**4
GOLDEN_ANGLE_RAD = 2 * math.pi / PHI2
W = (2 + PHI**(1/PHI**2)) / PHI4
BOS = 0.992022
LEAK = 1/PHI4
R_C = 1 - LEAK
G1 = 0.3243
DARK_GOLD = 0.290
SIGMA3 = 0.0728
BASE = 1.408382
RY_EV = 13.6057

THETA_LEAK = 0.564; THETA_RC = 0.854; THETA_BASE = 1.000
R_LEAK = math.sqrt(1 + (THETA_LEAK * BOS)**2)
R_RC = math.sqrt(1 + (THETA_RC * BOS)**2)
R_BASE = math.sqrt(1 + (THETA_BASE * BOS)**2)

MU_EFF = {26: 2.22, 27: 1.72, 28: 0.62}
REAL_CONFIG = {24:(5,1), 29:(10,1), 41:(4,1), 42:(5,1),
               44:(7,1), 45:(8,1), 46:(10,0), 47:(10,1)}

# ═══════════════════════════════════════════════════════════════
# ELEMENT DATA
# ═══════════════════════════════════════════════════════════════

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
    53:(139,198),54:(140,216),55:(244,343),56:(215,268),
    57:(187,240),72:(175,212),73:(170,217),74:(162,193),75:(151,217),
    76:(144,216),77:(141,202),78:(136,209),79:(136,166),80:(132,209),
    81:(145,196),82:(146,202),83:(148,207)
}

SYMBOLS = {
    1:'H',2:'He',3:'Li',4:'Be',5:'B',6:'C',7:'N',8:'O',9:'F',10:'Ne',
    11:'Na',12:'Mg',13:'Al',14:'Si',15:'P',16:'S',17:'Cl',18:'Ar',
    19:'K',20:'Ca',21:'Sc',22:'Ti',23:'V',24:'Cr',25:'Mn',26:'Fe',
    27:'Co',28:'Ni',29:'Cu',30:'Zn',31:'Ga',32:'Ge',33:'As',34:'Se',
    35:'Br',36:'Kr',37:'Rb',38:'Sr',39:'Y',40:'Zr',41:'Nb',42:'Mo',
    43:'Tc',44:'Ru',45:'Rh',46:'Pd',47:'Ag',48:'Cd',49:'In',50:'Sn',
    51:'Sb',52:'Te',53:'I',54:'Xe',55:'Cs',56:'Ba',57:'La',
    72:'Hf',73:'Ta',74:'W',75:'Re',76:'Os',77:'Ir',78:'Pt',
    79:'Au',80:'Hg',81:'Tl',82:'Pb',83:'Bi'
}

EN_PAULING = {
    1:2.20,2:0.00,3:0.98,4:1.57,5:2.04,6:2.55,7:3.04,8:3.44,9:3.98,10:0.00,
    11:0.93,12:1.31,13:1.61,14:1.90,15:2.19,16:2.58,17:3.16,18:0.00,
    19:0.82,20:1.00,21:1.36,22:1.54,23:1.63,24:1.66,25:1.55,26:1.83,
    27:1.88,28:1.91,29:1.90,30:1.65,31:1.81,32:2.01,33:2.18,34:2.55,
    35:2.96,36:0.00,37:0.82,38:0.95,39:1.22,40:1.33,41:1.60,42:2.16,
    43:1.90,44:2.20,45:2.28,46:2.20,47:1.93,48:1.69,49:1.78,50:1.96,
    51:2.05,52:2.10,53:2.66,54:0.00,55:0.79,56:0.89,57:1.10,
    72:1.30,73:1.50,74:2.36,75:1.90,76:2.20,77:2.20,78:2.28,
    79:2.54,80:2.00,81:1.62,82:2.33,83:2.02
}

# First ionization energies (eV)
IE1 = {
    1:13.60,2:24.59,3:5.39,4:9.32,5:8.30,6:11.26,7:14.53,8:13.62,9:17.42,10:21.56,
    11:5.14,12:7.65,13:5.99,14:8.15,15:10.49,16:10.36,17:12.97,18:15.76,
    19:4.34,20:6.11,21:6.56,22:6.83,23:6.75,24:6.77,25:7.43,26:7.90,
    27:7.88,28:7.64,29:7.73,30:9.39,31:6.00,32:7.90,33:9.79,34:9.75,
    35:11.81,36:14.00,37:4.18,38:5.69,39:6.22,40:6.63,41:6.76,42:7.09,
    43:7.28,44:7.36,45:7.46,46:8.34,47:7.58,48:8.99,49:5.79,50:7.34,
    51:8.64,52:9.01,53:10.45,54:12.13,55:3.89,56:5.21,57:5.58,
    72:6.83,73:7.55,74:7.86,75:7.83,76:8.44,77:8.97,78:8.96,
    79:9.23,80:10.44,81:6.11,82:7.42,83:7.29
}

FIBS = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233]

def nearest_fib_shell(Z):
    shell = 1
    for f in FIBS:
        if f <= Z: shell = f
        else: break
    return shell

# ═══════════════════════════════════════════════════════════════
# AUFBAU + PREDICT_RATIO
# ═══════════════════════════════════════════════════════════════

def aufbau(Z):
    sub = []
    for n in range(1, 8):
        for l in range(n):
            sub.append((n, l, 2*(2*l+1)))
    sub.sort(key=lambda s: (s[0]+s[1], s[0]))
    rem = Z; filled = []
    for n, l, cap in sub:
        if rem <= 0: break
        e = min(rem, cap); filled.append((n, l, e, cap)); rem -= e
    per = max(n for n,l,e,c in filled)
    n_p = sum(e for n,l,e,c in filled if n == per and l == 1)
    n_d_val = sum(e for n,l,e,c in filled if l == 2 and n == per-1)
    n_s_val = sum(e for n,l,e,c in filled if n == per and l == 0)
    last_l = filled[-1][1]
    blk = {0:'s',1:'p',2:'d',3:'f'}.get(last_l, '?')
    se = {}; sm2 = {}
    for n,l,e,cap in filled:
        se[n] = se.get(n,0)+e; sm2[n] = sm2.get(n,0)+cap
    if se.get(per,0) == sm2.get(per,0):
        if Z == 2 or (last_l == 1 and filled[-1][2] == filled[-1][3]):
            blk = 'ng'
            if Z == 2: n_p = 0
    n_d = 0 if blk in ('p','s','ng') else n_d_val
    n_s = n_s_val
    if Z in REAL_CONFIG and blk == 'd':
        n_d, n_s = REAL_CONFIG[Z]
    return per, n_p, n_d, n_s, blk

def predict_ratio(Z):
    per, n_p, n_d, n_s, block = aufbau(Z)
    if block == 'd':
        if Z in MU_EFF:
            mu = MU_EFF[Z]
            theta = 1 - (n_d/10)*DARK_GOLD + mu * LEAK
            return math.sqrt(1+(theta*BOS)**2), theta, per, n_p, n_d, n_s, block, "magnetic"
        is_boundary = (n_d <= 4 or n_d >= 9)
        has_s = (n_s > 0)
        if is_boundary and has_s:
            return 1+LEAK, THETA_LEAK, per, n_p, n_d, n_s, block, "leak"
        elif n_d >= 9 and not has_s:
            return BASE+DARK_GOLD*LEAK, THETA_BASE, per, n_p, n_d, n_s, block, "reflect"
        else:
            theta = 1 - (n_d/10)*DARK_GOLD
            return math.sqrt(1+(theta*BOS)**2), theta, per, n_p, n_d, n_s, block, "standard"
    elif block == 'ng':
        theta = 1 + n_p*(G1/BOS)*PHI**(-(per-1))
        return math.sqrt(1+(theta*BOS)**2), theta, per, n_p, n_d, n_s, block, "pythagorean"
    else:
        ratio = BASE + n_p*G1*PHI**(-(per-1))
        theta = ratio / BASE
        if block == 'p' and n_p >= 4 and per >= 3:
            ratio *= R_C
            return ratio, theta, per, n_p, n_d, n_s, block, "p-hole"
        return ratio, theta, per, n_p, n_d, n_s, block, "additive"


# ═══════════════════════════════════════════════════════════════
# BUILD ELEMENT DATABASE
# ═══════════════════════════════════════════════════════════════

elements = []
for Z in sorted(RADII.keys()):
    sym = SYMBOLS.get(Z)
    if not sym: continue
    r_cov, r_vdw = RADII[Z]
    ratio_obs = r_vdw / r_cov
    rp, theta, per, n_p, n_d, n_s, block, mode = predict_ratio(Z)
    G = (ratio_obs - rp) / rp * 100
    fib_shell = nearest_fib_shell(Z)
    remainder = Z - fib_shell
    r_norm = remainder / fib_shell if fib_shell > 0 else 0
    en = EN_PAULING.get(Z, 1.0)
    ie = IE1.get(Z, 7.0)

    elements.append({
        'Z': Z, 'sym': sym, 'r_cov': r_cov, 'r_vdw': r_vdw,
        'ratio_obs': ratio_obs, 'ratio_pred': rp, 'theta': theta,
        'per': per, 'n_p': n_p, 'n_d': n_d, 'n_s': n_s,
        'block': block, 'mode': mode, 'G': G,
        'fib_shell': fib_shell, 'remainder': remainder, 'r_norm': r_norm,
        'en': en, 'ie': ie,
    })

N = len(elements)
print(f"  {N} elements loaded\n")


# ═══════════════════════════════════════════════════════════════
# DEFINE COORDINATE MAPPINGS
# ═══════════════════════════════════════════════════════════════

def helix_r2(angles, z_vals):
    """How well does angle = a*z + b fit? (circular R²)"""
    if len(angles) < 4:
        return 0.0
    from scipy.optimize import minimize
    angles = np.array(angles)
    z_vals = np.array(z_vals, float)

    def cost(params):
        a, b = params
        pred = (a * z_vals + b) % (2*np.pi)
        diff = np.arctan2(np.sin(angles - pred), np.cos(angles - pred))
        return np.sum(diff**2)

    best = float('inf')
    for a0 in [GOLDEN_ANGLE_RAD, 2*math.pi/PHI, 1/PHI, 0.5, 1.0, 2.0]:
        for b0 in [0, math.pi/2, math.pi]:
            res = minimize(cost, [a0, b0], method='Nelder-Mead',
                          options={'maxiter':3000})
            if res.fun < best:
                best = res.fun

    # SS_tot
    mean_a = np.arctan2(np.mean(np.sin(angles)), np.mean(np.cos(angles)))
    diff_m = np.arctan2(np.sin(angles - mean_a), np.cos(angles - mean_a))
    ss_tot = np.sum(diff_m**2)
    return max(0, 1 - best / ss_tot) if ss_tot > 0 else 0


# ── Axis candidates ──
# For the "vertical" (progression) axis:
def get_z_candidates(el):
    """Return dict of candidate z-axis values."""
    return {
        'Z (atomic number)': el['Z'],
        'EN (electronegativity)': el['en'],
        'IE (ionization energy)': el['ie'],
        '1/r_cov (compactness)': 1000.0 / el['r_cov'],  # scaled
        'r_norm (Fibonacci rem)': el['r_norm'],
        'θ (mode parameter)': el['theta'],
        'G (gate overflow)': el['G'],
        'per + frac_pos': el['per'] + el['n_p']/8 + el['n_d']/12,
        'log(IE)': math.log(el['ie']) if el['ie'] > 0 else 0,
        'EN × r_norm': el['en'] * (el['r_norm'] + 0.1),
    }

# For the radial axis:
def get_r_candidates(el):
    """Return dict of candidate radius values."""
    return {
        'ratio_pred (current)': el['ratio_pred'],
        'ratio_obs': el['ratio_obs'],
        'θ': el['theta'],
        '1/r_cov': 100.0 / el['r_cov'],
        'EN/4': el['en'] / 4.0 if el['en'] > 0 else 0.1,
        'sqrt(IE/Ry)': math.sqrt(el['ie'] / RY_EV),
        'r_norm + 0.5': el['r_norm'] + 0.5,
    }

# For the angle:
def get_angle_candidates(el):
    return {
        'Z × golden (current)': (el['Z'] * GOLDEN_ANGLE_RAD) % (2*math.pi),
        'Z × 2π/φ': (el['Z'] * 2*math.pi/PHI) % (2*math.pi),
        'EN × 2π/4': (el['en'] * 2*math.pi / 4.0) % (2*math.pi),
        'IE × golden/Ry': (el['ie'] / RY_EV * GOLDEN_ANGLE_RAD * 10) % (2*math.pi),
        'r_norm × 2π': (el['r_norm'] * 2*math.pi) % (2*math.pi),
    }


# ═══════════════════════════════════════════════════════════════
# SCAN ALL COMBINATIONS
# ═══════════════════════════════════════════════════════════════

print("=" * 90)
print("  VORTEX EXPLORER — Scanning coordinate mappings for optimal vortex structure")
print("=" * 90)
print()

# Get all candidate names
z_names = list(get_z_candidates(elements[0]).keys())
r_names = list(get_r_candidates(elements[0]).keys())
angle_names = list(get_angle_candidates(elements[0]).keys())

# For efficiency, pre-compute all values
z_vals = {name: np.array([get_z_candidates(e)[name] for e in elements]) for name in z_names}
r_vals = {name: np.array([get_r_candidates(e)[name] for e in elements]) for name in r_names}
a_vals = {name: np.array([get_angle_candidates(e)[name] for e in elements]) for name in angle_names}

# Measure vortex quality for each (angle, z-axis) combination
# using the golden angle as default for angle, and scanning z-axes
# Metric: how well do the points lie on a helix?

print("  ── Part 1: Z-axis scan (angle = golden angle, radius = ratio_pred) ──\n")
print(f"  {'Z-axis':<30s}  {'Helix R²':>8s}  {'Z range':>10s}  {'Spread':>8s}")
print(f"  {'─'*65}")

default_angles = a_vals['Z × golden (current)']
results = []

for z_name in z_names:
    zv = z_vals[z_name]
    # Only meaningful if z-values span a range
    z_range = np.max(zv) - np.min(zv)
    if z_range < 0.01:
        print(f"  {z_name:<30s}  {'skip':>8s}  {z_range:>10.3f}")
        continue

    # Measure helix quality
    hr2 = helix_r2(default_angles, zv)
    # Measure radial spread (lower = tighter vortex)
    rv = np.array([e['ratio_pred'] for e in elements])
    radial_spread = np.std(rv)
    results.append((z_name, hr2, z_range, radial_spread))
    print(f"  {z_name:<30s}  {hr2:>8.4f}  {z_range:>10.3f}  {radial_spread:>8.4f}")

results.sort(key=lambda x: x[1], reverse=True)
print(f"\n  Best z-axis: {results[0][0]} (helix R² = {results[0][1]:.4f})")

# ── Part 2: Radius scan ──
print(f"\n  ── Part 2: Radius scan (angle = golden, z = Z) ──\n")
print(f"  {'Radius':<25s}  {'Radial σ/μ':>10s}  {'Band sep':>10s}")
print(f"  {'─'*50}")

for r_name in r_names:
    rv = r_vals[r_name]
    mu = np.mean(rv)
    sigma = np.std(rv)
    cv = sigma / mu if mu > 0 else 0
    # Band separation: how well does the radius separate the three modes?
    leak_r = [rv[i] for i in range(N) if elements[i]['mode'] in ('leak',)]
    base_r = [rv[i] for i in range(N) if elements[i]['mode'] in ('additive','pythagorean','p-hole')]
    mid_r = [rv[i] for i in range(N) if elements[i]['mode'] not in ('leak','additive','pythagorean','p-hole')]
    if leak_r and base_r and mid_r:
        band_sep = abs(np.mean(base_r) - np.mean(leak_r)) / (np.std(base_r) + np.std(leak_r) + 1e-10)
    else:
        band_sep = 0
    print(f"  {r_name:<25s}  {cv:>10.4f}  {band_sep:>10.3f}")


# ── Part 3: Full combination scan (top combos only) ──
print(f"\n  ── Part 3: Top coordinate systems ──\n")

# Test a curated set of promising combos
combos = [
    ('Z × golden (current)', 'ratio_pred (current)', 'Z (atomic number)', 'ORIGINAL'),
    ('Z × golden (current)', 'ratio_pred (current)', 'EN (electronegativity)', 'EN as height'),
    ('Z × golden (current)', 'ratio_pred (current)', 'IE (ionization energy)', 'IE as height'),
    ('Z × golden (current)', 'ratio_pred (current)', '1/r_cov (compactness)', '1/r_cov height'),
    ('Z × golden (current)', 'ratio_pred (current)', 'r_norm (Fibonacci rem)', 'r_norm height'),
    ('Z × golden (current)', 'ratio_pred (current)', 'per + frac_pos', 'Period height'),
    ('Z × golden (current)', 'ratio_pred (current)', 'log(IE)', 'log(IE) height'),
    ('Z × golden (current)', 'ratio_pred (current)', 'EN × r_norm', 'EN×r_norm height'),
    ('Z × golden (current)', 'EN/4', 'Z (atomic number)', 'EN as radius'),
    ('Z × golden (current)', 'sqrt(IE/Ry)', 'Z (atomic number)', 'sqrt(IE) radius'),
    ('Z × golden (current)', '1/r_cov', 'Z (atomic number)', '1/r_cov radius'),
    ('Z × golden (current)', 'θ', 'Z (atomic number)', 'θ as radius'),
    ('EN × 2π/4', 'ratio_pred (current)', 'Z (atomic number)', 'EN as angle'),
    ('r_norm × 2π', 'ratio_pred (current)', 'Z (atomic number)', 'r_norm as angle'),
    # Promising physical combos
    ('Z × golden (current)', 'sqrt(IE/Ry)', 'EN (electronegativity)', 'IE radius, EN height'),
    ('Z × golden (current)', '1/r_cov', 'EN (electronegativity)', '1/r height, EN height'),
    ('Z × golden (current)', 'EN/4', 'IE (ionization energy)', 'EN radius, IE height'),
    ('Z × golden (current)', 'θ', 'EN (electronegativity)', 'θ radius, EN height'),
    ('Z × golden (current)', 'sqrt(IE/Ry)', 'log(IE)', 'IE radius+height'),
    ('Z × golden (current)', 'r_norm + 0.5', 'EN (electronegativity)', 'r_norm radius, EN height'),
]

print(f"  {'Name':<25s}  {'Helix R²':>8s}  {'Description':>30s}")
print(f"  {'─'*70}")

combo_results = []
for angle_name, r_name, z_name, desc in combos:
    aa = a_vals[angle_name]
    rr = r_vals[r_name]
    zz = z_vals[z_name]

    z_range = np.max(zz) - np.min(zz)
    if z_range < 0.01:
        continue

    hr2 = helix_r2(aa, zz)
    combo_results.append((desc, hr2, angle_name, r_name, z_name))
    print(f"  {desc:<25s}  {hr2:>8.4f}  {angle_name[:15]:>15s} / {r_name[:15]:>15s}")

combo_results.sort(key=lambda x: x[1], reverse=True)
print(f"\n  Top 5:")
for i, (desc, hr2, an, rn, zn) in enumerate(combo_results[:5]):
    print(f"    {i+1}. {desc:<25s}  R² = {hr2:.4f}")


# ═══════════════════════════════════════════════════════════════
# GENERATE COMPARISON FIGURES
# ═══════════════════════════════════════════════════════════════

RESULTS_DIR = '/Users/universe/Unified_Theory_Physics/results/vortex_explorer'
os.makedirs(RESULTS_DIR, exist_ok=True)

# Color by block
BLOCK_COLORS = {'s': '#e74c3c', 'p': '#3498db', 'd': '#2ecc71', 'ng': '#f39c12', 'f': '#9b59b6'}

# Plot the top 6 most promising mappings as a 2×3 grid
top6 = combo_results[:6]

# ── Multi-panel comparison ──
fig = plt.figure(figsize=(22, 14))
fig.suptitle('Vortex Explorer: Which Coordinates Reveal the Spiral?', fontsize=16, fontweight='bold')

for idx, (desc, hr2, an, rn, zn) in enumerate(top6):
    ax = fig.add_subplot(2, 3, idx+1, projection='3d')

    aa = a_vals[an]
    rr = r_vals[rn]
    zz = z_vals[zn]

    xx = rr * np.cos(aa)
    yy = rr * np.sin(aa)

    colors = [BLOCK_COLORS.get(e['block'], 'gray') for e in elements]
    ax.scatter(xx, yy, zz, c=colors, s=25, alpha=0.8, edgecolors='k', linewidths=0.3)

    # Label a few key elements
    for i, e in enumerate(elements):
        if e['sym'] in ('H','He','Li','C','N','O','Fe','Cu','Au','U','Cs','F','Ne'):
            ax.text(xx[i], yy[i], zz[i], f" {e['sym']}", fontsize=6, alpha=0.7)

    ax.set_title(f'{desc}\nHelix R² = {hr2:.3f}', fontsize=10)
    ax.set_xlabel(rn.split('(')[0][:10], fontsize=7)
    ax.set_ylabel('', fontsize=7)
    ax.set_zlabel(zn.split('(')[0][:15], fontsize=7)
    ax.view_init(elev=20, azim=45)

plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, 'vortex_comparison_6panel.png'), dpi=150, bbox_inches='tight')
plt.close()
print(f"\n  Saved: {RESULTS_DIR}/vortex_comparison_6panel.png")


# ── Detailed 4-view plot of the BEST mapping ──
best = combo_results[0]
desc, hr2, an, rn, zn = best
print(f"\n  Generating 4-view plot for: {desc} (R² = {hr2:.4f})")

aa = a_vals[an]
rr = r_vals[rn]
zz = z_vals[zn]
xx = rr * np.cos(aa)
yy = rr * np.sin(aa)
colors = [BLOCK_COLORS.get(e['block'], 'gray') for e in elements]

fig = plt.figure(figsize=(20, 16))
fig.suptitle(f'Best Vortex Mapping: {desc}  (Helix R² = {hr2:.3f})', fontsize=16, fontweight='bold')

views = [
    ('Perspective', 20, 45),
    ('Top-down (looking along vortex axis)', 85, 0),
    ('Side view', 5, 0),
    ('Rear perspective', 20, 135),
]

for idx, (vname, elev, azim) in enumerate(views):
    ax = fig.add_subplot(2, 2, idx+1, projection='3d')
    ax.scatter(xx, yy, zz, c=colors, s=35, alpha=0.85, edgecolors='k', linewidths=0.4)

    # Draw guide helices at the three band radii
    z_lin = np.linspace(np.min(zz)*0.95, np.max(zz)*1.05, 500)
    # For helix, we need to map z back to angle
    # Use golden angle: angle = Z_index × golden_angle
    # Approximate Z from z-value by interpolation
    z_to_Z = dict(zip(zz, [e['Z'] for e in elements]))

    for r_band, band_color, band_label in [
        (R_LEAK, '#e74c3c', 'Leak'),
        (R_RC, '#f39c12', 'RC'),
        (R_BASE, '#3498db', 'Base')
    ]:
        # Only draw if radius mapping is ratio_pred
        if rn == 'ratio_pred (current)':
            a_helix = np.linspace(0, 60*math.pi, 2000)
            # Map angle to z: z grows with Z, angle = Z × golden
            # We need to invert: Z = angle / golden, then map Z → z
            Z_helix = a_helix / GOLDEN_ANGLE_RAD
            # Interpolate z from Z
            Z_data = np.array([e['Z'] for e in elements])
            z_data = zz
            # Simple: z ∝ Z for most mappings
            if np.corrcoef(Z_data, z_data)[0,1] > 0.5:
                z_interp = np.interp(Z_helix, Z_data, z_data)
                valid = (z_interp >= np.min(zz)*0.95) & (z_interp <= np.max(zz)*1.05)
                x_h = r_band * np.cos(a_helix[valid])
                y_h = r_band * np.sin(a_helix[valid])
                ax.plot(x_h, y_h, z_interp[valid], color=band_color, alpha=0.15, linewidth=0.5)

    # Labels
    for i, e in enumerate(elements):
        if e['sym'] in ('H','He','Li','C','O','F','Ne','Na','K','Fe','Cu','Au','Cs','Xe'):
            ax.text(xx[i], yy[i], zz[i], f" {e['sym']}", fontsize=6, alpha=0.8)

    ax.set_title(vname, fontsize=11)
    ax.view_init(elev=elev, azim=azim)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel(zn.split('(')[0][:15])

# Legend
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=c, label=b) for b, c in BLOCK_COLORS.items()]
fig.legend(handles=legend_elements, loc='lower center', ncol=5, fontsize=10)

plt.tight_layout(rect=[0, 0.04, 1, 0.96])
plt.savefig(os.path.join(RESULTS_DIR, 'vortex_best_4view.png'), dpi=150, bbox_inches='tight')
plt.close()
print(f"  Saved: {RESULTS_DIR}/vortex_best_4view.png")


# ── Also generate the EN-height plot specifically (likely the most intuitive) ──
print(f"\n  Generating EN-height specific plot...")

aa_gold = a_vals['Z × golden (current)']
rr_pred = r_vals['ratio_pred (current)']
zz_en = z_vals['EN (electronegativity)']

xx_en = rr_pred * np.cos(aa_gold)
yy_en = rr_pred * np.sin(aa_gold)

fig = plt.figure(figsize=(20, 16))
fig.suptitle('Vortex with Electronegativity Height\n'
             'x,y = ratio_pred × golden_angle spiral  |  z = Pauling EN',
             fontsize=14, fontweight='bold')

for idx, (vname, elev, azim) in enumerate(views):
    ax = fig.add_subplot(2, 2, idx+1, projection='3d')

    # Noble gases at EN=0 are special — mark them differently
    ng_mask = np.array([e['block'] == 'ng' for e in elements])
    not_ng = ~ng_mask

    ax.scatter(xx_en[not_ng], yy_en[not_ng], zz_en[not_ng],
               c=[colors[i] for i in range(N) if not ng_mask[i]],
               s=35, alpha=0.85, edgecolors='k', linewidths=0.4)
    ax.scatter(xx_en[ng_mask], yy_en[ng_mask], zz_en[ng_mask],
               c='gold', s=50, alpha=0.9, edgecolors='k', linewidths=0.8,
               marker='D', label='Noble gas')

    # Connect elements within each period to show the periodic rise
    for per in range(2, 7):
        per_idx = [i for i in range(N) if elements[i]['per'] == per and elements[i]['en'] > 0]
        if len(per_idx) >= 2:
            per_idx.sort(key=lambda i: elements[i]['Z'])
            xi = xx_en[per_idx]; yi = yy_en[per_idx]; zi = zz_en[per_idx]
            ax.plot(xi, yi, zi, color='gray', alpha=0.3, linewidth=0.8)

    for i, e in enumerate(elements):
        if e['sym'] in ('H','Li','C','O','F','Na','K','Fe','Cu','Au','Cs','Cl','Br'):
            ax.text(xx_en[i], yy_en[i], zz_en[i], f" {e['sym']}", fontsize=7, alpha=0.8)

    ax.set_title(vname, fontsize=11)
    ax.view_init(elev=elev, azim=azim)
    ax.set_xlabel('x (ratio × cos θ)')
    ax.set_ylabel('y (ratio × sin θ)')
    ax.set_zlabel('Electronegativity')

fig.legend(handles=legend_elements + [Patch(facecolor='gold', label='Noble gas')],
           loc='lower center', ncol=6, fontsize=10)
plt.tight_layout(rect=[0, 0.04, 1, 0.96])
plt.savefig(os.path.join(RESULTS_DIR, 'vortex_EN_height.png'), dpi=150, bbox_inches='tight')
plt.close()
print(f"  Saved: {RESULTS_DIR}/vortex_EN_height.png")


# ── IE-height plot (ionization energy is the most "physical" axis) ──
print(f"  Generating IE-height plot...")

zz_ie = z_vals['IE (ionization energy)']

fig = plt.figure(figsize=(20, 16))
fig.suptitle('Vortex with Ionization Energy Height\n'
             'x,y = ratio_pred × golden_angle spiral  |  z = IE₁ (eV)',
             fontsize=14, fontweight='bold')

for idx, (vname, elev, azim) in enumerate(views):
    ax = fig.add_subplot(2, 2, idx+1, projection='3d')

    ax.scatter(xx_en, yy_en, zz_ie,
               c=colors, s=35, alpha=0.85, edgecolors='k', linewidths=0.4)

    # Connect periods
    for per in range(2, 7):
        per_idx = [i for i in range(N) if elements[i]['per'] == per]
        if len(per_idx) >= 2:
            per_idx.sort(key=lambda i: elements[i]['Z'])
            xi = xx_en[per_idx]; yi = yy_en[per_idx]; zi = zz_ie[per_idx]
            ax.plot(xi, yi, zi, color='gray', alpha=0.3, linewidth=0.8)

    for i, e in enumerate(elements):
        if e['sym'] in ('H','He','Li','C','O','F','Ne','Na','K','Fe','Cu','Au','Cs','Xe','Ar'):
            ax.text(xx_en[i], yy_en[i], zz_ie[i], f" {e['sym']}", fontsize=7, alpha=0.8)

    ax.set_title(vname, fontsize=11)
    ax.view_init(elev=elev, azim=azim)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('IE₁ (eV)')

plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, 'vortex_IE_height.png'), dpi=150, bbox_inches='tight')
plt.close()
print(f"  Saved: {RESULTS_DIR}/vortex_IE_height.png")


# ═══════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════

print(f"\n{'='*90}")
print("  SUMMARY")
print(f"{'='*90}")
print()
print("  Z-axis ranking (golden angle, ratio_pred radius):")
for i, (name, hr2, zr, rs) in enumerate(results[:5]):
    marker = ' ← CURRENT' if 'atomic' in name else ''
    print(f"    {i+1}. {name:<30s}  Helix R² = {hr2:.4f}{marker}")

print(f"\n  Full combination ranking:")
for i, (desc, hr2, an, rn, zn) in enumerate(combo_results[:8]):
    marker = ' ← CURRENT' if desc == 'ORIGINAL' else ''
    print(f"    {i+1}. {desc:<30s}  Helix R² = {hr2:.4f}{marker}")

print(f"\n  Figures saved to: {RESULTS_DIR}/")
print()
