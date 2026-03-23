#!/usr/bin/env python3
"""
vortex_90deg_test.py — Test whether the three vortex bands are connected
by 90-degree turns, like Fibonacci spiral quarter-arcs meeting boundary conditions.

Hypothesis: each element on the golden-angle helix is a point where the
Fibonacci pattern hits the border condition (2/φ⁴ + 3/φ³ = 1) and turns 90°.
The three bands (leak, rc, baseline) would then be three faces of a
right-angle structure, not three sides of an equilateral triangle.
"""

import matplotlib
matplotlib.use('Agg')

import numpy as np
import math
import json
import os
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Arc

PHI = 1.6180339887498948
GOLDEN_ANGLE_RAD = 2 * math.pi / PHI**2   # 137.508°
GOLDEN_ANGLE_DEG = 360.0 / PHI**2
BOS = 0.9920
R_LEAK = math.sqrt(1 + (0.564 * BOS)**2)
R_RC   = math.sqrt(1 + (0.854 * BOS)**2)
R_BASE = math.sqrt(1 + (1.000 * BOS)**2)

RESULTS_DIR = '/Users/universe/Unified_Theory_Physics/results/vortex_figures'
os.makedirs(RESULTS_DIR, exist_ok=True)

# Load element data
with open('/Users/universe/Unified_Theory_Physics/results/vortex_3d_analysis.json') as f:
    data = json.load(f)

elements = sorted(data['element_data'], key=lambda e: e['Z'])
for e in elements:
    e['pred'] = e['predicted_ratio']
    e['sym'] = e['symbol']
    e['angle'] = (e['Z'] * GOLDEN_ANGLE_RAD) % (2 * math.pi)
    e['x'] = e['pred'] * math.cos(e['angle'])
    e['y'] = e['pred'] * math.sin(e['angle'])

band_shell = {'leak': R_LEAK, 'rc': R_RC, 'baseline': R_BASE}

print("=" * 80)
print("  90-DEGREE TURN TEST — Fibonacci Boundary Condition in the Vortex")
print("=" * 80)
print()

# ══════════════════════════════════════════════════════════════════
# TEST 1: Angular separation between bands
# ══════════════════════════════════════════════════════════════════
print("TEST 1: Angular separation between the three bands")
print("-" * 60)

# For each element, find its nearest neighbor on a DIFFERENT band
# and measure the angle between them (in the top-down projection)
angles_between_bands = {'leak→rc': [], 'rc→baseline': [], 'leak→baseline': []}

for e in elements:
    # Find nearest element on each other band (by Z proximity)
    for other_band in ['leak', 'rc', 'baseline']:
        if other_band == e['band']:
            continue
        others = [o for o in elements if o['band'] == other_band]
        if not others:
            continue
        nearest = min(others, key=lambda o: abs(o['Z'] - e['Z']))

        # Angle between the two points as seen from origin
        ang1 = math.atan2(e['y'], e['x'])
        ang2 = math.atan2(nearest['y'], nearest['x'])
        delta = abs(ang1 - ang2) % (2 * math.pi)
        if delta > math.pi:
            delta = 2 * math.pi - delta
        delta_deg = math.degrees(delta)

        key = f"{min(e['band'], other_band)}→{max(e['band'], other_band)}"
        if key in angles_between_bands:
            angles_between_bands[key].append(delta_deg)

for pair, angles in angles_between_bands.items():
    if angles:
        mean_ang = np.mean(angles)
        std_ang = np.std(angles)
        print(f"  {pair:20s}: mean = {mean_ang:.1f}° ± {std_ang:.1f}°")
        # Test against 90° and 60°
        err_90 = abs(mean_ang - 90) / 90 * 100
        err_60 = abs(mean_ang - 60) / 60 * 100
        err_120 = abs(mean_ang - 120) / 120 * 100
        print(f"    vs 90°: {err_90:.1f}% | vs 60°: {err_60:.1f}% | vs 120°: {err_120:.1f}%")

print()

