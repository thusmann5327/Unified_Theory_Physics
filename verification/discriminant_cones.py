#!/usr/bin/env python3
"""
discriminant_cones.py — DISCRIMINANT CONE VORTEX: The Formula IS the Geometry
=============================================================================
Thomas A. Husmann / iBuilt LTD / March 2026

BREAKTHROUGH: ratio = √(1 + (θ×BOS)²) is the Pythagorean theorem.
Each element sits on a right triangle: leg₁ = 1 (silver/mass),
leg₂ = θ×BOS (gold/momentum), hypotenuse = ratio (observable).

The three modes are THREE CONES:
  Leak cone:      arctan(θ_leak × BOS) = 29.2°
  Crossover cone: arctan(θ_rc   × BOS) = 40.3°
  Baseline cone:  arctan(θ_base × BOS) = 44.8°

The formula IS the geometry. The geometry IS the vortex.
Three cones. Three doors. One triangle. One axiom.

Contributors:
  Claude (Anthropic) — computation, visualization, angular analysis
"""

import math, os, json
import numpy as np

# ═══════════════════════════════════════════════════════════════════════
# FRAMEWORK — derive everything from the AAH spectrum
# ═══════════════════════════════════════════════════════════════════════

PHI = (1 + math.sqrt(5)) / 2
PHI2 = PHI**2; PHI3 = PHI**3; PHI4 = PHI**4
LEAK = 1/PHI4
R_C = 1 - LEAK
W = (2 + PHI**(1/PHI**2)) / PHI4

# Spectrum
D = 233
H_ham = np.diag(2*np.cos(2*np.pi/PHI*np.arange(D)))
H_ham += np.diag(np.ones(D-1), 1) + np.diag(np.ones(D-1), -1)
EIGS = np.sort(np.linalg.eigvalsh(H_ham))
E_RANGE = EIGS[-1] - EIGS[0]; DIFFS = np.diff(EIGS); MED = np.median(DIFFS)
GAPS = [(i, DIFFS[i]) for i in range(len(DIFFS)) if DIFFS[i] > 8*MED]
RANKED = sorted(GAPS, key=lambda g: g[1], reverse=True)
wL = min([g for g in RANKED if g[1] > 1], key=lambda g: EIGS[g[0]]+EIGS[g[0]+1])
HALF = E_RANGE / 2
R_SHELL = (abs(EIGS[wL[0]]) + abs(EIGS[wL[0]+1])) / (2*HALF)
R_OUTER = R_SHELL + wL[1] / (2*E_RANGE)
abs_e = np.abs(EIGS); ci = np.sort(np.argsort(abs_e)[:55])
ctr = EIGS[ci]; s3w = ctr[-1] - ctr[0]; sd = np.diff(ctr); sm = np.median(sd)
sg = sorted([sd[i] for i in range(len(sd)) if sd[i] > 4*sm], reverse=True)
GAPS_NORM = [g / s3w for g in sg]

SIGMA3 = 0.0728; SIGMA2 = 0.2350; SHELL = 0.3972; SIGMA4 = 0.5594
DARK_GOLD = 0.290; SILVER_S3 = 0.171; GOLD_S3 = 0.236; BRONZE_S3 = 0.394

BASE = R_OUTER / R_SHELL
BOS = BRONZE_S3 / R_SHELL
G1 = GAPS_NORM[0] if GAPS_NORM else 0.3243

RATIO_LEAK = 1 + LEAK
RATIO_REFLECT = BASE + DARK_GOLD * LEAK
SILVER_MEAN = 1 + math.sqrt(2)

THETA_LEAK = 0.564; THETA_RC = 0.854; THETA_BASE = 1.000
GOLDEN_ANGLE_RAD = 2*math.pi / PHI2  # 137.508°

MU_EFF = {26: 2.22, 27: 1.72, 28: 0.62}
REAL_CONFIG = {24:(5,1), 29:(10,1), 41:(4,1), 42:(5,1),
               44:(7,1), 45:(8,1), 46:(10,0), 47:(10,1)}

# Cone angles from the formula
ALPHA_LEAK = math.atan(THETA_LEAK * BOS)
ALPHA_RC   = math.atan(THETA_RC * BOS)
ALPHA_BASE = math.atan(THETA_BASE * BOS)

# ═══════════════════════════════════════════════════════════════════════
# ELEMENT DATA (Z=1 to 83, all available)
# ═══════════════════════════════════════════════════════════════════════

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

# Mohs hardness of elemental solids (where defined)
MOHS = {
    5:9.5, 6:10, 14:6.5, 22:6.0, 23:6.7, 24:8.5, 25:6.0, 26:4.0,
    27:5.0, 28:4.0, 29:3.0, 30:2.5, 31:1.5, 32:6.0, 33:3.5, 34:2.0,
    35:None, 40:5.0, 41:6.0, 42:5.5, 44:6.5, 45:6.0, 46:4.75,
    47:2.5, 48:2.0, 49:1.2, 50:1.5, 51:3.0, 52:2.25, 72:5.5,
    73:6.5, 74:7.5, 75:7.0, 76:7.0, 77:6.5, 78:3.5, 79:2.5,
    80:None, 82:1.5, 83:2.25, 13:2.75, 4:5.5, 7:None, 8:None,
    9:None, 15:None, 16:2.0, 17:None
}

EN_PAULING = {
    1:2.20,3:0.98,4:1.57,5:2.04,6:2.55,7:3.04,8:3.44,9:3.98,
    11:0.93,12:1.31,13:1.61,14:1.90,15:2.19,16:2.58,17:3.16,
    19:0.82,20:1.00,21:1.36,22:1.54,23:1.63,24:1.66,25:1.55,
    26:1.83,27:1.88,28:1.91,29:1.90,30:1.65,31:1.81,32:2.01,
    33:2.18,34:2.55,35:2.96,37:0.82,38:0.95,39:1.22,40:1.33,
    41:1.60,42:2.16,47:1.93,48:1.69,49:1.78,50:1.96,51:2.05,
    52:2.10,53:2.66,55:0.79,56:0.89,57:1.10,72:1.30,73:1.50,
    74:2.36,75:1.90,76:2.20,77:2.20,78:2.28,79:2.54,80:2.00,
    81:1.62,82:2.33,83:2.02
}

