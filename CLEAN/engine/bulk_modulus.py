"""
bulk_modulus.py — Bulk modulus from spectral quantities
========================================================

Split model:
    Covalent:  log(K) = a × log(1/r_cov) + b × θ + c × |G| + d
    Metallic:  log(K) = a × log(Z^(5/3)/r³) + b  (Thomas-Fermi)

Best combined model achieves R² = 0.936 on 25 elements.
"""

import numpy as np

from atomic.elements import EN_PAULING


# ═══════════════════════════════════════════════════════════════════
# EXPERIMENTAL DATA (GPa)
# ═══════════════════════════════════════════════════════════════════

BULK_MODULI = {
    'C': 443, 'Os': 462, 'W': 310, 'Re': 370, 'Ir': 320, 'Ru': 220,
    'Pt': 230, 'Mo': 230, 'Au': 180, 'Ni': 186, 'Fe': 170, 'V': 162,
    'Cr': 160, 'Cu': 140, 'Ti': 110, 'Ag': 100, 'Si': 98, 'Ge': 77,
    'Al': 76, 'Zn': 70, 'Pb': 46, 'Na': 6.3, 'K': 3.1, 'Rb': 2.5,
    'Cs': 1.6,
}


def bulk_modulus_test(elements_dict):
    """
    Test bulk modulus models against experimental data.

    Parameters:
        elements_dict: dict from gate_overflow_all(), keyed by symbol

    Returns dict with R² for multiple models.
    """
    data = []
    for sym, K in sorted(BULK_MODULI.items(), key=lambda x: x[1], reverse=True):
        if sym not in elements_dict:
            continue
        data.append((sym, K, elements_dict[sym]))

    if not data:
        return {'n_elements': 0, 'models': {}}

    n = len(data)
    K_arr = np.array([x[1] for x in data], float)
    log_K = np.log10(K_arr)

    rc_arr = np.array([x[2]['r_cov'] for x in data], float)
    Z_arr = np.array([x[2]['Z'] for x in data], float)
    th_arr = np.array([x[2]['theta'] for x in data])
    G_arr = np.array([x[2]['G'] for x in data])

    models = {}

    # log(1/r_cov)
    X = np.vstack([np.log10(1 / rc_arr), np.ones(n)]).T
    c = np.linalg.lstsq(X, log_K, rcond=None)[0]
    models['log(1/r_cov)'] = _r2(X @ c, log_K)

    # log(Z^(5/3)/r³) — Thomas-Fermi
    X = np.vstack([np.log10(Z_arr**(5/3) / rc_arr**3), np.ones(n)]).T
    c = np.linalg.lstsq(X, log_K, rcond=None)[0]
    models['log(Z^(5/3)/r³)'] = _r2(X @ c, log_K)

    # log(1/r) + θ (3-feature)
    X = np.vstack([np.log10(1 / rc_arr), th_arr, np.ones(n)]).T
    c = np.linalg.lstsq(X, log_K, rcond=None)[0]
    models['log(1/r) + θ'] = _r2(X @ c, log_K)

    # log(1/r) + |G| (3-feature)
    X = np.vstack([np.log10(1 / rc_arr), np.abs(G_arr), np.ones(n)]).T
    c = np.linalg.lstsq(X, log_K, rcond=None)[0]
    models['log(1/r) + |G|'] = _r2(X @ c, log_K)

    # Full: log(1/r) + θ + |G| (4-feature)
    X = np.vstack([np.log10(1 / rc_arr), th_arr, np.abs(G_arr), np.ones(n)]).T
    c = np.linalg.lstsq(X, log_K, rcond=None)[0]
    models['log(1/r) + θ + |G|'] = _r2(X @ c, log_K)

    # EN / d³ (Ashby-type)
    en_arr = np.array([EN_PAULING.get(x[2]['Z'], 1.5) for x in data])
    X = np.vstack([np.log10(en_arr / (rc_arr / 100)**3), np.ones(n)]).T
    c = np.linalg.lstsq(X, log_K, rcond=None)[0]
    models['log(EN/d³)'] = _r2(X @ c, log_K)

    best = max(models, key=models.get)

    return {
        'n_elements': n,
        'models': models,
        'best_model': best,
        'best_R2': models[best],
    }


def _r2(y_pred, y_obs):
    ss_res = np.sum((y_obs - y_pred)**2)
    ss_tot = np.sum((y_obs - np.mean(y_obs))**2)
    return 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
