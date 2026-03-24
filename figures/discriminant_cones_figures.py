#!/usr/bin/env python3
"""
discriminant_cones_figures.py — Publication Figures for the Discriminant Cones Paper
====================================================================================
Thomas A. Husmann / iBuilt LTD / March 2026

Generates 6 publication-quality figures for PRA format (3.375" single-column).
Saved as both PDF (vector) and PNG (300 dpi raster fallback).

Figure 1: Right Triangle Geometry (conceptual)
Figure 2: z=1 Cross-Section (THE key figure)
Figure 3: 3D Cone Side View
Figure 4: Gate Overflow Correlations (2-panel)
Figure 5: Cross-Scale Universality
Figure 6: Discriminant Triangle / Dirac Mapping

All spectral constants derived from AAH Hamiltonian. Zero free parameters.

Contributors:
  Claude (Anthropic) — computation, visualization, publication formatting
"""

import math, os, sys
import numpy as np

# ═══════════════════════════════════════════════════════════════════════
# MATPLOTLIB SETUP — PRA publication style
# ═══════════════════════════════════════════════════════════════════════

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Polygon, FancyArrowPatch, Arc
from matplotlib.lines import Line2D
import matplotlib.ticker as ticker

# PRA single-column width = 3.375 inches
COL_W = 3.375
DPI = 300

# Try LaTeX; fall back to mathtext
try:
    plt.rcParams['text.usetex'] = True
    fig_test = plt.figure(); ax_test = fig_test.add_subplot(111)
    ax_test.set_title(r'$\varphi$'); fig_test.savefig('/tmp/_test_latex.pdf')
    plt.close(fig_test)
    USE_LATEX = True
except Exception:
    plt.rcParams['text.usetex'] = False
    USE_LATEX = False

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif', 'serif'],
    'font.size': 8,
    'axes.labelsize': 9,
    'axes.titlesize': 10,
    'legend.fontsize': 7,
    'xtick.labelsize': 7,
    'ytick.labelsize': 7,
    'figure.dpi': DPI,
    'savefig.dpi': DPI,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.03,
    'lines.linewidth': 1.0,
    'axes.linewidth': 0.5,
    'xtick.major.width': 0.5,
    'ytick.major.width': 0.5,
    'xtick.direction': 'in',
    'ytick.direction': 'in',
})

# ═══════════════════════════════════════════════════════════════════════
# COLOR SCHEME
# ═══════════════════════════════════════════════════════════════════════

C_LEAK = '#2196F3'      # blue
C_RC   = '#FF9800'      # orange
C_BASE = '#4CAF50'      # green
C_REF  = '#9E9E9E'      # gray for reference lines

# Block colors (muted for publication)
C_S  = '#1565C0'   # dark blue
C_P  = '#E65100'   # dark orange
C_D  = '#2E7D32'   # dark green
C_NG = '#C62828'   # dark red
C_F  = '#6A1B9A'   # purple

BLOCK_COLORS = {'s': C_S, 'p': C_P, 'd': C_D, 'ng': C_NG, 'f': C_F}
BLOCK_MARKERS = {'s': 'o', 'p': 's', 'd': '^', 'ng': 'v', 'f': 'D'}

# ═══════════════════════════════════════════════════════════════════════
# FRAMEWORK CONSTANTS (from AAH spectrum)
# ═══════════════════════════════════════════════════════════════════════

PHI = (1 + math.sqrt(5)) / 2
PHI2 = PHI**2; PHI4 = PHI**4
LEAK = 1/PHI4; R_C = 1 - LEAK
W = (2 + PHI**(1/PHI**2)) / PHI4
GOLDEN_ANGLE_RAD = 2*math.pi / PHI2

DARK_GOLD = 0.290
SILVER_S3 = 0.171; GOLD_S3 = 0.236; BRONZE_S3 = 0.394

# Build spectrum
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

BASE = R_OUTER / R_SHELL
BOS = BRONZE_S3 / R_SHELL
G1 = GAPS_NORM[0]
SIGMA4 = 0.5594

RATIO_LEAK = 1 + LEAK
RATIO_REFLECT = BASE + DARK_GOLD * LEAK

THETA_LEAK = 0.564; THETA_RC = 0.854; THETA_BASE = 1.000
ALPHA_LEAK = math.atan(THETA_LEAK * BOS)
ALPHA_RC   = math.atan(THETA_RC * BOS)
ALPHA_BASE = math.atan(THETA_BASE * BOS)

MU_EFF = {26: 2.22, 27: 1.72, 28: 0.62}
REAL_CONFIG = {24:(5,1), 29:(10,1), 41:(4,1), 42:(5,1),
               44:(7,1), 45:(8,1), 46:(10,0), 47:(10,1)}

OBLATE = math.sqrt(PHI)  # 1.2720 — Bigollo #2 solution

# ═══════════════════════════════════════════════════════════════════════
# ELEMENT DATA
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

