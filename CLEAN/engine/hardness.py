"""
hardness.py — Compound hardness from gate overflow
====================================================

The gate overflow IS the hardness prediction:
    G < 0 → compact cloud → energy into bonding → HARD
    G > 0 → extended cloud → SOFT, metallic

Compound hardness: |G_A| × |G_B| ∝ Vickers hardness
Best 5-feature model achieves R² = 0.831 on log₁₀(Vickers).

Period 2 has no σ₃ gate — that absence is why B, C, N make
everything superhard.
"""

import math
import numpy as np

from core.constants import PHI


# ═══════════════════════════════════════════════════════════════════
# EXPERIMENTAL DATA
# ═══════════════════════════════════════════════════════════════════

MOHS_ELEMENTAL = {
    'C': 10, 'B': 9.3, 'Cr': 8.5, 'W': 7.5, 'V': 7.0, 'Re': 7.0,
    'Os': 7.0, 'Si': 6.5, 'Ir': 6.5, 'Ru': 6.5, 'Mn': 6.0, 'Ge': 6.0,
    'Ti': 6.0, 'Nb': 6.0, 'Ta': 6.5, 'Mo': 5.5, 'Be': 5.5, 'Hf': 5.5,
    'Co': 5.0, 'Zr': 5.0, 'Pd': 4.75, 'Ni': 4.0, 'Fe': 4.0, 'Y': 4.0,
    'Sc': 4.0, 'Pt': 3.5, 'Cu': 3.0, 'Al': 2.75, 'Ag': 2.5, 'Au': 2.5,
    'Zn': 2.5, 'Mg': 2.5, 'Ca': 1.75, 'Sn': 1.5, 'Pb': 1.5, 'Sr': 1.5,
    'Ba': 1.25, 'Li': 0.6, 'Na': 0.5, 'K': 0.4, 'Rb': 0.3, 'Cs': 0.2,
}

VICKERS_COMPOUNDS = {
    ('C', 'C', 'diamond'):   10000,
    ('B', 'N', 'cBN'):       4500,
    ('B', 'C', 'B4C'):       3000,
    ('Si', 'C', 'SiC'):      2500,
    ('Ti', 'B', 'TiB2'):     2500,
    ('Ti', 'C', 'TiC'):      2800,
    ('W', 'C', 'WC'):        2200,
    ('Ti', 'N', 'TiN'):      2000,
    ('Al', 'O', 'Al2O3'):    2000,
    ('Si', 'N', 'Si3N4'):    1500,
    ('Zr', 'O', 'ZrO2'):     1200,
    ('Si', 'O', 'SiO2'):     1100,
    ('Fe', 'O', 'Fe2O3'):    800,
    ('Ca', 'F', 'CaF2'):     200,
    ('Na', 'Cl', 'NaCl'):    20,
    ('K', 'Br', 'KBr'):      10,
    ('Au', 'Au', 'Au'):      25,
    ('Ag', 'Ag', 'Ag'):      25,
    ('Cu', 'Cu', 'Cu'):      50,
    ('Fe', 'Fe', 'Fe'):      200,
    ('Pb', 'Pb', 'Pb'):      5,
    ('Cs', 'Cs', 'Cs'):      0.2,
}


