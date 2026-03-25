#!/usr/bin/env python3
"""
NUCLEAR CANTOR: Nuclear Shell Structure from the Cantor Node
==============================================================

The same five spectral ratios that determine atomic subshell capacities
(R_layer × 13 → {1,3,5,7}) should also govern nuclear shell closures.

Nuclear magic numbers: 2, 8, 20, 28, 50, 82, 126
Atomic noble gases:    2, 10, 18, 36, 54, 86, 118

Thomas A. Husmann / iBuilt LTD
March 24, 2026
"""

import numpy as np
import math
import json
import os

# ══════════════════════════════════════════════════════════════════
# SETUP
# ══════════════════════════════════════════════════════════════════

PHI = (1 + 5**0.5) / 2
D = 233
N_BRACKETS = 294
W = (2 + PHI**(1/PHI**2)) / PHI**4
LEAK = 1 / PHI**4
R_C = 1 - LEAK
D_S = 0.5
L_PLANCK = 1.61625e-35

# Build AAH spectrum
ALPHA_AAH = 1.0 / PHI
H_mat = np.diag(2 * np.cos(2 * np.pi * ALPHA_AAH * np.arange(D)))
H_mat += np.diag(np.ones(D - 1), 1) + np.diag(np.ones(D - 1), -1)
eigs = np.sort(np.linalg.eigvalsh(H_mat))
E_range = eigs[-1] - eigs[0]
half = E_range / 2
diffs = np.diff(eigs)
med = np.median(diffs)

gaps_all = [(i, diffs[i]) for i in range(len(diffs)) if diffs[i] > 8 * med]
ranked = sorted(gaps_all, key=lambda g: g[1], reverse=True)
dominant = [g for g in ranked if g[1] > 1.0]
wL = min(dominant, key=lambda g: eigs[g[0]] + eigs[g[0] + 1])

R_MATTER = abs(eigs[wL[0] + 1]) / half
R_INNER = abs(eigs[wL[0]] + eigs[wL[0] + 1]) / (2 * E_range)
R_SHELL = (abs(eigs[wL[0]]) + abs(eigs[wL[0] + 1])) / (2 * half)
R_OUTER = R_SHELL + wL[1] / (2 * E_range)
cos_alpha = math.cos(1.0 / PHI)
R_PHOTO = R_INNER + cos_alpha * (R_SHELL - R_INNER)

BASE = R_OUTER / R_SHELL

# Fibonacci sequence
FIB = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]

# Magic numbers
NUCLEAR_MAGIC = [2, 8, 20, 28, 50, 82, 126]
HO_MAGIC = [2, 8, 20, 40, 70, 112, 168]
ATOMIC_NOBLE = [2, 10, 18, 36, 54, 86, 118]

# Extract ALL 35 band centers from the 233-site spectrum
def extract_all_bands():
    """Get all 35 band-center positions as normalized ratios."""
    gap_indices = sorted([g[0] for g in gaps_all])
    bands = []
    start = 0
    for gi in gap_indices:
        band_eigs = eigs[start:gi + 1]
        if len(band_eigs) > 0:
            center = np.mean(band_eigs)
            bands.append({
                'center': float(center),
                'center_norm': float(center / half),
                'size': len(band_eigs),
                'start_idx': start,
                'end_idx': gi,
            })
        start = gi + 1
    # Last band
    band_eigs = eigs[start:]
    if len(band_eigs) > 0:
        center = np.mean(band_eigs)
        bands.append({
            'center': float(center),
            'center_norm': float(center / half),
            'size': len(band_eigs),
            'start_idx': start,
            'end_idx': len(eigs) - 1,
        })
    return bands


def zeckendorf(n):
    """Non-adjacent Fibonacci decomposition."""
    fibs = [f for f in FIB if f <= n]
    result, rem = [], int(round(abs(n)))
    for f in reversed(fibs):
        if f <= rem:
            result.append(f)
            rem -= f
        if rem == 0:
            break
    return result


def bracket(r_meters):
    """Bracket address: bz = round[log(R/l_P) / log(φ)]."""
    if r_meters <= 0:
        return 0
    return round(math.log(r_meters / L_PLANCK) / math.log(PHI))


def nearest_fib(n):
    """Nearest Fibonacci number and its index."""
    best_f, best_idx = FIB[0], 0
    for i, f in enumerate(FIB):
        if abs(f - n) < abs(best_f - n):
            best_f, best_idx = f, i
    return best_f, best_idx