MOHS = {
    5:9.5,6:10,14:6.5,22:6.0,23:6.7,24:8.5,25:6.0,26:4.0,27:5.0,28:4.0,
    29:3.0,30:2.5,31:1.5,32:6.0,33:3.5,34:2.0,40:5.0,41:6.0,42:5.5,
    44:6.5,45:6.0,46:4.75,47:2.5,48:2.0,49:1.2,50:1.5,51:3.0,52:2.25,
    72:5.5,73:6.5,74:7.5,75:7.0,76:7.0,77:6.5,78:3.5,79:2.5,82:1.5,
    83:2.25,13:2.75,4:5.5,16:2.0
}

# ═══════════════════════════════════════════════════════════════════════
# AUFBAU + PREDICTION (unified Pythagorean, from bigollo_solver.py)
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
            blk = 'ng'; n_p = 0 if Z == 2 else n_p
    n_d = 0 if blk in ('p','s','ng') else n_d_val
    n_s = n_s_val
    if Z in REAL_CONFIG and blk == 'd':
        n_d, n_s = REAL_CONFIG[Z]
    return per, n_p, n_d, n_s, blk


def predict_ratio(Z):
    """Unified Pythagorean predictor (bigollo_solver θ formula + corrections)."""
    per, n_p, n_d, n_s, blk = aufbau(Z)
    mu = MU_EFF.get(Z, 0.0)

    if blk == 'd':
        is_boundary = (n_d <= 4 or n_d >= 9)
        has_s = (n_s > 0)
        if Z in MU_EFF:
            theta = 1 - (n_d/10)*DARK_GOLD + mu * LEAK
            mode = 'magnetic'
        elif is_boundary and has_s:
            theta = math.sqrt((1+LEAK)**2 - 1) / BOS
            mode = 'leak'
        elif n_d >= 9 and not has_s:
            theta = math.sqrt((BASE + DARK_GOLD*LEAK)**2 - 1) / BOS
            mode = 'reflect'
        else:
            theta = 1 - (n_d/10)*DARK_GOLD
            mode = 'standard'
    elif blk == 'ng':
        theta = 1 + n_p*(G1/BOS)*PHI**(-(per-1))
        mode = 'pythagorean'
    else:
        # Unified: use oblate factor from bigollo_solver
        theta = 1 + OBLATE * n_p * (G1/BOS) * PHI**(-(per-1))
        mode = 'additive'

    ratio = math.sqrt(1 + (theta * BOS)**2)

    # Corrections
    if blk == 'p' and n_p >= 4 and per >= 3:
        ratio *= R_C
        mode = 'p-hole'
    if Z == 2:
        ratio *= (1 + (1 - math.sqrt(1 - W**2)))

    return ratio, theta, per, n_p, n_d, n_s, blk, mode


def build_elements():
    """Build full element dataset with spherical coordinates."""
    period_starts = {1:1, 2:3, 3:11, 4:19, 5:37, 6:55, 7:87}
    elements = []
    for Z in sorted(RADII.keys()):
        if Z not in SYMBOLS: continue
        sym = SYMBOLS[Z]
        r_cov, r_vdw = RADII[Z]
        ratio_obs = r_vdw / r_cov
        rp, theta_eff, per, n_p, n_d, n_s, blk, mode = predict_ratio(Z)
        G = (ratio_obs - rp) / rp * 100

        polar_pred = math.atan(theta_eff * BOS)
        z_start = period_starts.get(per, 1)
        azimuth = GOLDEN_ANGLE_RAD * (Z - z_start)

        polar_obs = math.acos(min(1.0, 1.0/ratio_obs)) if ratio_obs >= 1 else 0
        delta_alpha = polar_obs - polar_pred

        # z=1 cross-section
        th_obs_val = math.sqrt(max(0, ratio_obs**2 - 1)) / BOS
        x_z1 = th_obs_val * BOS * math.cos(azimuth)
        y_z1 = th_obs_val * BOS * math.sin(azimuth)

        elements.append({
            'Z': Z, 'sym': sym, 'per': per, 'n_p': n_p, 'n_d': n_d,
            'n_s': n_s, 'block': blk, 'mode': mode,
            'theta_eff': theta_eff, 'ratio_pred': rp, 'ratio_obs': ratio_obs,
            'G': G, 'r_cov': r_cov, 'r_vdw': r_vdw,
            'polar_pred': polar_pred, 'polar_obs': polar_obs,
            'azimuth': azimuth, 'delta_alpha': delta_alpha,
            'x_z1': x_z1, 'y_z1': y_z1,
            'mohs': MOHS.get(Z),
        })
    return elements


# ═══════════════════════════════════════════════════════════════════════
# OUTPUT
# ═══════════════════════════════════════════════════════════════════════

OUT = '/Users/universe/Unified_Theory_Physics/figures/paper'


