"""
hidden_nineteen.py — Sub-sub-band structure within σ₃
======================================================

The σ₃ center band has 55 eigenvalues split by 9 sub-gaps into
10 sub-bands. The Madelung sequence has 19 subshells.

Hypothesis: two-level splitting of the Cantor hierarchy produces
exactly 19 groups matching the Madelung subshell structure.

Thomas A. Husmann / iBuilt LTD / March 2026
"""

import os
import sys
import json
import math
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'CLEAN'))

from core.constants import PHI, D
from core.hamiltonian import build_hamiltonian, diagonalize


# ═══════════════════════════════════════════════════════════════════
# REFERENCE DATA
# ═══════════════════════════════════════════════════════════════════

# Madelung filling order subshell sizes (1s through 7p)
MADELUNG = [2, 2, 6, 2, 6, 2, 10, 6, 2, 10, 6, 2, 14, 10, 6, 2, 14, 10, 6]
MADELUNG_LABELS = [
    '1s', '2s', '2p', '3s', '3p', '4s', '3d', '4p', '5s',
    '4d', '5p', '6s', '4f', '5d', '6p', '7s', '5f', '6d', '7p'
]

FIBS = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377]


def print_header(title):
    print()
    print("─" * 80)
    print(f"  {title}")
    print("─" * 80)


def find_gaps(eigenvalues, threshold_mult):
    """Find gaps where spacing > threshold_mult × median_spacing."""
    diffs = np.diff(eigenvalues)
    med = np.median(diffs)
    if med <= 0:
        return [], diffs, med
    gaps = [(i, diffs[i]) for i in range(len(diffs)) if diffs[i] > threshold_mult * med]
    return sorted(gaps, key=lambda g: g[1], reverse=True), diffs, med


def gaps_to_groups(n_eigs, gap_indices):
    """Convert sorted gap indices to group sizes."""
    boundaries = sorted(gap_indices)
    sizes = []
    prev = 0
    for b in boundaries:
        sizes.append(b - prev + 1)
        prev = b + 1
    sizes.append(n_eigs - prev)
    return sizes


# ═══════════════════════════════════════════════════════════════════
# BUILD SPECTRUM
# ═══════════════════════════════════════════════════════════════════

H = build_hamiltonian()
eigs = diagonalize(H)
E_range = eigs[-1] - eigs[0]

# Find dominant gaps
diffs_all = np.diff(eigs)
med_all = np.median(diffs_all)
all_gaps = [(i, diffs_all[i]) for i in range(len(diffs_all)) if diffs_all[i] > 8 * med_all]
ranked = sorted(all_gaps, key=lambda g: g[1], reverse=True)
dominant = sorted([g for g in ranked if g[1] > 1.0], key=lambda g: g[0])

# Three-band partition
idx_L = dominant[0][0]      # last index of left band
idx_R = dominant[1][0] + 1  # first index of right band
left_eigs = eigs[:idx_L + 1]
center_eigs = eigs[idx_L + 1:idx_R]
right_eigs = eigs[idx_R:]


# ═══════════════════════════════════════════════════════════════════
# TASK 1: TWO-LEVEL PARTITION OF σ₃
# ═══════════════════════════════════════════════════════════════════