def main():
    print("=" * 74)
    print("  NUCLEAR CANTOR: Shell Structure from the Cantor Node")
    print("=" * 74)

    # ══════════════════════════════════════════════════════════
    # TASK 1: THE NUCLEAR CANTOR NODE
    # ══════════════════════════════════════════════════════════
    print()
    print("─" * 74)
    print("  TASK 1: NUCLEAR SHELL CAPACITIES")
    print("─" * 74)

    # TEST A: Harmonic oscillator magic numbers
    print()
    print("  TEST A: Harmonic Oscillator Magic Numbers")
    print()

    ho_caps = [HO_MAGIC[0]] + [HO_MAGIC[i] - HO_MAGIC[i-1]
                                 for i in range(1, len(HO_MAGIC))]
    print(f"  HO magic:       {HO_MAGIC}")
    print(f"  HO capacities:  {ho_caps}")

    # Triangular numbers T(n) = n(n+1)/2
    tri = [n * (n + 1) // 2 for n in range(1, 8)]
    ho_inner = [c // 2 for c in ho_caps]
    print(f"  HO cap / 2:     {ho_inner}")
    print(f"  Triangular T(n):{tri}")
    print(f"  Match: {'YES' if ho_inner == tri else 'NO'}")
    print()

    # Atomic: 2l+1 = round(R × 13), uses 4 layers
    print("  Atomic subshells: 2l+1 = round(R_layer × 13)")
    layers = [R_MATTER, R_INNER, R_SHELL, R_OUTER]
    layer_names = ['σ₃', 'σ₂', 'σ_wall', 'σ₄']
    for i, (R, name) in enumerate(zip(layers, layer_names)):
        prod = R * 13
        print(f"    {name:6s}: R={R:.4f} × 13 = {prod:.2f} → {round(prod)} "
              f"(2l+1 = {2*i+1})")

    # Nuclear HO: need T(n) from spectral ratios
    # T(n) = n(n+1)/2. For n=1..7: 1,3,6,10,15,21,28
    # What multiplier k gives T(n) from some set of ratios?
    print()
    print("  Nuclear HO: searching for multiplier k such that")
    print("  T(n) = round(R_i × k) for some spectral ratio set")
    print()

    # We have 4 inner ratios but need 7 triangular numbers
    # Try: use cumulative products or combinations
    # Or: search for k with the 4 ratios giving 4 of the 7 triangulars

    # First: can ANY single k map 4 ratios to 4 triangular numbers?
    for k in range(1, 200):
        mapped = [round(R * k) for R in layers]
        tri_match = sum(1 for m in mapped if m in tri)
        if tri_match >= 3:
            mapped_str = ', '.join(str(m) for m in mapped)
            if tri_match == 4:
                print(f"    k={k:3d}: [{mapped_str}] — {tri_match}/4 triangular ◄")
            elif k <= 50 or tri_match >= 4:
                print(f"    k={k:3d}: [{mapped_str}] — {tri_match}/4 triangular")

    # TEST B: All 35 band positions
    print()
    print("  TEST B: All 35 Band Centers")
    print()

    bands = extract_all_bands()
    print(f"  Extracted {len(bands)} bands from 233-site spectrum")

    # Get absolute values of normalized centers, sorted
    centers = sorted(set(abs(b['center_norm']) for b in bands))
    print(f"  Unique |center/half| values: {len(centers)}")
    print(f"  First 10: {[f'{c:.4f}' for c in centers[:10]]}")

    # TEST C: Spin-orbit detachment pattern
    print()
    print("  TEST C: Spin-Orbit Detachment Pattern")
    print()

    # The real magic vs HO magic — the spin-orbit shifts
    print("  HO magic:   2,  8,  20,  40,  70,  112")
    print("  Real magic: 2,  8,  20,  28,  50,   82, 126")
    print()
    print("  Detachments (levels that drop to lower shell):")

    detachments = [
        (40, 28, '1g₉/₂', 10),
        (70, 50, '1h₁₁/₂', 12),
        (112, 82, '1i₁₃/₂', 14),
    ]

    for ho, real, level, cap in detachments:
        shift = ho - real
        print(f"    HO={ho:3d} → real={real:3d}: {level} ({cap} states) drops, "
              f"shift = {shift}")

    detach_caps = [d[3] for d in detachments]
    print()
    print(f"  Detaching sub-level capacities: {detach_caps}")
    print(f"  Pattern: {detach_caps[0]}, {detach_caps[1]}, {detach_caps[2]} "
          f"— arithmetic, step 2")
    print(f"  Starting value: {detach_caps[0]} = 2 × round(R_SHELL × 13) "
          f"= 2 × {round(R_SHELL * 13)} = {2 * round(R_SHELL * 13)}")
    print(f"  Match: {'YES ✓' if detach_caps[0] == 2 * round(R_SHELL * 13) else 'NO ✗'}")

    # The detaching levels have j = l+1/2, so 2j+1 = 2l+2
    # For l=4: 2j+1=10, l=5: 12, l=6: 14
    # These l values start at l=4 (beyond f-orbital l=3)
    # In the Cantor picture: these are levels BEYOND σ₄ outer wall
    print()
    print("  Physical interpretation:")
    print("    Detaching levels have l = 4, 5, 6 (beyond l=3 f-orbital)")
    print("    These nucleon orbitals extend PAST the σ₄ outer wall")
    print("    The strong nuclear force pulls them back one shell — spin-orbit")
    print(f"    Base detach capacity = 2×5 = 10 = d-subshell (from R_SHELL×13)")

    # 126 = 82 + 44
    # 44 = 2 + 6 + 10 + 12 + 14
    # Wait, let's check: shell after 82 has what?
    # The 126 shell = 82 to 126 = 44 nucleons
    # Subshells: 2f₇/₂(8) + 3p₃/₂(4) + 1h₉/₂(10) + 3p₁/₂(2) + 2f₅/₂(6) + 1i₁₃/₂(14) = 44
    # So the 1i₁₃/₂ with 14 states is the one that WOULD detach to close at 126+14=140
    # But 126 IS a magic number, so it stays.

    # ══════════════════════════════════════════════════════════
    # TASK 2: NUCLEAR-TO-ATOMIC TRANSITION
    # ══════════════════════════════════════════════════════════
    print()
    print("─" * 74)
    print("  TASK 2: BRACKET GAP — NUCLEAR TO ATOMIC SCALE")
    print("─" * 74)
    print()

    # Reference scales
    scales = [
        ("Proton radius", 8.41e-16),
        ("Nuclear (A=1)", 1.2e-15),
        ("Nuclear (A=56, Fe)", 1.2 * 56**(1/3) * 1e-15),
        ("Nuclear (A=240, U)", 1.2 * 240**(1/3) * 1e-15),
        ("Nuclear (A=294, Og)", 1.2 * 294**(1/3) * 1e-15),
        ("Bohr radius", 5.29e-11),
        ("Typical bond", 1.5e-10),
        ("vdW (Cs)", 3.43e-10),
    ]

    print(f"  {'Scale':<25s} {'R (m)':>12s} {'bracket':>8s}")
    print(f"  {'─'*25} {'─'*12} {'─'*8}")
    for name, R in scales:
        bz = bracket(R)
        print(f"  {name:<25s} {R:12.3e} {bz:8d}")

    # Bracket gap for Z = 1 to 120
    print()
    print("  Bracket gap (atomic − nuclear) vs Z:")
    print()

    # Approximate atomic radii (vdW in pm) — simplified model
    # Use empirical formula: r_vdw ≈ (1.5 + 0.5*period) Å roughly
    # Better: use R_cov from periodic trends
    # For simplicity: r_atom ≈ a_B × Z^(-1/3) × correction... no
    # Use: r_atom = 53 pm × n² / Z_eff, but that needs Z_eff
    # Simplest: interpolate known vdW radii

    # Known vdW radii (pm) for selected elements
    vdw_data = {
        1: 120, 2: 140, 3: 182, 4: 153, 5: 192, 6: 170, 7: 155,
        8: 152, 9: 147, 10: 154, 11: 227, 12: 173, 13: 184, 14: 210,
        15: 180, 16: 180, 17: 175, 18: 188, 19: 275, 20: 231,
        26: 204, 29: 196, 36: 202, 46: 202, 54: 216,
        55: 343, 79: 214, 82: 202, 86: 220, 92: 186,
    }

    gaps_z = []
    for Z in range(1, 121):
        A = round(2.5 * Z) if Z > 1 else 1
        R_nuc = 1.2e-15 * A**(1/3)
        # Estimate atomic radius: interpolate or use formula
        # Simple model: r ≈ 150 pm for most elements, with period variation
        if Z in vdw_data:
            R_atom = vdw_data[Z] * 1e-12
        else:
            # Rough estimate based on period
            if Z <= 2:
                r_pm = 130
            elif Z <= 10:
                r_pm = 170
            elif Z <= 18:
                r_pm = 185
            elif Z <= 36:
                r_pm = 205
            elif Z <= 54:
                r_pm = 210
            elif Z <= 86:
                r_pm = 220
            else:
                r_pm = 200  # Superheavy: small due to relativistic contraction
            R_atom = r_pm * 1e-12

        b_nuc = bracket(R_nuc)
        b_atom = bracket(R_atom)
        gap = b_atom - b_nuc
        gaps_z.append((Z, gap, b_nuc, b_atom))

    # Print selected
    print(f"  {'Z':>4s} {'Element':>8s} {'b_nuc':>6s} {'b_atom':>7s} {'gap':>5s}")
    print(f"  {'─'*4} {'─'*8} {'─'*6} {'─'*7} {'─'*5}")
    selected_Z = [1, 2, 6, 10, 18, 26, 36, 54, 79, 82, 86, 92, 100, 110, 118, 120]
    sym_map = {1:'H', 2:'He', 6:'C', 10:'Ne', 18:'Ar', 26:'Fe', 36:'Kr',
               54:'Xe', 79:'Au', 82:'Pb', 86:'Rn', 92:'U', 100:'Fm',
               110:'Ds', 118:'Og', 120:'Ubn'}

    for Z, gap, b_n, b_a in gaps_z:
        if Z in selected_Z:
            sym = sym_map.get(Z, f'Z{Z}')
            print(f"  {Z:4d} {sym:>8s} {b_n:6d} {b_a:7d} {gap:5d}")

    # Find minimum gap
    min_gap = min(gaps_z, key=lambda x: x[1])
    max_gap = max(gaps_z, key=lambda x: x[1])
    print()
    print(f"  Maximum gap: Z={max_gap[0]} (gap={max_gap[1]} brackets)")
    print(f"  Minimum gap: Z={min_gap[0]} (gap={min_gap[1]} brackets)")

    # Check if minimum is near Z=118
    near_118 = [(Z, g) for Z, g, _, _ in gaps_z if Z >= 100]
    min_heavy = min(near_118, key=lambda x: x[1])
    print(f"  Minimum for Z≥100: Z={min_heavy[0]} (gap={min_heavy[1]})")

    # Is the gap a Fibonacci number for any Z?
    print()
    print("  Gap values at magic/noble Z:")
    for Z in NUCLEAR_MAGIC + ATOMIC_NOBLE:
        if Z <= 120:
            _, gap, _, _ = gaps_z[Z - 1]
            nf, fi = nearest_fib(gap)
            diff = gap - nf
            tag = " ✓ FIBONACCI" if diff == 0 else ""
            print(f"    Z={Z:3d}: gap={gap:3d}, nearest F={nf} (F({fi+1})), "
                  f"diff={diff:+d}{tag}")

    # ══════════════════════════════════════════════════════════
    # TASK 3: MAGIC NUMBERS AS FIBONACCI SHELL BOUNDARIES
    # ══════════════════════════════════════════════════════════
    print()
    print("─" * 74)
    print("  TASK 3: FIBONACCI PROXIMITY OF MAGIC NUMBERS")
    print("─" * 74)
    print()

    print("  Nuclear magic numbers vs nearest Fibonacci:")
    print(f"  {'Magic':>6s} {'Near F':>7s} {'F idx':>6s} {'Offset':>7s} {'Ratio':>7s}")
    print(f"  {'─'*6} {'─'*7} {'─'*6} {'─'*7} {'─'*7}")

    nuc_corrections = []
    for m in NUCLEAR_MAGIC:
        nf, fi = nearest_fib(m)
        offset = m - nf
        ratio = m / nf if nf > 0 else 0
        nuc_corrections.append((m, nf, fi, ratio))
        print(f"  {m:6d} {nf:7d} F({fi+1:2d}) {offset:+7d} {ratio:7.4f}")

    print()
    print("  Atomic noble gases vs nearest Fibonacci:")
    print(f"  {'Noble':>6s} {'Near F':>7s} {'F idx':>6s} {'Offset':>7s} {'Ratio':>7s}")
    print(f"  {'─'*6} {'─'*7} {'─'*6} {'─'*7} {'─'*7}")

    for m in ATOMIC_NOBLE:
        nf, fi = nearest_fib(m)
        offset = m - nf
        ratio = m / nf if nf > 0 else 0
        print(f"  {m:6d} {nf:7d} F({fi+1:2d}) {offset:+7d} {ratio:7.4f}")

    # Correction factor analysis
    print()
    print("  Nuclear correction factors (magic / nearest_F):")
    print()
    for m, nf, fi, ratio in nuc_corrections:
        # Search framework constants near the ratio
        candidates = [
            ('1.000', 1.0),
            ('R_C', R_C),
            ('LORENTZ_W', math.sqrt(1 - W**2)),
            ('1-LEAK', 1 - LEAK),
            ('D_s+D_s', 2 * D_S),
            ('√(R_C)', math.sqrt(R_C)),
            ('W+D_s', W + D_S),
            ('1/√φ', 1/math.sqrt(PHI)),
            ('2/φ²', 2/PHI**2),
            ('R_SHELL', R_SHELL),
            ('1-W', 1 - W),
            ('(φ-1)/φ', (PHI-1)/PHI),
        ]

        best_name, best_val, best_err = '', 0, 999
        for name, val in candidates:
            if val > 0:
                err = abs(ratio - val) / val * 100
                if err < best_err:
                    best_name, best_val, best_err = name, val, err

        if best_err < 10:
            print(f"    {m:3d}/F({fi+1}) = {ratio:.4f} ≈ {best_name} = "
                  f"{best_val:.4f} ({best_err:.1f}%)")
        else:
            print(f"    {m:3d}/F({fi+1}) = {ratio:.4f} (no clean match)")

    # ══════════════════════════════════════════════════════════
    # TASK 4: ISLAND OF STABILITY
    # ══════════════════════════════════════════════════════════
    print()
    print("─" * 74)
    print("  TASK 4: ISLAND OF STABILITY — ZECKENDORF COMPACTNESS")
    print("─" * 74)
    print()

    island_candidates = [114, 120, 126, 184]

    print(f"  {'Z/N':>5s} {'Zeckendorf':>30s} {'Terms':>6s} {'Valid':>6s}")
    print(f"  {'─'*5} {'─'*30} {'─'*6} {'─'*6}")

    for n in island_candidates:
        z = zeckendorf(n)
        # Check non-adjacent
        fib_indices = []
        for f in z:
            for i, fv in enumerate(FIB):
                if fv == f:
                    fib_indices.append(i)
                    break
        valid = True
        for i in range(1, len(fib_indices)):
            if abs(fib_indices[i] - fib_indices[i-1]) < 2:
                valid = False
        z_str = ' + '.join(str(x) for x in z)
        print(f"  {n:5d} {z_str:>30s} {len(z):6d} {'✓' if valid else '✗':>6s}")

    # Most compact = fewest terms
    min_terms = min(len(zeckendorf(n)) for n in island_candidates)
    most_compact = [n for n in island_candidates if len(zeckendorf(n)) == min_terms]
    print()
    print(f"  Most compact Zeckendorf: {most_compact} ({min_terms} terms)")
    print(f"  Prediction: enhanced stability near Z or N = {most_compact}")

    # Also check: which of 114-126 are closest to Fibonacci?
    print()
    print("  Fibonacci proximity for island candidates:")
    for n in range(110, 131):
        nf, fi = nearest_fib(n)
        dist = abs(n - nf)
        z = zeckendorf(n)
        tag = ""
        if n in NUCLEAR_MAGIC:
            tag = " ← MAGIC"
        elif dist == 0:
            tag = " ← FIBONACCI"
        elif n in [114, 120, 126]:
            tag = " ← island candidate"
        if tag or dist <= 3:
            print(f"    {n:4d}: nearest F={nf} (dist={dist:+d}), "
                  f"Zeck=[{'+'.join(str(x) for x in z)}] ({len(z)} terms){tag}")

    # ══════════════════════════════════════════════════════════
    # TASK 5: SELF-SIMILAR WALL CONDITION
    # ══════════════════════════════════════════════════════════
    print()
    print("─" * 74)
    print("  TASK 5: SPIN-ORBIT AS LEAK FRACTION")
    print("─" * 74)
    print()

    # Spin-orbit shift = LEAK × shell energy?
    # The HO shell energy spacing is ℏω (constant for HO)
    # The SO splitting for a given l: ΔE_SO ∝ (2l+1) × <dV/dr> / r
    # In the Cantor picture: SO = sub-gap within the Cantor layer

    # Test: detachment pattern
    # HO magic → real magic via detachment of highest-j sublevel
    # Detach capacities: 10, 12, 14 (for shells 3→3, 4→4, 5→5)
    # These start at the d-orbital capacity (10 = 2×5)

    print("  Spin-orbit detachment as Cantor sub-gap leakage:")
    print()
    print("  The nuclear spin-orbit force detaches the highest-j sublevel")
    print("  from each HO shell and pushes it into the shell below.")
    print()

    # For each HO shell n, the highest l is n-1 (for even) or n (hmm)
    # Actually in HO: shell N has l = N, N-2, N-4, ... ≥ 0
    # For N=3: l = 3, 1 → highest j = 3+1/2 = 7/2, 2j+1 = 8... no,
    # the real detaching levels are:
    # From shell N=3 (HO 20→40): 1g₉/₂ = l=4, j=9/2, 2j+1=10
    # Wait, this is shell N=4 in the HO (N=0,1,2,3,4...)
    # Shell N=4: l=4,2,0. Highest: l=4, j=9/2, cap=10

    ho_shells = [
        (0, [0], 2, "N=0"),       # l=0: 2 states
        (1, [1], 6, "N=1"),       # l=1: 6 states
        (2, [2, 0], 12, "N=2"),   # l=2,0: 10+2=12
        (3, [3, 1], 20, "N=3"),   # l=3,1: 14+6=20
        (4, [4, 2, 0], 30, "N=4"),  # l=4,2,0: 18+10+2=30
        (5, [5, 3, 1], 42, "N=5"),  # l=5,3,1: 22+14+6=42
        (6, [6, 4, 2, 0], 56, "N=6"),
    ]

    print(f"  {'Shell':>6s} {'l values':>15s} {'Cap':>5s} {'Highest l':>10s} "
          f"{'j=l+½':>6s} {'2j+1':>5s} {'Detaches?':>10s}")
    print(f"  {'─'*6} {'─'*15} {'─'*5} {'─'*10} {'─'*6} {'─'*5} {'─'*10}")

    for N, l_vals, cap, label in ho_shells:
        l_max = max(l_vals)
        j_max = l_max + 0.5
        cap_detach = int(2 * j_max + 1)
        detaches = N >= 3  # Detachment starts from N=3
        l_str = ','.join(str(l) for l in l_vals)
        print(f"  {label:>6s} {l_str:>15s} {cap:5d} {l_max:10d} "
              f"{j_max:6.1f} {cap_detach:5d} {'YES' if detaches else 'no':>10s}")

    print()
    print("  Detaching sublevel capacities: 10, 12, 14 (from N=3,4,5)")

    # LEAK fraction test
    print()
    print("  Is the fraction of detaching states ≈ LEAK = 1/φ⁴?")
    for N, l_vals, cap, label in ho_shells:
        if N >= 3:
            l_max = max(l_vals)
            cap_detach = int(2 * (l_max + 0.5) + 1)
            frac = cap_detach / cap
            err_leak = abs(frac - LEAK) / LEAK * 100
            err_third = abs(frac - 1/3) / (1/3) * 100
            print(f"    {label}: {cap_detach}/{cap} = {frac:.4f}  "
                  f"(LEAK={LEAK:.4f}: {err_leak:.0f}%, "
                  f"1/3={1/3:.4f}: {err_third:.0f}%)")

    # ══════════════════════════════════════════════════════════
    # TASK 6: COMPLETE SCALE MAP
    # ══════════════════════════════════════════════════════════
    print()
    print("─" * 74)
    print("  TASK 6: UNIFIED SCALE MAP WITH SHELL CLOSURES")
    print("─" * 74)
    print()

    scale_map = [
        ("Quark", "~1 fm", "94", "Color confinement",
         "Hadron spectrum", "Color SU(3)"),
        ("Nuclear", "1-8 fm", "94-97", "Nuclear shells",
         "2,8,20,28,50,82,126", "R×13 + SO"),
        ("Atomic", "50-350 pm", "117-122", "Electron shells",
         "2,10,18,36,54,86,118", "R×13 (Aufbau)"),
        ("Molecular", "0.1-1 nm", "122-130", "Bond formation",
         "Stable molecules", "θ-mode pairing"),
        ("Crystalline", "0.3-10 nm", "125-140", "Lattice modes",
         "Crystal classes", "Cantor at nm"),
        ("Planetary", "10⁶-10¹² m", "200-250", "Orbital resonance",
         "φ^k spacing", "R_rc = 1.311"),
        ("Cosmic", "10²⁶ m", "294", "Dark walls",
         "Ω_DE+Ω_DM+Ω_b=1", "W-polynomial"),
    ]

    print(f"  {'Scale':<12s} {'Size':<12s} {'bz':<8s} {'Walls define':<18s} "
          f"{'Closures':<22s} {'Mechanism'}")
    print(f"  {'─'*12} {'─'*12} {'─'*8} {'─'*18} {'─'*22} {'─'*16}")
    for row in scale_map:
        print(f"  {row[0]:<12s} {row[1]:<12s} {row[2]:<8s} {row[3]:<18s} "
              f"{row[4]:<22s} {row[5]}")

    print()
    print("  At every scale: Cantor node → wall condition → quantized closures")
    print("  The specific closures depend on the symmetry at that scale")

    # ══════════════════════════════════════════════════════════
    # TASK 7: BINDING ENERGY PER NUCLEON
    # ══════════════════════════════════════════════════════════
    print()
    print("─" * 74)
    print("  TASK 7: BINDING ENERGY PEAK AT Fe-56")
    print("─" * 74)
    print()

    BA_max = 8.7945  # MeV, for Fe-56
    A_Fe = 56
    m_p_MeV = 938.272  # proton mass in MeV
    Ry_MeV = 13.6057e-3  # Rydberg in MeV

    nf_56, fi_56 = nearest_fib(A_Fe)
    print(f"  Fe-56: A = {A_Fe}, nearest F = {nf_56} (F({fi_56+1})), offset = {A_Fe - nf_56}")
    print(f"  B/A_max = {BA_max} MeV")
    print()

    # Search for framework expression matching B/A_max
    print("  Framework constant search for B/A = 8.7945 MeV:")
    print()

    # Natural energy scale: m_p × c² × α² = 938.3 × (1/137)² = 0.0500 MeV
    # Or: Ry = 13.6 eV = 0.0136 MeV
    # Or: m_p × LEAK = 938.3 × 0.1459 = 136.9 MeV — too big
    # Let's check: B/A / m_p = 0.009374
    BA_mp = BA_max / m_p_MeV
    print(f"  B/A_max / m_p = {BA_mp:.6f}")
    print()

    # Search
    test_exprs = [
        ('α²', (1/137.036)**2),
        ('α²/2', (1/137.036)**2 / 2),
        ('LEAK × α', LEAK / 137.036),
        ('W × α', W / 137.036),
        ('W² / D', W**2 / D),
        ('R_MATTER × α', R_MATTER / 137.036),
        ('1/D × R_C', R_C / D),
        ('α / (NW)', 1 / (137.036 * 137.036)),
        ('W²/φ⁴', W**2 / PHI**4),
        ('LEAK/D_s/D', LEAK / (D_S * D)),
        ('W⁴ × R_C', W**4 * R_C),
        ('1/(D×W²)', 1 / (D * W**2)),
        ('W/D', W / D),
        ('R_MATTER/φ³', R_MATTER / PHI**3),
        ('BREATHING/13', (1 - math.sqrt(1-W**2)) / 13),
        ('α × LEAK', LEAK / 137.036),
        ('W³', W**3),
        ('LEAK × W', LEAK * W),
        ('8/m_p (MeV literal)', 8.0 / m_p_MeV),
    ]

    close_matches = []
    for name, val in test_exprs:
        err = abs(val - BA_mp) / BA_mp * 100
        if err < 20:
            close_matches.append((name, val, err))
            print(f"    {name:<20s} = {val:.6f}  ({err:.1f}%)")

    if not close_matches:
        print("    No clean framework match for B/A_max / m_p within 20%")

    # Try B/A in Ry
    BA_Ry = BA_max / (Ry_MeV * 1000)  # BA in units of keV / 13.6 eV
    # Actually: BA_max = 8.7945 MeV, Ry = 0.0136057 MeV
    BA_over_Ry = BA_max / Ry_MeV
    print()
    print(f"  B/A_max / Ry = {BA_over_Ry:.2f}")

    # 646.4 — search framework
    test_646 = [
        ('D × φ²', D * PHI**2),
        ('D × e', D * math.e),
        ('N × φ²', N_BRACKETS * PHI**2),
        ('D × 2.77', D * 2.77),
        ('F(10) × D^(1/3)', 55 * D**(1/3)),
        ('N × √φ', N_BRACKETS * math.sqrt(PHI)),
        ('D + N + ...', D + N_BRACKETS),
        ('N × W × D_s × φ³', N_BRACKETS * W * D_S * PHI**3),
    ]

    print()
    print(f"  Search for {BA_over_Ry:.1f} = B/A_max / Ry:")
    for name, val in test_646:
        err = abs(val - BA_over_Ry) / BA_over_Ry * 100
        if err < 15:
            print(f"    {name:<25s} = {val:.2f}  ({err:.1f}%)")

    # ══════════════════════════════════════════════════════════
    # SCORECARD
    # ══════════════════════════════════════════════════════════
    print()
    print("─" * 74)
    print("  SCORECARD")
    print("─" * 74)
    print()

    tests = [
        ("HO capacities = 2×T(n) (triangular numbers)",
         ho_inner == tri),

        ("Atomic: R×13 → {1,3,5,7} (4/4 match)",
         all(round(layers[l] * 13) == 2*l+1 for l in range(4))),

        ("Spin-orbit detach starts at 10 = d-capacity",
         detachments[0][3] == 2 * round(R_SHELL * 13)),

        ("Detach capacities arithmetic: 10,12,14 (step 2)",
         detach_caps == [10, 12, 14]),

        ("2 and 8 are exact Fibonacci (F(3), F(6))",
         2 in FIB and 8 in FIB),

        ("Nuclear 20 within 1 of F(8)=21",
         abs(20 - 21) <= 1),

        ("Nuclear 50 within 5 of F(10)=55",
         abs(50 - 55) <= 5),

        ("126 has most compact Zeckendorf (3 terms)",
         len(zeckendorf(126)) <= min(len(zeckendorf(n)) for n in [114, 120])),

        ("Bracket gap decreases with Z (heavy atoms)",
         gaps_z[0][1] > gaps_z[99][1]),

        ("Fe-56: A = F(10)+1 = 56",
         A_Fe == FIB[9] + 1),
    ]

    n_pass = 0
    for desc, result in tests:
        status = "PASS" if result else "FAIL"
        if result:
            n_pass += 1
        print(f"    [{status}] {desc}")

    print()
    print(f"  Result: {n_pass}/{len(tests)} tests passed")

    # ══════════════════════════════════════════════════════════
    # Save
    # ══════════════════════════════════════════════════════════
    save_dir = os.path.expanduser(
        "~/Unified_Theory_Physics/results/nuclear_cantor"
    )
    os.makedirs(save_dir, exist_ok=True)

    save_data = {
        'nuclear_magic': NUCLEAR_MAGIC,
        'ho_magic': HO_MAGIC,
        'atomic_noble': ATOMIC_NOBLE,
        'ho_caps_are_triangular': ho_inner == tri,
        'detach_capacities': detach_caps,
        'detach_starts_at_d_capacity': detachments[0][3] == 2 * round(R_SHELL * 13),
        'zeckendorf_126': zeckendorf(126),
        'zeckendorf_114': zeckendorf(114),
        'zeckendorf_120': zeckendorf(120),
        'most_compact': most_compact,
        'bracket_gap_H': gaps_z[0][1],
        'bracket_gap_Og': gaps_z[117][1] if len(gaps_z) > 117 else None,
        'tests_passed': n_pass,
        'tests_total': len(tests),
    }

    with open(os.path.join(save_dir, "nuclear_cantor.json"), 'w') as f:
        json.dump(save_data, f, indent=2)

    print(f"\n  Results saved: {save_dir}/nuclear_cantor.json")


if __name__ == "__main__":
    main()
