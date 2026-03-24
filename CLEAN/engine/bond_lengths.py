"""
bond_lengths.py — Bond length prediction from additive covalent radii
======================================================================

d_AB = r_cov(A) + r_cov(B)

Simple additive model achieves R² = 0.966 across 22 compounds.
The covalent radius itself comes from the Cantor node predictor.

Key cross-scale matches:
    Benzene CC / BOS = R_BASELINE (0.02%)
    Diamond CC / N₂  = R_BASELINE (0.16%)
    Graphite interlayer / Diamond CC = Ω_DE/Ω_M (0.23%)
"""

import math
import numpy as np

from core.constants import PHI, W
from core.spectrum import BASE, BOS
from atomic.elements import RADII, SYMBOLS


# ═══════════════════════════════════════════════════════════════════
# EXPERIMENTAL BOND LENGTHS (Å)
# ═══════════════════════════════════════════════════════════════════

BOND_LENGTHS = {
    ('C', 'C', 'diamond'):   1.544,
    ('C', 'C', 'benzene'):   1.397,
    ('C', 'C', 'graphite'):  1.42,
    ('N', 'N', 'N2'):        1.098,
    ('O', 'O', 'O2'):        1.208,
    ('H', 'H', 'H2'):        0.741,
    ('H', 'O', 'water'):     0.958,
    ('H', 'C', 'methane'):   1.087,
    ('C', 'O', 'CO'):        1.128,
    ('C', 'N', 'HCN'):       1.156,
    ('C', 'Cl', 'CCl4'):     1.77,
    ('Si', 'O', 'quartz'):   1.61,
    ('Si', 'Si', 'Si'):      2.35,
    ('Ge', 'Ge', 'Ge'):      2.45,
    ('Ga', 'As', 'GaAs'):    2.45,
    ('Na', 'Cl', 'NaCl'):    2.36,
    ('K', 'Cl', 'KCl'):      2.67,
    ('Ca', 'F', 'CaF2'):     2.37,
    ('Al', 'N', 'AlN'):      1.89,
    ('Ti', 'O', 'TiO2'):     1.95,
    ('Fe', 'O', 'FeO'):      2.15,
    ('Cu', 'Cu', 'Cu'):      2.56,
}

GRAPHITE_INTERLAYER = 3.35  # Å


def predict_bond_length(sym_a, sym_b):
    """
    Predict bond length as sum of covalent radii.

    Returns (d_pred_pm, d_pred_angstrom, r_cov_a, r_cov_b).
    """
    Z_a = next((Z for Z, s in SYMBOLS.items() if s == sym_a), None)
    Z_b = next((Z for Z, s in SYMBOLS.items() if s == sym_b), None)
    if Z_a is None or Z_b is None:
        return None
    r_a = RADII[Z_a][0]  # covalent radius, pm
    r_b = RADII[Z_b][0]
    d_pm = r_a + r_b
    return d_pm, d_pm / 100.0, r_a, r_b


def bond_length_test():
    """
    Test additive bond length model against experimental data.

    Returns dict with per-compound results and R².
    """
    results = []
    preds = []
    obs = []

    for (a, b, name), d_exp in sorted(BOND_LENGTHS.items(), key=lambda x: x[1]):
        pred = predict_bond_length(a, b)
        if pred is None:
            continue
        d_pm, d_ang, r_a, r_b = pred
        err = abs(d_ang - d_exp) / d_exp * 100
        results.append({
            'name': name, 'a': a, 'b': b,
            'd_exp': d_exp, 'd_pred': d_ang,
            'r_cov_a': r_a, 'r_cov_b': r_b,
            'error_pct': err,
        })
        preds.append(d_ang)
        obs.append(d_exp)

    preds = np.array(preds)
    obs = np.array(obs)
    ss_res = np.sum((obs - preds)**2)
    ss_tot = np.sum((obs - np.mean(obs))**2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0

    return {
        'compounds': results,
        'n_compounds': len(results),
        'R2': r2,
        'mean_error_pct': np.mean([r['error_pct'] for r in results]),
    }


def cross_scale_matches():
    """
    Verify cross-scale bond length identities.

    Benzene CC / BOS = R_BASELINE
    Diamond CC / N₂ = R_BASELINE
    Graphite interlayer / Diamond CC = Ω_DE / Ω_M
    """
    cc_benzene = 1.397
    cc_diamond = 1.544
    n2_bond = 1.098
    omega_de_m = (W**2 + W) / (1 - W**2 - W)  # Ω_DE / Ω_M (total matter)
    ratio_graphite_diamond = GRAPHITE_INTERLAYER / cc_diamond

    return {
        'benzene_cc_over_bos': {
            'value': cc_benzene / BOS,
            'target': BASE,
            'error_pct': abs(cc_benzene / BOS - BASE) / BASE * 100,
        },
        'diamond_cc_over_n2': {
            'value': cc_diamond / n2_bond,
            'target': BASE,
            'error_pct': abs(cc_diamond / n2_bond - BASE) / BASE * 100,
        },
        'graphite_over_diamond': {
            'value': ratio_graphite_diamond,
            'target': omega_de_m,
            'error_pct': abs(ratio_graphite_diamond - omega_de_m) / omega_de_m * 100,
        },
    }