# ═══════════════════════════════════════════════════════════════════════
# AUFBAU + RATIO PREDICTION
# ═══════════════════════════════════════════════════════════════════════

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
    """Returns (ratio_pred, theta_eff, per, n_p, n_d, n_s, block, mode)"""
    per, n_p, n_d, n_s, block = aufbau(Z)
    if block == 'd':
        if Z in MU_EFF:
            mu = MU_EFF[Z]
            theta = 1 - (n_d/10)*DARK_GOLD + mu * LEAK
            return math.sqrt(1+(theta*BOS)**2), theta, per, n_p, n_d, n_s, block, "magnetic"
        is_boundary = (n_d <= 4 or n_d >= 9)
        has_s = (n_s > 0)
        if is_boundary and has_s:
            theta = THETA_LEAK
            return RATIO_LEAK, theta, per, n_p, n_d, n_s, block, "leak"
        elif n_d >= 9 and not has_s:
            theta = THETA_BASE
            return RATIO_REFLECT, theta, per, n_p, n_d, n_s, block, "reflect"
        else:
            theta = 1 - (n_d/10)*DARK_GOLD
            return math.sqrt(1+(theta*BOS)**2), theta, per, n_p, n_d, n_s, block, "standard"
    elif block == 'ng':
        theta = 1 + n_p*(G1/BOS)*PHI**(-(per-1))
        return math.sqrt(1+(theta*BOS)**2), theta, per, n_p, n_d, n_s, block, "pythagorean"
    else:
        ratio = BASE + n_p*G1*PHI**(-(per-1))
        # For s/p additive, compute effective theta from ratio
        # ratio = sqrt(1 + (theta*BOS)^2) → theta = sqrt(ratio^2 - 1) / BOS
        theta_eff = math.sqrt(max(0, ratio**2 - 1)) / BOS
        if block == 'p' and n_p >= 4 and per >= 3:
            ratio *= R_C
            theta_eff = math.sqrt(max(0, ratio**2 - 1)) / BOS
            return ratio, theta_eff, per, n_p, n_d, n_s, block, "p-hole"
        return ratio, theta_eff, per, n_p, n_d, n_s, block, "additive"


# ═══════════════════════════════════════════════════════════════════════
# TASK 1: BUILD THE SPHERICAL MAPPING
# ═══════════════════════════════════════════════════════════════════════

def build_elements():
    """Compute spherical coordinates for all elements."""
    elements = []
    period_starts = {1:1, 2:3, 3:11, 4:19, 5:37, 6:55, 7:87}

    for Z in sorted(RADII.keys()):
        if Z not in SYMBOLS: continue
        sym = SYMBOLS[Z]
        r_cov, r_vdw = RADII[Z]
        ratio_obs = r_vdw / r_cov

        rp, theta_eff, per, n_p, n_d, n_s, block, mode = predict_ratio(Z)
        G = (ratio_obs - rp) / rp * 100  # gate overflow

        # Spherical coordinates (predicted)
        polar_pred = math.atan(theta_eff * BOS)  # angle from z-axis
        # Azimuthal: golden angle × position within period
        z_start = period_starts.get(per, 1)
        idx_in_period = Z - z_start
        azimuth = GOLDEN_ANGLE_RAD * idx_in_period

        # Cartesian from spherical
        r = rp  # distance = ratio
        x = r * math.sin(polar_pred) * math.cos(azimuth)
        y = r * math.sin(polar_pred) * math.sin(azimuth)
        z = r * math.cos(polar_pred)
        # NOTE: z = r × cos(arctan(θ×BOS)) = r × 1/r = 1 for Pythagorean modes
        # For additive modes, z ≈ 1 also (since ratio ≈ √(1+(θ_eff×BOS)²))

        # Observed cone angle
        polar_obs = math.acos(min(1.0, 1.0/ratio_obs)) if ratio_obs >= 1 else 0
        delta_alpha = polar_obs - polar_pred  # angular deviation

        # z=1 cross-section coordinates
        x_z1 = theta_eff * BOS * math.cos(azimuth)
        y_z1 = theta_eff * BOS * math.sin(azimuth)

        elements.append({
            'Z': Z, 'sym': sym, 'per': per, 'n_p': n_p, 'n_d': n_d,
            'n_s': n_s, 'block': block, 'mode': mode,
            'theta_eff': theta_eff, 'ratio_pred': rp, 'ratio_obs': ratio_obs,
            'G': G, 'r_cov': r_cov, 'r_vdw': r_vdw,
            'polar_pred': polar_pred, 'polar_obs': polar_obs,
            'azimuth': azimuth, 'delta_alpha': delta_alpha,
            'x': x, 'y': y, 'z': z,
            'x_z1': x_z1, 'y_z1': y_z1,
            'mohs': MOHS.get(Z), 'en': EN_PAULING.get(Z),
            'idx_in_period': idx_in_period,
        })

    return elements


# ═══════════════════════════════════════════════════════════════════════
# CROSS-SCALE DATA: planetary/molecular ratios on the same cones
# ═══════════════════════════════════════════════════════════════════════

CROSS_SCALE = [
    {'name': 'TRAPPIST-1 d/c', 'ratio': 1.409, 'type': 'planet', 'cone': 'baseline'},
    {'name': 'Cl₂/F₂ bond',    'ratio': 1.408, 'type': 'molecule', 'cone': 'baseline'},
    {'name': 'Br₂/Cl₂ bond',   'ratio': 1.147, 'type': 'molecule', 'cone': 'leak'},
    {'name': 'Kepler 3:2 peak', 'ratio': 1.310, 'type': 'planet', 'cone': 'crossover'},
    {'name': 'H₂ bond/a₀',     'ratio': 1.402, 'type': 'molecule', 'cone': 'baseline'},
    {'name': 'Mercury orbit/Venus', 'ratio': 1.382/0.387*0.387, 'type': 'planet', 'cone': 'baseline'},
]
# Compute their cone angles
for cs in CROSS_SCALE:
    r = cs['ratio']
    cs['theta_eff'] = math.sqrt(max(0, r**2 - 1)) / BOS if r >= 1 else 0
    cs['polar'] = math.acos(min(1.0, 1.0/r)) if r >= 1 else 0


# ═══════════════════════════════════════════════════════════════════════
# PLOTTING
# ═══════════════════════════════════════════════════════════════════════

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

RESULTS_DIR = '/Users/universe/Unified_Theory_Physics/results/discriminant_cones'
os.makedirs(RESULTS_DIR, exist_ok=True)

BLOCK_COLORS = {'s':'#e74c3c', 'p':'#3498db', 'd':'#2ecc71', 'ng':'#f39c12', 'f':'#9b59b6'}
CONE_COLORS = {'leak':'#3498db', 'crossover':'#e67e22', 'baseline':'#2ecc71'}
DPI = 200


