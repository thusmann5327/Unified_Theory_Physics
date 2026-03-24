#!/usr/bin/env python3
"""
vortex_funnel.py — Find the coordinate system that creates a vortex FUNNEL
═══════════════════════════════════════════════════════════════════════════
The three band radii create cylinders, not a funnel. For a vortex shape,
the radius must CHANGE with height. This script tests mappings where
radius and height are correlated — creating a cone or tornado shape.

Key insight: in a physical vortex, the fastest-spinning material is at
the narrowest point. For atoms, the "fastest spinning" = highest EN or
IE. If we map height = IE and radius = 1/IE (or r_cov), then high-IE
elements are at the top AND at small radius → funnel!

Thomas A. Husmann / iBuilt LTD — March 2026
═══════════════════════════════════════════════════════════════════════════
"""

import matplotlib
matplotlib.use('Agg')

import numpy as np
import math
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Patch

PHI = (1 + math.sqrt(5)) / 2
GOLDEN_ANGLE_RAD = 2 * math.pi / PHI**2
W = (2 + PHI**(1/PHI**2)) / PHI**4
BOS = 0.992022
LEAK = 1/PHI**4; R_C = 1 - LEAK
G1 = 0.3243; DARK_GOLD = 0.290; BASE = 1.408382; RY_EV = 13.6057
THETA_LEAK = 0.564; THETA_RC = 0.854; THETA_BASE = 1.000
MU_EFF = {26:2.22, 27:1.72, 28:0.62}
REAL_CONFIG = {24:(5,1),29:(10,1),41:(4,1),42:(5,1),44:(7,1),45:(8,1),46:(10,0),47:(10,1)}

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

# ── aufbau + predict_ratio (compact) ──
def aufbau(Z):
    sub = []
    for n in range(1,8):
        for l in range(n):
            sub.append((n,l,2*(2*l+1)))
    sub.sort(key=lambda s: (s[0]+s[1],s[0]))
    rem = Z; filled = []
    for n,l,cap in sub:
        if rem <= 0: break
        e = min(rem,cap); filled.append((n,l,e,cap)); rem -= e
    per = max(n for n,l,e,c in filled)
    n_p = sum(e for n,l,e,c in filled if n==per and l==1)
    n_d_val = sum(e for n,l,e,c in filled if l==2 and n==per-1)
    n_s_val = sum(e for n,l,e,c in filled if n==per and l==0)
    last_l = filled[-1][1]
    blk = {0:'s',1:'p',2:'d',3:'f'}.get(last_l,'?')
    se={}; sm2={}
    for n,l,e,cap in filled: se[n]=se.get(n,0)+e; sm2[n]=sm2.get(n,0)+cap
    if se.get(per,0)==sm2.get(per,0):
        if Z==2 or (last_l==1 and filled[-1][2]==filled[-1][3]):
            blk='ng'
            if Z==2: n_p=0
    n_d = 0 if blk in ('p','s','ng') else n_d_val
    n_s = n_s_val
    if Z in REAL_CONFIG and blk=='d': n_d,n_s = REAL_CONFIG[Z]
    return per,n_p,n_d,n_s,blk

def predict_ratio(Z):
    per,n_p,n_d,n_s,block = aufbau(Z)
    if block=='d':
        if Z in MU_EFF:
            mu=MU_EFF[Z]; theta=1-(n_d/10)*DARK_GOLD+mu*LEAK
            return math.sqrt(1+(theta*BOS)**2),theta,per,n_p,n_d,n_s,block
        is_boundary=(n_d<=4 or n_d>=9); has_s=(n_s>0)
        if is_boundary and has_s: return 1+LEAK,THETA_LEAK,per,n_p,n_d,n_s,block
        elif n_d>=9 and not has_s: return BASE+DARK_GOLD*LEAK,THETA_BASE,per,n_p,n_d,n_s,block
        else:
            theta=1-(n_d/10)*DARK_GOLD
            return math.sqrt(1+(theta*BOS)**2),theta,per,n_p,n_d,n_s,block
    elif block=='ng':
        theta=1+n_p*(G1/BOS)*PHI**(-(per-1))
        return math.sqrt(1+(theta*BOS)**2),theta,per,n_p,n_d,n_s,block
    else:
        ratio=BASE+n_p*G1*PHI**(-(per-1)); theta=ratio/BASE
        if block=='p' and n_p>=4 and per>=3:
            ratio*=R_C; return ratio,theta,per,n_p,n_d,n_s,block
        return ratio,theta,per,n_p,n_d,n_s,block

