"""
ionic_radii.py — Ionic radius from φ-scaling
===============================================

Heyrovska-Husmann bridge:
    r_ion(+q) = d(AA) / φ^(q+1)

where d(AA) = homonuclear bond length = 2 × r_cov.

Charge-specific:
    +1 (alkali):         r = d/φ²     → 6.5% mean error
    +2 (alkaline earth): r = d/φ³     → 8.8% mean error
    +3:                  r = d/φ⁴     → variable
"""

import math

from core.constants import PHI, W, LEAK
from atomic.elements import RADII, SYMBOLS


# ═══════════════════════════════════════════════════════════════════
# SHANNON IONIC RADII (pm, coordination number VI)
# ═══════════════════════════════════════════════════════════════════

SHANNON_RADII = {
    # +1 ions
    ('Li', 1): 76, ('Na', 1): 102, ('K', 1): 138,
    ('Rb', 1): 152, ('Cs', 1): 167, ('Ag', 1): 115,
    ('Cu', 1): 77,
    # +2 ions
    ('Be', 2): 45, ('Mg', 2): 72, ('Ca', 2): 100,
    ('Sr', 2): 118, ('Ba', 2): 135, ('Zn', 2): 74,
    ('Fe', 2): 78, ('Cu', 2): 73, ('Ni', 2): 69,
    ('Co', 2): 75, ('Mn', 2): 83, ('Cd', 2): 95,
    ('Pb', 2): 119,
    # +3 ions
    ('Al', 3): 54, ('Fe', 3): 65, ('Cr', 3): 62,
    ('Sc', 3): 75, ('Y', 3): 90, ('La', 3): 103,
    ('Ti', 3): 67, ('V', 3): 64, ('Mn', 3): 65,
    ('Co', 3): 61, ('Ga', 3): 62, ('In', 3): 80,
}


def predict_ionic_radius(sym, charge):
    """
    Predict ionic radius using r_ion = 2 × r_cov / φ^(charge+1).

    Returns (r_pred_pm, r_cov_pm) or None if element not found.
    """
    Z = next((z for z, s in SYMBOLS.items() if s == sym), None)
    if Z is None or Z not in RADII:
        return None
    r_cov = RADII[Z][0]
    d_homo = 2 * r_cov
    r_pred = d_homo / PHI**(charge + 1)
    return r_pred, r_cov


def ionic_radius_test():
    """
    Test ionic radius predictions against Shannon data.

    Returns dict with per-ion results grouped by charge.
    """
    results = {1: [], 2: [], 3: []}

    for (sym, charge), r_obs in sorted(SHANNON_RADII.items()):
        pred = predict_ionic_radius(sym, charge)
        if pred is None:
            continue
        r_pred, r_cov = pred
        err = abs(r_pred - r_obs) / r_obs * 100
        results[charge].append({
            'sym': sym, 'charge': charge,
            'r_obs': r_obs, 'r_pred': r_pred,
            'r_cov': r_cov, 'error_pct': err,
        })

    summary = {}
    for charge, ions in results.items():
        if ions:
            errors = [x['error_pct'] for x in ions]
            summary[charge] = {
                'n_ions': len(ions),
                'mean_error_pct': sum(errors) / len(errors),
                'min_error_pct': min(errors),
                'max_error_pct': max(errors),
                'best_ion': min(ions, key=lambda x: x['error_pct'])['sym'],
                'ions': ions,
            }

    return summary