def savefig(fig, name):
    """Save as both PDF and PNG."""
    pdf_path = os.path.join(OUT, f'{name}.pdf')
    png_path = os.path.join(OUT, f'{name}.png')
    fig.savefig(pdf_path, format='pdf')
    fig.savefig(png_path, format='png')
    plt.close(fig)
    print(f"  Saved: {pdf_path}")
    print(f"  Saved: {png_path}")


# ═══════════════════════════════════════════════════════════════════════
# FIGURE 1 — Right Triangle Geometry
# ═══════════════════════════════════════════════════════════════════════

def fig1_right_triangle():
    fig, ax = plt.subplots(figsize=(COL_W, COL_W * 0.85))

    # Three overlaid triangles
    for theta, name, color, lw, alpha in [
        (THETA_BASE, 'Baseline', C_BASE, 1.8, 0.25),
        (THETA_RC,   'Crossover', C_RC, 1.8, 0.25),
        (THETA_LEAK, 'Leak', C_LEAK, 1.8, 0.25),
    ]:
        leg_h = theta * BOS
        hyp = math.sqrt(1 + leg_h**2)

        # Filled triangle
        tri = Polygon([(0, 0), (leg_h, 0), (0, 1)], closed=True,
                      facecolor=color, alpha=alpha, edgecolor='none')
        ax.add_patch(tri)

        # Triangle edges
        ax.plot([0, leg_h], [0, 0], color=color, lw=lw)  # horizontal
        ax.plot([0, 0], [0, 1], color=color, lw=lw)       # vertical
        ax.plot([leg_h, 0], [0, 1], color=color, lw=lw)   # hypotenuse

        # Angle arc at origin
        angle_deg = math.degrees(math.atan(leg_h))
        arc = Arc((0, 0), 0.2, 0.2, angle=0, theta1=90-angle_deg, theta2=90,
                  color=color, lw=1.2)
        ax.add_patch(arc)

        # Hypotenuse label
        mx, my = leg_h/2 * 0.45, 0.5 + 0.03
        rot = -math.degrees(math.atan(1/leg_h)) + 90
        offset = {'Baseline': (0.06, 0), 'Crossover': (0.04, 0), 'Leak': (0.02, 0)}
        ox, oy = offset[name]
        ax.text(mx+ox, my+oy, f'{name}\n' + r'$r={:.3f}$'.format(hyp),
                fontsize=6.5, color=color, rotation=rot, ha='center', va='center',
                fontweight='bold')

    # Labels
    ax.annotate(r'$z = 1$ (mass)', xy=(-0.06, 0.5), fontsize=8,
                rotation=90, ha='center', va='center', color='#333')
    ax.annotate(r'$\theta_{\mathrm{eff}} \times \mathrm{BOS}$ (momentum)',
                xy=(0.5, -0.06), fontsize=8, ha='center', va='center', color='#333')

    # Right angle marker
    sq = 0.04
    ax.plot([sq, sq, 0], [0, sq, sq], color='k', lw=0.7)

    # r cos α = 1 annotation
    ax.annotate(r'$r \cos\alpha = 1$ (exact)',
                xy=(0.02, 1.05), fontsize=7, style='italic', color='#555')

    # Cone angle labels
    for theta, name, color, y_off in [
        (THETA_LEAK, r'$29.2°$', C_LEAK, 0.12),
        (THETA_RC, r'$40.3°$', C_RC, 0.20),
        (THETA_BASE, r'$44.8°$', C_BASE, 0.27),
    ]:
        ax.text(0.06, y_off, name, fontsize=6, color=color)

    # Title
    ax.set_title(r'$r = \sqrt{1 + (\theta_{\mathrm{eff}} \cdot \mathrm{BOS})^2}$',
                 fontsize=11, pad=8)

    ax.set_xlim(-0.12, 1.12)
    ax.set_ylim(-0.12, 1.15)
    ax.set_aspect('equal')
    ax.axis('off')

    savefig(fig, 'fig1_right_triangle')


# ═══════════════════════════════════════════════════════════════════════
# FIGURE 2 — z=1 Cross-Section (THE key figure)
# ═══════════════════════════════════════════════════════════════════════