def task1_two_level():
    print_header("TASK 1: TWO-LEVEL PARTITION OF σ₃")

    n_center = len(center_eigs)
    print(f"\n  Center band: {n_center} eigenvalues")

    # Level 1: find sub-gaps (4× median threshold)
    gaps_L1, c_diffs, c_med = find_gaps(center_eigs, 4.0)
    n_subgaps = len(gaps_L1)
    gap_indices_L1 = [g[0] for g in gaps_L1]
    L1_sizes = gaps_to_groups(n_center, gap_indices_L1)

    print(f"  Level 1: {n_subgaps} sub-gaps → {len(L1_sizes)} sub-bands")
    print(f"  Sub-band sizes: {L1_sizes}")
    print(f"  Sum: {sum(L1_sizes)}")

    # Level 2: within each sub-band, find the largest internal gap
    # that exceeds 2× the sub-band's own median spacing
    L2_sizes = []
    split_count = 0

    print(f"\n  Level 2: splitting sub-bands with internal gaps > 2× local median")
    for band_idx, size in enumerate(L1_sizes):
        if size <= 2:
            L2_sizes.append(size)
            print(f"    Sub-band {band_idx+1} (size {size}): too small to split → [{size}]")
            continue

        # Extract this sub-band's eigenvalues
        start = sum(L1_sizes[:band_idx])
        band_eigs = center_eigs[start:start + size]
        band_diffs = np.diff(band_eigs)
        band_med = np.median(band_diffs)

        if band_med <= 0:
            L2_sizes.append(size)
            continue

        # Find largest gap exceeding 2× median
        max_gap_idx = np.argmax(band_diffs)
        max_gap_val = band_diffs[max_gap_idx]
        ratio = max_gap_val / band_med

        if ratio > 2.0 and size > 3:
            left_size = max_gap_idx + 1
            right_size = size - left_size
            L2_sizes.extend([left_size, right_size])
            split_count += 1
            print(f"    Sub-band {band_idx+1} (size {size}): gap ratio {ratio:.1f}× "
                  f"→ [{left_size}, {right_size}]")
        else:
            L2_sizes.append(size)
            print(f"    Sub-band {band_idx+1} (size {size}): max ratio {ratio:.1f}× "
                  f"→ no split [{size}]")

    print(f"\n  Level 2 result: {split_count} sub-bands split")
    print(f"  Total groups: {len(L2_sizes)}")
    print(f"  Group sizes:  {L2_sizes}")
    print(f"  Sum: {sum(L2_sizes)}")
    print(f"  Madelung ref: {MADELUNG} ({len(MADELUNG)} subshells, sum {sum(MADELUNG)})")

    return L1_sizes, L2_sizes


# ═══════════════════════════════════════════════════════════════════
# TASK 2: VARY THE GAP THRESHOLD
# ═══════════════════════════════════════════════════════════════════

def task2_threshold_sweep():
    print_header("TASK 2: GAP THRESHOLD SWEEP")

    c_diffs = np.diff(center_eigs)
    c_med = np.median(c_diffs)

    print(f"\n  Center band median spacing: {c_med:.6f}")
    print(f"  Center band max spacing:    {np.max(c_diffs):.6f}")
    print(f"  Ratio max/med:              {np.max(c_diffs)/c_med:.1f}×")

    print(f"\n  {'Threshold':>10s}  {'Gaps':>5s}  {'Groups':>7s}  {'Group sizes'}")
    print(f"  {'─'*10}  {'─'*5}  {'─'*7}  {'─'*40}")

    for T in [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0, 8.0, 10.0, 15.0, 20.0, 30.0]:
        gaps, _, _ = find_gaps(center_eigs, T)
        n_gaps = len(gaps)
        if n_gaps > 0:
            sizes = gaps_to_groups(len(center_eigs), [g[0] for g in gaps])
        else:
            sizes = [len(center_eigs)]
        marker = ""
        if n_gaps == 9:
            marker = " ◄── 10 sub-bands"
        elif n_gaps == 18:
            marker = " ◄── 19 groups!"
        elif n_gaps == 19:
            marker = " ◄── 20 groups"
        print(f"  {T:>10.1f}×  {n_gaps:>5d}  {len(sizes):>7d}  {sizes}{marker}")

    # Also: print sorted gap widths to see natural clustering
    print(f"\n  All spacings in center band (sorted, top 20):")
    sorted_diffs = np.sort(c_diffs)[::-1]
    for i, d in enumerate(sorted_diffs[:20]):
        ratio = d / c_med
        marker = "  ◄ dominant" if ratio > 10 else "  ◄ sub-gap" if ratio > 4 else ""
        print(f"    {i+1:>3d}: {d:.6f}  ({ratio:>5.1f}× median){marker}")


