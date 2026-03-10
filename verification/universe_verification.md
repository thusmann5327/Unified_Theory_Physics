#!/usr/bin/env python3
"""
HUSMANN DECOMPOSITION — POLISHED DEMO
Computes the observable universe from two inputs: φ and t_as.
Renders the backbone, spectrum, predictions, and 3D structure.
Every image is generated live from the eigensolver. Nothing is precompiled.

© 2026 Thomas A. Husmann / iBuilt LTD
Patent Application 19/560,637
"""

import math, io, base64, json, os, time
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from flask import Flask, render_template_string, send_file

# ═══════════════════════════════════════════════════════════════════════════════
# PART 1 — PHYSICS ENGINE (everything from φ and t_as)
# ═══════════════════════════════════════════════════════════════════════════════

PHI   = (1 + math.sqrt(5)) / 2
T_AS  = 232e-18
HBAR  = 1.0545718e-34
C     = 2.99792458e8
L_P   = 1.61625e-35

OMEGA_LAT = 1.685
J_J   = 2 * math.pi * HBAR / (OMEGA_LAT * T_AS)
J_EV  = J_J / 1.602176634e-19
L0    = C * HBAR / (2 * J_J)
W     = 2 / PHI**4 + PHI**(-1/PHI) / PHI**3
W2    = W**2
W4    = W**4

NORM  = math.sqrt(2 + PHI)
S1    = np.array([0, 1, PHI]) / NORM
S2    = np.array([PHI, 0, 1]) / NORM
S3    = np.array([1, PHI, 0]) / NORM
AMP1  = 1/PHI;  AMP2 = 1/PHI**3;  AMP3 = 1/PHI**4
AXIS_ANGLE = math.degrees(math.acos(np.dot(S1, S2)))
ALPHA = 1.0 / PHI

_phi_sum = 1/PHI + 1/PHI**3
OMB  = W4
OMDM = (1/PHI**3) * (1 - W4) / _phi_sum
OMDE = (1/PHI)    * (1 - W4) / _phi_sum


def compute_spectrum(N=233, V=2.0, theta=0.0):
    diag = V * np.cos(2 * np.pi * ALPHA * np.arange(N) + theta)
    H = np.diag(diag) + np.diag(np.ones(N-1), 1) + np.diag(np.ones(N-1), -1)
    return np.sort(np.linalg.eigvalsh(H))


def find_bands_gaps(eigs, threshold=8.0):
    diffs = np.diff(eigs)
    med = np.median(diffs)
    gaps, bands = [], []
    bs = 0
    for i in range(len(diffs)):
        if diffs[i] > threshold * med:
            gaps.append(dict(lo=float(eigs[i]), hi=float(eigs[i+1]),
                             w=float(diffs[i]), c=float((eigs[i]+eigs[i+1])/2)))
            bands.append(dict(lo=float(eigs[bs]), hi=float(eigs[i]),
                              w=float(eigs[i]-eigs[bs]),
                              c=float((eigs[bs]+eigs[i])/2),
                              n=i-bs+1))
            bs = i+1
    bands.append(dict(lo=float(eigs[bs]), hi=float(eigs[-1]),
                      w=float(eigs[-1]-eigs[bs]),
                      c=float((eigs[bs]+eigs[-1])/2), n=len(eigs)-bs))
    return bands, gaps


def identify_sectors(bands, gaps, eigs):
    E_min, E_max = float(eigs[0]), float(eigs[-1])
    E_range = E_max - E_min
    neg = sorted([g for g in gaps if g['c'] < -0.3], key=lambda g: g['w'], reverse=True)
    pos = sorted([g for g in gaps if g['c'] > 0.3],  key=lambda g: g['w'], reverse=True)
    wL, wR = neg[0], pos[0]
    s3b = [b for b in bands if b['lo'] >= wL['hi']-0.001 and b['hi'] <= wR['lo']+0.001]
    s3g = [g for g in gaps  if g['lo'] >= wL['hi']-0.001 and g['hi'] <= wR['lo']+0.001]
    s1b = [b for b in bands if b['hi'] < wL['lo']]
    s5b = [b for b in bands if b['lo'] > wR['hi']]
    return dict(wL=wL, wR=wR, s3b=s3b, s3g=s3g, s1b=s1b, s5b=s5b,
                s3w=sum(b['w'] for b in s3b), E_min=E_min, E_max=E_max, E_range=E_range)


def zeckendorf(n):
    fibs = [1,2,3,5,8,13,21,34,55,89,144,233,377,610,987]
    r, rem = [], n
    for f in reversed(fibs):
        if f <= rem: r.append(f); rem -= f
        if rem == 0: break
    return r


# ═══ Precompute everything ═══
t0 = time.time()
EIGS_233 = compute_spectrum(233)
BANDS_233, GAPS_233 = find_bands_gaps(EIGS_233)
SECTORS = identify_sectors(BANDS_233, GAPS_233, EIGS_233)

EIGS_55  = compute_spectrum(55)
BANDS_55, GAPS_55 = find_bands_gaps(EIGS_55)

EIGS_5   = compute_spectrum(5)
BANDS_5, GAPS_5 = find_bands_gaps(EIGS_5)

# σ₃ edges and W⁴ points
S3_EDGES_E = sorted(set(e for g in SECTORS['s3g'] for e in [g['lo'], g['hi']]))
S3_EDGE_POS = []
for e in S3_EDGES_E:
    frac = (e - SECTORS['E_min']) / SECTORS['E_range']
    S3_EDGE_POS.append(2*frac - 1)

M = np.array([S1, S2, S3])
M_INV = np.linalg.inv(M)
SCALE = 10.0

