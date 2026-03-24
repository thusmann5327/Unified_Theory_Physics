#!/usr/bin/env python3
"""
vortex_triangle.py — The Right Triangle IS the Vortex
═══════════════════════════════════════════════════════
ratio = √(1 + (θ × BOS)²)

Every element sits on a right triangle:
  leg₁ = 1           (the shell wall — constant)
  leg₂ = θ × BOS     (the mode-dependent leg)
  hypotenuse = ratio  (what we measure)

The angle of this triangle determines which CONE the element
sits on. Combined with golden-angle azimuthal rotation and
period-scaled height, this IS the vortex.

Three cone angles:
  leak:     arctan(0.560) = 29.2°   (narrowest)
  rc:       arctan(0.847) = 40.3°
  baseline: arctan(0.992) = 44.8°   (widest)

The vortex is a TRIPLE CONE with golden-angle spiral winding.
Scale the z-axis by φ^(-(per-1)) and it converges — funnel.

Thomas A. Husmann / iBuilt LTD — March 2026
═══════════════════════════════════════════════════════
"""

import matplotlib
matplotlib.use('Agg')

import numpy as np
import math
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Patch, FancyArrowPatch

PHI = (1 + math.sqrt(5)) / 2
GOLDEN_ANGLE_RAD = 2 * math.pi / PHI**2
W = (2 + PHI**(1/PHI**2)) / PHI**4
BOS = 0.992022
LEAK = 1/PHI**4; R_C = 1 - LEAK
G1 = 0.3243; DARK_GOLD = 0.290; BASE = 1.408382; RY_EV = 13.6057
THETA_LEAK = 0.564; THETA_RC = 0.854; THETA_BASE = 1.000
MU_EFF = {26:2.22,27:1.72,28:0.62}
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
            blk='ng';
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
            return math.sqrt(1+(theta*BOS)**2),theta,per,n_p,n_d,n_s,block,"magnetic"
        is_boundary=(n_d<=4 or n_d>=9); has_s=(n_s>0)
        if is_boundary and has_s: return 1+LEAK,THETA_LEAK,per,n_p,n_d,n_s,block,"leak"
        elif n_d>=9 and not has_s: return BASE+DARK_GOLD*LEAK,THETA_BASE,per,n_p,n_d,n_s,block,"reflect"
        else:
            theta=1-(n_d/10)*DARK_GOLD
            return math.sqrt(1+(theta*BOS)**2),theta,per,n_p,n_d,n_s,block,"standard"
    elif block=='ng':
        theta=1+n_p*(G1/BOS)*PHI**(-(per-1))
        return math.sqrt(1+(theta*BOS)**2),theta,per,n_p,n_d,n_s,block,"pythagorean"
    else:
        ratio=BASE+n_p*G1*PHI**(-(per-1)); theta=ratio/BASE
        if block=='p' and n_p>=4 and per>=3:
            ratio*=R_C; return ratio,theta,per,n_p,n_d,n_s,block,"p-hole"
        return ratio,theta,per,n_p,n_d,n_s,block,"additive"

# Build elements
elements = []
for Z in sorted(RADII.keys()):
    sym = SYMBOLS.get(Z)
    if not sym: continue
    r_cov,r_vdw = RADII[Z]
    rp,theta,per,n_p,n_d,n_s,block,mode = predict_ratio(Z)
    elements.append(dict(Z=Z,sym=sym,r_cov=r_cov,r_vdw=r_vdw,
                         ratio_pred=rp,theta=theta,per=per,n_p=n_p,
                         n_d=n_d,n_s=n_s,block=block,mode=mode))

N = len(elements)
BLOCK_COLORS = {'s':'#e74c3c','p':'#3498db','d':'#2ecc71','ng':'#f39c12','f':'#9b59b6'}
MODE_COLORS = {
    'leak':'#e74c3c','standard':'#2ecc71','magnetic':'#9b59b6',
    'reflect':'#f39c12','pythagorean':'#f39c12','additive':'#3498db','p-hole':'#1a5276'
}
RESULTS_DIR = '/Users/universe/Unified_Theory_Physics/results/vortex_explorer'
os.makedirs(RESULTS_DIR, exist_ok=True)


# ═══════════════════════════════════════════════════════════════════
# THE RIGHT TRIANGLE COORDINATES
# ═══════════════════════════════════════════════════════════════════