def hardness_test(elements_dict):
    """
    Test compound hardness models against Vickers data.

    Parameters:
        elements_dict: dict from gate_overflow_all(), keyed by symbol

    Returns dict with R² for multiple models.
    """
    hard_data = []
    for (a, b, name), hv in sorted(VICKERS_COMPOUNDS.items(), key=lambda x: x[1], reverse=True):
        if a not in elements_dict or b not in elements_dict:
            continue
        hard_data.append((a, b, name, hv, elements_dict[a], elements_dict[b]))

    if not hard_data:
        return {'n_compounds': 0, 'models': {}}

    n = len(hard_data)
    hv_arr = np.array([x[3] for x in hard_data], float)
    log_hv = np.log10(np.maximum(hv_arr, 0.1))

    rc_sum = np.array([x[4]['r_cov'] + x[5]['r_cov'] for x in hard_data], float)
    d_ang = rc_sum / 100.0
    G_prod = np.array([abs(x[4]['G']) * abs(x[5]['G']) for x in hard_data], float)
    G_prod_safe = np.maximum(G_prod, 0.01)
    th_prod = np.array([x[4]['theta'] * x[5]['theta'] for x in hard_data], float)
    per2_count = np.array([int(x[4]['period'] == 2) + int(x[5]['period'] == 2)
                           for x in hard_data], float)

    models = {}

    # log(1/d) + log(√|G|)
    X = np.vstack([np.log10(1 / d_ang), np.log10(np.sqrt(G_prod_safe)),
                   np.ones(n)]).T
    c = np.linalg.lstsq(X, log_hv, rcond=None)[0]
    models['log(1/d) + log(√|G|)'] = _r2(X @ c, log_hv)

    # + θ boost (4-feature)
    X = np.vstack([np.log10(1 / d_ang), np.log10(np.sqrt(G_prod_safe)),
                   np.log10(np.maximum(th_prod, 0.01)), np.ones(n)]).T
    c = np.linalg.lstsq(X, log_hv, rcond=None)[0]
    models['+log(θ_prod)'] = _r2(X @ c, log_hv)

    # + period-2 boost (4-feature)
    X = np.vstack([np.log10(1 / d_ang), np.log10(np.sqrt(G_prod_safe)),
                   per2_count, np.ones(n)]).T
    c = np.linalg.lstsq(X, log_hv, rcond=None)[0]
    models['+per2_count'] = _r2(X @ c, log_hv)

    # 5-feature full
    X = np.vstack([np.log10(1 / d_ang), np.log10(np.sqrt(G_prod_safe)),
                   np.log10(np.maximum(th_prod, 0.01)), per2_count,
                   np.ones(n)]).T
    c = np.linalg.lstsq(X, log_hv, rcond=None)[0]
    models['5-feature full'] = _r2(X @ c, log_hv)

    # Pure 1/d³
    X = np.vstack([np.log10(1 / d_ang**3), np.ones(n)]).T
    c = np.linalg.lstsq(X, log_hv, rcond=None)[0]
    models['log(1/d³)'] = _r2(X @ c, log_hv)

    best = max(models, key=models.get)

    # Per-compound results
    results = []
    for i, (a, b, name, hv, da, db) in enumerate(hard_data):
        results.append({
            'name': name, 'a': a, 'b': b,
            'vickers': hv,
            'G_A': da['G'], 'G_B': db['G'],
            'theta_A': da['theta'], 'theta_B': db['theta'],
            'r_cov_A': da['r_cov'], 'r_cov_B': db['r_cov'],
        })

    return {
        'n_compounds': n,
        'models': models,
        'best_model': best,
        'best_R2': models[best],
        'compounds': results,
    }


def elemental_hardness_test(elements_dict):
    """
    Test elemental Mohs hardness correlations.

    Returns dict with correlations and R² for multiple predictors.
    """
    data = []
    for sym, mohs in sorted(MOHS_ELEMENTAL.items(), key=lambda x: x[1], reverse=True):
        if sym not in elements_dict:
            continue
        data.append((sym, mohs, elements_dict[sym]))

    if not data:
        return {'n_elements': 0, 'models': {}}

    n = len(data)
    mohs_arr = np.array([x[1] for x in data])
    G_arr = np.array([x[2]['G'] for x in data])
    rcov_arr = np.array([x[2]['r_cov'] for x in data], float)
    theta_arr = np.array([x[2]['theta'] for x in data])

    models = {}

    # 1/r_cov
    X = np.vstack([1.0 / rcov_arr, np.ones(n)]).T
    c = np.linalg.lstsq(X, mohs_arr, rcond=None)[0]
    models['1/r_cov'] = _r2(X @ c, mohs_arr)

    # 1/r_cov + |G| (2-feature)
    X = np.vstack([1.0 / rcov_arr, np.abs(G_arr)]).T
    c = np.linalg.lstsq(X, mohs_arr, rcond=None)[0]
    models['1/r_cov + |G|'] = _r2(X @ c, mohs_arr)

    # θ + |G| (2-feature)
    X = np.vstack([theta_arr, np.abs(G_arr)]).T
    c = np.linalg.lstsq(X, mohs_arr, rcond=None)[0]
    models['θ + |G|'] = _r2(X @ c, mohs_arr)

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
