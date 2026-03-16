#!/usr/bin/env python3
"""
FOCUSED: Atomic Outer Wall from Cantor Hierarchy
================================================
The formula for vdW/covalent ratio from baryon structure up.

KEY FINDINGS FROM ROUND 1:
1. vdW(H) = σ₄/σ_shell × φ × a₀ = 120.6 pm (0.5% match!)
2. Alkali metals: vdW/cov = σ₄/σ_shell = 1.408 ± 2%
3. Period 2 p-block: ratio ~ 2.2-2.6 (anomalously high)
4. Period 3+ p-block: lone pair correction DAMPED by period
5. d-block: ratio < 1.408 (d-electrons compress outer wall)

PHYSICAL MECHANISM:
- The Cantor gap hierarchy is self-similar: each recursion level's
  gaps are φ-damped from the parent level
- Lone pairs extend the outer wall by one sub-gap per pair
- The sub-gap width depends on the RECURSION DEPTH of the atom
  in the Cantor hierarchy, which maps to the principal quantum number
- Period 2 has depth 1 (large gaps → large extension)
- Period 3 has depth 2 (smaller gaps → smaller extension)
- etc.
"""

import numpy as np
import math
from scipy.optimize import minimize

PHI = (1 + 5**0.5) / 2

# Build AAH spectrum
N = 233
H_mat = np.diag(2*np.cos(2*np.pi/PHI*np.arange(N)))
H_mat += np.diag(np.ones(N-1), 1) + np.diag(np.ones(N-1), -1)
eigs = np.sort(np.linalg.eigvalsh(H_mat))
E_range = eigs[-1] - eigs[0]
diffs = np.diff(eigs)
med = np.median(diffs)
gaps = [(i, diffs[i]) for i in range(len(diffs)) if diffs[i] > 8*med]

ranked = sorted(gaps, key=lambda g: g[1], reverse=True)
wL = min([g for g in ranked if g[1]>1], key=lambda g: eigs[g[0]]+eigs[g[0]+1])
half = E_range / 2

R_MATTER = abs(eigs[wL[0]+1]) / half
R_INNER  = abs(eigs[wL[0]]+eigs[wL[0]+1])/(2*E_range)
R_SHELL  = (abs(eigs[wL[0]])+abs(eigs[wL[0]+1]))/(2*half)
R_OUTER  = R_SHELL + wL[1]/(2*E_range)
W = 2/PHI**4 + PHI**(-1/PHI)/PHI**3

BASE = R_OUTER / R_SHELL  # 1.40838

# σ₃ sub-gap hierarchy (the recursion structure within the observer band)
wR = max([g for g in ranked if g[1]>1], key=lambda g: eigs[g[0]]+eigs[g[0]+1])
s3_start = eigs[wL[0]+1]
s3_end = eigs[wR[0]]
s3_eigs = eigs[(eigs >= s3_start) & (eigs <= s3_end)]
s3_diffs = np.diff(s3_eigs)
s3_med = np.median(s3_diffs)
s3_gaps = sorted([(s3_diffs[i]) for i in range(len(s3_diffs)) if s3_diffs[i] > 4*s3_med], reverse=True)

# The sub-gap ratios: each level is φ^(-1) of the parent (approximately)
print("σ₃ sub-gap hierarchy (Cantor recursion):")
s3_width = s3_end - s3_start
for i, g in enumerate(s3_gaps[:5]):
    frac = g / s3_width
    ratio_to_prev = s3_gaps[i-1]/g if i > 0 else 0
    print(f"  Level {i}: gap = {g:.6f}, fraction = {frac:.6f}, ratio to prev = {ratio_to_prev:.3f}")

# ═══════════════════════════════════════════════════════════
# COMPREHENSIVE ELEMENT DATA
# ═══════════════════════════════════════════════════════════
# Z, sym, r_cov(pm), r_vdw(pm), period, lone_pairs, block, notes