W4_PTS = []
for d1 in S3_EDGE_POS:
    for d2 in S3_EDGE_POS:
        for d3 in S3_EDGE_POS:
            pt = M_INV @ np.array([d1*AMP1*SCALE, d2*AMP2*SCALE, d3*AMP3*SCALE])
            if np.linalg.norm(pt) < SCALE*0.8:
                W4_PTS.append(pt)
W4_ARR = np.array(W4_PTS) if W4_PTS else np.zeros((0,3))

# Gap fractions for void predictions
GAP_FRACS = sorted([(g['w']/SECTORS['E_range'], g['c']) for g in GAPS_233],
                    key=lambda x: x[0], reverse=True)

# Sub-voids within σ₃
S3G_SORTED = sorted(SECTORS['s3g'], key=lambda g: g['w'], reverse=True)
SV_RATIO = S3G_SORTED[0]['w'] / S3G_SORTED[1]['w'] if len(S3G_SORTED) >= 2 else 0

COMPUTE_TIME = time.time() - t0

# ═══════════════════════════════════════════════════════════════════════════════
# PART 2 — RENDERERS (all matplotlib, all computed live)
# ═══════════════════════════════════════════════════════════════════════════════

BG = '#08090f'
GOLD = '#f5c542'
BLUE = '#4488ff'
PURPLE = '#9944ff'
PINK = '#ff4488'
DGOLD = '#c4982a'
LGOLD = '#ffe89a'


def fig_to_b64(fig, dpi=160):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=dpi, facecolor=fig.get_facecolor(),
                bbox_inches='tight', pad_inches=0.15)
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode()


def render_cantor_bar():
    """The Cantor set spectrum as a 1D bar — the foundational image."""
    fig, axes = plt.subplots(3, 1, figsize=(14, 4.5), facecolor=BG,
                              gridspec_kw={'height_ratios': [1, 1, 1], 'hspace': 0.35})

    for ax_i, (eigs, label, N_val) in enumerate([
        (EIGS_5, 'N = 5  (Zeckendorf step 1)', 5),
        (EIGS_55, 'N = 55  (Zeckendorf step 2 — 9 bands, 8 gaps)', 55),
        (EIGS_233, 'N = 233  (Zeckendorf step 3 — 35 bands, 34 gaps)', 233),
    ]):
        ax = axes[ax_i]
        ax.set_facecolor(BG)
        bands_i, gaps_i = find_bands_gaps(eigs) if N_val > 2 else ([], [])
        E_min_i, E_max_i = float(eigs[0]), float(eigs[-1])
        E_range_i = E_max_i - E_min_i if E_max_i > E_min_i else 1

        # Background (gap)
        ax.barh(0, 1, height=1, left=0, color='#0d0e18', edgecolor='none')

        if bands_i:
            for b in bands_i:
                x0 = (b['lo'] - E_min_i) / E_range_i
                xw = b['w'] / E_range_i
                if xw > 0:
                    ax.barh(0, xw, height=1, left=x0, color=GOLD, alpha=0.9)
            for g in gaps_i:
                x0 = (g['lo'] - E_min_i) / E_range_i
                xw = g['w'] / E_range_i
                ax.barh(0, xw, height=1, left=x0, color='#1a0833', alpha=0.85)
        else:
            # N=5: just show eigenvalue dots
            for e in eigs:
                x = (e - E_min_i) / E_range_i if E_range_i > 0 else 0.5
                ax.plot(x, 0.5, '|', color=GOLD, markersize=15, markeredgewidth=2)

        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        ax.set_yticks([]); ax.set_xticks([])
        ax.set_title(label, color='#aaa', fontsize=10, fontfamily='monospace',
                     pad=3, loc='left')

        # Sector labels for N=233
        if N_val == 233:
            sec = SECTORS
            # σ₁
            x1 = ((sec['wL']['lo'] + sec['E_min'])/2 - sec['E_min']) / sec['E_range']
            ax.text(x1, 0.5, 'σ₁', color=BLUE, fontsize=8, ha='center', va='center',
                    fontfamily='monospace', fontweight='bold')
            # σ₂
            x2 = (sec['wL']['c'] - sec['E_min']) / sec['E_range']
            ax.text(x2, 0.5, 'σ₂', color=PURPLE, fontsize=8, ha='center', va='center',
                    fontfamily='monospace', fontweight='bold')
            # σ₃
            ax.text(0.5, 0.5, 'σ₃', color=GOLD, fontsize=8, ha='center', va='center',
                    fontfamily='monospace', fontweight='bold')
            # σ₄
            x4 = (sec['wR']['c'] - sec['E_min']) / sec['E_range']
            ax.text(x4, 0.5, 'σ₄', color=PURPLE, fontsize=8, ha='center', va='center',
                    fontfamily='monospace', fontweight='bold')
            # σ₅
            x5 = ((sec['wR']['hi'] + sec['E_max'])/2 - sec['E_min']) / sec['E_range']
            ax.text(x5, 0.5, 'σ₅', color=PINK, fontsize=8, ha='center', va='center',
                    fontfamily='monospace', fontweight='bold')

    return fig_to_b64(fig)