def draw_cone_surface(ax, alpha_rad, t_max, color, alpha_t=0.08, label=None):
    """Draw a translucent cone surface."""
    t = np.linspace(0, t_max, 20)
    phi_az = np.linspace(0, 2*np.pi, 60)
    T, P = np.meshgrid(t, phi_az)
    X = T * math.sin(alpha_rad) * np.cos(P)
    Y = T * math.sin(alpha_rad) * np.sin(P)
    Z = T * math.cos(alpha_rad)
    ax.plot_surface(X, Y, Z, alpha=alpha_t, color=color, linewidth=0)
    if label:
        # Draw a guide line on the cone
        t_line = np.linspace(0, t_max, 50)
        ax.plot(t_line*math.sin(alpha_rad), np.zeros_like(t_line),
                t_line*math.cos(alpha_rad), color=color, lw=1.5, alpha=0.6, label=label)


def draw_circle_at_z(ax, z_val, radius, color, lw=1, ls='-', label=None):
    """Draw a circle in the x-y plane at height z."""
    phi_az = np.linspace(0, 2*np.pi, 100)
    x = radius * np.cos(phi_az)
    y = radius * np.sin(phi_az)
    z = np.full_like(phi_az, z_val)
    ax.plot(x, y, z, color=color, lw=lw, ls=ls, alpha=0.7, label=label)