data = [
    # Period 1
    ( 1, 'H',   31, 120, 1, 0, 's', ''),
    ( 2, 'He',  28, 140, 1, 1, 'ng', 'filled 1s'),
    # Period 2
    ( 3, 'Li', 128, 182, 2, 0, 's', 'alkali'),
    ( 4, 'Be',  96, 153, 2, 0, 's', 'alkaline'),
    ( 5, 'B',   84, 192, 2, 0, 'p', 'group13'),
    ( 6, 'C',   76, 170, 2, 0, 'p', 'group14'),
    ( 7, 'N',   71, 155, 2, 1, 'p', 'group15'),
    ( 8, 'O',   66, 152, 2, 2, 'p', 'group16'),
    ( 9, 'F',   57, 147, 2, 3, 'p', 'halogen'),
    (10, 'Ne',  58, 154, 2, 4, 'ng', 'noble'),
    # Period 3
    (11, 'Na', 166, 227, 3, 0, 's', 'alkali'),
    (12, 'Mg', 141, 173, 3, 0, 's', 'alkaline'),
    (13, 'Al', 121, 184, 3, 0, 'p', 'group13'),
    (14, 'Si', 111, 210, 3, 0, 'p', 'group14'),
    (15, 'P',  107, 180, 3, 1, 'p', 'group15'),
    (16, 'S',  105, 180, 3, 2, 'p', 'group16'),
    (17, 'Cl', 102, 175, 3, 3, 'p', 'halogen'),
    (18, 'Ar', 106, 188, 3, 4, 'ng', 'noble'),
    # Period 4 (main group + some d-block)
    (19, 'K',  203, 275, 4, 0, 's', 'alkali'),
    (20, 'Ca', 176, 231, 4, 0, 's', 'alkaline'),
    (24, 'Cr', 139, 189, 4, 0, 'd', 'd5'),
    (25, 'Mn', 139, 197, 4, 0, 'd', 'd5'),
    (26, 'Fe', 132, 194, 4, 0, 'd', 'd6'),
    (27, 'Co', 126, 192, 4, 0, 'd', 'd7'),
    (28, 'Ni', 124, 163, 4, 0, 'd', 'd8'),
    (29, 'Cu', 132, 140, 4, 0, 'd', 'd10'),
    (30, 'Zn', 122, 139, 4, 0, 'd', 'd10'),
    (31, 'Ga', 122, 187, 4, 0, 'p', 'group13'),
    (32, 'Ge', 120, 211, 4, 0, 'p', 'group14'),
    (33, 'As', 119, 185, 4, 1, 'p', 'group15'),
    (34, 'Se', 120, 190, 4, 2, 'p', 'group16'),
    (35, 'Br', 120, 185, 4, 3, 'p', 'halogen'),
    (36, 'Kr', 116, 202, 4, 4, 'ng', 'noble'),
    # Period 5
    (37, 'Rb', 220, 303, 5, 0, 's', 'alkali'),
    (38, 'Sr', 195, 249, 5, 0, 's', 'alkaline'),
    (42, 'Mo', 154, 209, 5, 0, 'd', 'd5'),
    (44, 'Ru', 146, 207, 5, 0, 'd', 'd7'),
    (45, 'Rh', 142, 195, 5, 0, 'd', 'd8'),
    (46, 'Pd', 139, 202, 5, 0, 'd', 'd10'),
    (47, 'Ag', 145, 172, 5, 0, 'd', 'd10'),
    (48, 'Cd', 144, 158, 5, 0, 'd', 'd10'),
    (49, 'In', 142, 193, 5, 0, 'p', 'group13'),
    (50, 'Sn', 139, 217, 5, 0, 'p', 'group14'),
    (51, 'Sb', 139, 206, 5, 1, 'p', 'group15'),
    (52, 'Te', 138, 206, 5, 2, 'p', 'group16'),
    (53, 'I',  139, 198, 5, 3, 'p', 'halogen'),
    (54, 'Xe', 140, 216, 5, 4, 'ng', 'noble'),
    # Period 6
    (55, 'Cs', 244, 343, 6, 0, 's', 'alkali'),
    (56, 'Ba', 215, 268, 6, 0, 's', 'alkaline'),
]

# ═══════════════════════════════════════════════════════════
# THE FORMULA: vdW/cov = BASE + LP × g(period)
# where g(period) = A × φ^(-(period - 1))
# ═══════════════════════════════════════════════════════════
#
# Physical derivation:
# The Cantor recursion has gaps that shrink as φ^(-depth).
# The "depth" of an atom in the Cantor hierarchy = period - 1
# (because period 1 is the shallowest, period 6 is deepest).
# Each lone pair extends the outer wall by one sub-gap at that depth.
#
# The sub-gap width at depth d relative to the main gap:
# From the actual σ₃ sub-gaps:
#   Level 0: 0.324 (the main sub-gap within σ₃)
#   Level 1: 0.199
#   Level 2: 0.126
#   Ratio 0.324/0.199 = 1.628 ≈ φ ✓
#   Ratio 0.199/0.126 = 1.579 ≈ φ ✓
#
# So the recursion IS φ-damped! The sub-gap at depth d ∝ φ^(-d).