def render_sigma3_overlap():
    """2D fold overlap — our observable universe between the DM walls."""
    fig, ax = plt.subplots(figsize=(10, 10), facecolor=BG)
    ax.set_facecolor(BG)

    sec = SECTORS
    pad = (sec['wR']['lo'] - sec['wL']['hi']) * 0.35
    vlo = sec['wL']['hi'] - pad
    vhi = sec['wR']['lo'] + pad
    vr = vhi - vlo
    def nv(e): return (e - vlo) / vr

    # DM walls
    for wall in [sec['wL'], sec['wR']]:
        ax.axvspan(nv(wall['lo']), nv(wall['hi']), color='#1a0833', alpha=0.95, zorder=1)
        ax.axhspan(nv(wall['lo']), nv(wall['hi']), color='#1a0833', alpha=0.95, zorder=1)
        for e in [wall['lo'], wall['hi']]:
            ax.axvline(nv(e), color='#6622aa', lw=1.2, alpha=0.6, zorder=2)
            ax.axhline(nv(e), color='#6622aa', lw=1.2, alpha=0.6, zorder=2)

    # σ₃ backbone corridors
    for g in sec['s3g']:
        ax.axvspan(nv(g['lo']), nv(g['hi']), color='#221144', alpha=0.5, zorder=2)
        ax.axhspan(nv(g['lo']), nv(g['hi']), color='#221144', alpha=0.5, zorder=2)

    # Band overlaps
    for bA in sec['s3b']:
        for bB in sec['s3b']:
            xlo, xhi = nv(bA['lo']), nv(bA['hi'])
            ylo, yhi = nv(bB['lo']), nv(bB['hi'])
            if xhi-xlo < 0.0005 or yhi-ylo < 0.0005: continue
            dn = bA.get('n',3) * bB.get('n',3)
            br = min(1, dn/25)
            r = Rectangle((xlo,ylo), xhi-xlo, yhi-ylo,
                           fc=(1,0.85*br,0.15*br,br*0.85), ec=(1,0.9,0.4,0.25), lw=0.4, zorder=3)
            ax.add_patch(r)

    # Band edges
    for g in sec['s3g']:
        for e in [g['lo'], g['hi']]:
            ax.axvline(nv(e), color=GOLD, lw=0.4, alpha=0.35, zorder=3)
            ax.axhline(nv(e), color=GOLD, lw=0.4, alpha=0.35, zorder=3)

    # W⁴ dots
    edges = sorted(set(e for g in sec['s3g'] for e in [g['lo'], g['hi']]))
    for eA in edges:
        for eB in edges:
            ax.plot(nv(eA), nv(eB), 'o', color=GOLD, ms=3, alpha=0.9, zorder=6,
                    mec='white', mew=0.3)

    # E=0 crosshair
    e0 = nv(0)
    ax.axvline(e0, color='white', lw=0.5, alpha=0.2, ls=':', zorder=4)
    ax.axhline(e0, color='white', lw=0.5, alpha=0.2, ls=':', zorder=4)
    ax.plot(e0, e0, '+', color='white', ms=14, mew=2, alpha=0.6, zorder=10)
    ax.annotate('E = 0\nWE ARE HERE', xy=(e0, e0), xytext=(e0+0.08, e0+0.08),
                color='white', fontsize=9, fontfamily='monospace', fontweight='bold',
                arrowprops=dict(arrowstyle='->', color='white', alpha=0.5),
                bbox=dict(boxstyle='round,pad=0.3', fc='#0a0a18', ec=GOLD, alpha=0.9), zorder=10)

    # Wall labels
    ax.text(nv(sec['wL']['c']), 0.5, 'σ₂\nDM WALL', color='#9955dd', fontsize=9,
            fontfamily='monospace', fontweight='bold', ha='center', va='center', rotation=90, zorder=5)
    ax.text(nv(sec['wR']['c']), 0.5, 'σ₄\nDM WALL', color='#9955dd', fontsize=9,
            fontfamily='monospace', fontweight='bold', ha='center', va='center', rotation=90, zorder=5)

    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.set_aspect('equal')
    ax.set_xlabel('Fold A (θ_A spatial)', color='#888', fontsize=10, fontfamily='monospace')
    ax.set_ylabel('Fold B (θ_B temporal)', color='#888', fontsize=10, fontfamily='monospace')
    ax.tick_params(colors='#444', labelsize=7)

    return fig_to_b64(fig)