# ══════════════════════════════════════════════════════════════════
# TEST 2: Consecutive element turn angles
# ══════════════════════════════════════════════════════════════════
print("TEST 2: Turn angles between consecutive elements (Z, Z+1, Z+2)")
print("-" * 60)

# For each triple of consecutive elements, measure the turn angle
# This is the angle ABC where A=element[i], B=element[i+1], C=element[i+2]
turn_angles = []
turn_data = []

for i in range(len(elements) - 2):
    e1, e2, e3 = elements[i], elements[i+1], elements[i+2]
    # Vector B→A and B→C
    v1 = np.array([e1['x'] - e2['x'], e1['y'] - e2['y']])
    v2 = np.array([e3['x'] - e2['x'], e3['y'] - e2['y']])

    cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-12)
    cos_angle = np.clip(cos_angle, -1, 1)
    angle = math.degrees(math.acos(cos_angle))
    turn_angles.append(angle)
    turn_data.append({
        'Z': e2['Z'], 'sym': e2['sym'], 'band': e2['band'],
        'angle': angle,
        'band_change': e1['band'] != e2['band'] or e2['band'] != e3['band']
    })

turn_arr = np.array(turn_angles)
print(f"  All turns:      mean = {np.mean(turn_arr):.1f}° ± {np.std(turn_arr):.1f}°")
print(f"  Median:         {np.median(turn_arr):.1f}°")

# Separate by whether a band change occurs
band_change = [t for t in turn_data if t['band_change']]
no_change = [t for t in turn_data if not t['band_change']]

if band_change:
    bc_angles = [t['angle'] for t in band_change]
    print(f"  At band changes: mean = {np.mean(bc_angles):.1f}° ± {np.std(bc_angles):.1f}° (n={len(bc_angles)})")
if no_change:
    nc_angles = [t['angle'] for t in no_change]
    print(f"  Within band:     mean = {np.mean(nc_angles):.1f}° ± {np.std(nc_angles):.1f}° (n={len(nc_angles)})")

print()

# ══════════════════════════════════════════════════════════════════
# TEST 3: Golden angle and 90° relationship
# ══════════════════════════════════════════════════════════════════
print("TEST 3: Golden angle ↔ 90° relationship")
print("-" * 60)

# The golden angle is 137.508°. How does it relate to 90°?
# 137.508° = 90° + 47.508°
# 47.508° / 90° = 0.528 ≈ ?
# BUT: 360° - 137.508° = 222.492°
# 222.492° / 137.508° = 1.618 = φ (EXACT — this is the definition)
#
# Key: after N golden angle steps, when does the cumulative angle
# hit a multiple of 90°?

print(f"  Golden angle = {GOLDEN_ANGLE_DEG:.3f}°")
print(f"  360° - golden = {360 - GOLDEN_ANGLE_DEG:.3f}° (= golden × φ)")
print(f"  Golden / 90° = {GOLDEN_ANGLE_DEG/90:.6f}")
print(f"  Golden / 120° = {GOLDEN_ANGLE_DEG/120:.6f} (≈ {GOLDEN_ANGLE_DEG/120:.4f})")
print()

# Find Z values where cumulative angle is closest to multiples of 90°
print("  Z values where cumulative golden angle ≈ N × 90°:")
best_90s = []
for z in range(1, 100):
    cum_angle = (z * GOLDEN_ANGLE_DEG) % 360
    # Distance to nearest 90° multiple
    nearest_90 = min(cum_angle % 90, 90 - (cum_angle % 90))
    if nearest_90 < 5:  # within 5° of a 90° boundary
        n_quarter = round(z * GOLDEN_ANGLE_DEG / 90)
        best_90s.append({'Z': z, 'cum_angle': cum_angle, 'nearest_90': nearest_90,
                         'n_quarter': n_quarter})
        # Look up element
        elem = next((e for e in elements if e['Z'] == z), None)
        sym = elem['sym'] if elem else '?'
        band = elem['band'] if elem else '?'
        print(f"    Z={z:3d} ({sym:3s}, {band:8s}): cum={cum_angle:7.2f}°, "
              f"dist to 90n = {nearest_90:.2f}°, quarter turns = {n_quarter}")

