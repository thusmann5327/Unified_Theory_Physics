#!/usr/bin/env python3
"""
vortex_connected.py — Regenerate vortex figures with golden-angle helix lines
connecting consecutive elements so the spiral shape is visible.
"""

import matplotlib
matplotlib.use('Agg')

import numpy as np
import math
import json
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Patch

# ── Constants ──────────────────────────────────────────────────────
PHI = 1.6180339887498948
GOLDEN_ANGLE_RAD = 2 * math.pi / PHI**2   # 137.508°
W = (2 + PHI**(1/PHI**2)) / PHI**4
BOS = 0.9920
R_C = 1 - 1/PHI**4
THETA_LEAK = 0.564; THETA_RC = 0.854; THETA_BASE = 1.000
R_LEAK = math.sqrt(1 + (THETA_LEAK * BOS)**2)
R_RC   = math.sqrt(1 + (THETA_RC * BOS)**2)
R_BASE = math.sqrt(1 + (THETA_BASE * BOS)**2)

RESULTS_DIR = '/Users/universe/Unified_Theory_Physics/results/vortex_figures'
os.makedirs(RESULTS_DIR, exist_ok=True)

# ── Load element data from the vortex analysis ────────────────────
with open('/Users/universe/Unified_Theory_Physics/results/vortex_3d_analysis.json') as f:
    data = json.load(f)

elements = data['element_data']

# Sort by Z
elements.sort(key=lambda e: e['Z'])

# Compute cylindrical coordinates with golden angle
for e in elements:
    e['pred'] = e['predicted_ratio']
    e['sym'] = e['symbol']
    e['angle'] = (e['Z'] * GOLDEN_ANGLE_RAD) % (2 * math.pi)
    e['x'] = e['pred'] * math.cos(e['angle'])
    e['y'] = e['pred'] * math.sin(e['angle'])

block_colors = {
    's': '#3498DB',   # blue
    'p': '#E74C3C',   # red
    'd': '#2ECC71',   # green
    'f': '#9B59B6',   # purple
    'ng': '#F39C12',  # orange
}

band_colors = {
    'leak': '#E74C3C',      # red
    'rc': '#2ECC71',        # green
    'baseline': '#3498DB',  # blue
}

band_shell = {'leak': R_LEAK, 'rc': R_RC, 'baseline': R_BASE}

Z_arr = np.array([e['Z'] for e in elements])
R_arr = np.array([e['pred'] for e in elements])
X_arr = np.array([e['x'] for e in elements])
Y_arr = np.array([e['y'] for e in elements])
ang_arr = np.array([e['angle'] for e in elements])
bands = [e['band'] for e in elements]

# ── Helper: draw smooth helix between Z_min and Z_max ─────────────
def helix_line(r, z_min, z_max, n_points=500):
    """Generate smooth golden-angle helix at radius r."""
    z = np.linspace(z_min, z_max, n_points)
    angle = z * GOLDEN_ANGLE_RAD
    x = r * np.cos(angle)
    y = r * np.sin(angle)
    return x, y, z

# ══════════════════════════════════════════════════════════════════
# FIGURE 1: 3D point cloud with helix lines (4 views)
# ══════════════════════════════════════════════════════════════════
print("Generating 3D point cloud with helix lines...")

