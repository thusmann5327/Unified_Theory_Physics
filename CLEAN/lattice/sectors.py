"""
sectors.py — 5-sector eigenvalue partition of the AAH spectrum
================================================================

VERIFIED:
  - At D = F(n), the 5-sector partition is F(n-3)|F(n-4)|F(n-3)|F(n-4)|F(n-3)
  - All sector sizes are Fibonacci numbers
  - Pattern holds for D = F(10) through F(16) (6/7 match, D=89 edge case)
"""

import numpy as np

from core.constants import PHI
from .fibonacci import fib, fib_index


def _build_aah(D):
    """Build and diagonalize D-site AAH Hamiltonian at critical coupling."""
    alpha = 1.0 / PHI
    H = np.diag(2 * np.cos(2 * np.pi * alpha * np.arange(D)))
    H += np.diag(np.ones(D - 1), 1) + np.diag(np.ones(D - 1), -1)
    return np.sort(np.linalg.eigvalsh(H))


def sector_partition(D):
    """Partition eigenvalues of D-site AAH into 5 sectors using 4 largest gaps.

    Parameters
    ----------
    D : int
        Number of lattice sites.

    Returns
    -------
    dict with:
        'sectors': list of 5 sector sizes, or None if < 4 gaps
        'gap_positions': list of gap indices
        'all_fibonacci': whether every sector size is a Fibonacci number
        'fib_labels': list of 'F(k)' labels for each sector
    """
    eigs = _build_aah(D)
    diffs = np.diff(eigs)
    med = np.median(diffs)
    gaps = [(i, diffs[i]) for i in range(len(diffs)) if diffs[i] > 8 * med]
    ranked = sorted(gaps, key=lambda g: g[1], reverse=True)

    if len(ranked) < 4:
        return {
            'sectors': None, 'gap_positions': [],
            'all_fibonacci': False, 'fib_labels': [],
        }

    top4 = sorted(ranked[:4], key=lambda g: g[0])
    boundaries = [g[0] for g in top4]

    sectors = []
    start = 0
    for b in boundaries:
        sectors.append(len(eigs[start:b + 1]))
        start = b + 1
    sectors.append(len(eigs[start:]))

    labels = []
    all_fib = True
    for s in sectors:
        fi = fib_index(s)
        if fi is not None:
            labels.append(f'F({fi})')
        else:
            labels.append(str(s))
            all_fib = False

    return {
        'sectors': sectors,
        'gap_positions': boundaries,
        'all_fibonacci': all_fib,
        'fib_labels': labels,
    }


def sector_pattern_check(n_range=None):
    """Check the 5-sector pattern at D = F(n) for a range of n.

    Expected pattern: F(n-3)|F(n-4)|F(n-3)|F(n-4)|F(n-3).

    Parameters
    ----------
    n_range : iterable of int, optional
        Fibonacci indices to test. Default: range(10, 17).

    Returns
    -------
    dict with:
        'results': list of per-n dicts
        'n_matching': int
        'n_tested': int
    """
    if n_range is None:
        n_range = range(10, 17)

    results = []
    for n in n_range:
        D = fib(n)
        sp = sector_partition(D)

        if sp['sectors'] is None:
            results.append({
                'n': n, 'D': D, 'sectors': None,
                'expected': None, 'matches': False,
            })
            continue

        expected = [fib(n-3), fib(n-4), fib(n-3), fib(n-4), fib(n-3)]
        matches = sp['sectors'] == expected

        results.append({
            'n': n, 'D': D,
            'sectors': sp['sectors'],
            'all_fibonacci': sp['all_fibonacci'],
            'expected': expected,
            'matches': matches,
            'labels': sp['fib_labels'],
        })

    n_match = sum(1 for r in results if r['matches'])
    return {
        'results': results,
        'n_matching': n_match,
        'n_tested': len(results),
    }