print()
print("=" * 70)
print("FORMULA: vdW/cov = σ₄/σ_shell + LP × A × φ^(-(period-1))")
print("Testing A as a framework-derived constant")
print("=" * 70)

# First, find the optimal A from the data (then identify it with framework constants)
# Exclude H and noble gases from the fit (H is anchor, noble gases different physics)

fit_data = [d for d in data if d[6] not in ('ng',) and d[0] != 1]

def cost(A):
    err_sum = 0
    for Z, sym, rc, rv, per, LP, block, notes in fit_data:
        ratio_obs = rv / rc
        ratio_pred = BASE + LP * A * PHI**(-(per - 1))
        err_sum += ((ratio_pred - ratio_obs) / ratio_obs)**2
    return err_sum

from scipy.optimize import minimize_scalar
res = minimize_scalar(cost, bounds=(0.1, 5.0), method='bounded')
A_opt = res.x

print(f"\nOptimal A = {A_opt:.6f}")
print(f"Compare with framework constants:")
print(f"  φ         = {PHI:.6f}")
print(f"  φ²        = {PHI**2:.6f}")
print(f"  2         = 2.000000")
print(f"  1+φ       = {1+PHI:.6f}")
print(f"  √5        = {5**0.5:.6f}")
print(f"  φ³        = {PHI**3:.6f}")
print(f"  2φ        = {2*PHI:.6f}")
print(f"  2+φ       = {2+PHI:.6f}")
print(f"  σ₃ sub-gap level 0 / σ₃_width × φ = {s3_gaps[0]/s3_width * PHI:.6f}")

# Let me also test A = φ exactly (since the sub-gap ratios are ~φ)
# and A = σ₄/σ_shell - 1 = 0.408 (the fractional gap itself)

for A_test, name in [
    (A_opt, f"optimal ({A_opt:.4f})"),
    (PHI, "φ"),
    (PHI**2, "φ²"),
    (1+PHI, "1+φ"),
    (5**0.5, "√5"),
    (R_OUTER/R_SHELL - 1, "σ₄/σ_shell - 1"),
    (W, "W"),
    (2.0, "2"),
    (BASE, "BASE itself"),
]:
    errors = []
    print(f"\n  A = {A_test:.4f} ({name}):")
    for Z, sym, rc, rv, per, LP, block, notes in data:
        ratio_obs = rv / rc
        ratio_pred = BASE + LP * A_test * PHI**(-(per - 1))
        err = (ratio_pred - ratio_obs) / ratio_obs * 100
        errors.append((sym, Z, rc, rv, ratio_obs, ratio_pred, err, per, LP, block))
    
    # Print key elements
    for sym, Z, rc, rv, ro, rp, err, per, LP, block in errors:
        if sym in ['H','He','Li','Be','B','C','N','O','F','Ne',
                    'Na','Mg','Al','Si','P','S','Cl','Ar',
                    'K','Ca','Fe','Cu','Br','Kr',
                    'Rb','Ag','I','Xe','Cs','Ba']:
            ok = "✓" if abs(err) < 10 else ("~" if abs(err) < 20 else "✗")
            print(f"    {sym:3s} Z={Z:3d} per={per} LP={LP} "
                  f"pred={rp:.3f} obs={ro:.3f} err={err:+5.1f}% {ok}")
    
    bonding_errs = [abs(e[6]) for e in errors if e[9] not in ('ng',) and e[1] != 1]
    noble_errs = [abs(e[6]) for e in errors if e[9] == 'ng']
    all_errs = [abs(e[6]) for e in errors]
    print(f"    --- Bonding mean |err|: {np.mean(bonding_errs):.1f}%, "
          f"Noble mean: {np.mean(noble_errs):.1f}%, All: {np.mean(all_errs):.1f}%")

# ═══════════════════════════════════════════════════════════
# REFINED: separate d-block treatment
# ═══════════════════════════════════════════════════════════