# ═══════════════════════════════════════════════════════════════════
# TASK 3: ZECKENDORF BOUNDARIES
# ═══════════════════════════════════════════════════════════════════

def task3_zeckendorf():
    print_header("TASK 3: ZECKENDORF BOUNDARIES")

    def zeckendorf(n):
        fibs = [f for f in FIBS if f <= n and f > 0]
        result = []
        rem = n
        for f in reversed(fibs):
            if f <= rem:
                result.append(f)
                rem -= f
            if rem == 0:
                break
        return result

    def has_consecutive_fibs(n):
        """Check if Zeckendorf representation requires consecutive Fibonacci numbers."""
        zeck = zeckendorf(n)
        fib_indices = []
        for z in zeck:
            if z in FIBS:
                fib_indices.append(FIBS.index(z))
        fib_indices.sort()
        for i in range(len(fib_indices) - 1):
            if fib_indices[i+1] - fib_indices[i] == 1:
                return True
        return False

    # All numbers 1-55 with their Zeckendorf representations
    print(f"\n  Zeckendorf representations for 1-55:")

    # Numbers whose Zeckendorf decomposition contains consecutive Fibonacci indices
    # (these are NOT forbidden — Zeckendorf guarantees non-consecutive)
    # Instead: check which numbers CANNOT be written as non-consecutive sums
    # Actually Zeckendorf theorem says EVERY positive integer has a unique
    # representation as sum of non-consecutive Fibonacci numbers.
    # So no number is "forbidden" in Zeckendorf.

    # What IS interesting: the gap positions within the 55 eigenvalues
    # correspond to eigenvalue indices. Let's check if gap positions
    # are at Fibonacci-index positions.

    gaps_L1, _, _ = find_gaps(center_eigs, 4.0)
    gap_positions = sorted([g[0] for g in gaps_L1])

    print(f"\n  Sub-gap positions (indices within 55-eigenvalue center band):")
    print(f"    Positions: {gap_positions}")
    print(f"    1-indexed:  {[g+1 for g in gap_positions]}")

    # Check if gap positions are near Fibonacci numbers
    print(f"\n  Gap position vs nearest Fibonacci:")
    fib_set = set(FIBS)
    for pos in gap_positions:
        pos1 = pos + 1  # 1-indexed
        nearest = min(FIBS, key=lambda f: abs(f - pos1))
        is_fib = pos1 in fib_set
        diff = pos1 - nearest
        print(f"    Position {pos1:>3d}  nearest F = {nearest:>3d}  "
              f"diff = {diff:>+3d}  {'✓ FIBONACCI' if is_fib else ''}")

    # Zeckendorf addresses of gap positions
    print(f"\n  Zeckendorf addresses of gap positions:")
    for pos in gap_positions:
        zeck = zeckendorf(pos + 1)
        print(f"    Position {pos+1:>3d}: {' + '.join(str(z) for z in zeck)}")

    # Count how many gap positions are Fibonacci
    n_fib = sum(1 for p in gap_positions if (p+1) in fib_set)
    print(f"\n  {n_fib}/{len(gap_positions)} gap positions are Fibonacci numbers")

    return gap_positions


# ═══════════════════════════════════════════════════════════════════
# TASK 4: FULL 233-EIGENVALUE PARTITION
# ═══════════════════════════════════════════════════════════════════