# Build elements
elements = []
for Z in sorted(RADII.keys()):
    sym = SYMBOLS.get(Z)
    if not sym: continue
    r_cov,r_vdw = RADII[Z]
    rp,theta,per,n_p,n_d,n_s,block = predict_ratio(Z)
    en = EN_PAULING.get(Z,1.0)
    ie = IE1.get(Z,7.0)
    elements.append(dict(Z=Z,sym=sym,r_cov=r_cov,r_vdw=r_vdw,
                         ratio_pred=rp,theta=theta,per=per,n_p=n_p,
                         n_d=n_d,n_s=n_s,block=block,en=en,ie=ie))

N = len(elements)
BLOCK_COLORS = {'s':'#e74c3c','p':'#3498db','d':'#2ecc71','ng':'#f39c12','f':'#9b59b6'}
RESULTS_DIR = '/Users/universe/Unified_Theory_Physics/results/vortex_explorer'
os.makedirs(RESULTS_DIR, exist_ok=True)

print("=" * 80)
print("  VORTEX FUNNEL — Coordinate systems that create cone/tornado shapes")
print("=" * 80)
print(f"  {N} elements\n")


# ═══════════════════════════════════════════════════════════════════
# FUNNEL MAPPINGS — radius changes with height
# ═══════════════════════════════════════════════════════════════════

# The key insight: for a vortex funnel, we need:
#   - angle = golden angle × Z (preserves the spiral)
#   - height and radius must be ANTI-correlated (narrow at top)
#   OR: height and radius CORRELATED (wide at top = mushroom/plume)

mappings = {}

# ── 1. Physical vortex: r_cov as radius, IE as height ──
# Large atoms (Cs, Rb) at wide radius, low IE → base of tornado
# Small atoms (F, O, N) at narrow radius, high IE → top of tornado
mappings['r_cov radius, IE height'] = {
    'r': np.array([e['r_cov'] for e in elements], float) / 100.0,  # scale to ~1-2
    'z': np.array([e['ie'] for e in elements], float),
    'desc': 'Big slow atoms at base, small energetic atoms at top'
}

# ── 2. Inverse: 1/r_cov radius, IE height ──
# Small atoms at LARGE radius (more energetic → further out)
mappings['1/r_cov radius, IE height'] = {
    'r': 100.0 / np.array([e['r_cov'] for e in elements], float),
    'z': np.array([e['ie'] for e in elements], float),
    'desc': 'Compact energetic atoms at large radius and high — plume'
}

# ── 3. r_cov as radius, EN as height ──
mappings['r_cov radius, EN height'] = {
    'r': np.array([e['r_cov'] for e in elements], float) / 100.0,
    'z': np.array([e['en'] for e in elements], float),
    'desc': 'Size radius, reactivity height — noble gases at ground'
}

# ── 4. θ as radius, EN as height ──
# θ separates modes well (band_sep=2.433), EN is smooth
mappings['θ radius, EN height'] = {
    'r': np.array([e['theta'] for e in elements], float),
    'z': np.array([e['en'] for e in elements], float),
    'desc': 'Mode parameter radius, reactivity height'
}

# ── 5. ratio_pred × (1 + EN/10) — radius expands with EN ──
# This modulates the band radius by EN, creating a horn shape
rp_arr = np.array([e['ratio_pred'] for e in elements], float)
en_arr = np.array([e['en'] for e in elements], float)
ie_arr = np.array([e['ie'] for e in elements], float)
mappings['ratio×(1+EN/10), Z height'] = {
    'r': rp_arr * (1 + en_arr / 10),
    'z': np.array([e['Z'] for e in elements], float),
    'desc': 'Bands widen with EN — horn/trumpet shape'
}