print()

# ══════════════════════════════════════════════════════════════════
# TEST 4: Fibonacci numbers and 90° turns
# ══════════════════════════════════════════════════════════════════
print("TEST 4: Fibonacci Z-values and turn geometry")
print("-" * 60)

fibs = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
print("  At Fibonacci Z values:")
for f in fibs:
    cum = (f * GOLDEN_ANGLE_DEG) % 360
    nearest_90 = min(cum % 90, 90 - (cum % 90))
    elem = next((e for e in elements if e['Z'] == f), None)
    sym = elem['sym'] if elem else '-'
    band = elem['band'] if elem else '-'
    print(f"    Z=F={f:3d} ({sym:3s}, {band:8s}): angle={cum:7.2f}°, "
          f"dist to 90° = {nearest_90:.2f}°")

print()

# ══════════════════════════════════════════════════════════════════
# TEST 5: Three-band triangle angles in top-down projection
# ══════════════════════════════════════════════════════════════════
print("TEST 5: Triangle formed by three bands — equilateral or right-angle?")
print("-" * 60)

# For each period, find one representative element per band (if exists)
# and measure the triangle they form
periods = sorted(set(e['period'] for e in elements))
triangles = []

for per in periods:
    per_els = [e for e in elements if e['period'] == per]
    bands_present = set(e['band'] for e in per_els)

    if len(bands_present) >= 2:
        # Get centroid of each band within this period
        centroids = {}
        for b in bands_present:
            b_els = [e for e in per_els if e['band'] == b]
            cx = np.mean([e['x'] for e in b_els])
            cy = np.mean([e['y'] for e in b_els])
            centroids[b] = (cx, cy)

        if len(centroids) >= 3:
            # Measure triangle angles
            pts = list(centroids.values())
            names = list(centroids.keys())
            for i in range(len(pts)):
                v1 = np.array(pts[(i-1) % len(pts)]) - np.array(pts[i])
                v2 = np.array(pts[(i+1) % len(pts)]) - np.array(pts[i])
                cos_a = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-12)
                cos_a = np.clip(cos_a, -1, 1)
                angle = math.degrees(math.acos(cos_a))
                triangles.append({'period': per, 'vertex': names[i], 'angle': angle})
            print(f"  Period {per}: " +
                  " | ".join(f"{t['vertex']}={t['angle']:.1f}°"
                            for t in triangles[-len(centroids):]))
        elif len(centroids) == 2:
            names = list(centroids.keys())
            pts = list(centroids.values())
            dx = pts[1][0] - pts[0][0]
            dy = pts[1][1] - pts[0][1]
            ang = math.degrees(math.atan2(dy, dx))
            print(f"  Period {per}: {names[0]}↔{names[1]}, angle to x-axis = {ang:.1f}°")

if triangles:
    all_angles = [t['angle'] for t in triangles]
    print(f"\n  All triangle angles: mean = {np.mean(all_angles):.1f}° ± {np.std(all_angles):.1f}°")
    print(f"  Closest to 60° (equilateral): {abs(np.mean(all_angles) - 60):.1f}°")
    print(f"  Closest to 90° (right-angle): {abs(np.mean(all_angles) - 90):.1f}°")

print()

# ══════════════════════════════════════════════════════════════════
# TEST 6: The 90° boundary condition test
# ══════════════════════════════════════════════════════════════════
print("TEST 6: Band transitions as boundary condition 90° turns")
print("-" * 60)

# Key idea: when Z traverses the periodic table, each time the
# element switches from one band to another, does the DIRECTION
# of the helix path rotate by ~90°?