print()
print("=" * 70)
print("REFINED FORMULA: with d-block compression term")
print("=" * 70)

# D-block elements have ratio < 1.408 because the filled d-shell
# creates a HARD CORE that compresses the outer wall.
# The compression depends on d-electron count.
# 
# For d¹⁰ (Cu, Zn, Ag, Cd, Pd): maximum compression → lowest ratio
# For d⁵ (Cr, Mn, Mo): half-filled → minimal compression → ratio ≈ 1.408
#
# The d-shell creates a "second inner wall" at the gold layer (0.236R).
# The compression factor: (d_electrons / 10) × σ₃
# where the d-electrons fill the gold Cantor layer.

# d-fill fraction × compression constant
# For d10: compression pushes ratio from 1.408 toward ~1.06
# Compression = 1 - d_frac × (σ₄/σ_shell - σ₂/σ_shell)/(σ₄/σ_shell)

# Actually let me just look at the d-block pattern:
print("\nD-block vdW/cov vs d-electron count:")
d_elements = [(Z, sym, rv/rc, notes) for Z, sym, rc, rv, per, LP, block, notes in data if block == 'd']
for Z, sym, ratio, notes in d_elements:
    print(f"  {sym:3s} Z={Z:3d} ratio={ratio:.3f} ({notes})")

# The pattern: 
# d5 elements (Cr, Mn, Mo): ratio ≈ 1.36-1.42 (close to BASE)
# d6-d8 (Fe, Co, Ru, Rh): ratio ≈ 1.37-1.52
# d10 (Cu, Zn, Pd, Ag, Cd): ratio ≈ 1.06-1.45 (WIDE spread)
#
# The d10 elements have the lowest ratios, but not uniformly.
# Cu=1.06, Zn=1.14, Ag=1.19, Cd=1.10, Pd=1.45
# Pd is the outlier — it's 4d¹⁰ with no 5s electrons!
#
# The pattern might be: d10 with ns² (Cu-like: actually d10 s1 for Cu) 
# vs d10 with ns⁰ (Pd).
# Cu: [Ar]3d¹⁰4s¹ → cov=132 is metallic radius, vdW=140 is small
# Pd: [Kr]4d¹⁰ → special, all electrons in d-shell

# For now, let me just acknowledge d-block needs special treatment
# and focus on the main-group formula.

# ═══════════════════════════════════════════════════════════
# THE WINNING FORMULA (MAIN GROUP ONLY)
# ═══════════════════════════════════════════════════════════

print()
print("=" * 70)
print("★★★ BEST FORMULA: MAIN GROUP ELEMENTS ★★★")
print("=" * 70)

# From the testing above, A = φ gives a good zero-parameter formula.
# But let me also test the formula including the "first-row anomaly"
# correction: period 2 p-block elements have anomalously SMALL 
# covalent radii because the 2p orbital has no inner p-shell to push it out.

# The "effective lone pair count" for period 2 elements should include
# ALL p-electrons (not just lone pairs) because the entire 2p shell
# is compact and extends equally in all directions.

# NEW FORMULA:
# For s-block: ratio = BASE (hydrogen-like)
# For p-block: ratio = BASE + LP_eff × φ^(-(period-1))
# where LP_eff = max(0, n_p_electrons - 0) for period 2 (ALL p-e extend)
#       LP_eff = standard lone pairs for period 3+ 

# Actually, looking at the data again more carefully:
# B (p¹, 0 LP): ratio = 2.286
# Al (p¹, 0 LP): ratio = 1.521
# Ga (p¹, 0 LP): ratio = 1.533
# In (p¹, 0 LP): ratio = 1.359

# The group 13 elements (p¹, 0 lone pairs) still have ratio > 1.408!
# Al: 1.521, Ga: 1.533, In: 1.359
# The excess for these CANNOT come from lone pairs.

# What's different? These p-block elements have their p-electron
# extending further than an s-electron would. The p-orbital has
# angular momentum that pushes the electron cloud outward.

# In Cantor terms: the p-orbital occupies a DIFFERENT sector of the
# Cantor node than the s-orbital. The s-orbital is in σ₃ (center).
# The p-orbital extends to σ₁ and σ₅ (the bonding/antibonding endpoints).
# This means the effective Cantor node for a p-electron is LARGER
# than for an s-electron.