def task4_full_partition():
    print_header("TASK 4: FULL 233-EIGENVALUE PARTITION")

    # Sort all gaps by width
    all_spacings = np.diff(eigs)
    sorted_gap_indices = np.argsort(all_spacings)[::-1]

    # 18-group partition (19 groups from 18 largest gaps)
    print(f"\n  a) 19-group partition (18 largest gaps):")
    top18 = sorted_gap_indices[:18].tolist()
    sizes_19 = gaps_to_groups(233, top18)
    print(f"     Sizes: {sizes_19}")
    print(f"     Sum: {sum(sizes_19)}")

    # 34-group partition (33 largest gaps → 34 groups)
    print(f"\n  b) 34-group partition (33 largest gaps = F(9)-1):")
    top33 = sorted_gap_indices[:33].tolist()
    sizes_34 = gaps_to_groups(233, top33)
    print(f"     Sizes: {sizes_34}")
    print(f"     Sum: {sum(sizes_34)}")

    # Natural gaps at 4× median
    print(f"\n  c) Natural partition (gaps > 4× median):")
    med = np.median(all_spacings)
    natural_gaps = [i for i in range(len(all_spacings)) if all_spacings[i] > 4 * med]
    sizes_nat = gaps_to_groups(233, natural_gaps)
    print(f"     Threshold: 4× median = {4*med:.6f}")
    print(f"     Gaps found: {len(natural_gaps)}")
    print(f"     Groups: {len(sizes_nat)}")
    print(f"     Sizes: {sizes_nat}")
    print(f"     Sum: {sum(sizes_nat)}")

    # Natural gaps at 8× median (the standard threshold)
    natural_gaps_8 = [i for i in range(len(all_spacings)) if all_spacings[i] > 8 * med]
    sizes_nat8 = gaps_to_groups(233, natural_gaps_8)
    print(f"\n  d) Standard partition (gaps > 8× median):")
    print(f"     Gaps found: {len(natural_gaps_8)}")
    print(f"     Groups: {len(sizes_nat8)}")
    print(f"     Sizes: {sizes_nat8}")

    # Compare to Madelung
    mad_sorted = sorted(MADELUNG)
    print(f"\n  Madelung (sorted): {mad_sorted}")
    print(f"  19-group (sorted): {sorted(sizes_19)}")

    # Compare sorted group sizes
    print(f"\n  Comparison: 19-group vs Madelung")
    print(f"  {'Madelung':>10s}  {'19-group':>10s}")
    for m, g in zip(sorted(MADELUNG, reverse=True), sorted(sizes_19, reverse=True)):
        print(f"  {m:>10d}  {g:>10d}")

    return sizes_19, sizes_34, sizes_nat


# ═══════════════════════════════════════════════════════════════════
# TASK 5: OUTER BAND RECURSION
# ═══════════════════════════════════════════════════════════════════

def task5_outer_bands():
    print_header("TASK 5: HIERARCHICAL RECURSION WITHIN OUTER BANDS")

    for name, band_eigs in [("Left (σ₁)", left_eigs), ("Right (σ₅)", right_eigs)]:
        n = len(band_eigs)
        print(f"\n  {name}: {n} eigenvalues")

        for T in [4.0, 6.0, 8.0]:
            gaps, _, med = find_gaps(band_eigs, T)
            if gaps:
                sizes = gaps_to_groups(n, [g[0] for g in gaps])
            else:
                sizes = [n]
            print(f"    {T:.0f}× threshold: {len(gaps)} gaps → {len(sizes)} sub-bands  {sizes}")

    # Combined outer bands
    both_outer = np.concatenate([left_eigs, right_eigs])
    both_outer.sort()
    print(f"\n  Combined outer (σ₁+σ₅): {len(both_outer)} eigenvalues")
    # Note: these are NOT contiguous — there's a huge gap between them
    # So sub-gaps within each are what matter, not combined


# ═══════════════════════════════════════════════════════════════════
# TASK 6: σ₂ + σ₃ + σ₄ PARTITION
# ═══════════════════════════════════════════════════════════════════

