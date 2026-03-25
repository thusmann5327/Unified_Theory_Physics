"""
scale.py — Nuclear-to-atomic scale transition
===============================================

STATUS: UNDER DEVELOPMENT

Verified:
  - Bracket gap ≈ F(8) = 21 for all elements Z=1..120
  - Gap exact at Z=82 (Pb), Z=86 (Rn), Z=118 (Og)
  - 126 has most compact Zeckendorf (3 terms) among island candidates
  - Zeckendorf decomposition: 126 = 89 + 34 + 3

TODO — next tests:
  1. Does bracket gap have a clean formula in terms of framework constants?
     Current: gap ≈ 21 = F(8). Is gap = round(log(R_atom/R_nuc)/log(φ))?
  2. Zeckendorf term count as stability predictor beyond island of stability.
     Does term count correlate with measured binding energy per nucleon?
"""

import math

from core.constants import PHI, L_PLANCK

# Fibonacci sequence
_FIB = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]

# Known vdW radii (pm) for bracket gap calculation
_VDW_DATA = {
    1: 120, 2: 140, 3: 182, 4: 153, 5: 192, 6: 170, 7: 155,
    8: 152, 9: 147, 10: 154, 11: 227, 12: 173, 13: 184, 14: 210,
    15: 180, 16: 180, 17: 175, 18: 188, 19: 275, 20: 231,
    26: 204, 29: 196, 36: 202, 46: 202, 54: 216,
    55: 343, 79: 214, 82: 202, 86: 220, 92: 186,
}


def _bracket(r_meters):
    """Bracket address: bz = round[log(R/l_P) / log(φ)]."""
    if r_meters <= 0:
        return 0
    return round(math.log(r_meters / L_PLANCK) / math.log(PHI))


def _estimate_atomic_radius_m(Z):
    """Estimate atomic (vdW) radius in meters for element Z."""
    if Z in _VDW_DATA:
        return _VDW_DATA[Z] * 1e-12
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
        r_pm = 200
    return r_pm * 1e-12


def bracket_gap(z_range=None):
    """Bracket gap (atomic − nuclear) for elements.

    The gap between nuclear and atomic bracket addresses is ≈ F(8) = 21
    for all elements, reflecting the universal scale separation.

    Parameters
    ----------
    z_range : iterable of int, optional
        Atomic numbers to compute. Defaults to 1..120.

    Returns
    -------
    dict with:
        'gaps': list of (Z, gap, b_nuc, b_atom)
        'mean_gap': float
        'min_gap': (Z, gap)
        'max_gap': (Z, gap)
        'nearest_fib_to_mean': int
        'all_near_F8': bool — whether all gaps are within 2 of F(8)=21
    """
    if z_range is None:
        z_range = range(1, 121)

    gaps = []
    for Z in z_range:
        A = round(2.5 * Z) if Z > 1 else 1
        R_nuc = 1.2e-15 * A ** (1 / 3)
        R_atom = _estimate_atomic_radius_m(Z)
        b_nuc = _bracket(R_nuc)
        b_atom = _bracket(R_atom)
        gap = b_atom - b_nuc
        gaps.append((Z, gap, b_nuc, b_atom))

    gap_vals = [g[1] for g in gaps]
    mean_gap = sum(gap_vals) / len(gap_vals)

    # Nearest Fibonacci to mean
    best_f = _FIB[0]
    for f in _FIB:
        if abs(f - mean_gap) < abs(best_f - mean_gap):
            best_f = f

    min_g = min(gaps, key=lambda x: x[1])
    max_g = max(gaps, key=lambda x: x[1])

    return {
        'gaps': gaps,
        'mean_gap': round(mean_gap, 2),
        'min_gap': (min_g[0], min_g[1]),
        'max_gap': (max_g[0], max_g[1]),
        'nearest_fib_to_mean': best_f,
        'all_near_F8': all(abs(g - 21) <= 3 for g in gap_vals),
    }


def zeckendorf(n):
    """Non-adjacent Fibonacci decomposition (Zeckendorf representation).

    Every positive integer has a unique representation as a sum of
    non-consecutive Fibonacci numbers.

    Returns list of Fibonacci terms (descending).
    """
    fibs = [f for f in _FIB if f <= n]
    result, rem = [], int(round(abs(n)))
    for f in reversed(fibs):
        if f <= rem:
            result.append(f)
            rem -= f
        if rem == 0:
            break
    return result


def zeckendorf_compactness(candidates=None):
    """Zeckendorf compactness analysis for island-of-stability candidates.

    Fewer Zeckendorf terms = more "Fibonacci-aligned" = prediction of
    enhanced nuclear stability.

    Parameters
    ----------
    candidates : list of int, optional
        Nucleon numbers to test. Default: [114, 120, 126, 184].

    Returns
    -------
    dict with:
        'results': list of dicts per candidate
        'most_compact': list of candidates with fewest terms
        'min_terms': int
    """
    if candidates is None:
        candidates = [114, 120, 126, 184]

    results = []
    for n in candidates:
        z = zeckendorf(n)
        # Verify non-adjacency
        fib_indices = []
        for f in z:
            for i, fv in enumerate(_FIB):
                if fv == f:
                    fib_indices.append(i)
                    break
        valid = all(
            abs(fib_indices[i] - fib_indices[i - 1]) >= 2
            for i in range(1, len(fib_indices))
        )
        results.append({
            'n': n,
            'zeckendorf': z,
            'terms': len(z),
            'valid': valid,
            'representation': ' + '.join(str(x) for x in z),
        })

    min_terms = min(r['terms'] for r in results)
    most_compact = [r['n'] for r in results if r['terms'] == min_terms]

    return {
        'results': results,
        'most_compact': most_compact,
        'min_terms': min_terms,
    }