fig = plt.figure(figsize=(16, 12))
for view_idx, (elev, azim, title_suffix) in enumerate([
    (20, 45, 'Perspective'), (20, 135, 'Rear'),
    (85, 0, 'Top-down'), (5, 0, 'Side')
]):
    ax = fig.add_subplot(2, 2, view_idx + 1, projection='3d')

    # Draw smooth helix lines for each band
    for band_name, color in band_colors.items():
        r = band_shell[band_name]
        hx, hy, hz = helix_line(r, 3, 99)
        ax.plot(hx, hy, hz, color=color, alpha=0.25, linewidth=0.5)

    # Draw elements connected by lines within each band
    for band_name, color in band_colors.items():
        band_els = sorted([e for e in elements if e['band'] == band_name], key=lambda e: e['Z'])
        if len(band_els) < 2:
            continue
        bx = [e['x'] for e in band_els]
        by = [e['y'] for e in band_els]
        bz = [e['Z'] for e in band_els]
        # Connect consecutive same-band elements with lines
        ax.plot(bx, by, bz, color=color, alpha=0.4, linewidth=1.0, linestyle='-')

    # Plot element dots colored by block
    for e in elements:
        c = block_colors.get(e['block'], '#888888')
        marker = {'leak': 'o', 'rc': 's', 'baseline': '^'}[e['band']]
        ax.scatter([e['x']], [e['y']], [e['Z']], c=c, marker=marker, s=30, alpha=0.9,
                   edgecolors='k', linewidths=0.3)

    ax.set_xlabel('X', fontsize=8)
    ax.set_ylabel('Y', fontsize=8)
    ax.set_zlabel('Z (atomic #)', fontsize=8)
    ax.set_title(title_suffix, fontsize=10, fontweight='bold')
    ax.view_init(elev=elev, azim=azim)

fig.suptitle('Bigollo Vortex — Golden Angle Helix (Z × 137.508°)\n'
             'Lines connect consecutive elements on same band',
             fontsize=13, fontweight='bold', y=0.98)

legend_els = [Patch(facecolor=c, edgecolor='k', label=f'{b}-block') for b, c in block_colors.items()]
legend_els += [plt.Line2D([0],[0], color=c, linewidth=2, label=f'{b} band (R={band_shell[b]:.3f})')
               for b, c in band_colors.items()]
fig.legend(handles=legend_els, loc='lower center', ncol=4, fontsize=8,
           bbox_to_anchor=(0.5, 0.01))
plt.tight_layout(rect=[0, 0.05, 1, 0.95])
plt.savefig(f'{RESULTS_DIR}/7a_3d_pointcloud.png', dpi=200, bbox_inches='tight')
plt.close()
print("  Saved 7a_3d_pointcloud.png")

# ══════════════════════════════════════════════════════════════════
# FIGURE 2: Top-down with spiral connecting lines
# ══════════════════════════════════════════════════════════════════
print("Generating top-down with spiral lines...")

fig, ax = plt.subplots(figsize=(11, 11))

# Draw smooth spirals for each shell
for band_name, color in band_colors.items():
    r = band_shell[band_name]
    hx, hy, hz = helix_line(r, 3, 99, n_points=2000)
    ax.plot(hx, hy, color=color, alpha=0.15, linewidth=0.5)

# Draw shell circles
for r_shell, label in [(R_LEAK, f'Leak R={R_LEAK:.3f}'),
                        (R_RC, f'Crossover R={R_RC:.3f}'),
                        (R_BASE, f'Baseline R={R_BASE:.3f}')]:
    circle = plt.Circle((0, 0), r_shell, fill=False, linestyle='--',
                         color='gray', alpha=0.4, linewidth=0.5)
    ax.add_patch(circle)

# Connect consecutive same-band elements
for band_name, color in band_colors.items():
    band_els = sorted([e for e in elements if e['band'] == band_name], key=lambda e: e['Z'])
    if len(band_els) >= 2:
        bx = [e['x'] for e in band_els]
        by = [e['y'] for e in band_els]
        ax.plot(bx, by, color=color, alpha=0.35, linewidth=0.8)

# Plot elements colored by block
for e in elements:
    c = block_colors.get(e['block'], '#888888')
    marker = {'leak': 'o', 'rc': 's', 'baseline': '^'}[e['band']]
    ax.scatter(e['x'], e['y'], c=c, marker=marker, s=45, alpha=0.9,
              edgecolors='k', linewidths=0.3, zorder=5)
    ax.annotate(e['sym'], (e['x'], e['y']), fontsize=4, alpha=0.6,
                ha='center', va='bottom', textcoords='offset points',
                xytext=(0, 3))