print("=" * 80)
print("  THE RIGHT TRIANGLE IS THE VORTEX")
print("  ratio = √(1 + (θ × BOS)²)")
print("=" * 80)
print()

# For each element, compute the right-triangle components
for e in elements:
    tb = e['theta'] * BOS
    # Cone angle from z-axis
    e['cone_angle'] = math.atan(tb)        # radians
    e['cone_deg'] = math.degrees(e['cone_angle'])
    e['leg_horiz'] = tb                     # horizontal leg = θ×BOS
    e['leg_vert'] = 1.0                     # vertical leg = 1
    e['hypotenuse'] = e['ratio_pred']       # = √(1 + (θ×BOS)²)
    e['golden_azimuth'] = (e['Z'] * GOLDEN_ANGLE_RAD) % (2*math.pi)

# Print cone angles by mode
print("  Cone angles by mode:")
modes_seen = {}
for e in elements:
    m = e['mode']
    if m not in modes_seen:
        modes_seen[m] = []
    modes_seen[m].append(e['cone_deg'])

for mode in sorted(modes_seen.keys()):
    angles = modes_seen[mode]
    print(f"    {mode:>12s}: mean cone = {np.mean(angles):5.1f}°  "
          f"range [{min(angles):.1f}°, {max(angles):.1f}°]  n={len(angles)}")

print()
print(f"  Leak cone:     arctan({THETA_LEAK*BOS:.3f}) = {math.degrees(math.atan(THETA_LEAK*BOS)):.1f}°")
print(f"  RC cone:       arctan({THETA_RC*BOS:.3f}) = {math.degrees(math.atan(THETA_RC*BOS)):.1f}°")
print(f"  Baseline cone: arctan({THETA_BASE*BOS:.3f}) = {math.degrees(math.atan(THETA_BASE*BOS)):.1f}°")


# ═══════════════════════════════════════════════════════════════════
# MAPPING A: Flat cone (z = 1 for all, shows the triangle)
# Each element on a cone surface, golden angle rotation
# ═══════════════════════════════════════════════════════════════════

# x = θ×BOS × cos(golden_azimuth)
# y = θ×BOS × sin(golden_azimuth)
# z = 1 for all (the constant leg)
# This is flat — all at z=1. But it shows the cone structure in x-y.

# ═══════════════════════════════════════════════════════════════════
# MAPPING B: Period-scaled cone (z = φ^(-(per-1)))
# Height SHRINKS with period → converging vortex funnel
# ═══════════════════════════════════════════════════════════════════

# The "1" in the right triangle represents the shell wall.
# But each period is a Cantor recursion depth. The effective "1"
# shrinks as φ^(-(per-1)):
#   Period 1: z = 1.000
#   Period 2: z = 0.618
#   Period 3: z = 0.382
#   Period 4: z = 0.236
#   Period 5: z = 0.146
#   Period 6: z = 0.090
# This creates a CONVERGING VORTEX — later periods are compressed.

print(f"\n  Period heights (z = φ^(-(per-1))):")
for per in range(1, 7):
    h = PHI**(-(per-1))
    print(f"    Period {per}: z = {h:.4f}")


# ═══════════════════════════════════════════════════════════════════
# MAPPING C: Cumulative golden-angle height
# z advances by golden_angle / (2π) per element → smooth spiral
# ═══════════════════════════════════════════════════════════════════

# z = Z × (golden_angle / 2π) = Z × 1/φ²
# This gives a smooth upward spiral where each element advances
# by 1/φ² ≈ 0.382 turns. Height is proportional to Z but in
# golden-angle units.

# ═══════════════════════════════════════════════════════════════════
# GENERATE ALL THREE MAPPINGS
# ═══════════════════════════════════════════════════════════════════

# Compute coordinates for all three
azimuth = np.array([e['golden_azimuth'] for e in elements])
leg_h = np.array([e['leg_horiz'] for e in elements])  # θ×BOS
per_arr = np.array([e['per'] for e in elements], float)
Z_arr = np.array([e['Z'] for e in elements], float)
colors = [BLOCK_COLORS.get(e['block'], 'gray') for e in elements]
mode_col = [MODE_COLORS.get(e['mode'], 'gray') for e in elements]