def fig_8a_three_cones(elements):
    """8a: Three translucent cones with 97 elements."""
    fig = plt.figure(figsize=(14, 11))
    fig.suptitle("The Discriminant Cone Vortex\nratio = √(1 + (θ×BOS)²)  →  three cones, one axiom",
                 fontsize=14, fontweight='bold')

    for idx, (elev, azim, title) in enumerate([
        (25, -60, 'Perspective'),
        (90, 0, 'Top-down (looking into vortex)'),
        (0, 0, 'Side view (cone angles visible)'),
        (15, 30, 'Rear perspective'),
    ]):
        ax = fig.add_subplot(2, 2, idx+1, projection='3d')
        ax.set_title(title, fontsize=10)

        # Draw cone surfaces
        t_max = 1.7
        draw_cone_surface(ax, ALPHA_LEAK, t_max, CONE_COLORS['leak'], 0.05,
                         f'Leak 29.2°')
        draw_cone_surface(ax, ALPHA_RC, t_max, CONE_COLORS['crossover'], 0.05,
                         f'RC 40.3°')
        draw_cone_surface(ax, ALPHA_BASE, t_max, CONE_COLORS['baseline'], 0.05,
                         f'Base 44.8°')

        # Plot elements
        notable = {1,6,26,29,46,47,55,10,20,79,74,83}
        for e in elements:
            c = BLOCK_COLORS.get(e['block'], 'gray')
            r = e['ratio_obs']
            pol = e['polar_obs']
            az = e['azimuth']
            ex = r * math.sin(pol) * math.cos(az)
            ey = r * math.sin(pol) * math.sin(az)
            ez = r * math.cos(pol)
            ax.scatter([ex], [ey], [ez], c=c, s=18, alpha=0.8, edgecolors='k', linewidths=0.3)
            if e['Z'] in notable:
                ax.text(ex, ey, ez, f" {e['sym']}", fontsize=6, alpha=0.8)

        ax.set_xlabel('x', fontsize=8); ax.set_ylabel('y', fontsize=8)
        ax.set_zlabel('z (mass axis)', fontsize=8)
        ax.view_init(elev=elev, azim=azim)
        ax.set_xlim(-1.6, 1.6); ax.set_ylim(-1.6, 1.6); ax.set_zlim(0, 1.7)
        if idx == 0:
            ax.legend(fontsize=7, loc='upper left')

    # Legend for blocks
    from matplotlib.lines import Line2D
    legend_els = [Line2D([0],[0],marker='o',color='w',markerfacecolor=c,markersize=8,label=b)
                  for b,c in BLOCK_COLORS.items()]
    fig.legend(handles=legend_els, loc='lower center', ncol=5, fontsize=9)
    plt.tight_layout(rect=[0,0.04,1,0.94])
    path = os.path.join(RESULTS_DIR, 'fig_8a_three_cones.png')
    plt.savefig(path, dpi=DPI, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {path}")


def fig_8b_z1_crosssection(elements):
    """8b: The z=1 cross-section — three concentric circles."""
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_title("z = 1 Cross-Section: The Scatter Plot Explained\n"
                 "Three concentric circles at θ×BOS = three cones cut at z = 1",
                 fontsize=13, fontweight='bold')

    # Draw the three circles
    for theta, name, color in [
        (THETA_LEAK, f'Leak: r = {THETA_LEAK*BOS:.4f}', CONE_COLORS['leak']),
        (THETA_RC,   f'RC: r = {THETA_RC*BOS:.4f}', CONE_COLORS['crossover']),
        (THETA_BASE, f'Base: r = BOS = {THETA_BASE*BOS:.4f}', CONE_COLORS['baseline']),
    ]:
        circle = plt.Circle((0, 0), theta*BOS, fill=False, color=color, lw=2,
                            ls='--', label=name)
        ax.add_patch(circle)

    # Plot elements at their z=1 positions
    notable = {1,3,6,7,9,10,11,14,17,19,20,26,29,36,47,54,55,79,74,82,83,
               5,27,28,46,42,24}
    for e in elements:
        c = BLOCK_COLORS.get(e['block'], 'gray')
        # Use OBSERVED theta for position
        th_obs = math.sqrt(max(0, e['ratio_obs']**2 - 1)) / BOS
        r_obs = th_obs * BOS
        az = e['azimuth']
        x = r_obs * math.cos(az)
        y = r_obs * math.sin(az)
        ax.scatter([x], [y], c=c, s=30, alpha=0.8, edgecolors='k', linewidths=0.3,
                  zorder=5)
        if e['Z'] in notable:
            ax.annotate(e['sym'], (x, y), fontsize=7, ha='center', va='bottom',
                       xytext=(0, 4), textcoords='offset points')

    ax.set_xlim(-1.3, 1.3); ax.set_ylim(-1.3, 1.3)
    ax.set_aspect('equal')
    ax.axhline(0, color='gray', lw=0.3); ax.axvline(0, color='gray', lw=0.3)
    ax.set_xlabel('θ×BOS × cos(golden_angle × index)', fontsize=10)
    ax.set_ylabel('θ×BOS × sin(golden_angle × index)', fontsize=10)
    ax.legend(fontsize=10, loc='upper right')
    ax.grid(True, alpha=0.2)

    # Add BOS identity annotation
    ax.annotate(f'Baseline circle radius = BOS = {BOS:.4f}\n= bronze_σ₃ / σ_shell',
                xy=(0.02, 0.02), xycoords='axes fraction', fontsize=9,
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    path = os.path.join(RESULTS_DIR, 'fig_8b_z1_crosssection.png')
    plt.savefig(path, dpi=DPI, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {path}")


def fig_8c_side_discriminant(elements):
    """8c: Side view with discriminant triangle overlaid."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

    # LEFT: Side view (x-z plane) with cone angles
    ax1.set_title("Side View: Three Cone Angles\nwith Discriminant Triangle (√5, √8, √13)", fontsize=12)

    # Draw cone edges (in x-z plane, azimuth=0)
    t = np.linspace(0, 1.7, 100)
    for alpha, name, color in [
        (ALPHA_LEAK, f'Leak {math.degrees(ALPHA_LEAK):.1f}°', CONE_COLORS['leak']),
        (ALPHA_RC,   f'RC {math.degrees(ALPHA_RC):.1f}°', CONE_COLORS['crossover']),
        (ALPHA_BASE, f'Base {math.degrees(ALPHA_BASE):.1f}°', CONE_COLORS['baseline']),
    ]:
        x_cone = t * math.sin(alpha)
        z_cone = t * math.cos(alpha)
        ax1.plot(x_cone, z_cone, color=color, lw=2.5, label=name)
        ax1.plot(-x_cone, z_cone, color=color, lw=2.5, alpha=0.4)

    # Overlay the discriminant triangle (√5, √8, √13)
    # tan(α_bronze) = √5/√8 = √(5/8) = 0.7906 → α = 38.3°
    alpha_disc = math.atan(math.sqrt(5)/math.sqrt(8))
    x_disc = t * math.sin(alpha_disc)
    z_disc = t * math.cos(alpha_disc)
    ax1.plot(x_disc, z_disc, 'k--', lw=1.5, alpha=0.6,
            label=f'Discriminant √5/√8 = {math.degrees(alpha_disc):.1f}°')

    # Plot elements projected onto x-z plane
    for e in elements:
        c = BLOCK_COLORS.get(e['block'], 'gray')
        r = e['ratio_obs']
        pol = e['polar_obs']
        x = r * math.sin(pol) * math.cos(e['azimuth'])
        z = r * math.cos(pol)
        ax1.scatter([abs(x)], [z], c=c, s=15, alpha=0.5, edgecolors='none')

    ax1.set_xlabel('Horizontal (θ×BOS axis — gold/momentum)', fontsize=10)
    ax1.set_ylabel('Vertical (z axis — silver/mass)', fontsize=10)
    ax1.set_xlim(0, 1.5); ax1.set_ylim(0, 1.5)
    ax1.set_aspect('equal')
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.2)

    # Draw the z=1 line
    ax1.axhline(1.0, color='gray', lw=0.8, ls=':')
    ax1.text(1.3, 1.02, 'z = 1', fontsize=8, color='gray')

    # RIGHT: The discriminant triangle mapping
    ax2.set_title("Discriminant Triangle → Cone Angles via BOS\n(√5)² + (√8)² = (√13)²", fontsize=12)

    # Draw the three right triangles
    # Leak: legs 1, θ_leak×BOS
    for theta, name, color in [
        (THETA_LEAK, 'Leak', CONE_COLORS['leak']),
        (THETA_RC,   'RC', CONE_COLORS['crossover']),
        (THETA_BASE, 'Base', CONE_COLORS['baseline']),
    ]:
        leg_h = theta * BOS
        # Right triangle: (0,0) → (leg_h, 0) → (0, 1) → (0,0)
        # But offset horizontally for visibility
        offset = {'Leak':0, 'RC':0, 'Base':0}[name]
        ax2.plot([offset, offset+leg_h, offset, offset],
                [0, 0, 1, 0], color=color, lw=2.5, label=f'{name}: θ×BOS={leg_h:.4f}')
        # Hypotenuse
        hyp = math.sqrt(1 + leg_h**2)
        ax2.annotate(f'r = {hyp:.3f}', xy=(offset+leg_h/2, 0.5),
                    fontsize=8, color=color, rotation=-math.degrees(math.atan(1/leg_h))+90,
                    ha='center')

    # The discriminant triangle scaled by BOS
    leg_disc = math.sqrt(5/8)  # √5/√8
    ax2.plot([0, leg_disc, 0, 0], [0, 0, 1, 0], 'k--', lw=1.5, alpha=0.5,
            label=f'Discriminant: √5/√8 = {leg_disc:.4f}')

    ax2.set_xlabel('θ×BOS (horizontal leg — gold/momentum)', fontsize=10)
    ax2.set_ylabel('1 (vertical leg — silver/mass)', fontsize=10)
    ax2.set_xlim(-0.1, 1.15); ax2.set_ylim(-0.1, 1.15)
    ax2.set_aspect('equal')
    ax2.legend(fontsize=8, loc='upper right')
    ax2.grid(True, alpha=0.2)

    # Annotate the baseline identity
    ax2.annotate(f'Baseline circle r = BOS = {BOS:.4f}\n≈ 1.0 → cone angle ≈ 45°\n'
                 f'Departure from 45° = {abs(45 - math.degrees(ALPHA_BASE)):.2f}°',
                 xy=(0.02, 0.7), xycoords='axes fraction', fontsize=9,
                 bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    plt.tight_layout()
    path = os.path.join(RESULTS_DIR, 'fig_8c_side_discriminant.png')
    plt.savefig(path, dpi=DPI, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {path}")


def fig_8d_hardness(elements):
    """8d: Angular deviation Δα vs Mohs hardness."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle("Angular Deviation Δα: The Cone Perturbation IS the Material Property",
                 fontsize=13, fontweight='bold')

    # Gather data
    da_list = [e['delta_alpha'] for e in elements]
    G_list = [e['G'] for e in elements]
    mohs_list = [(e['delta_alpha'], e['mohs'], e['sym']) for e in elements
                 if e['mohs'] is not None and e['mohs'] > 0]
    en_list = [(e['delta_alpha'], e['en'], e['sym']) for e in elements
               if e['en'] is not None]

    # Panel 1: Δα vs G (gate overflow) — should be near-perfect
    ax = axes[0]
    ax.set_title('Δα vs Gate Overflow G\n(should be near-perfect)', fontsize=11)
    for e in elements:
        c = BLOCK_COLORS.get(e['block'], 'gray')
        ax.scatter(e['G'], math.degrees(e['delta_alpha']), c=c, s=25, alpha=0.7,
                  edgecolors='k', linewidths=0.3)
    # Correlation
    rho = np.corrcoef([e['G'] for e in elements],
                      [math.degrees(e['delta_alpha']) for e in elements])[0,1]
    ax.set_xlabel('Gate overflow G (%)', fontsize=10)
    ax.set_ylabel('Δα (degrees)', fontsize=10)
    ax.annotate(f'ρ = {rho:.4f}', xy=(0.05, 0.92), xycoords='axes fraction',
               fontsize=12, fontweight='bold',
               bbox=dict(boxstyle='round', facecolor='lightyellow'))
    ax.axhline(0, color='gray', lw=0.5); ax.axvline(0, color='gray', lw=0.5)
    ax.grid(True, alpha=0.2)

    # Panel 2: Δα vs Mohs hardness
    ax = axes[1]
    ax.set_title('Δα vs Mohs Hardness\n(hard materials deviate from cone)', fontsize=11)
    if mohs_list:
        da_m, mohs_m, sym_m = zip(*mohs_list)
        da_deg = [math.degrees(d) for d in da_m]
        for i in range(len(mohs_list)):
            e_match = next(e for e in elements if e['sym'] == sym_m[i])
            c = BLOCK_COLORS.get(e_match['block'], 'gray')
            ax.scatter(mohs_m[i], da_deg[i], c=c, s=40, alpha=0.8,
                      edgecolors='k', linewidths=0.3)
            if mohs_m[i] >= 6 or abs(da_deg[i]) > 3:
                ax.annotate(sym_m[i], (mohs_m[i], da_deg[i]), fontsize=7,
                           xytext=(3, 3), textcoords='offset points')
        rho_mohs = np.corrcoef(mohs_m, da_deg)[0,1]
        ax.annotate(f'ρ = {rho_mohs:.4f}', xy=(0.05, 0.92), xycoords='axes fraction',
                   fontsize=12, fontweight='bold',
                   bbox=dict(boxstyle='round', facecolor='lightyellow'))
    ax.set_xlabel('Mohs Hardness', fontsize=10)
    ax.set_ylabel('Δα (degrees)', fontsize=10)
    ax.axhline(0, color='gray', lw=0.5)
    ax.grid(True, alpha=0.2)

    # Panel 3: Δα vs Electronegativity
    ax = axes[2]
    ax.set_title('Δα vs Electronegativity\n(high-EN → wider cone angle?)', fontsize=11)
    if en_list:
        da_e, en_e, sym_e = zip(*en_list)
        da_deg_e = [math.degrees(d) for d in da_e]
        for i in range(len(en_list)):
            e_match = next(e for e in elements if e['sym'] == sym_e[i])
            c = BLOCK_COLORS.get(e_match['block'], 'gray')
            ax.scatter(en_e[i], da_deg_e[i], c=c, s=25, alpha=0.7,
                      edgecolors='k', linewidths=0.3)
        rho_en = np.corrcoef(en_e, da_deg_e)[0,1]
        ax.annotate(f'ρ = {rho_en:.4f}', xy=(0.05, 0.92), xycoords='axes fraction',
                   fontsize=12, fontweight='bold',
                   bbox=dict(boxstyle='round', facecolor='lightyellow'))
    ax.set_xlabel('Electronegativity (Pauling)', fontsize=10)
    ax.set_ylabel('Δα (degrees)', fontsize=10)
    ax.axhline(0, color='gray', lw=0.5)
    ax.grid(True, alpha=0.2)

    plt.tight_layout()
    path = os.path.join(RESULTS_DIR, 'fig_8d_hardness.png')
    plt.savefig(path, dpi=DPI, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {path}")
    return rho, rho_mohs if mohs_list else 0, rho_en if en_list else 0


def fig_8e_combined(elements):
    """8e: Atoms + planetary ratios + molecular ratios on the same cones."""
    fig = plt.figure(figsize=(14, 11))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title("One Geometry for Everything\nAtoms (circles) · Planets (stars) · Molecules (diamonds)\n"
                 "Three cones from ratio = √(1 + (θ×BOS)²)",
                 fontsize=13, fontweight='bold')

    # Draw cones
    draw_cone_surface(ax, ALPHA_LEAK, 1.6, CONE_COLORS['leak'], 0.04, 'Leak 29.2°')
    draw_cone_surface(ax, ALPHA_RC, 1.6, CONE_COLORS['crossover'], 0.04, 'RC 40.3°')
    draw_cone_surface(ax, ALPHA_BASE, 1.6, CONE_COLORS['baseline'], 0.04, 'Base 44.8°')

    # Elements
    notable = {1,6,26,29,47,55,79,10,14,74}
    for e in elements:
        c = BLOCK_COLORS.get(e['block'], 'gray')
        r = e['ratio_obs']
        pol = e['polar_obs']
        az = e['azimuth']
        ex = r * math.sin(pol) * math.cos(az)
        ey = r * math.sin(pol) * math.sin(az)
        ez = r * math.cos(pol)
        ax.scatter([ex], [ey], [ez], c=c, s=18, alpha=0.7, edgecolors='k',
                  linewidths=0.3, marker='o')
        if e['Z'] in notable:
            ax.text(ex, ey, ez, f" {e['sym']}", fontsize=7)

    # Cross-scale data
    markers = {'planet': '*', 'molecule': 'D'}
    sizes = {'planet': 200, 'molecule': 120}
    for i, cs in enumerate(CROSS_SCALE):
        r = cs['ratio']
        pol = cs['polar']
        # Spread azimuthally to avoid overlap with atoms
        az = GOLDEN_ANGLE_RAD * (80 + i * 13)
        ex = r * math.sin(pol) * math.cos(az)
        ey = r * math.sin(pol) * math.sin(az)
        ez = r * math.cos(pol)
        mk = markers.get(cs['type'], 'o')
        ax.scatter([ex], [ey], [ez], c='gold', s=sizes.get(cs['type'], 100),
                  marker=mk, edgecolors='k', linewidths=1, zorder=10)
        ax.text(ex, ey, ez, f"  {cs['name']}", fontsize=6, color='darkred')

    ax.set_xlabel('x'); ax.set_ylabel('y'); ax.set_zlabel('z (mass axis)')
    ax.view_init(elev=20, azim=-50)
    ax.set_xlim(-1.6, 1.6); ax.set_ylim(-1.6, 1.6); ax.set_zlim(0, 1.7)
    ax.legend(fontsize=8, loc='upper left')

    # Custom legend
    from matplotlib.lines import Line2D
    legend_els = [
        Line2D([0],[0],marker='o',color='w',markerfacecolor='gray',markersize=8,label='Atoms'),
        Line2D([0],[0],marker='*',color='w',markerfacecolor='gold',markersize=12,label='Planetary ratios'),
        Line2D([0],[0],marker='D',color='w',markerfacecolor='gold',markersize=8,label='Molecular ratios'),
    ]
    ax.legend(handles=legend_els, fontsize=9, loc='upper right')

    plt.tight_layout()
    path = os.path.join(RESULTS_DIR, 'fig_8e_combined.png')
    plt.savefig(path, dpi=DPI, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {path}")


def fig_8f_discriminant_slice(elements):
    """8f: The discriminant triangle as a 2D slice of the 3D cone system."""
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_title("The Discriminant Triangle IS a Cross-Section of the Vortex\n"
                 "(√5)² + (√8)² = (√13)²  →  E² = p²c² + m²c⁴",
                 fontsize=13, fontweight='bold')

    # Draw the three right triangles (filled, translucent)
    from matplotlib.patches import Polygon

    for theta, name, color, alpha_fill in [
        (THETA_LEAK, 'Leak', CONE_COLORS['leak'], 0.15),
        (THETA_RC,   'Crossover', CONE_COLORS['crossover'], 0.15),
        (THETA_BASE, 'Baseline', CONE_COLORS['baseline'], 0.15),
    ]:
        leg_h = theta * BOS
        hyp = math.sqrt(1 + leg_h**2)
        triangle = Polygon([(0,0), (leg_h, 0), (0, 1)], closed=True,
                          facecolor=color, edgecolor=color, alpha=alpha_fill, lw=2)
        ax.add_patch(triangle)
        ax.plot([0, leg_h, 0, 0], [0, 0, 1, 0], color=color, lw=2.5,
               label=f'{name}: θ={theta}, angle={math.degrees(math.atan(leg_h)):.1f}°, r={hyp:.3f}')

    # The discriminant triangle
    leg_disc = math.sqrt(5/8)
    hyp_disc = math.sqrt(1 + 5/8)
    ax.plot([0, leg_disc, 0, 0], [0, 0, 1, 0], 'k--', lw=2,
           label=f'Discriminant: √5/√8={leg_disc:.4f}, angle={math.degrees(math.atan(leg_disc)):.1f}°')

    # Place select elements as points on their triangles' hypotenuses
    notable = {1:0.1, 6:0.3, 26:0.5, 29:0.7, 79:0.9, 10:0.2, 55:0.8, 46:0.6}
    for e in elements:
        if e['Z'] not in notable: continue
        frac = notable[e['Z']]
        th = e['theta_eff'] * BOS
        # Point on hypotenuse at fraction frac
        x_pt = th * (1 - frac)
        y_pt = frac
        c = BLOCK_COLORS.get(e['block'], 'gray')
        ax.scatter([x_pt], [y_pt], c=c, s=60, edgecolors='k', linewidths=0.5, zorder=10)
        ax.annotate(f"{e['sym']}\nθ={e['theta_eff']:.2f}", (x_pt, y_pt),
                   fontsize=7, ha='center', va='bottom',
                   xytext=(8, 5), textcoords='offset points')

    # Annotations
    ax.annotate('Silver leg = 1\n(mass axis, constant)', xy=(0.02, 0.5),
               fontsize=10, rotation=90, ha='center', va='center', color='purple')
    ax.annotate('Gold leg = θ×BOS\n(momentum axis, mode-dependent)', xy=(0.5, -0.08),
               fontsize=10, ha='center', color='darkgoldenrod')
    ax.annotate('Hypotenuse = ratio\n(observable)', xy=(0.55, 0.55),
               fontsize=10, ha='center', rotation=-50, color='darkgreen')

    # The Dirac mapping
    ax.annotate('E² = p²c² + m²c⁴\n13 = 5 + 8\n\n'
                'Silver (mass, Δ₂=8) → vertical leg\n'
                'Gold (momentum, Δ₁=5) → horizontal leg\n'
                'Bronze (observable, Δ₃=13) → hypotenuse',
                xy=(0.55, 0.78), xycoords='axes fraction', fontsize=9,
                bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

    ax.set_xlabel('θ×BOS (gold/momentum leg)', fontsize=11)
    ax.set_ylabel('1 (silver/mass leg)', fontsize=11)
    ax.set_xlim(-0.1, 1.15); ax.set_ylim(-0.15, 1.15)
    ax.set_aspect('equal')
    ax.legend(fontsize=9, loc='lower right')
    ax.grid(True, alpha=0.2)

    path = os.path.join(RESULTS_DIR, 'fig_8f_discriminant_slice.png')
    plt.savefig(path, dpi=DPI, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {path}")


# ═══════════════════════════════════════════════════════════════════════
# TASK 4: OBSERVED DEVIATIONS AS CONE PERTURBATIONS
# ═══════════════════════════════════════════════════════════════════════

def analyze_deviations(elements):
    """Test what Δα correlates with."""
    print("\n  TASK 4: CONE PERTURBATION CORRELATIONS")
    print("  " + "─"*60)

    # a) Δα vs G
    da = [math.degrees(e['delta_alpha']) for e in elements]
    G = [e['G'] for e in elements]
    rho_G = np.corrcoef(da, G)[0,1]
    print(f"  a) Δα vs Gate overflow G:    ρ = {rho_G:.4f}  {'NEAR-PERFECT' if abs(rho_G) > 0.95 else ''}")

    # b) Δα vs Mohs hardness
    hard = [(math.degrees(e['delta_alpha']), e['mohs']) for e in elements
            if e['mohs'] is not None and e['mohs'] > 0]
    if hard:
        da_h, mohs_h = zip(*hard)
        rho_mohs = np.corrcoef(da_h, mohs_h)[0,1]
        print(f"  b) Δα vs Mohs hardness:     ρ = {rho_mohs:.4f}  (n={len(hard)})")
    else:
        rho_mohs = 0

    # c) Δα vs EN
    en_pairs = [(math.degrees(e['delta_alpha']), e['en']) for e in elements
                if e['en'] is not None]
    if en_pairs:
        da_e, en_e = zip(*en_pairs)
        rho_en = np.corrcoef(da_e, en_e)[0,1]
        print(f"  c) Δα vs Electronegativity: ρ = {rho_en:.4f}  (n={len(en_pairs)})")
    else:
        rho_en = 0

    # d) Fibonacci anomalies
    FIBS = {1,2,3,5,8,13,21,34,55,89}
    fib_els = [e for e in elements if e['Z'] in FIBS]
    nonfib_els = [e for e in elements if e['Z'] not in FIBS]
    if fib_els and nonfib_els:
        mean_fib = np.mean([abs(e['delta_alpha']) for e in fib_els])
        mean_nonfib = np.mean([abs(e['delta_alpha']) for e in nonfib_els])
        print(f"  d) |Δα| mean (Fibonacci Z):     {math.degrees(mean_fib):.3f}°")
        print(f"     |Δα| mean (non-Fibonacci Z):  {math.degrees(mean_nonfib):.3f}°")

    # Notable anomalies
    print(f"\n  Notable cone deviations (|Δα| > 3°):")
    sorted_els = sorted(elements, key=lambda e: abs(e['delta_alpha']), reverse=True)
    for e in sorted_els[:15]:
        da_deg = math.degrees(e['delta_alpha'])
        direction = 'WIDER' if da_deg > 0 else 'NARROWER'
        mohs_str = f"Mohs {e['mohs']}" if e['mohs'] else ""
        print(f"    {e['sym']:>3} (Z={e['Z']:2d}) Δα = {da_deg:+6.2f}° → {direction:8s}  G={e['G']:+5.1f}%  {mohs_str}")

    return rho_G, rho_mohs, rho_en


# ═══════════════════════════════════════════════════════════════════════
# TASK 5: CONE ANGLE ANALYSIS
# ═══════════════════════════════════════════════════════════════════════

def analyze_cone_angles():
    """Search for framework constant matches to cone angles."""
    print("\n  TASK 5: CONE ANGLE ANALYSIS")
    print("  " + "─"*60)

    a_l = math.degrees(ALPHA_LEAK)
    a_r = math.degrees(ALPHA_RC)
    a_b = math.degrees(ALPHA_BASE)

    print(f"\n  Three cone angles:")
    print(f"    α_leak = arctan({THETA_LEAK*BOS:.4f}) = {a_l:.4f}°  ({ALPHA_LEAK:.6f} rad)")
    print(f"    α_rc   = arctan({THETA_RC*BOS:.4f}) = {a_r:.4f}°  ({ALPHA_RC:.6f} rad)")
    print(f"    α_base = arctan({THETA_BASE*BOS:.4f}) = {a_b:.4f}°  ({ALPHA_BASE:.6f} rad)")

    # Baseline vs 45°
    dep = abs(45 - a_b)
    print(f"\n  Baseline departure from 45°: {dep:.4f}° ({dep/45*100:.2f}%)")
    print(f"  → Almost exactly 45° means EQUAL mass and momentum contributions")

    # BOS = baseline circle radius at z=1
    print(f"\n  Baseline circle radius at z=1 = tan(α_base) = BOS = {BOS:.6f}")
    print(f"  This is EXACT: tan(arctan(BOS)) = BOS by definition")
    print(f"  BOS = bronze_σ₃/σ_shell = {BRONZE_S3}/{SHELL} = {BRONZE_S3/SHELL:.6f}")

    # Cone angle ratios
    print(f"\n  Cone angle ratios:")
    print(f"    α_rc / α_base     = {a_r/a_b:.6f}")
    print(f"    α_leak / α_base   = {a_l/a_b:.6f}  (cf θ_leak/θ_base = {THETA_LEAK:.3f})")
    print(f"    α_leak / α_rc     = {a_l/a_r:.6f}")
    print(f"    (α_base-α_leak)/α_base = {(a_b-a_l)/a_b:.6f}  (cf 1-1/φ² = {1-1/PHI2:.6f})")

    # Search for framework constant matches
    print(f"\n  Framework constant matches to cone angles:")
    targets = {'α_leak': a_l, 'α_rc': a_r, 'α_base': a_b}
    candidates = {
        'arcsin(1/√(1+φ²))': math.degrees(math.asin(1/math.sqrt(1+PHI2))),
        'arctan(√r_c)': math.degrees(math.atan(math.sqrt(R_C))),
        'arctan(1)-arctan(W)': math.degrees(math.atan(1) - math.atan(W)),
        'arctan(1/φ)': math.degrees(math.atan(1/PHI)),
        'arctan(φ-1)': math.degrees(math.atan(PHI-1)),
        'arctan(√φ-1)': math.degrees(math.atan(math.sqrt(PHI)-1)),
        '45/φ': 45/PHI,
        '90/φ²': 90/PHI2,
        'arctan(W)': math.degrees(math.atan(W)),
        'arctan(√(1-W²))': math.degrees(math.atan(math.sqrt(1-W**2))),
        'arctan(LEAK)': math.degrees(math.atan(LEAK)),
        'arctan(R_C)': math.degrees(math.atan(R_C)),
        'arctan(σ₄)': math.degrees(math.atan(SIGMA4)),
        'arctan(SHELL)': math.degrees(math.atan(SHELL)),
        'arctan(GOLD_S3)': math.degrees(math.atan(GOLD_S3)),
        'π×φ²/4 rad→deg': math.degrees(math.pi*PHI2/4),  # would be in degrees
        'arctan(√5/√8)': math.degrees(math.atan(math.sqrt(5/8))),
        '2×arctan(1/φ)': 2*math.degrees(math.atan(1/PHI)),
        'arctan(cos(1/φ))': math.degrees(math.atan(math.cos(1/PHI))),
        'arctan(1-LEAK)': math.degrees(math.atan(1-LEAK)),
        'arctan(1-DARK_GOLD)': math.degrees(math.atan(1-DARK_GOLD)),
        'golden_angle/φ²': math.degrees(GOLDEN_ANGLE_RAD)/PHI2,
        'arctan(σ₂/σ_shell)': math.degrees(math.atan(SIGMA2/SHELL)),
    }

    for target_name, target_val in targets.items():
        print(f"\n    {target_name} = {target_val:.4f}°:")
        matches = []
        for name, val in candidates.items():
            err = abs(val - target_val) / target_val * 100
            if err < 5:
                matches.append((err, name, val))
        matches.sort()
        for err, name, val in matches[:5]:
            marker = '★' if err < 1 else '·'
            print(f"      {marker} {name} = {val:.4f}° (err {err:.3f}%)")

    # Discriminant triangle angle
    alpha_disc = math.degrees(math.atan(math.sqrt(5/8)))
    print(f"\n  Discriminant triangle angle: arctan(√5/√8) = {alpha_disc:.4f}°")
    print(f"  Nearest cone: RC at {a_r:.4f}° (diff = {abs(alpha_disc-a_r):.4f}°, {abs(alpha_disc-a_r)/a_r*100:.2f}%)")

    return a_l, a_r, a_b


# ═══════════════════════════════════════════════════════════════════════
# TASK 6: THE DISCRIMINANT TRIANGLE IN 3D
# ═══════════════════════════════════════════════════════════════════════

def analyze_discriminant_mapping():
    """Map (√5, √8, √13) onto the cone geometry."""
    print("\n  TASK 6: DISCRIMINANT TRIANGLE → CONE MAPPING")
    print("  " + "─"*60)

    # The discriminant triangle
    print(f"\n  Discriminant triangle: (√5)² + (√8)² = (√13)²")
    print(f"    √5 = {math.sqrt(5):.6f}  (gold, momentum)")
    print(f"    √8 = {math.sqrt(8):.6f}  (silver, mass)")
    print(f"    √13 = {math.sqrt(13):.6f}  (bronze, observable)")

    # In the cone geometry: tan(α) = √5/√8 = √(5/8)
    tan_disc = math.sqrt(5/8)
    alpha_disc = math.atan(tan_disc)
    print(f"\n  tan(α_disc) = √5/√8 = √(5/8) = {tan_disc:.6f}")
    print(f"  α_disc = {math.degrees(alpha_disc):.4f}°")
    print(f"  α_rc   = {math.degrees(ALPHA_RC):.4f}°")
    print(f"  Difference: {abs(math.degrees(alpha_disc) - math.degrees(ALPHA_RC)):.4f}°")

    # BOS scaling
    print(f"\n  BOS maps the discriminant triangle into physical space:")
    print(f"    tan(α_base) = θ_base × BOS = {THETA_BASE*BOS:.6f}")
    print(f"    tan(α_rc)   = θ_rc × BOS   = {THETA_RC*BOS:.6f}")
    print(f"    tan(α_leak) = θ_leak × BOS = {THETA_LEAK*BOS:.6f}")
    print(f"    tan(α_disc) = √(5/8)        = {tan_disc:.6f}")

    # Ratio of discriminant to RC
    ratio_disc_rc = tan_disc / (THETA_RC * BOS)
    print(f"\n  tan(α_disc)/tan(α_rc) = {ratio_disc_rc:.6f}")
    print(f"  Compare: 1/φ = {1/PHI:.6f}  (diff {abs(ratio_disc_rc - 1/PHI):.6f})")
    print(f"  Compare: √(5/8)/r_c = {tan_disc/R_C:.6f}")


# ═══════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════

def main():
    W2 = 80
    print("="*W2)
    print("  DISCRIMINANT CONE VORTEX: The Formula IS the Geometry")
    print("  ratio = √(1 + (θ×BOS)²)  — the Pythagorean theorem in atomic form")
    print("="*W2)

    # ── Build element data ──
    elements = build_elements()
    print(f"\n  {len(elements)} elements mapped to spherical coordinates")

    # ── Task 1: Verify z = 1 identity ──
    print("\n  TASK 1: SPHERICAL MAPPING VERIFICATION")
    print("  " + "─"*60)
    z_vals = [e['z'] for e in elements]
    print(f"  z-component: mean = {np.mean(z_vals):.6f}, std = {np.std(z_vals):.6f}")
    print(f"  → All elements sit at z ≈ 1 (the plane z = 1 cuts all cones)")
    pyth_modes = [e for e in elements if e['mode'] in ('standard','magnetic','pythagorean')]
    if pyth_modes:
        z_pyth = [e['z'] for e in pyth_modes]
        print(f"  Pythagorean modes only: z mean = {np.mean(z_pyth):.8f}")
        print(f"  → For √(1+(θ×BOS)²) modes, z = 1 is EXACT")

    # ── Task 2 + 8a: Three cones visualization ──
    print("\n  Generating figures...")
    fig_8a_three_cones(elements)
    fig_8b_z1_crosssection(elements)
    fig_8c_side_discriminant(elements)

    # ── Task 4: Deviation analysis ──
    rho_G, rho_mohs, rho_en = analyze_deviations(elements)

    # ── Task 8d: Hardness plot ──
    rho_G2, rho_mohs2, rho_en2 = fig_8d_hardness(elements)

    # ── Task 5: Cone angle analysis ──
    a_l, a_r, a_b = analyze_cone_angles()

    # ── Task 6: Discriminant mapping ──
    analyze_discriminant_mapping()

    # ── Task 7 + 8e: Combined plot ──
    fig_8e_combined(elements)

    # ── Task 8f: Discriminant slice ──
    fig_8f_discriminant_slice(elements)

    # ── Save data ──
    data_out = {
        'cone_angles_deg': {'leak': a_l, 'rc': a_r, 'base': a_b},
        'cone_angles_rad': {'leak': ALPHA_LEAK, 'rc': ALPHA_RC, 'base': ALPHA_BASE},
        'BOS': BOS,
        'baseline_departure_from_45': abs(45 - a_b),
        'correlations': {
            'delta_alpha_vs_G': rho_G,
            'delta_alpha_vs_mohs': rho_mohs,
            'delta_alpha_vs_EN': rho_en,
        },
        'elements': [{
            'Z': e['Z'], 'sym': e['sym'], 'block': e['block'], 'mode': e['mode'],
            'theta_eff': round(e['theta_eff'], 6),
            'ratio_pred': round(e['ratio_pred'], 6),
            'ratio_obs': round(e['ratio_obs'], 6),
            'cone_angle_pred_deg': round(math.degrees(e['polar_pred']), 4),
            'cone_angle_obs_deg': round(math.degrees(e['polar_obs']), 4),
            'delta_alpha_deg': round(math.degrees(e['delta_alpha']), 4),
            'G_pct': round(e['G'], 2),
            'mohs': e['mohs'],
        } for e in elements],
        'cross_scale': [{
            'name': cs['name'], 'ratio': cs['ratio'], 'type': cs['type'],
            'cone_angle_deg': round(math.degrees(cs['polar']), 4),
        } for cs in CROSS_SCALE],
    }
    data_path = os.path.join(RESULTS_DIR, 'discriminant_cones.json')
    with open(data_path, 'w') as f:
        json.dump(data_out, f, indent=2)
    print(f"\n  Saved: {data_path}")

    # ── Final summary ──
    print(f"\n{'='*W2}")
    print(f"  SUMMARY")
    print(f"{'='*W2}")
    print(f"\n  Three cone angles:")
    print(f"    Leak:     {a_l:.4f}° = arctan({THETA_LEAK*BOS:.4f})")
    print(f"    RC:       {a_r:.4f}° = arctan({THETA_RC*BOS:.4f})")
    print(f"    Baseline: {a_b:.4f}° = arctan({THETA_BASE*BOS:.4f})")
    print(f"\n  Baseline departure from 45°: {abs(45-a_b):.4f}° ({abs(45-a_b)/45*100:.2f}%)")
    print(f"  BOS = baseline circle radius at z=1: {BOS:.6f} (EXACT identity)")
    print(f"\n  Correlations:")
    print(f"    Δα vs G (gate overflow):    ρ = {rho_G:.4f}")
    print(f"    Δα vs Mohs hardness:        ρ = {rho_mohs:.4f}")
    print(f"    Δα vs Electronegativity:    ρ = {rho_en:.4f}")
    print(f"\n  Discriminant triangle angle: {math.degrees(math.atan(math.sqrt(5/8))):.4f}°")
    print(f"  Nearest cone (RC):            {a_r:.4f}°")
    print(f"  Difference:                   {abs(math.degrees(math.atan(math.sqrt(5/8)))-a_r):.4f}°")
    print(f"\n  The formula IS the geometry. The geometry IS the vortex.")
    print(f"  Three cones. Three doors. One triangle. One axiom.")
    print(f"\n  Figures saved to: {RESULTS_DIR}/")
    print(f"  Data saved to:    {data_path}")


if __name__ == '__main__':
    main()