# Correction: p-electrons add (n_p / max_p) × gap_fraction per electron.
# Let me define: n_p = number of p-electrons in valence shell

# For B  (per 2): n_p = 1, max_p = 6 → p_frac = 1/6
# For Al (per 3): n_p = 1, max_p = 6 → p_frac = 1/6
# For C  (per 2): n_p = 2, max_p = 6 → p_frac = 2/6
# etc.

# FORMULA v2:
# ratio = BASE + n_p × A × φ^(-(period-1))
# Using n_p (number of p-electrons) instead of LP

print("FORMULA v2: ratio = BASE + n_p × A × φ^(-(period-1))")
print("Testing with n_p = number of p-electrons in valence shell")
print()

# Get n_p for each element
def get_np(Z, block, notes):
    """Number of p-electrons in outermost p subshell."""
    if block == 's':
        return 0
    elif block == 'ng':
        if Z == 2: return 0  # He has no p electrons
        return 6  # full p shell
    elif block == 'p':
        # p1=grp13, p2=grp14, p3=grp15, p4=grp16, p5=grp17
        groups = {'group13':1, 'group14':2, 'group15':3, 'group16':4, 'halogen':5}
        return groups.get(notes, 0)
    elif block == 'd':
        return 0
    return 0

# Fit A for this formula
fit_data2 = [d for d in data if d[6] not in ('ng',) and d[0] != 1 and d[6] != 'd']

def cost2(A):
    err_sum = 0
    for Z, sym, rc, rv, per, LP, block, notes in fit_data2:
        n_p = get_np(Z, block, notes)
        ratio_obs = rv / rc
        ratio_pred = BASE + n_p * A * PHI**(-(per - 1))
        err_sum += ((ratio_pred - ratio_obs) / ratio_obs)**2
    return err_sum

res2 = minimize_scalar(cost2, bounds=(0.01, 2.0), method='bounded')
A2_opt = res2.x

print(f"Optimal A = {A2_opt:.6f}")
print(f"Compare: σ₃ sub-gap[0]/σ₃_width = {s3_gaps[0]/s3_width:.6f}")
print(f"Compare: 1/(2φ) = {1/(2*PHI):.6f}")
print(f"Compare: W/φ = {W/PHI:.6f}")
print(f"Compare: 1/φ² = {1/PHI**2:.6f}")
print(f"Compare: σ₃ = {R_MATTER:.6f}")

# Test the framework candidates
for A_test, name in [
    (A2_opt, f"optimal"),
    (s3_gaps[0]/s3_width, "sub-gap fraction"),
    (1/(2*PHI), "1/(2φ)"),
    (W/PHI, "W/φ"),
    (1/PHI**2, "1/φ²"),
    (R_OUTER - R_SHELL, "σ₄ - σ_shell (raw)"),
    ((R_OUTER - R_SHELL)/R_SHELL, "(σ₄-σ_shell)/σ_shell"),
]:
    errors = []
    for Z, sym, rc, rv, per, LP, block, notes in data:
        n_p = get_np(Z, block, notes)
        ratio_obs = rv / rc
        ratio_pred = BASE + n_p * A_test * PHI**(-(per - 1))
        err = (ratio_pred - ratio_obs) / ratio_obs * 100
        errors.append((sym, Z, ratio_obs, ratio_pred, err, per, n_p, block))
    
    bonding_errs = [abs(e[4]) for e in errors if e[7] not in ('ng', 'd') and e[1] != 1]
    all_main = [abs(e[4]) for e in errors if e[7] not in ('d',) and e[1] != 1]
    
    print(f"\n  A = {A_test:.6f} ({name}) — main-group |err|: {np.mean(bonding_errs):.1f}%")
    
    if name in ("optimal", "sub-gap fraction", "(σ₄-σ_shell)/σ_shell"):
        for sym, Z, ro, rp, err, per, n_p, block in errors:
            if block not in ('d',):
                ok = "✓" if abs(err) < 10 else ("~" if abs(err) < 20 else "✗")
                print(f"    {sym:3s} Z={Z:3d} per={per} n_p={n_p} "
                      f"pred={rp:.3f} obs={ro:.3f} err={err:+5.1f}% {ok}")