# Mapping B: period-scaled converging cone
x_B = leg_h * PHI**(-(per_arr-1)) * np.cos(azimuth)
y_B = leg_h * PHI**(-(per_arr-1)) * np.sin(azimuth)
z_B = PHI**(-(per_arr-1))  # height = φ^(-(per-1))

# Mapping C: smooth spiral with triangle radius
x_C = leg_h * np.cos(azimuth)
y_C = leg_h * np.sin(azimuth)
z_C = Z_arr / PHI**2  # height in golden-angle units

# Mapping D: same as C but scale radii by 1/√per for funnel
x_D = leg_h / np.sqrt(per_arr) * np.cos(azimuth)
y_D = leg_h / np.sqrt(per_arr) * np.sin(azimuth)
z_D = Z_arr  # plain Z height

# Mapping E: observed ratio as radius (let data speak), Z height
ratio_obs = np.array([e['r_vdw']/e['r_cov'] for e in elements])
x_E = ratio_obs * np.cos(azimuth)
y_E = ratio_obs * np.sin(azimuth)
z_E = Z_arr


# ═══════════════════════════════════════════════════════════════════
# HERO FIGURE: The Right-Triangle Vortex (4 panels)
# ═══════════════════════════════════════════════════════════════════

fig = plt.figure(figsize=(22, 18))
fig.suptitle(
    'The Right Triangle IS the Vortex\n'
    r'ratio = $\sqrt{1 + (\theta \times BOS)^2}$   |   '
    r'radius = $\theta \times BOS$   |   golden angle azimuth',
    fontsize=15, fontweight='bold'
)

# Panel 1: Period-scaled converging cone (Mapping B)
configs = [
    (x_B, y_B, z_B, 'Converging Cone\nz = φ^(-(per-1)), r = θ×BOS × φ^(-(per-1))',
     20, 45, True),
    (x_B, y_B, z_B, 'Top-down (looking into the vortex)',
     85, 0, False),
    (x_C, y_C, z_C, 'Smooth Spiral\nr = θ×BOS, z = Z/φ²',
     20, 45, True),
    (x_C, y_C, z_C, 'Side view',
     5, 0, False),
]

for idx, (xx, yy, zz, title, elev, azim, label_els) in enumerate(configs):
    ax = fig.add_subplot(2, 2, idx+1, projection='3d')
    ax.scatter(xx, yy, zz, c=colors, s=35, alpha=0.85, edgecolors='k', linewidths=0.4)

    # Draw cone guide surfaces
    if idx < 2:
        # Draw cone circles at each period height
        theta_circle = np.linspace(0, 2*np.pi, 200)
        for per in range(1, 7):
            h = PHI**(-(per-1))
            for theta_band, col, ls in [(THETA_LEAK*BOS, '#e74c3c', '--'),
                                         (THETA_RC*BOS, '#f39c12', '-.'),
                                         (THETA_BASE*BOS, '#3498db', '-')]:
                r_cone = theta_band * h
                xc = r_cone * np.cos(theta_circle)
                yc = r_cone * np.sin(theta_circle)
                zc = np.full_like(theta_circle, h)
                ax.plot(xc, yc, zc, color=col, alpha=0.15, linewidth=0.5, linestyle=ls)

    # Connect elements within each period
    for per in range(1, 7):
        per_idx = [i for i in range(N) if elements[i]['per'] == per]
        if len(per_idx) >= 2:
            per_idx.sort(key=lambda i: elements[i]['Z'])
            ax.plot(xx[per_idx], yy[per_idx], zz[per_idx],
                    color='gray', alpha=0.25, linewidth=0.7)

    if label_els:
        for i, e in enumerate(elements):
            if e['sym'] in ('H','He','Li','C','N','O','F','Ne','Na','K','Ca',
                           'Sc','Fe','Cu','Br','Kr','Rb','Cs','Au','Xe','Bi'):
                ax.text(xx[i], yy[i], zz[i], f" {e['sym']}", fontsize=6, alpha=0.8)

    ax.set_title(title, fontsize=10)
    ax.view_init(elev=elev, azim=azim)

legend_elements = [
    Patch(facecolor='#e74c3c', label='s-block'),
    Patch(facecolor='#3498db', label='p-block'),
    Patch(facecolor='#2ecc71', label='d-block'),
    Patch(facecolor='#f39c12', label='noble gas'),
    Patch(facecolor='#9b59b6', label='f-block'),
]
fig.legend(handles=legend_elements, loc='lower center', ncol=5, fontsize=11)
plt.tight_layout(rect=[0, 0.04, 1, 0.94])
plt.savefig(os.path.join(RESULTS_DIR, 'vortex_right_triangle.png'), dpi=150, bbox_inches='tight')
plt.close()
print(f"\n  Saved: {RESULTS_DIR}/vortex_right_triangle.png")