# ── 6. ratio_pred as radius, but height = period with EN sub-position ──
# Each period is one "loop" of the vortex, EN determines height within loop
per_arr = np.array([e['per'] for e in elements], float)
mappings['ratio radius, per+EN/5 height'] = {
    'r': rp_arr,
    'z': per_arr + en_arr / 5.0,
    'desc': 'Stacked period rings with EN gradient within each'
}

# ── 7. The Cantor funnel: ratio/period as radius, Z as height ──
# Ratio shrinks in higher periods → funnel narrows upward
mappings['ratio/√per radius, Z height'] = {
    'r': rp_arr / np.sqrt(per_arr),
    'z': np.array([e['Z'] for e in elements], float),
    'desc': 'Bands narrow by 1/√period — natural Cantor compression'
}

# ── 8. EN-weighted radius, log(IE) height ──
mappings['EN/4 radius, log(IE) height'] = {
    'r': np.maximum(en_arr / 4.0, 0.05),
    'z': np.log(ie_arr),
    'desc': 'Reactivity radius, log-energy height'
}

# ── 9. sqrt(IE/Ry) radius, EN height ──
mappings['√(IE/Ry) radius, EN height'] = {
    'r': np.sqrt(ie_arr / RY_EV),
    'z': en_arr,
    'desc': 'Binding energy radius, reactivity height'
}

# ── 10. The tornado: r_cov radius, 1/r_cov height ──
# r_cov IS the radius, and 1/r_cov IS the height → perfect anti-correlation
rcov_arr = np.array([e['r_cov'] for e in elements], float)
mappings['r_cov radius, 1/r_cov height'] = {
    'r': rcov_arr / 100.0,
    'z': 100.0 / rcov_arr,
    'desc': 'Pure size: wide at bottom, narrow at top — TORNADO'
}

# ── 11. Period-stacked rings with golden advance ──
# Each period at a height, elements spiral around at golden angles
# Radius = ratio_pred (preserves band structure)
mappings['ratio radius, per height'] = {
    'r': rp_arr,
    'z': per_arr,
    'desc': 'Band-structure rings stacked by period'
}

# ── 12. The vortex sheet: r_cov × ratio_pred, IE height ──
mappings['r_cov×ratio radius, IE height'] = {
    'r': rcov_arr / 100.0 * rp_arr,
    'z': ie_arr,
    'desc': 'Size × mode radius, energy height'
}


# ═══════════════════════════════════════════════════════════════════
# MEASURE FUNNEL-NESS
# ═══════════════════════════════════════════════════════════════════

print(f"  {'Mapping':<35s}  {'ρ(r,z)':>7s}  {'r-range':>8s}  {'z-range':>8s}  {'shape':>10s}")
print(f"  {'─'*75}")

angles = np.array([(e['Z'] * GOLDEN_ANGLE_RAD) % (2*math.pi) for e in elements])

funnel_scores = []
for name, m in mappings.items():
    r = m['r']; z = m['z']
    rho = np.corrcoef(r, z)[0,1]
    r_range = np.max(r) - np.min(r)
    z_range = np.max(z) - np.min(z)

    if rho < -0.3: shape = 'FUNNEL ↓'
    elif rho > 0.3: shape = 'PLUME ↑'
    else: shape = 'cylinder'

    funnel_scores.append((name, rho, r_range, z_range, shape))
    print(f"  {name:<35s}  {rho:>+7.3f}  {r_range:>8.3f}  {z_range:>8.3f}  {shape:>10s}")

print()

# Sort by |ρ| — strongest correlation = most funnel-like
funnel_scores.sort(key=lambda x: abs(x[1]), reverse=True)
print("  Ranking by funnel strength (|ρ(radius, height)|):")
for i, (name, rho, rr, zr, shape) in enumerate(funnel_scores[:6]):
    print(f"    {i+1}. {name:<35s}  ρ = {rho:+.3f}  {shape}")