def task6_atomic_sectors():
    print_header("TASK 6: THE σ₂ + σ₃ + σ₄ PARTITION")

    # The five-sector model: find the 4 largest gaps → 5 sectors
    all_spacings = np.diff(eigs)
    sorted_indices = np.argsort(all_spacings)[::-1]

    # Top 4 gaps → 5 sectors
    top4 = sorted(sorted_indices[:4].tolist())
    sector_sizes_5 = gaps_to_groups(233, top4)
    print(f"\n  5-sector partition (4 largest gaps):")
    print(f"    Sector sizes: {sector_sizes_5}")
    print(f"    Sum: {sum(sector_sizes_5)}")

    # The two dominant gaps split into 3 bands (89|55|89)
    # Additional gaps split further
    # Top 4 includes the 2 dominant gaps plus 2 more
    print(f"\n  Top 4 gap positions: {top4}")
    print(f"  Top 4 gap widths: {[f'{all_spacings[i]:.4f}' for i in top4]}")

    # Identify which sectors are σ₁, σ₂, σ₃, σ₄, σ₅
    # σ₃ is the central sector (around E=0)
    # Label sectors by their mean eigenvalue
    sectors = []
    prev = 0
    for boundary in top4:
        sector_eigs = eigs[prev:boundary + 1]
        sectors.append(sector_eigs)
        prev = boundary + 1
    sectors.append(eigs[prev:])

    print(f"\n  Sector identification:")
    for i, sec in enumerate(sectors):
        label = f"σ{i+1}"
        mean_e = np.mean(sec)
        print(f"    {label}: {len(sec):>3d} eigenvalues, "
              f"E ∈ [{sec[0]:>7.3f}, {sec[-1]:>7.3f}], mean = {mean_e:>7.3f}")

    # The 'atomic' sectors (central three): σ₂ + σ₃ + σ₄
    # With 5-sector partition from top-4 gaps
    if len(sectors) >= 5:
        atomic_eigs = np.concatenate(sectors[1:4])
        n_atomic = len(atomic_eigs)
        dark_eigs_count = len(sectors[0]) + len(sectors[4])
    else:
        # Fallback: use center band
        atomic_eigs = center_eigs
        n_atomic = len(atomic_eigs)
        dark_eigs_count = 233 - n_atomic

    print(f"\n  Atomic sectors (σ₂+σ₃+σ₄): {n_atomic} eigenvalues")
    print(f"  Dark sectors (σ₁+σ₅):      {dark_eigs_count} eigenvalues")
    print(f"  Compare: Z_max = 118, D×D_s = 116.5")

    # Sub-gaps within atomic sectors
    if n_atomic > 2:
        atomic_sorted = np.sort(atomic_eigs)
        for T in [2.0, 3.0, 4.0, 6.0, 8.0]:
            gaps, _, _ = find_gaps(atomic_sorted, T)
            if gaps:
                sizes = gaps_to_groups(n_atomic, [g[0] for g in gaps])
            else:
                sizes = [n_atomic]
            marker = " ◄── 19 groups!" if len(sizes) == 19 else ""
            print(f"    {T:.0f}× threshold: {len(gaps)} gaps → {len(sizes)} groups{marker}")
            if len(sizes) <= 25:
                print(f"      Sizes: {sizes}")

    return sector_sizes_5, n_atomic


# ═══════════════════════════════════════════════════════════════════
# TASK 7: RAW SUMMARY
# ═══════════════════════════════════════════════════════════════════