# Compute the direction of motion at each Z
directions = []
for i in range(1, len(elements)):
    dx = elements[i]['x'] - elements[i-1]['x']
    dy = elements[i]['y'] - elements[i-1]['y']
    direction = math.degrees(math.atan2(dy, dx))
    directions.append({
        'Z': elements[i]['Z'],
        'sym': elements[i]['sym'],
        'band': elements[i]['band'],
        'prev_band': elements[i-1]['band'],
        'direction': direction,
        'band_changed': elements[i]['band'] != elements[i-1]['band']
    })

# At band transitions, compute the change in direction
print("  Band transitions (direction change):")
for i in range(1, len(directions)):
    if directions[i]['band_changed']:
        delta_dir = (directions[i]['direction'] - directions[i-1]['direction']) % 360
        if delta_dir > 180:
            delta_dir -= 360
        err_90 = min(abs(delta_dir - 90), abs(delta_dir + 90),
                     abs(delta_dir - 270), abs(delta_dir + 270))
        flag = " ← 90°!" if err_90 < 15 else ""
        print(f"    Z={directions[i]['Z']:3d} ({directions[i]['sym']:3s}): "
              f"{directions[i]['prev_band']:8s} → {directions[i]['band']:8s}, "
              f"Δdir = {delta_dir:+7.1f}°, dist to ±90° = {err_90:.1f}°{flag}")

# Count how many transitions are within 15° of 90°
transitions = [d for d in directions if d['band_changed']]
if transitions:
    # For each transition, get the direction change
    trans_deltas = []
    for i in range(1, len(directions)):
        if directions[i]['band_changed']:
            delta_dir = (directions[i]['direction'] - directions[i-1]['direction']) % 360
            if delta_dir > 180:
                delta_dir -= 360
            trans_deltas.append(abs(delta_dir))

    near_90 = sum(1 for d in trans_deltas if min(abs(d-90), abs(d-270)) < 20)
    print(f"\n  Band transitions near ±90° (within 20°): {near_90}/{len(trans_deltas)} "
          f"({100*near_90/len(trans_deltas):.0f}%)")
    print(f"  Expected by chance (uniform): 44% (80° out of 180°)")

print()

# ══════════════════════════════════════════════════════════════════
# TEST 7: Shell radii and right-angle geometry
# ══════════════════════════════════════════════════════════════════
print("TEST 7: Pythagorean right-angle test on shell radii")
print("-" * 60)

# If the three shells form a right triangle, then R_BASE² = R_LEAK² + R_RC²
# (or some permutation)
print(f"  R_LEAK² = {R_LEAK**2:.6f}")
print(f"  R_RC²   = {R_RC**2:.6f}")
print(f"  R_BASE² = {R_BASE**2:.6f}")
print(f"  R_LEAK² + R_RC²  = {R_LEAK**2 + R_RC**2:.6f}")
print(f"  vs R_BASE²       = {R_BASE**2:.6f}")
err = abs(R_LEAK**2 + R_RC**2 - R_BASE**2) / R_BASE**2 * 100
print(f"  Pythagorean error: {err:.2f}%")
print()

# Alternative: test in the DIFFERENCE space
# Δ₁ = R_RC - R_LEAK = 0.1647
# Δ₂ = R_BASE - R_RC = 0.0980
# Δ₁² + Δ₂² = ? vs something²
d1 = R_RC - R_LEAK
d2 = R_BASE - R_RC
d_total = R_BASE - R_LEAK
print(f"  Gap 1 (leak→rc):    Δ₁ = {d1:.6f}")
print(f"  Gap 2 (rc→base):    Δ₂ = {d2:.6f}")
print(f"  Total gap:           Δ  = {d_total:.6f}")
print(f"  Δ₁/Δ = {d1/d_total:.6f} vs 1/φ = {1/PHI:.6f} ({abs(d1/d_total - 1/PHI)/(1/PHI)*100:.2f}%)")
print(f"  Δ₂/Δ = {d2/d_total:.6f} vs 1/φ² = {1/PHI**2:.6f} ({abs(d2/d_total - 1/PHI**2)/(1/PHI**2)*100:.2f}%)")
print(f"  Δ₁/Δ₂ = {d1/d2:.6f} vs φ = {PHI:.6f} ({abs(d1/d2 - PHI)/PHI*100:.2f}%)")
print()

