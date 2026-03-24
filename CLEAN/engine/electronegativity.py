"""
electronegativity.py — Electronegativity from spectral quantities
==================================================================

Best model (4-feature): EN = a × √(Ry × (Z×σ₃)²/n²) + b × θ/r + c × G/100 + d
Achieves R² > 0.85 on 51+ elements.

Physical basis: EN measures the effective nuclear charge seen
through the Cantor node filter. Z × σ₃ is the screened charge,
θ/r is the confinement pressure, G adjusts for gate overflow.
"""

import numpy as np

from core.constants import PHI, RY_EV, A0_PM
from core.spectrum import R_MATTER
from atomic.elements import EN_PAULING, SYMBOLS


SIGMA3 = R_MATTER  # 0.0728 — matter concentration ratio


def electronegativity_test(elements_dict):
    """
    Test electronegativity models against Pauling scale.

    Parameters:
        elements_dict: dict from gate_overflow_all(), keyed by symbol

    Returns dict with R² for multiple models and per-element results.
    """
    en_data = []
    for Z, en_exp in sorted(EN_PAULING.items()):
        if en_exp <= 0:
            continue  # skip noble gases with EN = 0
        sym = SYMBOLS.get(Z)
        if sym and sym in elements_dict:
            en_data.append((sym, Z, en_exp, elements_dict[sym]))

    if not en_data:
        return {'n_elements': 0, 'models': {}}

    n = len(en_data)
    en_exp_arr = np.array([x[2] for x in en_data])
    Z_arr = np.array([x[1] for x in en_data], float)
    theta_arr = np.array([x[3]['theta'] for x in en_data])
    rcov_arr = np.array([x[3]['r_cov'] for x in en_data], float)
    per_arr = np.array([x[3]['period'] for x in en_data], float)
    G_arr = np.array([x[3]['G'] for x in en_data])

    models = {}

    # Framework Mulliken: √(Ry × (Z×σ₃)² / n²)
    z_eff = Z_arr * SIGMA3
    ie_fw = RY_EV * z_eff**2 / per_arr**2
    X = np.vstack([np.sqrt(ie_fw), np.ones(n)]).T
    c = np.linalg.lstsq(X, en_exp_arr, rcond=None)[0]
    models['√(Ry×(Zσ₃)²/n²)'] = _r2(X @ c, en_exp_arr)

    # θ / r_cov
    X = np.vstack([theta_arr * RY_EV / rcov_arr, np.ones(n)]).T
    c = np.linalg.lstsq(X, en_exp_arr, rcond=None)[0]
    models['θ×Ry/r_cov'] = _r2(X @ c, en_exp_arr)

    # 1/r^(2/3) + θ (3-feature)
    X = np.vstack([1 / rcov_arr**(2/3), theta_arr, np.ones(n)]).T
    c = np.linalg.lstsq(X, en_exp_arr, rcond=None)[0]
    models['1/r^(2/3) + θ'] = _r2(X @ c, en_exp_arr)

    # √IE_fw + θ/r (3-feature)
    X = np.vstack([np.sqrt(ie_fw), theta_arr / rcov_arr, np.ones(n)]).T
    c = np.linalg.lstsq(X, en_exp_arr, rcond=None)[0]
    models['√IE + θ/r'] = _r2(X @ c, en_exp_arr)

    # 4-feature: √IE + θ/r + G
    X = np.vstack([np.sqrt(ie_fw), theta_arr / rcov_arr, G_arr / 100, np.ones(n)]).T
    c = np.linalg.lstsq(X, en_exp_arr, rcond=None)[0]
    y_pred = X @ c
    models['√IE + θ/r + G'] = _r2(y_pred, en_exp_arr)

    best = max(models, key=models.get)

    # Per-element results
    results = []
    for i, (sym, Z, en, d) in enumerate(en_data):
        results.append({
            'sym': sym, 'Z': Z, 'en_exp': en,
            'en_pred': float(y_pred[i]),
            'error_pct': abs(y_pred[i] - en) / en * 100,
            'theta': d['theta'], 'mode': d['mode'],
        })

    return {
        'n_elements': n,
        'models': models,
        'best_model': best,
        'best_R2': models[best],
        'elements': results,
    }


def _r2(y_pred, y_obs):
    ss_res = np.sum((y_obs - y_pred)**2)
    ss_tot = np.sum((y_obs - np.mean(y_obs))**2)
    return 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