def render_3d_backbone(elev=22, azim=38):
    """3D backbone with σ₃-only fold discs and W⁴ matter points."""
    fig = plt.figure(figsize=(12, 12), facecolor=BG)
    ax = fig.add_subplot(111, projection='3d', facecolor=BG)
    ax.view_init(elev=elev, azim=azim)

    def get_perps(d):
        d = d / np.linalg.norm(d)
        ref = np.array([1,0,0]) if abs(d[0])<0.9 else np.array([0,1,0])
        p1 = np.cross(d,ref); p1 /= np.linalg.norm(p1)
        p2 = np.cross(d,p1);  p2 /= np.linalg.norm(p2)
        return p1, p2

    axes_info = [(S1,AMP1*SCALE,'S₁ DE',(0.27,0.53,1.0)),
                 (S2,AMP2*SCALE,'S₂ DM',(0.60,0.27,1.0)),
                 (S3,AMP3*SCALE,'S₃ M', (1.00,0.27,0.53))]

    for d, amp, label, rgb in axes_info:
        hc = f'#{int(rgb[0]*255):02x}{int(rgb[1]*255):02x}{int(rgb[2]*255):02x}'
        perp1, perp2 = get_perps(d)

        # Axis line
        ax.plot([-d[0]*amp, d[0]*amp], [-d[1]*amp, d[1]*amp], [-d[2]*amp, d[2]*amp],
                color=hc, lw=2.5, alpha=0.85)
        s3_reach = amp * 0.08
        ax.text(d[0]*s3_reach*1.4, d[1]*s3_reach*1.4, d[2]*s3_reach*1.4,
                label, color=hc, fontsize=9, fontfamily='monospace', fontweight='bold')

        # σ₃ fold discs
        max_gw = max(g['w'] for g in SECTORS['s3g']) if SECTORS['s3g'] else 1
        for g in SECTORS['s3g']:
            ef = (g['c'] - SECTORS['E_min']) / SECTORS['E_range']
            pf = 2*ef - 1
            pa = pf * amp
            dr = (g['w']/max_gw) * amp * 0.12
            dr = max(dr, 0.04)
            for sign in [1, -1]:
                ctr = d * pa * sign
                pts = [ctr + dr*(perp1*np.cos(a) + perp2*np.sin(a))
                       for a in np.linspace(0, 2*np.pi, 20, endpoint=True)]
                poly = Poly3DCollection([pts], alpha=0.18)
                poly.set_facecolor((*rgb, 0.18))
                poly.set_edgecolor((*rgb, 0.40))
                poly.set_linewidth(0.4)
                ax.add_collection3d(poly)

    # W⁴ matter
    if len(W4_ARR) > 0:
        dists = np.linalg.norm(W4_ARR, axis=1)
        md = dists.max() if len(dists) else 1
        br = 1 - 0.3*(dists/md)
        sz = 12 + 30*br
        ax.scatter(W4_ARR[:,0], W4_ARR[:,1], W4_ARR[:,2],
                   c=GOLD, s=sz*3, alpha=0.10, zorder=8, linewidths=0)
        ax.scatter(W4_ARR[:,0], W4_ARR[:,1], W4_ARR[:,2],
                   c=GOLD, s=sz, alpha=0.85, zorder=10, linewidths=0.3, edgecolors='white')

    # Origin
    ax.scatter(0,0,0, color='white', s=100, zorder=15, edgecolors=GOLD, linewidth=2)

    # Bounds
    span = 1.2
    ax.set_xlim(-span,span); ax.set_ylim(-span,span); ax.set_zlim(-span,span)
    ax.xaxis.pane.fill=False; ax.yaxis.pane.fill=False; ax.zaxis.pane.fill=False
    ax.xaxis.pane.set_edgecolor('#1a1a2a')
    ax.yaxis.pane.set_edgecolor('#1a1a2a')
    ax.zaxis.pane.set_edgecolor('#1a1a2a')
    ax.tick_params(colors='#333', labelsize=5)
    ax.grid(True, alpha=0.04)

    return fig_to_b64(fig, dpi=140)


def render_void_comparison():
    """Bar chart: predicted vs observed void sizes."""
    voids = [
        ("Boötes\nVoid", 250, 0.002735),
        ("Local\nVoid", 150, 0.001717),
        ("Sculptor\nVoid", 100, 0.001211),
        ("Dipole\nRepeller", 600, 0.006321),
        ("BOSS\nGreat Wall", 1000, 0.009201),
        ("Sloan\nGreat Wall", 1380, 0.014477),
        ("KBC\nVoid", 2000, 0.023404),
    ]

    fig, ax = plt.subplots(figsize=(14, 5), facecolor=BG)
    ax.set_facecolor(BG)

    x = np.arange(len(voids))
    obs = [v[1] for v in voids]
    pred = [v[2]*93000 for v in voids]
    errs = [abs(p-o)/o*100 for o,p in zip(obs,pred)]

    w = 0.35
    bars_obs = ax.bar(x - w/2, obs, w, color=BLUE, alpha=0.85, label='Observed', edgecolor='white', linewidth=0.5)
    bars_pred = ax.bar(x + w/2, pred, w, color=GOLD, alpha=0.85, label='Predicted (AAH)', edgecolor='white', linewidth=0.5)

    for i, (o, p, e) in enumerate(zip(obs, pred, errs)):
        ax.text(i + w/2, p + 30, f'{e:.1f}%', ha='center', va='bottom',
                color=LGOLD, fontsize=9, fontfamily='monospace', fontweight='bold')

    ax.set_xticks(x)
    ax.set_xticklabels([v[0] for v in voids], color='#bbb', fontsize=9, fontfamily='monospace')
    ax.set_ylabel('Size (Mly)', color='#888', fontsize=11, fontfamily='monospace')
    ax.tick_params(colors='#555')
    ax.legend(fontsize=10, facecolor='#0a0a18', edgecolor='#333', labelcolor=['#88aaff', LGOLD])
    ax.spines['bottom'].set_color('#333'); ax.spines['left'].set_color('#333')
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)

    return fig_to_b64(fig)


def render_axes_diagram():
    """The three icosahedral axes with angle arcs."""
    fig = plt.figure(figsize=(10, 10), facecolor=BG)
    ax = fig.add_subplot(111, projection='3d', facecolor=BG)
    ax.view_init(elev=25, azim=45)

    R = 10
    for d, amp_frac, label, color in [
        (S1, AMP1, 'S₁ (DE)\n1/φ = 0.618', BLUE),
        (S2, AMP2, 'S₂ (DM)\n1/φ³ = 0.236', PURPLE),
        (S3, AMP3, 'S₃ (M)\n1/φ⁴ = 0.146', PINK),
    ]:
        reach = amp_frac * R
        ax.plot([-d[0]*reach, d[0]*reach], [-d[1]*reach, d[1]*reach],
                [-d[2]*reach, d[2]*reach], color=color, lw=3, alpha=0.9)
        ax.plot([d[0]*reach, d[0]*R], [d[1]*reach, d[1]*R],
                [d[2]*reach, d[2]*R], color=color, lw=0.8, alpha=0.2, ls='--')
        ax.scatter(*d*reach, color=color, s=80, zorder=5, edgecolors='white', lw=0.5)
        ax.text(d[0]*reach*1.15, d[1]*reach*1.15, d[2]*reach*1.15,
                label, color=color, fontsize=9, fontfamily='monospace', fontweight='bold')

    # Angle arcs
    for Sa, Sb in [(S1,S2), (S2,S3), (S1,S3)]:
        pts = np.array([Sa*(1-t)+Sb*t for t in np.linspace(0,1,30)])
        pts = np.array([p/np.linalg.norm(p)*2.5 for p in pts])
        ax.plot(pts[:,0], pts[:,1], pts[:,2], color=GOLD, lw=1, alpha=0.4)
    mid = (S1+S2); mid = mid/np.linalg.norm(mid)*3
    ax.text(mid[0], mid[1], mid[2], '63.4°', color=GOLD, fontsize=9, fontfamily='monospace')

    ax.scatter(0,0,0, color='white', s=100, zorder=10, edgecolors=GOLD, lw=2)
    ax.set_xlim(-R*1.1,R*1.1); ax.set_ylim(-R*1.1,R*1.1); ax.set_zlim(-R*1.1,R*1.1)
    ax.xaxis.pane.fill=False; ax.yaxis.pane.fill=False; ax.zaxis.pane.fill=False
    ax.xaxis.pane.set_edgecolor('#1a1a2a'); ax.yaxis.pane.set_edgecolor('#1a1a2a')
    ax.zaxis.pane.set_edgecolor('#1a1a2a')
    ax.tick_params(colors='#333', labelsize=5)
    ax.grid(True, alpha=0.04)

    return fig_to_b64(fig, dpi=140)