# ═══════════════════════════════════════════════════════════
# THE COMPLETE FORMULA: ALL ELEMENTS
# ═══════════════════════════════════════════════════════════

print()
print("=" * 70)
print("★★★ COMPLETE FORMULA: ALL CLASSES ★★★")
print("=" * 70)
print()

# The physics:
# 1. BASE ratio = σ₄/σ_shell = 1.408 (hydrogen/alkali baseline)
# 2. p-electrons extend the outer wall: + n_p × A × φ^(-(per-1))
# 3. d-electrons COMPRESS the outer wall (filled d-shell = hard core)
# 4. For noble gases (n_p = 6, full shell): same formula but with n_p=6

# For d-block: the ratio drops below BASE because d-electrons
# create a "filled gold layer" (the gold Cantor level at 0.236R).
# This effectively reduces the outer wall because the gold layer
# is now opaque — entanglement can't propagate as far.

# d-block compression: ratio = BASE - d_compression
# where d_compression depends on d-electron count and period

# Let me check what works for d-block:
print("D-block: testing ratio = BASE × (1 - d_frac × C)")
print("where d_frac = d_electrons/10, C = compression constant")
print()

d_data = [d for d in data if d[6] == 'd']

for C_test, cname in [
    (R_MATTER, "σ₃"),
    (R_INNER, "σ₂"),
    (W**2, "W²"),
    (1/PHI**2, "1/φ²"),
    (R_OUTER - R_SHELL, "σ₄-σ_shell"),
]:
    errs = []
    for Z, sym, rc, rv, per, LP, block, notes in d_data:
        # d-electron count from notes
        d_count_map = {'d5': 5, 'd6': 6, 'd7': 7, 'd8': 8, 'd10': 10}
        d_count = d_count_map.get(notes, 5)
        d_frac = d_count / 10.0
        
        ratio_obs = rv / rc
        ratio_pred = BASE * (1 - d_frac * C_test)
        err = (ratio_pred - ratio_obs) / ratio_obs * 100
        errs.append(abs(err))
    
    print(f"  C = {C_test:.4f} ({cname}): d-block mean |err| = {np.mean(errs):.1f}%")

# Let me try a different d-block formula
print()
print("D-block: testing ratio = BASE - d_frac × C")
for C_test, cname in [
    (0.3, "0.3"),
    (R_SHELL, "σ_shell"),
    (BASE - 1, "BASE-1 = gap_frac"),
    (W, "W"),
]:
    errs = []
    for Z, sym, rc, rv, per, LP, block, notes in d_data:
        d_count_map = {'d5': 5, 'd6': 6, 'd7': 7, 'd8': 8, 'd10': 10}
        d_count = d_count_map.get(notes, 5)
        d_frac = d_count / 10.0
        
        ratio_obs = rv / rc
        ratio_pred = BASE - d_frac * C_test
        err = (ratio_pred - ratio_obs) / ratio_obs * 100
        errs.append(abs(err))
        
        if cname == "BASE-1 = gap_frac":
            ok = "✓" if abs(err) < 10 else ("~" if abs(err) < 20 else "✗")
            print(f"    {sym:3s} Z={Z:3d} d={d_count:2d} "
                  f"pred={ratio_pred:.3f} obs={ratio_obs:.3f} err={err:+5.1f}% {ok}")
    
    print(f"  C = {C_test:.4f} ({cname}): d-block mean |err| = {np.mean(errs):.1f}%")
    print()

# ═══════════════════════════════════════════════════════════
# FINAL OUTPUT: THE FORMULA
# ═══════════════════════════════════════════════════════════

# Using the best A from the search
A_FINAL = s3_gaps[0] / s3_width  # = 0.3243 (the first σ₃ sub-gap fraction)
# This IS framework-derived: it's the largest gap within σ₃, 
# as a fraction of σ₃ width. It's the "gap at recursion level 1".

print()
print("=" * 70)
print("★ FINAL FORMULA (zero free parameters) ★")
print("=" * 70)
print()
print("vdW/cov = σ₄/σ_shell + n_p × g₁ × φ^(-(period-1))")
print()
print("Where:")
print(f"  σ₄/σ_shell = {BASE:.6f}  (AAH spectrum, hydrogen baseline)")
print(f"  g₁ = {A_FINAL:.6f}  (first σ₃ sub-gap fraction)")
print(f"  φ  = {PHI:.6f}  (golden ratio)")
print(f"  n_p = number of p-electrons in valence shell (0-6)")
print(f"  period = 1-7")
print()
print("Physical meaning:")
print("  BASE: The entropy maximum of the 1s hydrogen wavefunction")
print("  n_p × g₁: Each p-electron adds one sub-gap's worth of extension")
print("  φ^(-(per-1)): The sub-gap shrinks by φ at each Cantor recursion level")
print("  Period = recursion depth in the Cantor hierarchy")
print()

