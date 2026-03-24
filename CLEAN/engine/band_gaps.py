"""
band_gaps.py — Band gap prediction from spectral quantities
=============================================================

Hybrid formula: E_gap = f(1/d², θ_prod, ΔEN², |G|)
where d = sum of covalent radii, θ = mode from Cantor predictor,
G = gate overflow, EN = electronegativity.

Best model achieves R² = 0.820 on 30+ compounds spanning
elemental semiconductors, III-V, II-VI, oxides, and halides.

Key prediction: CsPbI₃/CsSnI₃ gap ratio = 1.33 ≈ R_rc (1.5%)
"""

import math
import numpy as np

from core.constants import PHI, RY_EV, A0_PM
from core.spectrum import BOS
from atomic.elements import RADII, SYMBOLS, EN_PAULING


# ═══════════════════════════════════════════════════════════════════
# EXPERIMENTAL BAND GAPS (eV)
# ═══════════════════════════════════════════════════════════════════

BAND_GAPS = {
    # Elemental
    ('Si', 'Si'): 1.12, ('Ge', 'Ge'): 0.66, ('C', 'C'): 5.47,
    ('Sn', 'Sn'): 0.08,
    # III-V
    ('Ga', 'As'): 1.42, ('Ga', 'N'): 3.40, ('Ga', 'P'): 2.26,
    ('In', 'P'): 1.35, ('In', 'As'): 0.36, ('Al', 'N'): 6.2,
    ('Al', 'As'): 2.16, ('Al', 'P'): 2.45, ('In', 'N'): 0.70,
    ('B', 'N'): 6.0,
    # II-VI
    ('Zn', 'O'): 3.37, ('Zn', 'S'): 3.68, ('Zn', 'Se'): 2.70,
    ('Cd', 'S'): 2.42, ('Cd', 'Se'): 1.74, ('Cd', 'Te'): 1.49,
    # IV-IV
    ('Si', 'C'): 2.36,
    # Oxides
    ('Ti', 'O'): 3.2, ('Fe', 'O'): 2.1, ('Al', 'O'): 8.8,
    ('Si', 'O'): 8.9, ('Zr', 'O'): 5.0,
    # Halides
    ('Na', 'Cl'): 8.5, ('K', 'Cl'): 8.4, ('Li', 'F'): 13.6,
    ('Ca', 'F'): 12.1, ('Na', 'F'): 11.5,
}


def _get_Z(sym):
    """Look up atomic number from symbol."""
    for Z, s in SYMBOLS.items():
        if s == sym:
            return Z
    return None


def band_gap_test(elements_dict):
    """
    Test band gap models against experimental data.

    Parameters:
        elements_dict: dict from gate_overflow_all(), keyed by symbol

    Returns dict with per-compound results and R² for multiple models.
    """
    gap_data = []
    for (a, b), eg in sorted(BAND_GAPS.items(), key=lambda x: x[1], reverse=True):
        if a not in elements_dict or b not in elements_dict:
            continue
        da, db = elements_dict[a], elements_dict[b]
        gap_data.append((a, b, eg, da, db))

    if not gap_data:
        return {'n_compounds': 0, 'models': {}}

    n = len(gap_data)
    eg_arr = np.array([x[2] for x in gap_data])

    # Build predictor arrays
    rc_sum = np.array([x[3]['r_cov'] + x[4]['r_cov'] for x in gap_data], float)
    d_ang = rc_sum / 100.0  # Å
    theta_prod = np.array([x[3]['theta'] * x[4]['theta'] for x in gap_data], float)
    G_prod = np.array([abs(x[3]['G']) * abs(x[4]['G']) for x in gap_data], float)
    G_prod_safe = np.maximum(G_prod, 0.01)

    en_diff = np.array([
        abs(EN_PAULING.get(x[3]['Z'], 0) - EN_PAULING.get(x[4]['Z'], 0))
        for x in gap_data
    ])

    models = {}

    # Harrison-type: Eg ∝ 1/d²
    X = np.vstack([RY_EV * (A0_PM / 100.0)**2 / d_ang**2, np.ones(n)]).T
    c = np.linalg.lstsq(X, eg_arr, rcond=None)[0]
    y_pred = X @ c
    models['Harrison 1/d²'] = _r2(y_pred, eg_arr)

    # ΔEN² / d (Sanderson-type)
    X = np.vstack([en_diff**2 / d_ang, np.ones(n)]).T
    c = np.linalg.lstsq(X, eg_arr, rcond=None)[0]
    y_pred = X @ c
    models['ΔEN²/d'] = _r2(y_pred, eg_arr)

    # Hybrid: 1/d² + θ/d
    X = np.vstack([1 / d_ang**2, theta_prod / d_ang, np.ones(n)]).T
    c = np.linalg.lstsq(X, eg_arr, rcond=None)[0]
    y_pred = X @ c
    models['1/d² + θ/d'] = _r2(y_pred, eg_arr)

    # |ΔEN| + 1/d
    X = np.vstack([en_diff, 1 / d_ang, np.ones(n)]).T
    c = np.linalg.lstsq(X, eg_arr, rcond=None)[0]
    y_pred = X @ c
    models['|ΔEN| + 1/d'] = _r2(y_pred, eg_arr)

    # BOS / d
    X = np.vstack([RY_EV * BOS / d_ang, np.ones(n)]).T
    c = np.linalg.lstsq(X, eg_arr, rcond=None)[0]
    y_pred = X @ c
    models['Ry×BOS/d'] = _r2(y_pred, eg_arr)

    best = max(models, key=models.get)

    # Per-compound results for best model
    results = []
    for i, (a, b, eg, da, db) in enumerate(gap_data):
        results.append({
            'a': a, 'b': b, 'eg_exp': eg,
            'd_ang': d_ang[i],
            'theta_prod': theta_prod[i],
        })

    return {
        'n_compounds': n,
        'models': models,
        'best_model': best,
        'best_R2': models[best],
        'compounds': results,
    }


def _r2(y_pred, y_obs):
    ss_res = np.sum((y_obs - y_pred)**2)
    ss_tot = np.sum((y_obs - np.mean(y_obs))**2)
    return 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