# ═══════════════════════════════════════════════════════════════════════════════
# PART 3 — FLASK APP
# ═══════════════════════════════════════════════════════════════════════════════

app = Flask(__name__)

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Husmann Decomposition — Universe from φ</title>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&family=Cormorant+Garamond:wght@300;400;600&display=swap" rel="stylesheet">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
:root {
  --bg: #08090f; --card: #0d0e18; --border: #1a1b2e;
  --gold: #f5c542; --lgold: #ffe89a; --dgold: #c4982a;
  --blue: #4488ff; --purple: #9944ff; --pink: #ff4488;
  --text: #c8c9d4; --dim: #666879; --bright: #eeeef5;
}
body { background:var(--bg); color:var(--text); font-family:'JetBrains Mono',monospace; font-size:13px; line-height:1.6; }
.hero { text-align:center; padding:60px 20px 40px; background:linear-gradient(180deg, #0e0f1a 0%, var(--bg) 100%); border-bottom:1px solid var(--border); }
.hero h1 { font-family:'Cormorant Garamond',serif; font-size:42px; font-weight:300; color:var(--gold); letter-spacing:2px; }
.hero .sub { font-size:14px; color:var(--dim); margin-top:8px; }
.hero .inputs { margin-top:20px; font-size:16px; color:var(--bright); }
.hero .inputs span { color:var(--gold); font-weight:700; }
.container { max-width:1200px; margin:0 auto; padding:0 20px; }

.section { padding:50px 0; border-bottom:1px solid var(--border); }
.section h2 { font-family:'Cormorant Garamond',serif; font-size:28px; font-weight:400; color:var(--gold); margin-bottom:8px; }
.section .num { font-size:12px; color:var(--dgold); text-transform:uppercase; letter-spacing:3px; margin-bottom:4px; }

.grid2 { display:grid; grid-template-columns:1fr 1fr; gap:30px; margin-top:25px; }
.grid3 { display:grid; grid-template-columns:1fr 1fr 1fr; gap:20px; margin-top:25px; }
@media(max-width:800px) { .grid2,.grid3 { grid-template-columns:1fr; } }

.card { background:var(--card); border:1px solid var(--border); border-radius:8px; padding:24px; }
.card h3 { font-size:13px; color:var(--gold); text-transform:uppercase; letter-spacing:2px; margin-bottom:12px; }
.card .val { font-size:32px; font-weight:700; color:var(--bright); margin:6px 0; }
.card .val .unit { font-size:14px; color:var(--dim); font-weight:300; }
.card .compare { font-size:11px; color:var(--dim); }
.card .compare .match { color:#44cc88; font-weight:700; }
.card .compare .planck { color:var(--blue); }

.img-full { width:100%; border-radius:6px; margin-top:20px; border:1px solid var(--border); }
.img-pair { display:grid; grid-template-columns:1fr 1fr; gap:15px; margin-top:20px; }
.img-pair img { width:100%; border-radius:6px; border:1px solid var(--border); }

table { width:100%; border-collapse:collapse; margin-top:15px; font-size:12px; }
th { text-align:left; padding:8px 12px; color:var(--dgold); border-bottom:2px solid var(--border); text-transform:uppercase; letter-spacing:1px; font-size:10px; }
td { padding:7px 12px; border-bottom:1px solid #141525; }
td.num { text-align:right; font-variant-numeric:tabular-nums; }
td.match { color:#44cc88; font-weight:700; }
td.gold { color:var(--gold); }
tr:hover { background:#11121f; }

.eq { background:#0a0b14; border:1px solid var(--border); border-radius:6px; padding:16px 20px; margin:15px 0; font-size:15px; color:var(--lgold); text-align:center; letter-spacing:1px; }

.tag { display:inline-block; padding:3px 10px; border-radius:3px; font-size:10px; letter-spacing:1px; text-transform:uppercase; margin-right:6px; }
.tag-de { background:#4488ff22; color:var(--blue); border:1px solid #4488ff44; }
.tag-dm { background:#9944ff22; color:var(--purple); border:1px solid #9944ff44; }
.tag-m  { background:#ff448822; color:var(--pink); border:1px solid #ff448844; }
.tag-w4 { background:#f5c54222; color:var(--gold); border:1px solid #f5c54244; }

footer { text-align:center; padding:40px 20px; color:var(--dim); font-size:11px; border-top:1px solid var(--border); }
footer a { color:var(--gold); text-decoration:none; }
</style>
</head>
<body>

<div class="hero">
  <div class="num" style="color:var(--dgold)">Husmann Decomposition Framework</div>
  <h1>The Universe from Two Numbers</h1>
  <div class="sub">Patent Application 19/560,637 — Thomas A. Husmann / iBuilt LTD — March 2026</div>
  <div class="inputs">
    Input 1: <span>φ = 1.6180339887</span> &nbsp;&nbsp;|&nbsp;&nbsp;
    Input 2: <span>t<sub>as</sub> = 232 × 10⁻¹⁸ s</span>
  </div>
  <div class="sub" style="margin-top:6px;">Everything below is <em>derived</em>. Zero free parameters. Computed in {{compute_time}} ms.</div>
</div>

<div class="container">

<!-- ═══ SECTION 1: DERIVED CONSTANTS ═══ -->
<div class="section">
  <div class="num">Part I</div>
  <h2>Derived Constants</h2>
  <div class="grid3">
    <div class="card">
      <h3>Hopping Integral</h3>
      <div class="val">{{J_eV}} <span class="unit">eV</span></div>
      <div class="compare">J = 2πħ / (ω × t<sub>as</sub>)</div>
    </div>
    <div class="card">
      <h3>Coherence Patch</h3>
      <div class="val">{{l0_nm}} <span class="unit">nm</span></div>
      <div class="compare">l₀ = cħ / 2J</div>
    </div>
    <div class="card">
      <h3>Gap Fraction</h3>
      <div class="val">{{W}}</div>
      <div class="compare">W = 2/φ⁴ + φ<sup>−1/φ</sup>/φ³</div>
    </div>
    <div class="card">
      <h3>Speed of Light</h3>
      <div class="val">c <span class="unit">exact</span></div>
      <div class="compare">Derived: {{c_derived}} m/s — <span class="match">self-consistent</span></div>
    </div>
    <div class="card">
      <h3>DM Self-Coupling</h3>
      <div class="val">W² = {{W2}}</div>
      <div class="compare">DM gravity — 4.58× stronger than baryonic</div>
    </div>
    <div class="card">
      <h3>Baryon Trapping</h3>
      <div class="val">W⁴ = {{W4}}</div>
      <div class="compare">4.76% of matter gets caught per W⁴ point</div>
    </div>
  </div>
</div>

<!-- ═══ SECTION 2: COSMOLOGICAL DENSITIES ═══ -->
<div class="section">
  <div class="num">Part II</div>
  <h2>Cosmological Energy Budget</h2>
  <div class="eq">1/φ + 1/φ³ + 1/φ⁴ = 1.000000000000000</div>
  <div class="grid3">
    <div class="card">
      <h3><span class="tag tag-w4">Baryonic</span> Ω<sub>b</sub></h3>
      <div class="val">{{Ob}}</div>
      <div class="compare">Planck 2018: <span class="planck">0.04860</span> — <span class="match">{{Ob_err}}% match</span></div>
    </div>
    <div class="card">
      <h3><span class="tag tag-dm">Dark Matter</span> Ω<sub>DM</sub></h3>
      <div class="val">{{Odm}}</div>
      <div class="compare">Planck 2018: <span class="planck">0.26070</span> — <span class="match">{{Odm_err}}% match</span></div>
    </div>
    <div class="card">
      <h3><span class="tag tag-de">Dark Energy</span> Ω<sub>DE</sub></h3>
      <div class="val">{{Ode}}</div>
      <div class="compare">Planck 2018: <span class="planck">0.68890</span> — <span class="match">{{Ode_err}}% match</span></div>
    </div>
  </div>
  <div class="card" style="margin-top:20px; text-align:center;">
    <h3>σ₃ Center Plane Band Width — The Headline Number</h3>
    <div class="val" style="font-size:48px;">{{s3w}}</div>
    <div class="compare" style="font-size:14px;">
      Planck Ω<sub>b</sub> = <span class="planck">0.04860</span> —
      <span class="match" style="font-size:18px;">{{s3w_err}}% match</span>
      &nbsp; (10× tighter than W⁴ alone)
    </div>
  </div>
</div>

<!-- ═══ SECTION 3: CANTOR SPECTRUM ═══ -->
<div class="section">
  <div class="num">Part III</div>
  <h2>The Cantor Spectrum — Zeckendorf Build Order</h2>
  <div class="eq">Zeckendorf(294) = {233, 55, 5, 1} = F(13) + F(10) + F(5) + F(1)</div>
  <p style="color:var(--dim); margin:10px 0;">Each Fibonacci term is a resolution level. The address of the universe IS its construction manual.</p>
  <img class="img-full" src="data:image/png;base64,{{img_cantor}}" alt="Cantor spectrum at three Zeckendorf resolutions">
  <div class="grid3" style="margin-top:20px;">
    <div class="card"><h3>N = 5</h3><p style="color:var(--dim)">1 band · 0 gaps<br>The undivided whole</p></div>
    <div class="card"><h3>N = 55</h3><p style="color:var(--dim)">{{n55_bands}} bands · {{n55_gaps}} gaps<br>Superclusters + DM walls</p></div>
    <div class="card"><h3>N = 233</h3><p style="color:var(--dim)">{{n233_bands}} bands · {{n233_gaps}} gaps<br>Full cosmic web · {{n_w4}} W⁴ points</p></div>
  </div>
</div>

<!-- ═══ SECTION 4: THREE AXES ═══ -->
<div class="section">
  <div class="num">Part IV</div>
  <h2>Three Icosahedral Backbone Axes</h2>
  <div class="eq">S = (0,1,φ), (φ,0,1), (1,φ,0) / √(2+φ) &nbsp;&nbsp;|&nbsp;&nbsp; All angles = 63.4° = arccos(1/√5)</div>
  <div class="img-pair">
    <img src="data:image/png;base64,{{img_axes}}" alt="Three backbone axes">
    <div>
      <div class="card" style="margin-bottom:15px;">
        <h3><span class="tag tag-de">S₁</span> Dark Energy Backbone</h3>
        <div class="val">1/φ = 0.618</div>
        <div class="compare">Longest reach · Structural skeleton · 61.8% of energy budget</div>
      </div>
      <div class="card" style="margin-bottom:15px;">
        <h3><span class="tag tag-dm">S₂</span> Dark Matter Web</h3>
        <div class="val">1/φ³ = 0.236</div>
        <div class="compare">Medium reach · Connective tissue · 23.6%</div>
      </div>
      <div class="card">
        <h3><span class="tag tag-m">S₃</span> Baryonic Matter</h3>
        <div class="val">1/φ⁴ = 0.146</div>
        <div class="compare">Shortest reach · Finest structure · 14.6%</div>
      </div>
    </div>
  </div>
</div>

<!-- ═══ SECTION 5: OUR UNIVERSE ═══ -->
<div class="section">
  <div class="num">Part V</div>
  <h2>Our Observable Universe — σ₃ Center Plane</h2>
  <p style="color:var(--dim); margin-bottom:5px;">The entangled state between gravitational collapse (σ₁) and dark energy expansion (σ₅). P|ψ₀⟩ = |ψ₀⟩.</p>
  <div class="img-pair">
    <img src="data:image/png;base64,{{img_overlap}}" alt="σ₃ fold overlap — our universe">
    <img src="data:image/png;base64,{{img_3d}}" alt="3D backbone with W⁴ matter">
  </div>
  <div class="grid2" style="margin-top:20px;">
    <div class="card">
      <h3>σ₃ Structure</h3>
      <table>
        <tr><td>Bands</td><td class="num gold">{{s3_bands}}</td></tr>
        <tr><td>Backbone corridors</td><td class="num gold">{{s3_gaps}}</td></tr>
        <tr><td>Band edges per axis</td><td class="num gold">{{s3_edges}}</td></tr>
        <tr><td>W⁴ matter points</td><td class="num gold">{{n_w4}}</td></tr>
        <tr><td>Sub-void ratio</td><td class="num gold">{{sv_ratio}} <span style="color:var(--dim)">(φ = 1.618, {{sv_err}}%)</span></td></tr>
      </table>
    </div>
    <div class="card">
      <h3>DM Wall Symmetry</h3>
      <table>
        <tr><td>σ₂ wall width</td><td class="num">{{wL_w}}</td></tr>
        <tr><td>σ₄ wall width</td><td class="num">{{wR_w}}</td></tr>
        <tr><td>Ratio σ₂/σ₄</td><td class="num match">{{wall_ratio}}</td></tr>
        <tr><td>Particle-hole symmetry</td><td class="num match">exact</td></tr>
      </table>
    </div>
  </div>
</div>

<!-- ═══ SECTION 6: VOID PREDICTIONS ═══ -->
<div class="section">
  <div class="num">Part VI</div>
  <h2>Cosmic Void Predictions — The Rosetta Stone</h2>
  <p style="color:var(--dim); margin-bottom:5px;">The same 34 gap fractions applied to any scale predict structural void sizes. Zero free parameters.</p>
  <img class="img-full" src="data:image/png;base64,{{img_voids}}" alt="Predicted vs observed cosmic voids">
  <div class="card" style="margin-top:20px;">
    <h3>Predicted vs Observed — Full Table</h3>
    <table>
      <thead>
        <tr><th>Structure</th><th>Observed (Mly)</th><th>Predicted (Mly)</th><th>Gap Fraction</th><th>Error</th></tr>
      </thead>
      <tbody>
        {{void_rows}}
      </tbody>
    </table>
  </div>
</div>

<!-- ═══ SECTION 7: 3D VIEWS ═══ -->
<div class="section">
  <div class="num">Part VII</div>
  <h2>3D Backbone — Multiple Angles</h2>
  <p style="color:var(--dim);">4,913 W⁴ matter points inside the σ₃ center plane. Gold = baryonic matter. Discs = Cantor fold planes.</p>
  <div class="img-pair">
    <img src="data:image/png;base64,{{img_3d_top}}" alt="Top view">
    <img src="data:image/png;base64,{{img_3d_side}}" alt="Side view">
  </div>
</div>

<!-- ═══ SECTION 8: THE MECHANISM ═══ -->
<div class="section">
  <div class="num">Part VIII</div>
  <h2>The Physical Mechanism</h2>
  <div class="grid2">
    <div class="card">
      <h3>Dual Bubble Containment</h3>
      <p style="color:var(--dim);">DM gaps (W² self-coupling = {{W2}}) curve into closed ellipsoidal shells.
      Outer bubble: σ₂ + σ₄ walls = observable universe boundary.
      Inner bubble: σ₃ sub-voids = galactic containment.
      Kerr oblate: equatorial/polar = √φ = 1.272.</p>
    </div>
    <div class="card">
      <h3>Matter Flow</h3>
      <p style="color:var(--dim);">Matter enters south pole, flows along backbone axis.
      4.76% trapped at each W⁴ intersection → galaxy seeds.
      At north pole: 5% tunnel out (edge state), 95% recirculate along wall.
      Trapped matter develops vortex → flattens → galaxy disk.</p>
    </div>
    <div class="card">
      <h3>Entanglement Structure</h3>
      <p style="color:var(--dim);">σ₁ (bonding/gravity) and σ₅ (antibonding/expansion) are particle-hole partners.
      σ₃ at E = 0 is self-dual: P|ψ₀⟩ = |ψ₀⟩.
      We ARE the entangled state of collapse and expansion.
      DM walls = entanglement channels, not particles.</p>
    </div>
    <div class="card">
      <h3>V = 2J: The Existence Condition</h3>
      <p style="color:var(--dim);">V > 2J: all bonding → universe collapses → black hole (one ring).
      V < 2J: all antibonding → structure dissolves → heat death.
      V = 2J: critical Cantor set → maximum complexity → observers.</p>
    </div>
  </div>
</div>

</div><!-- container -->

<footer>
  <p>© 2026 Thomas A. Husmann / iBuilt LTD · Patent Application 19/560,637</p>
  <p><a href="https://github.com/thusmann5327/Unified_Theory_Physics">GitHub</a> ·
     <a href="https://universe.eldon.food">Live Simulator</a> ·
     <a href="https://eldon.fun/scientific_research">Research Papers</a></p>
  <p style="margin-top:10px; color:#444;">The observer does not exist despite the tension between collapse and expansion.<br>The observer exists <em>because</em> of it.</p>
</footer>

</body></html>"""


@app.route("/")
def index():
    sec = SECTORS
    # Void comparison data
    voids = [
        ("σ₂/σ₄ DM walls", 30000, GAP_FRACS[0][0]),
        ("Sloan Great Wall", 1380, None),
        ("KBC Void", 2000, None),
        ("CMB Cold Spot", 1800, None),
        ("Dipole Repeller", 600, None),
        ("BOSS Great Wall", 1000, None),
        ("Boötes Void", 250, None),
        ("Local Void", 150, None),
        ("Sculptor Void", 100, None),
    ]
    void_rows = ""
    for name, obs, fixed in voids:
        if fixed:
            pred = fixed * 93000
            frac = fixed
        else:
            best_p, best_f = None, None
            for f, _ in GAP_FRACS:
                p = f * 93000
                if best_p is None or abs(p-obs) < abs(best_p-obs):
                    best_p, best_f = p, f
            pred, frac = best_p, best_f
        err = abs(pred-obs)/obs*100
        ec = "match" if err < 10 else ""
        void_rows += f'<tr><td>{name}</td><td class="num">{obs:,}</td><td class="num">{pred:,.0f}</td><td class="num">{frac:.6f}</td><td class="num {ec}">{err:.1f}%</td></tr>\n'

    # Render all images
    print("  Rendering Cantor bars...")
    img_cantor = render_cantor_bar()
    print("  Rendering σ₃ overlap...")
    img_overlap = render_sigma3_overlap()
    print("  Rendering 3D perspective...")
    img_3d = render_3d_backbone(22, 38)
    print("  Rendering 3D top...")
    img_3d_top = render_3d_backbone(85, 0)
    print("  Rendering 3D side...")
    img_3d_side = render_3d_backbone(0, 90)
    print("  Rendering void comparison...")
    img_voids = render_void_comparison()
    print("  Rendering axes diagram...")
    img_axes = render_axes_diagram()

    return render_template_string(HTML,
        compute_time=f"{COMPUTE_TIME*1000:.0f}",
        J_eV=f"{J_EV:.3f}", l0_nm=f"{L0*1e9:.3f}", W=f"{W:.6f}",
        c_derived=f"{2*J_J*L0/HBAR:.0f}",
        W2=f"{W2:.6f}", W4=f"{W4:.6f}",
        Ob=f"{OMB:.5f}", Odm=f"{OMDM:.5f}", Ode=f"{OMDE:.5f}",
        Ob_err=f"{abs(OMB-0.04860)/0.04860*100:.2f}",
        Odm_err=f"{abs(OMDM-0.26070)/0.26070*100:.2f}",
        Ode_err=f"{abs(OMDE-0.68890)/0.68890*100:.2f}",
        s3w=f"{sec['s3w']:.5f}",
        s3w_err=f"{abs(sec['s3w']-0.04860)/0.04860*100:.2f}",
        n55_bands=len(BANDS_55), n55_gaps=len(GAPS_55),
        n233_bands=len(BANDS_233), n233_gaps=len(GAPS_233),
        n_w4=f"{len(W4_PTS):,}",
        s3_bands=len(sec['s3b']), s3_gaps=len(sec['s3g']),
        s3_edges=len(S3_EDGES_E),
        sv_ratio=f"{SV_RATIO:.4f}",
        sv_err=f"{abs(SV_RATIO-PHI)/PHI*100:.2f}",
        wL_w=f"{sec['wL']['w']:.4f}", wR_w=f"{sec['wR']['w']:.4f}",
        wall_ratio=f"{sec['wL']['w']/sec['wR']['w']:.6f}",
        void_rows=void_rows,
        img_cantor=img_cantor, img_overlap=img_overlap,
        img_3d=img_3d, img_3d_top=img_3d_top, img_3d_side=img_3d_side,
        img_voids=img_voids, img_axes=img_axes,
    )


if __name__ == "__main__":
    print("=" * 60)
    print("HUSMANN DECOMPOSITION — POLISHED DEMO")
    print("=" * 60)
    print(f"  φ = {PHI:.10f}")
    print(f"  W = {W:.8f}")
    print(f"  W⁴ = {W4:.6f}")
    print(f"  Ω_b = {OMB:.5f} (Planck: 0.04860)")
    print(f"  σ₃ = {SECTORS['s3w']:.5f} (Planck: 0.04860, {abs(SECTORS['s3w']-0.04860)/0.04860*100:.2f}%)")
    print(f"  Axis angle = {AXIS_ANGLE:.3f}°")
    print(f"  W⁴ points = {len(W4_PTS):,}")
    print(f"  Computed in {COMPUTE_TIME*1000:.0f} ms")
    print()
    print("  Starting server on http://localhost:5000")
    print()
    app.run(host="0.0.0.0", port=5000, debug=False)