# ═══════════════════════════════════════════════════════════════════
# HERO FIGURE 2: The converging cone in full detail
# ═══════════════════════════════════════════════════════════════════

fig = plt.figure(figsize=(20, 16))
fig.suptitle(
    'The Converging Vortex Cone\n'
    r'Each period shrinks by $1/\varphi$  →  triple cone converges to origin',
    fontsize=15, fontweight='bold'
)

for idx, (elev, azim, vname) in enumerate([
    (25, 30, 'Perspective (φ-compressed)'),
    (85, 0, 'Top-down (three nested cones)'),
    (0, 0, 'Side view (convergence visible)'),
    (25, 120, 'Rear perspective'),
]):
    ax = fig.add_subplot(2, 2, idx+1, projection='3d')
    ax.scatter(x_B, y_B, z_B, c=colors, s=40, alpha=0.9, edgecolors='k', linewidths=0.4, zorder=5)

    # Draw cone surfaces
    theta_circle = np.linspace(0, 2*np.pi, 300)
    for per in range(1, 7):
        h = PHI**(-(per-1))
        for theta_band, col, lw in [(THETA_LEAK*BOS, '#e74c3c', 0.8),
                                     (THETA_RC*BOS, '#f39c12', 0.8),
                                     (THETA_BASE*BOS, '#3498db', 0.8)]:
            r_cone = theta_band * h
            xc = r_cone * np.cos(theta_circle)
            yc = r_cone * np.sin(theta_circle)
            zc = np.full_like(theta_circle, h)
            ax.plot(xc, yc, zc, color=col, alpha=0.2, linewidth=lw)

    # Draw convergence lines from period 1 to 6
    for theta_band, col in [(THETA_LEAK*BOS, '#e74c3c'),
                             (THETA_RC*BOS, '#f39c12'),
                             (THETA_BASE*BOS, '#3498db')]:
        for angle_line in [0, math.pi/2, math.pi, 3*math.pi/2]:
            perz = [PHI**(-(p-1)) for p in range(1, 7)]
            perr = [theta_band * hz for hz in perz]
            xl = [r * math.cos(angle_line) for r in perr]
            yl = [r * math.sin(angle_line) for r in perr]
            ax.plot(xl, yl, perz, color=col, alpha=0.15, linewidth=0.5)

    # Connect within periods
    for per in range(1, 7):
        per_idx = [i for i in range(N) if elements[i]['per'] == per]
        if len(per_idx) >= 2:
            per_idx.sort(key=lambda i: elements[i]['Z'])
            ax.plot(x_B[per_idx], y_B[per_idx], z_B[per_idx],
                    color='gray', alpha=0.3, linewidth=0.8)

    # Labels
    for i, e in enumerate(elements):
        if e['sym'] in ('H','He','Li','C','O','F','Ne','Na','K','Fe','Cu','Au','Cs','Xe','Ar'):
            ax.text(x_B[i], y_B[i], z_B[i], f" {e['sym']}", fontsize=7, alpha=0.85)

    ax.set_title(vname, fontsize=11)
    ax.view_init(elev=elev, azim=azim)
    ax.set_zlabel('z = φ^(-(per-1))')

fig.legend(handles=legend_elements, loc='lower center', ncol=5, fontsize=11)
plt.tight_layout(rect=[0, 0.04, 1, 0.94])
plt.savefig(os.path.join(RESULTS_DIR, 'vortex_converging_cone.png'), dpi=200, bbox_inches='tight')
plt.close()
print(f"  Saved: {RESULTS_DIR}/vortex_converging_cone.png")


# ═══════════════════════════════════════════════════════════════════
# HERO FIGURE 3: Show the actual right triangles for a few elements
# ═══════════════════════════════════════════════════════════════════

fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111, projection='3d')
ax.set_title(
    'Right Triangles of Selected Elements\n'
    r'Each triangle: leg₁=1 (vertical), leg₂=θ×BOS (horizontal), hypotenuse=ratio',
    fontsize=12, fontweight='bold'
)