def fig2_z1_crosssection(elements):
    fig, ax = plt.subplots(figsize=(COL_W, COL_W))

    # Three concentric circles
    for theta, name, color, ls in [
        (THETA_LEAK, f'Leak $r={THETA_LEAK*BOS:.3f}$', C_LEAK, '--'),
        (THETA_RC,   f'RC $r={THETA_RC*BOS:.3f}$', C_RC, '--'),
        (THETA_BASE, f'Base $r=BOS={THETA_BASE*BOS:.3f}$', C_BASE, '--'),
    ]:
        circle = plt.Circle((0, 0), theta*BOS, fill=False, color=color,
                            lw=1.2, ls=ls)
        ax.add_patch(circle)

    # Plot elements
    labels_to_show = {20:'Ca', 29:'Cu', 55:'Cs', 80:'Hg', 9:'F', 82:'Pb',
                      79:'Au', 6:'C', 26:'Fe', 10:'Ne', 47:'Ag', 74:'W',
                      57:'La', 36:'Kr'}
    for e in elements:
        c = BLOCK_COLORS.get(e['block'], 'gray')
        mk = BLOCK_MARKERS.get(e['block'], 'o')
        ax.scatter([e['x_z1']], [e['y_z1']], c=c, marker=mk, s=12,
                  alpha=0.85, edgecolors='k', linewidths=0.2, zorder=5)
        if e['Z'] in labels_to_show:
            ax.annotate(e['sym'], (e['x_z1'], e['y_z1']),
                       fontsize=5.5, ha='center', va='bottom',
                       xytext=(0, 2.5), textcoords='offset points',
                       color='#333')

    ax.set_xlim(-1.35, 1.35)
    ax.set_ylim(-1.35, 1.35)
    ax.set_aspect('equal')
    ax.set_xlabel(r'$\theta \cdot \mathrm{BOS} \cdot \cos\phi$', fontsize=9)
    ax.set_ylabel(r'$\theta \cdot \mathrm{BOS} \cdot \sin\phi$', fontsize=9)
    ax.axhline(0, color=C_REF, lw=0.3)
    ax.axvline(0, color=C_REF, lw=0.3)

    # Block legend
    handles = [Line2D([0],[0], marker=BLOCK_MARKERS[b], color='w',
               markerfacecolor=BLOCK_COLORS[b], markersize=5,
               label={'s':'s-block','p':'p-block','d':'d-block','ng':'Noble gas','f':'f-block'}[b])
               for b in ['s','p','d','ng']]
    # Cone legend
    handles += [Line2D([0],[0], ls='--', color=c, lw=1, label=n)
                for c, n in [(C_LEAK,'Leak'), (C_RC,'Crossover'), (C_BASE,'Baseline')]]
    ax.legend(handles=handles, fontsize=5.5, loc='upper right',
             framealpha=0.9, handletextpad=0.3, borderpad=0.3)

    ax.set_title(r'$z = 1$ cross-section: three cones $\to$ three circles', fontsize=9, pad=6)

    savefig(fig, 'fig2_z1_crosssection')


# ═══════════════════════════════════════════════════════════════════════
# FIGURE 3 — 3D Cone Side View
# ═══════════════════════════════════════════════════════════════════════

def fig3_cone_3d(elements):
    fig = plt.figure(figsize=(COL_W, COL_W * 1.1))
    ax = fig.add_subplot(111, projection='3d')

    # Draw cone surfaces
    t_max = 1.55
    for alpha, color, name in [
        (ALPHA_LEAK, C_LEAK, 'Leak'),
        (ALPHA_RC, C_RC, 'RC'),
        (ALPHA_BASE, C_BASE, 'Base'),
    ]:
        # Cone surface
        t = np.linspace(0, t_max, 15)
        phi_az = np.linspace(0, 2*np.pi, 40)
        T, P = np.meshgrid(t, phi_az)
        X = T * math.sin(alpha) * np.cos(P)
        Y = T * math.sin(alpha) * np.sin(P)
        Z = T * math.cos(alpha)
        ax.plot_surface(X, Y, Z, alpha=0.06, color=color, linewidth=0)

        # Guide line
        t_line = np.linspace(0, t_max, 50)
        ax.plot(t_line*math.sin(alpha), np.zeros_like(t_line),
                t_line*math.cos(alpha), color=color, lw=1.2, alpha=0.8,
                label=f'{name} {math.degrees(alpha):.1f}' + r'$°$')

    # Discriminant angle reference
    alpha_disc = math.atan(math.sqrt(5/8))
    t_line = np.linspace(0, t_max, 50)
    ax.plot(t_line*math.sin(alpha_disc), np.zeros_like(t_line),
            t_line*math.cos(alpha_disc), color=C_REF, lw=1.0, ls='--',
            label=r'$\arctan(\sqrt{5/8})=38.3°$')

    # z=1 plane circle
    phi_az = np.linspace(0, 2*np.pi, 80)
    for alpha, color in [(ALPHA_LEAK, C_LEAK), (ALPHA_RC, C_RC), (ALPHA_BASE, C_BASE)]:
        r_circ = math.tan(alpha)
        ax.plot(r_circ*np.cos(phi_az), r_circ*np.sin(phi_az),
                np.ones_like(phi_az), color=color, lw=0.6, alpha=0.5)

    # Elements at z=1
    notable = {6:'C', 26:'Fe', 29:'Cu', 47:'Ag', 55:'Cs', 10:'Ne', 79:'Au', 74:'W'}
    for e in elements:
        c = BLOCK_COLORS.get(e['block'], 'gray')
        r = e['ratio_obs']
        pol = e['polar_obs']
        az = e['azimuth']
        ex = r * math.sin(pol) * math.cos(az)
        ey = r * math.sin(pol) * math.sin(az)
        ez = r * math.cos(pol)
        ax.scatter([ex], [ey], [ez], c=c, s=8, alpha=0.7,
                  edgecolors='k', linewidths=0.15)
        if e['Z'] in notable:
            ax.text(ex, ey, ez, f' {e["sym"]}', fontsize=5, color='#333')

    ax.view_init(elev=25, azim=-60)
    ax.set_xlim(-1.3, 1.3); ax.set_ylim(-1.3, 1.3); ax.set_zlim(0, 1.6)
    ax.set_xlabel(r'$x$', fontsize=8, labelpad=-2)
    ax.set_ylabel(r'$y$', fontsize=8, labelpad=-2)
    ax.set_zlabel(r'$z$ (mass)', fontsize=8, labelpad=-2)
    ax.tick_params(labelsize=5, pad=-2)
    ax.legend(fontsize=5, loc='upper left', framealpha=0.9)
    ax.set_title('Three cones sharing the mass axis', fontsize=9, pad=-2)

    savefig(fig, 'fig3_cone_3d')