# ═══════════════════════════════════════════════════════════════════
# GENERATE PLOTS — Top 4 funnel candidates
# ═══════════════════════════════════════════════════════════════════

# Pick the top 4 by |ρ|
top4 = funnel_scores[:4]

fig = plt.figure(figsize=(22, 18))
fig.suptitle('Vortex Funnel Search: Which Mapping Creates a Tornado?', fontsize=16, fontweight='bold')

views = [(20, 45, 'Perspective'), (20, 135, 'Rear'), (85, 0, 'Top-down'), (5, 0, 'Side')]

for m_idx, (name, rho, rr, zr, shape) in enumerate(top4):
    m = mappings[name]
    r = m['r']; z = m['z']
    x = r * np.cos(angles)
    y = r * np.sin(angles)
    colors = [BLOCK_COLORS.get(e['block'], 'gray') for e in elements]

    for v_idx, (elev, azim, vname) in enumerate(views):
        ax_idx = m_idx * 4 + v_idx + 1
        ax = fig.add_subplot(4, 4, ax_idx, projection='3d')
        ax.scatter(x, y, z, c=colors, s=20, alpha=0.8, edgecolors='k', linewidths=0.3)

        if v_idx == 0:  # Only label in perspective view
            for i, e in enumerate(elements):
                if e['sym'] in ('H','He','F','Cs','Fe','Au','Ne','Ar','C','O'):
                    ax.text(x[i], y[i], z[i], f" {e['sym']}", fontsize=5, alpha=0.7)

        if v_idx == 0:
            ax.set_title(f'{name}\nρ={rho:+.2f} {shape}', fontsize=8)
        else:
            ax.set_title(vname, fontsize=8)
        ax.view_init(elev=elev, azim=azim)
        ax.tick_params(labelsize=5)

legend_elements = [Patch(facecolor=c, label=b) for b, c in BLOCK_COLORS.items()]
fig.legend(handles=legend_elements, loc='lower center', ncol=5, fontsize=10)
plt.tight_layout(rect=[0, 0.03, 1, 0.96])
plt.savefig(os.path.join(RESULTS_DIR, 'vortex_funnel_4x4.png'), dpi=150, bbox_inches='tight')
plt.close()
print(f"\n  Saved: {RESULTS_DIR}/vortex_funnel_4x4.png")


# ═══════════════════════════════════════════════════════════════════
# HERO PLOT — The best funnel in full detail
# ═══════════════════════════════════════════════════════════════════

best_name = funnel_scores[0][0]
best_rho = funnel_scores[0][1]
m = mappings[best_name]
r = m['r']; z = m['z']
x = r * np.cos(angles)
y = r * np.sin(angles)
colors = [BLOCK_COLORS.get(e['block'], 'gray') for e in elements]

# Also find the best ANTI-correlated (true funnel, narrow at top)
funnels = [f for f in funnel_scores if f[1] < -0.2]
plumes = [f for f in funnel_scores if f[1] > 0.2]

print(f"\n  Best funnel (narrow at top): {funnels[0][0] if funnels else 'none'}")
print(f"  Best plume (wide at top):    {plumes[0][0] if plumes else 'none'}")

# Plot both the best funnel and best plume side by side
fig = plt.figure(figsize=(22, 10))