ax.set_xlabel('X (r cos θ)', fontsize=10)
ax.set_ylabel('Y (r sin θ)', fontsize=10)
ax.set_title('Top-Down View — Looking Down the Vortex Axis\n'
             'Golden angle phyllotaxis (Z × 137.508°), lines connect same-band elements',
             fontsize=11, fontweight='bold')
ax.set_aspect('equal')
ax.set_xlim(-1.7, 1.7)
ax.set_ylim(-1.7, 1.7)
ax.grid(True, alpha=0.2)

legend_els = [Patch(facecolor=c, edgecolor='k', label=f'{b}-block') for b, c in block_colors.items()]
legend_els += [plt.Line2D([0],[0], color=c, linewidth=2, label=f'{b} band')
               for b, c in band_colors.items()]
ax.legend(handles=legend_els, loc='upper right', fontsize=8)
plt.savefig(f'{RESULTS_DIR}/7b_top_down.png', dpi=200, bbox_inches='tight')
plt.close()
print("  Saved 7b_top_down.png")

# ══════════════════════════════════════════════════════════════════
# FIGURE 3: Side view with band ribbons
# ══════════════════════════════════════════════════════════════════
print("Generating side view with connecting lines...")

fig, ax = plt.subplots(figsize=(16, 8))

# Connect consecutive same-band elements with lines
for band_name, color in band_colors.items():
    band_els = sorted([e for e in elements if e['band'] == band_name], key=lambda e: e['Z'])
    if len(band_els) >= 2:
        bz = [e['Z'] for e in band_els]
        br = [e['pred'] for e in band_els]
        ax.plot(bz, br, color=color, alpha=0.3, linewidth=1.0,
                label=f'{band_name} band (R={band_shell[band_name]:.3f})')

# Band reference lines
for r_val, label in [(R_LEAK, 'R_leak'), (R_RC, 'R_rc'), (R_BASE, 'R_base')]:
    ax.axhline(y=r_val, color='gray', linestyle=':', alpha=0.3, linewidth=0.5)
    ax.text(100.5, r_val, label, fontsize=7, color='gray', va='center')

# Plot elements colored by block
for e in elements:
    c = block_colors.get(e['block'], '#888888')
    marker = {'leak': 'o', 'rc': 's', 'baseline': '^'}[e['band']]
    ax.scatter(e['Z'], e['pred'], c=c, marker=marker, s=35, alpha=0.9,
              edgecolors='k', linewidths=0.3, zorder=5)
    ax.annotate(e['sym'], (e['Z'], e['pred']), fontsize=4, alpha=0.5,
                ha='center', va='bottom', textcoords='offset points', xytext=(0, 3))

ax.set_xlabel('Z (Atomic Number)', fontsize=11)
ax.set_ylabel('Predicted vdW/cov Ratio', fontsize=11)
ax.set_title('Bigollo Scatter — Three Quantized Bands with Connecting Lines\n'
             'Elements connected within each band, colored by electron block',
             fontsize=12, fontweight='bold')
ax.grid(True, alpha=0.2)
ax.set_xlim(0, 102)

legend_els = [Patch(facecolor=c, edgecolor='k', label=f'{b}') for b, c in block_colors.items()]
legend_els += [plt.Line2D([0],[0], color=c, linewidth=2, label=f'{b}')
               for b, c in band_colors.items()]
ax.legend(handles=legend_els, loc='upper right', fontsize=8, ncol=2, title='Block / Band')
plt.tight_layout()
plt.savefig(f'{RESULTS_DIR}/7c_side_view.png', dpi=200, bbox_inches='tight')
plt.close()
print("  Saved 7c_side_view.png")