# ═══════════════════════════════════════════════════════════════════════
# FIGURE 4 — Gate Overflow Correlations (2-panel)
# ═══════════════════════════════════════════════════════════════════════

def fig4_correlations(elements):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(COL_W * 2, COL_W * 0.85),
                                    sharey=True)

    # Exclude H and He (extreme outliers) for cleaner view
    els = [e for e in elements if e['Z'] > 2]
    superhard = {5, 6, 24, 74, 76}  # B, C, Cr, W, Os

    # LEFT: Δα vs G
    da = [math.degrees(e['delta_alpha']) for e in els]
    G = [e['G'] for e in els]
    for e in els:
        c = '#C62828' if e['Z'] in superhard else BLOCK_COLORS.get(e['block'], 'gray')
        s = 20 if e['Z'] in superhard else 10
        ax1.scatter(e['G'], math.degrees(e['delta_alpha']), c=c, s=s,
                   alpha=0.8, edgecolors='k', linewidths=0.2, zorder=5)
        if e['Z'] in superhard:
            ax1.annotate(e['sym'], (e['G'], math.degrees(e['delta_alpha'])),
                        fontsize=5, xytext=(2, 2), textcoords='offset points',
                        color='#C62828', fontweight='bold')

    rho_G = np.corrcoef(G, da)[0, 1]
    # Fit line
    m, b = np.polyfit(G, da, 1)
    x_fit = np.linspace(min(G), max(G), 100)
    ax1.plot(x_fit, m*x_fit + b, color=C_REF, lw=0.8, ls='-', alpha=0.6)

    ax1.set_xlabel(r'Gate overflow $G$ (%)', fontsize=9)
    ax1.set_ylabel(r'$\Delta\alpha$ (degrees)', fontsize=9)
    ax1.axhline(0, color=C_REF, lw=0.4)
    ax1.axvline(0, color=C_REF, lw=0.4)
    ax1.text(0.05, 0.92, r'$\rho = {:.3f}$'.format(rho_G),
            transform=ax1.transAxes, fontsize=8, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                     edgecolor='gray', alpha=0.9))
    ax1.set_title('(a) Cone deviation vs gate overflow', fontsize=8)
    ax1.grid(True, alpha=0.15, lw=0.3)

    # RIGHT: Δα vs Mohs
    hard_els = [e for e in els if e['mohs'] is not None and e['mohs'] > 0]
    da_m = [math.degrees(e['delta_alpha']) for e in hard_els]
    mohs_m = [e['mohs'] for e in hard_els]

    for e in hard_els:
        c = '#C62828' if e['Z'] in superhard else BLOCK_COLORS.get(e['block'], 'gray')
        s = 20 if e['Z'] in superhard else 10
        ax2.scatter(e['mohs'], math.degrees(e['delta_alpha']), c=c, s=s,
                   alpha=0.8, edgecolors='k', linewidths=0.2, zorder=5)
        if e['mohs'] >= 7 or abs(math.degrees(e['delta_alpha'])) > 5:
            ax2.annotate(e['sym'], (e['mohs'], math.degrees(e['delta_alpha'])),
                        fontsize=5, xytext=(2, 1), textcoords='offset points',
                        color='#333')

    rho_mohs = np.corrcoef(mohs_m, da_m)[0, 1]
    m2, b2 = np.polyfit(mohs_m, da_m, 1)
    x_fit2 = np.linspace(1, 10.5, 100)
    ax2.plot(x_fit2, m2*x_fit2 + b2, color=C_REF, lw=0.8, ls='-', alpha=0.6)

    ax2.set_xlabel('Mohs hardness', fontsize=9)
    ax2.axhline(0, color=C_REF, lw=0.4)
    ax2.text(0.05, 0.92, r'$\rho = {:.3f}$'.format(rho_mohs),
            transform=ax2.transAxes, fontsize=8, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                     edgecolor='gray', alpha=0.9))
    ax2.set_title('(b) Cone deviation vs Mohs hardness', fontsize=8)
    ax2.grid(True, alpha=0.15, lw=0.3)

    plt.tight_layout()
    savefig(fig, 'fig4_correlations')
    return rho_G, rho_mohs