# Test: sqrt(Δ₁² + Δ₂²) vs something
hyp = math.sqrt(d1**2 + d2**2)
print(f"  √(Δ₁² + Δ₂²) = {hyp:.6f}")
print(f"  vs Δ_total     = {d_total:.6f}  (err {abs(hyp-d_total)/d_total*100:.2f}%)")
print(f"  vs Δ₁ × √φ    = {d1*math.sqrt(PHI):.6f}  (err {abs(hyp-d1*math.sqrt(PHI))/(d1*math.sqrt(PHI))*100:.2f}%)")
# If Δ₁/Δ₂ = φ, then √(Δ₁² + Δ₂²) = Δ₂ × √(φ²+1) = Δ₂ × √(φ+2)
# since φ² = φ+1, so φ²+1 = φ+2
sqrt_phi_plus_2 = math.sqrt(PHI + 2)
print(f"  vs Δ₂ × √(φ+2) = {d2*sqrt_phi_plus_2:.6f}  (err {abs(hyp-d2*sqrt_phi_plus_2)/(d2*sqrt_phi_plus_2)*100:.2f}%)")
print()

# ══════════════════════════════════════════════════════════════════
# TEST 8: The boundary law at each turn
# ══════════════════════════════════════════════════════════════════
print("TEST 8: Boundary law 2/φ⁴ + 3/φ³ = 1 at band transitions")
print("-" * 60)

# The boundary law defines V = 2J, the critical point.
# At each band transition, test if the ratio of elements on each
# side locally satisfies the boundary partition.

# Count elements in windows around each transition
for i in range(1, len(elements)):
    if elements[i]['band'] != elements[i-1]['band']:
        Z_trans = elements[i]['Z']
        # Window of 10 elements centered on transition
        window = [e for e in elements if abs(e['Z'] - Z_trans) <= 5]
        before = [e for e in window if e['Z'] < Z_trans]
        after = [e for e in window if e['Z'] >= Z_trans]
        if before and after:
            # What fraction of the window is on each side?
            frac_before = len(before) / len(window)
            frac_after = len(after) / len(window)
            # Compare to boundary law fractions: 2/φ⁴ = 0.292, 3/φ³ = 0.708
            bl_small = 2/PHI**4  # 0.2918
            bl_large = 3/PHI**3  # 0.7082

print(f"  Boundary law fractions: 2/φ⁴ = {2/PHI**4:.4f}, 3/φ³ = {3/PHI**3:.4f}")
print(f"  Band populations: leak={sum(1 for e in elements if e['band']=='leak')}, "
      f"rc={sum(1 for e in elements if e['band']=='rc')}, "
      f"baseline={sum(1 for e in elements if e['band']=='baseline')}")
n_leak = sum(1 for e in elements if e['band'] == 'leak')
n_rc = sum(1 for e in elements if e['band'] == 'rc')
n_base = sum(1 for e in elements if e['band'] == 'baseline')
total = len(elements)
print(f"  leak/total     = {n_leak/total:.4f} vs 1/φ⁴ = {1/PHI**4:.4f} ({abs(n_leak/total - 1/PHI**4)/(1/PHI**4)*100:.1f}%)")
print(f"  rc/total       = {n_rc/total:.4f} vs σ₃ = 0.0728 ({abs(n_rc/total - 0.0728)/0.0728*100:.1f}%)")
print(f"  (leak+rc)/total = {(n_leak+n_rc)/total:.4f} vs 2/φ⁴ = {2/PHI**4:.4f} ({abs((n_leak+n_rc)/total - 2/PHI**4)/(2/PHI**4)*100:.1f}%)")
print(f"  base/total     = {n_base/total:.4f} vs 3/φ³ = {3/PHI**3:.4f} ({abs(n_base/total - 3/PHI**3)/3*PHI**3*100:.1f}%)")
print()