# ══════════════════════════════════════════════════════════════════
# FIGURE 4: Unwrapped cylinder with helix diagonals
# ══════════════════════════════════════════════════════════════════
print("Generating unwrapped cylinder...")

fig, axes = plt.subplots(3, 1, figsize=(16, 12), sharex=True)
for ax_idx, band_name in enumerate(['baseline', 'rc', 'leak']):
    ax = axes[ax_idx]
    band_els = sorted([e for e in elements if e['band'] == band_name], key=lambda e: e['Z'])

    # Draw golden angle reference line (the ideal helix unwrapped is a diagonal)
    z_line = np.arange(3, 100)
    ang_line = (z_line * math.degrees(GOLDEN_ANGLE_RAD)) % 360
    ax.plot(z_line, ang_line, color=band_colors[band_name], alpha=0.1,
            linewidth=0.5, linestyle='-')

    # Connect consecutive elements
    if len(band_els) >= 2:
        bz = [e['Z'] for e in band_els]
        ba = [math.degrees(e['angle']) for e in band_els]
        ax.plot(bz, ba, color=band_colors[band_name], alpha=0.4, linewidth=1.0)

    # Plot points colored by block
    for e in band_els:
        c = block_colors.get(e['block'], '#888888')
        ax.scatter(e['Z'], math.degrees(e['angle']), c=c, s=45, alpha=0.9,
                  edgecolors='k', linewidths=0.3, zorder=5)
        ax.annotate(e['sym'], (e['Z'], math.degrees(e['angle'])),
                    fontsize=5, alpha=0.6, ha='center', va='bottom',
                    textcoords='offset points', xytext=(0, 4))

    r = band_shell[band_name]
    ax.set_ylabel('Angle (°)', fontsize=10)
    ax.set_title(f'{band_name.upper()} band — R = {r:.4f}  ({len(band_els)} elements)',
                 fontsize=10, fontweight='bold', color=band_colors[band_name])
    ax.set_ylim(-5, 365)
    ax.set_yticks([0, 90, 137.5, 180, 270, 360])
    ax.axhline(y=137.508, color='gold', alpha=0.3, linestyle=':', label='137.5° golden angle')
    ax.grid(True, alpha=0.2)
    ax.legend(fontsize=7, loc='upper right')

axes[-1].set_xlabel('Z (Atomic Number)', fontsize=11)
fig.suptitle('Unwrapped Vortex Cylinder — Golden Angle Helix\n'
             'Each element at Z × 137.508° (mod 360°), lines connect consecutive same-band elements',
             fontsize=12, fontweight='bold')
plt.tight_layout(rect=[0, 0, 1, 0.94])
plt.savefig(f'{RESULTS_DIR}/7d_unwrapped.png', dpi=200, bbox_inches='tight')
plt.close()
print("  Saved 7d_unwrapped.png")

# ══════════════════════════════════════════════════════════════════
# FIGURE 5: Concentric shells with helix paths
# ══════════════════════════════════════════════════════════════════
print("Generating concentric shells with helix paths...")

fig = plt.figure(figsize=(14, 11))
ax = fig.add_subplot(111, projection='3d')

# Draw translucent shell surfaces
z_cyl = np.linspace(3, 99, 40)
t_cyl = np.linspace(0, 2*np.pi, 40)
Z_cyl, T_cyl = np.meshgrid(z_cyl, t_cyl)
for r_shell, c_shell in [(R_LEAK, '#ff9999'), (R_RC, '#99ff99'), (R_BASE, '#9999ff')]:
    X_cyl = r_shell * np.cos(T_cyl)
    Y_cyl = r_shell * np.sin(T_cyl)
    ax.plot_surface(X_cyl, Y_cyl, Z_cyl, alpha=0.05, color=c_shell)

# Draw helix lines on each shell
for band_name, color in band_colors.items():
    r = band_shell[band_name]
    hx, hy, hz = helix_line(r, 3, 99, n_points=1000)
    ax.plot(hx, hy, hz, color=color, alpha=0.3, linewidth=0.8)