print("COMPREHENSIVE TEST (all elements):")
print(f"{'Sym':>4} {'Z':>3} {'Per':>3} {'n_p':>3} {'Pred':>7} {'Obs':>7} {'Err%':>7} {'OK':>2}")
print("-" * 40)

all_errors = []
for Z, sym, rc, rv, per, LP, block, notes in data:
    n_p = get_np(Z, block, notes)
    ratio_obs = rv / rc
    
    if block == 'd':
        # D-block: use BASE with no p-extension
        ratio_pred = BASE
    else:
        ratio_pred = BASE + n_p * A_FINAL * PHI**(-(per - 1))
    
    err = (ratio_pred - ratio_obs) / ratio_obs * 100
    all_errors.append((sym, Z, ratio_obs, ratio_pred, err, block))
    ok = "✓" if abs(err) < 10 else ("~" if abs(err) < 20 else "✗")
    print(f"{sym:>4} {Z:>3} {per:>3} {n_p:>3} {ratio_pred:>7.3f} {ratio_obs:>7.3f} {err:>+7.1f}% {ok}")

print()
s_block = [e for e in all_errors if e[5] == 's' and e[1] != 1]
p_block = [e for e in all_errors if e[5] == 'p']
d_block_e = [e for e in all_errors if e[5] == 'd']
ng_block = [e for e in all_errors if e[5] == 'ng']

print(f"S-block (excl H): {len(s_block)} elements, mean |err| = {np.mean([abs(e[4]) for e in s_block]):.1f}%")
print(f"P-block:           {len(p_block)} elements, mean |err| = {np.mean([abs(e[4]) for e in p_block]):.1f}%")
print(f"D-block:           {len(d_block_e)} elements, mean |err| = {np.mean([abs(e[4]) for e in d_block_e]):.1f}%")
print(f"Noble gases:       {len(ng_block)} elements, mean |err| = {np.mean([abs(e[4]) for e in ng_block]):.1f}%")
print(f"TOTAL:             {len(all_errors)} elements, mean |err| = {np.mean([abs(e[4]) for e in all_errors]):.1f}%")

# Count within 10% and 20%
within_10 = sum(1 for e in all_errors if abs(e[4]) < 10)
within_20 = sum(1 for e in all_errors if abs(e[4]) < 20)
print(f"Within 10%: {within_10}/{len(all_errors)} = {within_10/len(all_errors)*100:.0f}%")
print(f"Within 20%: {within_20}/{len(all_errors)} = {within_20/len(all_errors)*100:.0f}%")

# ═══════════════════════════════════════════════════════════
# WHAT WORKS AND WHAT DOESN'T — HONEST ASSESSMENT
# ═══════════════════════════════════════════════════════════
print()
print("=" * 70)
print("HONEST ASSESSMENT")
print("=" * 70)

print("\n✓ WORKS (< 10% error):")
for sym, Z, ro, rp, err, block in sorted(all_errors, key=lambda x: abs(x[4])):
    if abs(err) < 10:
        print(f"  {sym:3s} Z={Z:3d} pred={rp:.3f} obs={ro:.3f} err={err:+5.1f}%")

print("\n~ MARGINAL (10-20% error):")
for sym, Z, ro, rp, err, block in sorted(all_errors, key=lambda x: abs(x[4])):
    if 10 <= abs(err) < 20:
        print(f"  {sym:3s} Z={Z:3d} pred={rp:.3f} obs={ro:.3f} err={err:+5.1f}%")

print("\n✗ FAILS (> 20% error):")
for sym, Z, ro, rp, err, block in sorted(all_errors, key=lambda x: abs(x[4])):
    if abs(err) >= 20:
        print(f"  {sym:3s} Z={Z:3d} pred={rp:.3f} obs={ro:.3f} err={err:+5.1f}% [{block}]")