# ══════════════════════════════════════════════════════════════════
# VISUALIZATION: Top-down with angle annotations
# ══════════════════════════════════════════════════════════════════
print("Generating annotated top-down figure...")

band_colors = {'leak': '#E74C3C', 'rc': '#2ECC71', 'baseline': '#3498DB'}
block_colors = {'s': '#3498DB', 'p': '#E74C3C', 'd': '#2ECC71', 'f': '#9B59B6', 'ng': '#F39C12'}

fig, axes = plt.subplots(1, 2, figsize=(22, 10))

# LEFT: Top-down with inter-band connections showing angles
ax = axes[0]

# Draw shell circles
for r_shell, label, color in [(R_LEAK, 'Leak', '#E74C3C'),
                                (R_RC, 'Crossover', '#2ECC71'),
                                (R_BASE, 'Baseline', '#3498DB')]:
    circle = plt.Circle((0, 0), r_shell, fill=False, linestyle='--',
                         color=color, alpha=0.3, linewidth=1)
    ax.add_patch(circle)

# Connect consecutive elements with lines, colored by band
for i in range(len(elements) - 1):
    e1, e2 = elements[i], elements[i+1]
    color = '#999999'
    if e1['band'] == e2['band']:
        color = band_colors[e1['band']]
        alpha = 0.3
    else:
        color = '#FF6600'  # orange for band transitions
        alpha = 0.6
    ax.plot([e1['x'], e2['x']], [e1['y'], e2['y']],
            color=color, alpha=alpha, linewidth=0.8)

# Plot elements
for e in elements:
    c = block_colors.get(e['block'], '#888888')
    ax.scatter(e['x'], e['y'], c=c, s=30, alpha=0.9,
              edgecolors='k', linewidths=0.3, zorder=5)
    ax.annotate(e['sym'], (e['x'], e['y']), fontsize=3.5, alpha=0.5,
                ha='center', va='bottom', textcoords='offset points', xytext=(0, 3))

# Mark a few triangles formed by nearby elements on different bands
# Find triads: one element from each band, close in Z
for z_center in [10, 25, 40, 55, 70]:
    nearby = [e for e in elements if abs(e['Z'] - z_center) <= 3]
    bands_here = {}
    for e in nearby:
        if e['band'] not in bands_here:
            bands_here[e['band']] = e
    if len(bands_here) >= 2:
        pts = list(bands_here.values())
        for j in range(len(pts)):
            for k in range(j+1, len(pts)):
                ax.plot([pts[j]['x'], pts[k]['x']], [pts[j]['y'], pts[k]['y']],
                        'k--', alpha=0.15, linewidth=0.5)

ax.set_xlabel('X', fontsize=10)
ax.set_ylabel('Y', fontsize=10)
ax.set_title('Top-Down: All Consecutive Connections\n'
             'Orange = band transition, colored = within band',
             fontsize=11, fontweight='bold')
ax.set_aspect('equal')
ax.set_xlim(-1.7, 1.7); ax.set_ylim(-1.7, 1.7)
ax.grid(True, alpha=0.2)

# RIGHT: Histogram of turn angles at band transitions vs within band
ax = axes[1]

# Compute turn angles for consecutive triples
within_angles = []
transition_angles = []

for i in range(1, len(elements) - 1):
    e1, e2, e3 = elements[i-1], elements[i], elements[i+1]
    v1 = np.array([e1['x'] - e2['x'], e1['y'] - e2['y']])
    v2 = np.array([e3['x'] - e2['x'], e3['y'] - e2['y']])
    norm = np.linalg.norm(v1) * np.linalg.norm(v2)
    if norm < 1e-12:
        continue
    cos_a = np.clip(np.dot(v1, v2) / norm, -1, 1)
    angle = math.degrees(math.acos(cos_a))

    if e1['band'] != e2['band'] or e2['band'] != e3['band']:
        transition_angles.append(angle)
    else:
        within_angles.append(angle)