for plot_idx, (candidates, title) in enumerate([(funnels, 'FUNNEL (narrow at top)'),
                                                  (plumes, 'PLUME (wide at top)')]):
    if not candidates:
        continue
    name = candidates[0][0]
    rho = candidates[0][1]
    m = mappings[name]
    r = m['r']; z = m['z']
    x = r * np.cos(angles)
    y = r * np.sin(angles)

    for v_idx, (elev, azim, vname) in enumerate([(20, 45, 'Perspective'),
                                                   (85, 0, 'Top-down'),
                                                   (5, 0, 'Side')]):
        ax = fig.add_subplot(2, 3, plot_idx*3 + v_idx + 1, projection='3d')
        ax.scatter(x, y, z, c=colors, s=30, alpha=0.85, edgecolors='k', linewidths=0.4)

        # Connect periods
        for per in range(1, 7):
            per_idx = [i for i in range(N) if elements[i]['per'] == per]
            if len(per_idx) >= 2:
                per_idx.sort(key=lambda i: elements[i]['Z'])
                ax.plot(x[per_idx], y[per_idx], z[per_idx],
                        color='gray', alpha=0.25, linewidth=0.7)

        # Labels
        for i, e in enumerate(elements):
            if e['sym'] in ('H','He','Li','C','N','O','F','Ne','Na','Cl','Ar',
                           'K','Fe','Cu','Br','Kr','Cs','Au','Xe'):
                ax.text(x[i], y[i], z[i], f" {e['sym']}", fontsize=6, alpha=0.8)

        if v_idx == 0:
            ax.set_title(f'{title}\n{name}\nρ(r,z)={rho:+.3f}', fontsize=10)
        else:
            ax.set_title(vname, fontsize=10)
        ax.view_init(elev=elev, azim=azim)

fig.legend(handles=legend_elements, loc='lower center', ncol=5, fontsize=10)
plt.tight_layout(rect=[0, 0.05, 1, 0.95])
plt.savefig(os.path.join(RESULTS_DIR, 'vortex_funnel_vs_plume.png'), dpi=150, bbox_inches='tight')
plt.close()
print(f"  Saved: {RESULTS_DIR}/vortex_funnel_vs_plume.png")


# ═══════════════════════════════════════════════════════════════════
# PERIOD-STACKED RINGS — one hero plot
# ═══════════════════════════════════════════════════════════════════

print(f"\n  Generating period-stacked ring plot...")

m = mappings['ratio radius, per+EN/5 height']
r = m['r']; z = m['z']
x = r * np.cos(angles)
y = r * np.sin(angles)

fig = plt.figure(figsize=(16, 14))
fig.suptitle('Period-Stacked Vortex Rings\n'
             'radius = ratio_pred (band structure)  |  height = period + EN/5',
             fontsize=14, fontweight='bold')

for idx, (elev, azim, vname) in enumerate([(20, 45, 'Perspective'),
                                            (85, 0, 'Top-down'),
                                            (5, 0, 'Side'),
                                            (20, 135, 'Rear')]):
    ax = fig.add_subplot(2, 2, idx+1, projection='3d')
    ax.scatter(x, y, z, c=colors, s=35, alpha=0.85, edgecolors='k', linewidths=0.4)

    # Connect elements within each period
    for per in range(1, 7):
        per_idx = [i for i in range(N) if elements[i]['per'] == per]
        if len(per_idx) >= 2:
            per_idx.sort(key=lambda i: elements[i]['Z'])
            ax.plot(x[per_idx], y[per_idx], z[per_idx],
                    color='gray', alpha=0.3, linewidth=0.8)
            # Period label
            mid = per_idx[len(per_idx)//2]
            ax.text(x[mid], y[mid], z[mid], f'  P{per}', fontsize=8,
                    color='dimgray', fontweight='bold')

    for i, e in enumerate(elements):
        if e['sym'] in ('H','He','Li','C','O','F','Ne','Na','K','Ca',
                       'Fe','Cu','Br','Kr','Cs','Au','Xe','Ar'):
            ax.text(x[i], y[i], z[i], f" {e['sym']}", fontsize=6, alpha=0.8)

    ax.set_title(vname, fontsize=11)
    ax.view_init(elev=elev, azim=azim)
    ax.set_zlabel('Period + EN/5')

fig.legend(handles=legend_elements, loc='lower center', ncol=5, fontsize=10)
plt.tight_layout(rect=[0, 0.04, 1, 0.96])
plt.savefig(os.path.join(RESULTS_DIR, 'vortex_period_rings.png'), dpi=150, bbox_inches='tight')
plt.close()
print(f"  Saved: {RESULTS_DIR}/vortex_period_rings.png")

print(f"\n  Done. All figures in {RESULTS_DIR}/")