# Connect consecutive same-band elements
for band_name, color in band_colors.items():
    band_els = sorted([e for e in elements if e['band'] == band_name], key=lambda e: e['Z'])
    if len(band_els) >= 2:
        bx = [e['x'] for e in band_els]
        by = [e['y'] for e in band_els]
        bz = [e['Z'] for e in band_els]
        ax.plot(bx, by, bz, color=color, alpha=0.5, linewidth=1.2)

# Plot elements
for e in elements:
    c = block_colors.get(e['block'], '#888888')
    ax.scatter([e['x']], [e['y']], [e['Z']], c=c, s=25, alpha=0.9,
              edgecolors='k', linewidths=0.3)

ax.set_xlabel('X', fontsize=9)
ax.set_ylabel('Y', fontsize=9)
ax.set_zlabel('Z (atomic #)', fontsize=9)
ax.set_title('Three Concentric Vortex Shells\n'
             'Golden-angle helix lines + element connections',
             fontsize=12, fontweight='bold')
ax.view_init(elev=15, azim=45)

legend_els = [plt.Line2D([0],[0], color=c, linewidth=2, label=f'{b} (R={band_shell[b]:.3f})')
              for b, c in band_colors.items()]
ax.legend(handles=legend_els, loc='upper left', fontsize=9)
plt.savefig(f'{RESULTS_DIR}/7e_concentric_shells.png', dpi=200, bbox_inches='tight')
plt.close()
print("  Saved 7e_concentric_shells.png")

# ══════════════════════════════════════════════════════════════════
# FIGURE 6: Single clean 3D view with helix + connections
# ══════════════════════════════════════════════════════════════════
print("Generating clean single 3D view...")

fig = plt.figure(figsize=(14, 11))
ax = fig.add_subplot(111, projection='3d')

# Smooth helix backbone for each band
for band_name, color in band_colors.items():
    r = band_shell[band_name]
    hx, hy, hz = helix_line(r, 3, 99, n_points=1500)
    ax.plot(hx, hy, hz, color=color, alpha=0.2, linewidth=0.6,
            label=f'{band_name} helix (R={r:.3f})')

# Connect consecutive same-band elements with solid lines
for band_name, color in band_colors.items():
    band_els = sorted([e for e in elements if e['band'] == band_name], key=lambda e: e['Z'])
    if len(band_els) >= 2:
        bx = [e['x'] for e in band_els]
        by = [e['y'] for e in band_els]
        bz = [e['Z'] for e in band_els]
        ax.plot(bx, by, bz, color=color, alpha=0.6, linewidth=1.5)

# Plot elements with labels
for e in elements:
    c = block_colors.get(e['block'], '#888888')
    ax.scatter([e['x']], [e['y']], [e['Z']], c=c, s=35, alpha=0.95,
              edgecolors='k', linewidths=0.4)
    ax.text(e['x'], e['y'], e['Z'] + 0.8, e['sym'],
            fontsize=3.5, alpha=0.5, ha='center')

ax.set_xlabel('X', fontsize=10)
ax.set_ylabel('Y', fontsize=10)
ax.set_zlabel('Z (Atomic Number)', fontsize=10)
ax.set_title('Bigollo Vortex — 97 Elements on Three Golden-Angle Helices\n'
             'Shell gap ratio = 0.627 ≈ 1/φ = 0.618 (1.5%)',
             fontsize=13, fontweight='bold')
ax.view_init(elev=18, azim=60)
ax.legend(fontsize=9, loc='upper left')
plt.tight_layout()
plt.savefig(f'{RESULTS_DIR}/vortex_clean_3d.png', dpi=200, bbox_inches='tight')
plt.close()
print("  Saved vortex_clean_3d.png")

print()
print("All figures regenerated with golden-angle helix connecting lines.")
print(f"View at: {RESULTS_DIR}/")