# Show triangles for selected elements
show_elements = ['H','Li','C','Fe','Cu','Au','Cs','F','Ne','Sc']
for e in elements:
    if e['sym'] not in show_elements:
        continue

    az = e['golden_azimuth']
    tb = e['leg_horiz']  # θ×BOS
    col = BLOCK_COLORS.get(e['block'], 'gray')

    # Triangle vertices in 3D:
    # Origin = (0, 0, 0)
    # Horizontal leg endpoint = (tb×cos(az), tb×sin(az), 0)
    # Vertical leg endpoint = (tb×cos(az), tb×sin(az), 1)
    # The hypotenuse goes from origin to the vertical endpoint

    ox, oy = 0, 0
    hx, hy = tb * math.cos(az), tb * math.sin(az)

    # Draw the three sides of the right triangle
    # Horizontal leg (along the x-y plane)
    ax.plot([ox, hx], [oy, hy], [0, 0], color=col, linewidth=1.5, alpha=0.6)
    # Vertical leg (up from horizontal endpoint)
    ax.plot([hx, hx], [hy, hy], [0, 1], color=col, linewidth=1.5, alpha=0.6)
    # Hypotenuse (from origin to top)
    ax.plot([ox, hx], [oy, hy], [0, 1], color=col, linewidth=2.5, alpha=0.8)

    # Element point at the top (where leg₁ meets hypotenuse)
    ax.scatter([hx], [hy], [1], c=[col], s=60, edgecolors='k', linewidths=0.5, zorder=10)
    ax.text(hx, hy, 1.05, f'{e["sym"]}\nθ={e["theta"]:.2f}',
            fontsize=8, ha='center', color=col, fontweight='bold')

    # Right angle marker at base (tiny square)
    # (skip for clarity)

# Draw the three cone circles at z=1
theta_circle = np.linspace(0, 2*np.pi, 200)
for theta_band, col, label in [(THETA_LEAK*BOS, '#e74c3c', 'Leak cone'),
                                 (THETA_RC*BOS, '#f39c12', 'RC cone'),
                                 (THETA_BASE*BOS, '#3498db', 'Base cone')]:
    xc = theta_band * np.cos(theta_circle)
    yc = theta_band * np.sin(theta_circle)
    zc = np.ones_like(theta_circle)
    ax.plot(xc, yc, zc, color=col, alpha=0.3, linewidth=1, label=label)

ax.set_xlabel('θ×BOS × cos(golden angle)')
ax.set_ylabel('θ×BOS × sin(golden angle)')
ax.set_zlabel('1 (constant leg)')
ax.set_zlim(0, 1.2)
ax.view_init(elev=20, azim=35)
ax.legend(loc='upper right', fontsize=9)

plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, 'vortex_triangles_shown.png'), dpi=200, bbox_inches='tight')
plt.close()
print(f"  Saved: {RESULTS_DIR}/vortex_triangles_shown.png")


# ═══════════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════════

print(f"\n{'='*80}")
print("  SUMMARY")
print(f"{'='*80}")
print()
print("  ratio = √(1 + (θ×BOS)²)  →  every element is a right triangle")
print()
print("  The vortex structure:")
print("    • Three CONE ANGLES from the z-axis (leak 29°, rc 40°, base 45°)")
print("    • Golden-angle rotation (137.5°) advances each element azimuthally")
print("    • Period scaling φ^(-(per-1)) makes the cones CONVERGE → funnel")
print()
print("  The right triangle decomposition:")
print("    • Vertical leg = 1 (shell wall constant — the 'existence condition')")
print("    • Horizontal leg = θ×BOS (mode-dependent — encodes electron config)")
print("    • Hypotenuse = ratio = vdW/cov (the observable)")
print()
print("  The Pythagorean relation σ₄² = σ_shell² + bronze_σ₃² (0.012% error)")
print("  is the SAME triangle at the Cantor node level:")
print(f"    0.5594² = 0.3972² + 0.394²")
print(f"    {0.5594**2:.4f} = {0.3972**2:.4f} + {0.394**2:.4f} = {0.3972**2+0.394**2:.4f}")
print(f"    Error: {abs(0.5594**2 - 0.3972**2 - 0.394**2)/0.5594**2*100:.3f}%")
print()
print(f"  Figures saved to: {RESULTS_DIR}/")