bins = np.arange(0, 185, 5)
if within_angles:
    ax.hist(within_angles, bins=bins, alpha=0.5, color='#3498DB',
            label=f'Within band (n={len(within_angles)})', density=True)
if transition_angles:
    ax.hist(transition_angles, bins=bins, alpha=0.5, color='#E74C3C',
            label=f'Band transitions (n={len(transition_angles)})', density=True)

ax.axvline(x=90, color='red', linestyle='--', alpha=0.7, label='90°')
ax.axvline(x=60, color='blue', linestyle='--', alpha=0.7, label='60°')
ax.axvline(x=120, color='green', linestyle='--', alpha=0.7, label='120°')
ax.axvline(x=GOLDEN_ANGLE_DEG - 90, color='gold', linestyle=':', alpha=0.7,
           label=f'Golden-90° = {GOLDEN_ANGLE_DEG-90:.1f}°')

ax.set_xlabel('Turn Angle (°)', fontsize=10)
ax.set_ylabel('Density', fontsize=10)
ax.set_title('Distribution of Turn Angles\n'
             'At band transitions vs within band',
             fontsize=11, fontweight='bold')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.2)

plt.tight_layout()
plt.savefig(f'{RESULTS_DIR}/90deg_analysis.png', dpi=200, bbox_inches='tight')
plt.close()
print("  Saved 90deg_analysis.png")

# ══════════════════════════════════════════════════════════════════
# SUMMARY
# ══════════════════════════════════════════════════════════════════
print()
print("=" * 80)
print("  SUMMARY")
print("=" * 80)
print()
print(f"  Shell gap ratio:  Δ₁/Δ_total = {d1/d_total:.4f} vs 1/φ = {1/PHI:.4f} ({abs(d1/d_total - 1/PHI)/(1/PHI)*100:.2f}%)")
print(f"  Gap ratio:        Δ₁/Δ₂ = {d1/d2:.4f} vs φ = {PHI:.4f} ({abs(d1/d2 - PHI)/PHI*100:.2f}%)")
print(f"  Pythagorean:      R_L² + R_RC² = {R_LEAK**2+R_RC**2:.4f} vs R_B² = {R_BASE**2:.4f} ({err:.2f}%)")
print()

if within_angles and transition_angles:
    print(f"  Turn angles within band:     {np.mean(within_angles):.1f}° ± {np.std(within_angles):.1f}°")
    print(f"  Turn angles at transitions:  {np.mean(transition_angles):.1f}° ± {np.std(transition_angles):.1f}°")

    mean_trans = np.mean(transition_angles)
    if abs(mean_trans - 90) < abs(mean_trans - 60):
        print(f"  → Transitions closer to 90° than 60°: YES")
    else:
        print(f"  → Transitions closer to 60° than 90°: equilateral geometry dominates")

print()
print(f"  Band populations: {n_leak} leak + {n_rc} rc + {n_base} baseline = {total}")
print(f"  (leak+rc)/base = {(n_leak+n_rc)/n_base:.4f} vs 2/φ⁴ / (3/φ³) = {(2/PHI**4)/(3/PHI**3):.4f}")
print()

# Save results
results = {
    'shell_gap_ratio': d1/d_total,
    'inverse_phi': 1/PHI,
    'gap_ratio_error_pct': abs(d1/d_total - 1/PHI)/(1/PHI)*100,
    'delta1_over_delta2': d1/d2,
    'phi': PHI,
    'gap_phi_error_pct': abs(d1/d2 - PHI)/PHI*100,
    'pythagorean_error_pct': err,
    'mean_turn_within_band': float(np.mean(within_angles)) if within_angles else None,
    'mean_turn_at_transition': float(np.mean(transition_angles)) if transition_angles else None,
    'band_populations': {'leak': n_leak, 'rc': n_rc, 'baseline': n_base},
}

with open('/Users/universe/Unified_Theory_Physics/results/vortex_90deg_results.json', 'w') as f:
    json.dump(results, f, indent=2)
print("Saved results to vortex_90deg_results.json")