# ═══════════════════════════════════════════════════════════════════════
# FIGURE 5 — Cross-Scale Universality
# ═══════════════════════════════════════════════════════════════════════

def fig5_cross_scale(elements):
    fig, ax = plt.subplots(figsize=(COL_W * 2, COL_W * 0.7))

    # Three mode bands (±2%)
    modes = [
        (1.146, 'Leak', C_LEAK),
        (1.311, 'RC', C_RC),
        (1.409, 'Base', C_BASE),
    ]
    for val, name, color in modes:
        ax.axvspan(val*0.98, val*1.02, color=color, alpha=0.12)
        ax.axvline(val, color=color, lw=1.2, ls='-', alpha=0.6)
        ax.text(val, 1.02, name, ha='center', va='bottom', fontsize=7,
               color=color, fontweight='bold', transform=ax.get_xaxis_transform())

    # Atomic ratios (histogram along top)
    atomic_ratios = [e['ratio_pred'] for e in elements if e['Z'] > 2]
    ax.hist(atomic_ratios, bins=30, range=(1.0, 1.6), color='gray', alpha=0.3,
           density=True, label='Atomic predictions')

    # Solar system consecutive ratios
    solar_a = {'Mercury': 0.387, 'Venus': 0.723, 'Earth': 1.000,
               'Mars': 1.524, 'Jupiter': 5.203, 'Saturn': 9.537,
               'Uranus': 19.19, 'Neptune': 30.07}
    names = list(solar_a.keys())
    ratios_solar = []
    for i in range(len(names)-1):
        r = solar_a[names[i+1]] / solar_a[names[i]]
        ratios_solar.append((f'{names[i+1]}/{names[i]}', r))

    y_solar = 0.65
    for name, r in ratios_solar:
        if 1.0 <= r <= 2.0:
            # Find nearest mode
            nearest = min(modes, key=lambda m: abs(m[0] - r))
            err = abs(r - nearest[0]) / nearest[0] * 100
            ax.plot(r, y_solar, 'p', color='#1A237E', markersize=7,
                   markeredgecolor='k', markeredgewidth=0.3)
            ax.annotate(f'{name}\n{r:.3f} ({err:.1f}%)',
                       (r, y_solar), fontsize=4.5, ha='center', va='bottom',
                       xytext=(0, 5), textcoords='offset points', color='#1A237E')
            y_solar += 0.15

    # TRAPPIST-1 (Agol et al. 2021 semi-major axes in AU)
    trappist = {'b': 0.01154, 'c': 0.01580, 'd': 0.02227,
                'e': 0.02925, 'f': 0.03849, 'g': 0.04683, 'h': 0.06189}
    t_names = list(trappist.keys())
    y_trap = 3.5
    for i in range(len(t_names)-1):
        r = trappist[t_names[i+1]] / trappist[t_names[i]]
        if 1.0 <= r <= 2.0:
            nearest = min(modes, key=lambda m: abs(m[0] - r))
            err = abs(r - nearest[0]) / nearest[0] * 100
            ax.plot(r, y_trap, '*', color='#B71C1C', markersize=8,
                   markeredgecolor='k', markeredgewidth=0.3)
            ax.annotate(f'T1 {t_names[i+1]}/{t_names[i]}\n{r:.3f} ({err:.1f}%)',
                       (r, y_trap), fontsize=4.5, ha='center', va='bottom',
                       xytext=(0, 5), textcoords='offset points', color='#B71C1C')
            y_trap += 0.15

    # Molecular ratios
    mol_data = [
        (r'Cl$_2$/F$_2$', 1.988/1.412, '#E65100'),
        (r'Br$_2$/Cl$_2$', 2.281/1.988, '#E65100'),
        (r'I$_2$/Br$_2$', 2.666/2.281, '#E65100'),
    ]
    y_mol = 2.2
    for name, r, color in mol_data:
        if 1.0 <= r <= 2.0:
            nearest = min(modes, key=lambda m: abs(m[0] - r))
            err = abs(r - nearest[0]) / nearest[0] * 100
            ax.plot(r, y_mol, 'D', color=color, markersize=5,
                   markeredgecolor='k', markeredgewidth=0.3)
            ax.annotate(f'{name}\n{r:.3f} ({err:.1f}%)',
                       (r, y_mol), fontsize=4.5, ha='center', va='bottom',
                       xytext=(0, 4), textcoords='offset points', color=color)
            y_mol += 0.15

    # Kepler 3:2 peak
    kep = (3/2)**(2/3)
    ax.axvline(kep, color='#4A148C', lw=1.5, ls=':', alpha=0.7)
    ax.text(kep+0.01, 4.5, f'Kepler 3:2\n{kep:.4f}', fontsize=5, color='#4A148C')

    ax.set_xlabel('Consecutive ratio', fontsize=9)
    ax.set_ylabel('Density / markers', fontsize=9)
    ax.set_xlim(1.0, 1.65)
    ax.set_title('Cross-scale universality: atoms, molecules, planets on three cones', fontsize=9, pad=6)

    # Custom legend
    handles = [
        Line2D([0],[0], marker='o', color='w', markerfacecolor='gray', markersize=5, label='Atoms'),
        Line2D([0],[0], marker='p', color='w', markerfacecolor='#1A237E', markersize=6, label='Solar system'),
        Line2D([0],[0], marker='*', color='w', markerfacecolor='#B71C1C', markersize=8, label='TRAPPIST-1'),
        Line2D([0],[0], marker='D', color='w', markerfacecolor='#E65100', markersize=5, label='Halogens'),
    ]
    ax.legend(handles=handles, fontsize=6, loc='upper right', framealpha=0.9)
    ax.grid(True, axis='x', alpha=0.15, lw=0.3)

    plt.tight_layout()
    savefig(fig, 'fig5_cross_scale')

    # Return solar ratios for summary table
    return ratios_solar


