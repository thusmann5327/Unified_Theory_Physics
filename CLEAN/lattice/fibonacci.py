"""
fibonacci.py — Fibonacci arithmetic and the shift identity
============================================================

VERIFIED:
  - round(F(k)/φ⁴) = F(k-4) for all k ≥ 5 (proven via Binet's formula)
  - Consequence: wall bands of size F(k) lose F(k-4) states under collapse

Proof sketch (Binet):
    F(n) = (φⁿ − ψⁿ)/√5, ψ = −1/φ
    F(k)/φ⁴ = F(k-4) + (−1)^k(φ⁸−1)/(φ^(k+4)√5)
    Correction → 0 as φ⁻ᵏ. Already < 0.5 at k=5. QED.
"""

import math

from core.constants import PHI

# 1-indexed Fibonacci table
_FIB = {
    1: 1, 2: 1, 3: 2, 4: 3, 5: 5, 6: 8, 7: 13, 8: 21,
    9: 34, 10: 55, 11: 89, 12: 144, 13: 233, 14: 377,
    15: 610, 16: 987, 17: 1597, 18: 2584, 19: 4181, 20: 6765,
}


def fib(n):
    """Return F(n) with 1-indexed Fibonacci: F(1)=1, F(2)=1, F(3)=2, ..."""
    if n in _FIB:
        return _FIB[n]
    # Extend table if needed
    while max(_FIB) < n:
        k = max(_FIB)
        _FIB[k + 1] = _FIB[k] + _FIB[k - 1]
    return _FIB[n]


def fib_index(val):
    """Return the 1-indexed Fibonacci index of val, or None."""
    for k, v in sorted(_FIB.items()):
        if v == val:
            return k
        if v > val:
            break
    return None


def shift_identity(k_range=None):
    """Test round(F(k)/φ⁴) = F(k-4) for a range of k.

    Parameters
    ----------
    k_range : iterable of int, optional
        Values of k to test. Default: range(5, 17).

    Returns
    -------
    dict with:
        'results': list of per-k dicts
        'all_match': bool
        'n_tested': int
    """
    if k_range is None:
        k_range = range(5, 17)

    results = []
    for k in k_range:
        fk = fib(k)
        fk4 = fib(k - 4)
        ratio = fk / PHI**4
        rounded = round(ratio)
        match = rounded == fk4
        err = abs(ratio - fk4) / fk4 * 100 if fk4 > 0 else 0
        results.append({
            'k': k, 'F_k': fk, 'F_k_over_phi4': ratio,
            'F_k_minus_4': fk4, 'rounded': rounded,
            'match': match, 'error_pct': round(err, 4),
        })

    return {
        'results': results,
        'all_match': all(r['match'] for r in results),
        'n_tested': len(results),
    }
