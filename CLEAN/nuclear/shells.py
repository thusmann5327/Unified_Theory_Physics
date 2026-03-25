"""
shells.py — Nuclear shell structure from Cantor spectral ratios
================================================================

STATUS: UNDER DEVELOPMENT

Verified:
  - HO shell capacities = n(n+1) = 2 × T(n) (triangular numbers)
  - Spin-orbit detachment capacities: 10, 12, 14 (start at d-capacity)
  - Nuclear magic 2, 8 are exact Fibonacci

TODO — next tests:
  1. WHY triangular for nuclei but odd for atoms?
     Hypothesis: nucleons are composite (3 quarks) → each quark carries
     its own angular momentum → total degeneracy = sum over quarks
     = T(n) instead of single-particle 2l+1. Test: does T(n) = sum
     of 2l+1 for l = 0..n-1? YES: 1+3+5+...+(2n-1) = n². But T(n) ≠ n².
     Actually T(n) = n(n+1)/2, and the HO degeneracy for shell N is
     (N+1)(N+2)/2, not n(n+1). Need to reconcile indexing.

  2. Clean correction factor for magic/F(k).
     Current: 82/89 = 0.921 ≈ √(R_C) = 0.924 (0.3%). Is this a theorem?
     Test: does the correction come from the Cantor node wall position?
     Specifically: magic(k) = F(k) × (1 - σ₃_width/k)?

  3. Spin-orbit fraction converges to what?
     Current: 10/30, 12/42, 14/56 → 1/3, 2/7, 1/4.
     Limit: (2N+2)/(N(N+1)) = 2/(N) → 0. But the FRACTION that detaches
     decreases. The ABSOLUTE capacity (2N+2) increases by 2 each shell.
     Is the step-2 increment related to spin (2 spin states)?

  4. Does the full 35-band spectrum give nuclear subshell structure?
     The 233-site chain has 35 bands. If we use all 35 band-center
     positions as ratios, can we get the nuclear subshell sequence
     (2, 4, 2, 6, 4, 2, 8, 6, 4, 2, 10, ...)?
"""

import math

from core.spectrum import R_MATTER, R_INNER, R_SHELL, R_OUTER

# Nuclear magic numbers (observed)
NUCLEAR_MAGIC = [2, 8, 20, 28, 50, 82, 126]

# Harmonic oscillator magic (without spin-orbit)
HO_MAGIC = [2, 8, 20, 40, 70, 112, 168]

# Fibonacci sequence for proximity tests
_FIB = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377]


def ho_shell_capacities():
    """Harmonic oscillator shell capacities = n(n+1) = 2×T(n).

    Returns list of dicts with shell number, capacity, triangular check.
    """
    results = []
    for n in range(1, 8):
        cap = n * (n + 1)
        tri = n * (n + 1) // 2
        results.append({
            'shell': n,
            'capacity': cap,
            'half_cap': tri,
            'is_triangular': tri == n * (n + 1) // 2,
        })
    return results


def spin_orbit_detachment():
    """Spin-orbit detachment pattern: highest-j sublevel drops one shell.

    The detaching sublevels have capacities 10, 12, 14 — starting at
    the d-subshell capacity (10 = 2 × round(R_SHELL × 13)).

    Returns dict with detachment data and Cantor connection.
    """
    detachments = []
    for N in range(4, 7):  # HO shells N=4,5,6 (detachment starts here)
        l_max = N
        j_max = l_max + 0.5
        cap_detach = int(2 * j_max + 1)
        ho_total = N * (N + 1)
        frac = cap_detach / ho_total
        detachments.append({
            'HO_shell': N,
            'l_max': l_max,
            'j_max': j_max,
            'detach_capacity': cap_detach,
            'shell_total': ho_total,
            'fraction': round(frac, 4),
        })

    d_capacity = 2 * round(R_SHELL * 13)
    caps = [d['detach_capacity'] for d in detachments]

    return {
        'detachments': detachments,
        'capacities': caps,
        'is_arithmetic': all(caps[i+1] - caps[i] == 2 for i in range(len(caps)-1)),
        'starts_at_d_capacity': caps[0] == d_capacity,
        'd_capacity': d_capacity,
        'R_SHELL_times_13': round(R_SHELL * 13, 4),
    }


def magic_fibonacci_proximity():
    """How close each nuclear magic number is to a Fibonacci number.

    Returns list of dicts with magic number, nearest F, offset, ratio.
    """
    results = []
    for m in NUCLEAR_MAGIC:
        best_f, best_idx = _FIB[0], 0
        for i, f in enumerate(_FIB):
            if abs(f - m) < abs(best_f - m):
                best_f, best_idx = f, i
        results.append({
            'magic': m,
            'nearest_fib': best_f,
            'fib_index': best_idx + 1,
            'offset': m - best_f,
            'ratio': round(m / best_f, 4) if best_f > 0 else None,
            'is_exact': m == best_f,
        })
    return results