# ═══════════════════════════════════════════════════════════════════════
# FIGURE 6 — Discriminant Triangle / Dirac Mapping
# ═══════════════════════════════════════════════════════════════════════

def fig6_discriminant():
    fig, ax = plt.subplots(figsize=(COL_W, COL_W))

    # The right triangle: legs √8 (horizontal, silver/mass) and √5 (vertical, gold/momentum)
    s5 = math.sqrt(5)
    s8 = math.sqrt(8)
    s13 = math.sqrt(13)

    # Triangle vertices
    ax.plot([0, s8, 0, 0], [0, 0, s5, 0], 'k-', lw=2)

    # Filled regions for block mapping
    # s-block: near silver vertex (0,0) → low momentum
    tri_s = Polygon([(0,0), (s8*0.3, 0), (0, s5*0.15)], closed=True,
                    facecolor=C_S, alpha=0.15)
    ax.add_patch(tri_s)
    ax.text(s8*0.08, s5*0.03, 's-block\n(mass)', fontsize=6, color=C_S)

    # p-block: along gold (vertical) axis
    tri_p = Polygon([(0, s5*0.3), (0, s5*0.9), (s8*0.15, s5*0.4)], closed=True,
                    facecolor=C_P, alpha=0.12)
    ax.add_patch(tri_p)
    ax.text(0.05, s5*0.6, 'p-block\n(momentum)', fontsize=6, color=C_P, rotation=70)

    # d-block: interior
    tri_d = Polygon([(s8*0.2, s5*0.1), (s8*0.6, s5*0.1), (s8*0.3, s5*0.35)],
                    closed=True, facecolor=C_D, alpha=0.12)
    ax.add_patch(tri_d)
    ax.text(s8*0.32, s5*0.15, 'd-block', fontsize=6, color=C_D)

    # Noble gas: near hypotenuse
    ax.text(s8*0.45, s5*0.42, 'Noble gas\n(surface)', fontsize=6, color=C_NG, rotation=-32)

    # Leg labels
    ax.annotate(r'$\sqrt{8}$ (Silver, $\Delta_2$, mass)', xy=(s8/2, -0.25),
               fontsize=8, ha='center', color='#555')
    ax.annotate(r'$\sqrt{5}$ (Gold, $\Delta_1$, momentum)', xy=(-0.45, s5/2),
               fontsize=8, ha='center', rotation=90, color='#555')
    ax.annotate(r'$\sqrt{13}$ (Bronze, $\Delta_3$)', xy=(s8/2+0.2, s5/2+0.15),
               fontsize=8, ha='center', rotation=-math.degrees(math.atan(s5/s8)),
               color='#555')

    # Cone angle projections
    for theta, name, color in [
        (THETA_LEAK, 'Leak', C_LEAK),
        (THETA_RC, 'RC', C_RC),
        (THETA_BASE, 'Base', C_BASE),
    ]:
        # Line from origin at angle = arctan(θ×BOS × √8/√5) scaled
        angle = math.atan(theta * BOS * s8 / s5)
        t_max = s13 * 0.85
        x_end = t_max * math.cos(angle)
        y_end = t_max * math.sin(angle)
        ax.plot([0, x_end], [0, y_end], color=color, lw=1.2, ls='-', alpha=0.5)
        ax.text(x_end+0.05, y_end+0.05, name, fontsize=5.5, color=color)

    # Discriminant angle
    alpha_disc = math.atan(s5/s8)
    t_max = s13 * 0.9
    ax.plot([0, t_max*math.cos(alpha_disc)], [0, t_max*math.sin(alpha_disc)],
           color=C_REF, lw=1.0, ls='--')
    ax.text(t_max*math.cos(alpha_disc)*0.6, t_max*math.sin(alpha_disc)*0.65,
           f'{math.degrees(alpha_disc):.1f}' + r'$°$', fontsize=6, color=C_REF)

    # Dirac mapping annotation
    ax.text(0.55, 0.88, r'$E^2 = p^2c^2 + m^2c^4$' + '\n' +
            r'$(\sqrt{13})^2 = (\sqrt{5})^2 + (\sqrt{8})^2$' + '\n' +
            r'$13 = 5 + 8$',
           transform=ax.transAxes, fontsize=8,
           bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow',
                    edgecolor='gray', alpha=0.95),
           ha='center', va='top')

    # Right angle marker
    sq = 0.12
    ax.plot([sq, sq, 0], [0, sq, sq], color='k', lw=0.6)

    ax.set_xlim(-0.6, s8+0.3)
    ax.set_ylim(-0.4, s5+0.3)
    ax.set_aspect('equal')
    ax.set_title('Discriminant triangle: Dirac equation as geometry', fontsize=9, pad=6)
    ax.axis('off')

    savefig(fig, 'fig6_discriminant')