def task7_raw_summary(L1_sizes, L2_sizes, sizes_19, sizes_34, sizes_nat,
                       sector_sizes_5, n_atomic):
    print_header("TASK 7: RAW SUMMARY — ALL PARTITIONS")

    partitions = {
        '5-sector (4 gaps)': sector_sizes_5,
        'σ₃ 10-sub-band (L1)': L1_sizes,
        'σ₃ two-level (L2)': L2_sizes,
        'Full 233, 19-group': sizes_19,
        'Full 233, 34-group': sizes_34,
        'Full 233, natural': sizes_nat,
        'Madelung reference': MADELUNG,
    }

    for name, sizes in partitions.items():
        print(f"\n  {name}:")
        print(f"    Groups: {len(sizes)}")
        print(f"    Sizes:  {sizes}")
        print(f"    Sum:    {sum(sizes)}")
        print(f"    Sorted: {sorted(sizes)}")

    # Unique elements in each partition
    print(f"\n  Unique group sizes present:")
    for name, sizes in partitions.items():
        unique = sorted(set(sizes))
        print(f"    {name:<30s}: {unique}")

    # Match quality: for each partition, compute overlap with Madelung
    print(f"\n  ─── MATCH QUALITY vs MADELUNG ────────────────────────────")
    mad_sorted = sorted(MADELUNG)
    for name, sizes in partitions.items():
        if name == 'Madelung reference':
            continue
        s_sorted = sorted(sizes)

        # Exact match count
        # Use multiset intersection
        from collections import Counter
        c_mad = Counter(MADELUNG)
        c_sizes = Counter(sizes)
        common = sum((c_mad & c_sizes).values())
        total = max(len(MADELUNG), len(sizes))
        print(f"    {name:<30s}: {common}/{total} sizes match "
              f"({len(sizes)} groups vs 19 Madelung)")

    # Does any partition give exactly 19 groups?
    print(f"\n  ─── PARTITIONS WITH 19 GROUPS ────────────────────────────")
    found_19 = False
    for name, sizes in partitions.items():
        if len(sizes) == 19:
            print(f"    ✓ {name}: {sizes}")
            found_19 = True
    if not found_19:
        print(f"    None found. The 19-subshell structure does not emerge")
        print(f"    directly from gap thresholding alone.")

    # Closest match
    print(f"\n  ─── CLOSEST TO 19 GROUPS ─────────────────────────────────")
    closest = min(partitions.items(),
                  key=lambda kv: abs(len(kv[1]) - 19) if kv[0] != 'Madelung reference' else 999)
    print(f"    {closest[0]}: {len(closest[1])} groups")
    print(f"    Sizes: {closest[1]}")

    return partitions


# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

def main():
    print()
    print("=" * 80)
    print("  THE HIDDEN 19: Sub-sub-band structure within σ₃")
    print("  Do Cantor sub-gaps produce the Madelung subshell count?")
    print("=" * 80)

    L1_sizes, L2_sizes = task1_two_level()
    task2_threshold_sweep()
    task3_zeckendorf()
    sizes_19, sizes_34, sizes_nat = task4_full_partition()
    task5_outer_bands()
    sector_sizes_5, n_atomic = task6_atomic_sectors()
    partitions = task7_raw_summary(
        L1_sizes, L2_sizes, sizes_19, sizes_34, sizes_nat,
        sector_sizes_5, n_atomic
    )

    # Save results
    save_dir = os.path.expanduser(
        "~/Unified_Theory_Physics/results/hidden_nineteen"
    )
    os.makedirs(save_dir, exist_ok=True)

    save_data = {
        'center_band_size': len(center_eigs),
        'L1_sub_bands': L1_sizes,
        'L2_two_level': L2_sizes,
        'full_19_group': sizes_19,
        'full_34_group': sizes_34,
        'full_natural': sizes_nat,
        'sector_5': sector_sizes_5,
        'n_atomic': n_atomic,
        'madelung': MADELUNG,
    }
    def to_native(obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, list):
            return [to_native(x) for x in obj]
        if isinstance(obj, dict):
            return {k: to_native(v) for k, v in obj.items()}
        return obj

    with open(os.path.join(save_dir, "hidden_nineteen.json"), 'w') as f:
        json.dump(to_native(save_data), f, indent=2)

    # Raw text output
    raw_path = os.path.expanduser(
        "~/Unified_Theory_Physics/results/subband_sizes_raw.txt"
    )
    with open(raw_path, 'w') as f:
        for name, sizes in partitions.items():
            f.write(f"{name}:\n")
            f.write(f"  groups: {len(sizes)}\n")
            f.write(f"  sizes: {sizes}\n")
            f.write(f"  sorted: {sorted(sizes)}\n")
            f.write(f"  sum: {sum(sizes)}\n\n")

    print(f"\n  Results saved: {save_dir}/hidden_nineteen.json")
    print(f"  Raw sizes:     {raw_path}")


if __name__ == "__main__":
    main()