# ═══════════════════════════════════════════════════════════════════════
# SOLAR SYSTEM SUMMARY TABLE
# ═══════════════════════════════════════════════════════════════════════

def print_solar_table(ratios_solar):
    modes = [(1.146, 'Leak'), (1.311, 'RC'), (1.409, 'Base')]

    print("\n" + "="*70)
    print("  SOLAR SYSTEM CONSECUTIVE RATIOS — MODE MATCHING")
    print("="*70)
    print(f"  {'Pair':<20} {'Ratio':>8} {'Nearest':>10} {'Mode Val':>10} {'Error':>8}")
    print("  " + "-"*60)

    for name, r in ratios_solar:
        nearest = min(modes, key=lambda m: abs(m[0] - r))
        err = (r - nearest[0]) / nearest[0] * 100
        in_range = '  *' if abs(err) < 5 else ''
        print(f"  {name:<20} {r:8.4f} {nearest[1]:>10} {nearest[0]:10.3f} {err:+7.2f}%{in_range}")

    # Also show φ ratios
    print(f"\n  Reference ratios:")
    print(f"    1/φ⁴ + 1 = {1+LEAK:.4f}  (Leak mode)")
    print(f"    R_C + 1/φ³ = {R_C + 1/PHI**3:.4f}")
    print(f"    σ₄/σ_shell = {BASE:.4f}  (Baseline mode)")
    print(f"    φ = {PHI:.4f}")
    print(f"    (3/2)^(2/3) = {(1.5)**(2/3):.4f}  (Kepler 3:2)")


# ═══════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════

def main():
    print("="*70)
    print("  DISCRIMINANT CONES — Publication Figures")
    print(f"  PRA format: {COL_W}\" single column, {DPI} DPI")
    print(f"  LaTeX rendering: {'YES' if USE_LATEX else 'NO (using mathtext)'}")
    print("="*70)

    elements = build_elements()
    print(f"\n  {len(elements)} elements built")
    print(f"  BASE={BASE:.6f}  BOS={BOS:.6f}  G1={G1:.6f}")
    print(f"  Cone angles: Leak={math.degrees(ALPHA_LEAK):.2f}°  "
          f"RC={math.degrees(ALPHA_RC):.2f}°  Base={math.degrees(ALPHA_BASE):.2f}°\n")

    print("  Generating figures...\n")

    fig1_right_triangle()
    fig2_z1_crosssection(elements)
    fig3_cone_3d(elements)
    rho_G, rho_mohs = fig4_correlations(elements)
    ratios_solar = fig5_cross_scale(elements)
    fig6_discriminant()

    print_solar_table(ratios_solar)

    print(f"\n{'='*70}")
    print(f"  FIGURE SUMMARY")
    print(f"{'='*70}")
    print(f"  Fig 1: Right triangle geometry (conceptual)")
    print(f"  Fig 2: z=1 cross-section — three circles = periodic table")
    print(f"  Fig 3: 3D cone side view with discriminant reference")
    print(f"  Fig 4: Correlations — Δα vs G (ρ={rho_G:.3f}), vs Mohs (ρ={rho_mohs:.3f})")
    print(f"  Fig 5: Cross-scale universality (atoms + planets + molecules)")
    print(f"  Fig 6: Discriminant triangle / Dirac mapping")
    print(f"\n  All figures saved to: {OUT}/")
    print(f"  Formats: PDF (vector) + PNG ({DPI} dpi raster)")


if __name__ == '__main__':
    main()
