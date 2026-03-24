"""
transport.py — Transport classification from θ mode
=====================================================

The θ mode from the Cantor predictor classifies transport:
    leak mode (θ = 0.564)    → ELECTRICAL CONDUCTOR (Ag, Cu, Au)
    baseline/additive        → INSULATOR / PHONON (Diamond, Si)
    p-hole                   → SEMICONDUCTOR
    magnetic                 → ANOMALOUS TRANSPORT

Key result: All top 3 electrical conductors (Ag, Cu, Au) are
leak mode. Diamond is highest thermal but lowest electrical
because it's baseline mode (pure phonon transport).
"""

import math
import numpy as np


# ═══════════════════════════════════════════════════════════════════
# EXPERIMENTAL DATA
# ═══════════════════════════════════════════════════════════════════

CONDUCTIVITY_ELEC = {  # S/m
    'Ag': 6.30e7, 'Cu': 5.96e7, 'Au': 4.10e7, 'Al': 3.77e7,
    'Na': 2.10e7, 'Mo': 1.87e7, 'W': 1.79e7, 'Co': 1.72e7,
    'Zn': 1.69e7, 'Ni': 1.43e7, 'Fe': 1.00e7, 'Cr': 7.87e6,
    'Pt': 9.43e6, 'Sn': 9.17e6, 'Pb': 4.81e6, 'Ti': 2.38e6,
}

THERMAL_CONDUCTIVITY = {  # W/(m·K)
    'C': 2200, 'Ag': 429, 'Cu': 401, 'Au': 318, 'Al': 237,
    'W': 174, 'Mo': 138, 'Fe': 80, 'Ni': 91, 'Cr': 94,
    'Co': 100, 'Pt': 72, 'Pb': 35, 'Ti': 22, 'Na': 142,
}


def classify_transport(elements_dict):
    """
    Classify transport mechanism by θ mode.

    Returns dict mapping element → transport type.
    """
    classification = {}
    for sym, d in elements_dict.items():
        mode = d['mode']
        if mode == 'leak':
            transport = 'electron_conductor'
        elif mode in ('additive', 'pythagorean'):
            transport = 'insulator_phonon'
        elif mode == 'p-hole':
            transport = 'semiconductor'
        elif mode == 'magnetic':
            transport = 'anomalous'
        elif mode in ('standard', 'reflect'):
            transport = 'metallic'
        else:
            transport = 'unknown'
        classification[sym] = {
            'transport': transport,
            'mode': mode,
            'theta': d['theta'],
        }
    return classification


def conductivity_test(elements_dict):
    """
    Test mode-conductivity correlation.

    Returns dict with correlations and leak-mode statistics.
    """
    elec_data = []
    for sym, sigma in sorted(CONDUCTIVITY_ELEC.items(), key=lambda x: x[1], reverse=True):
        if sym not in elements_dict:
            continue
        elec_data.append((sym, sigma, elements_dict[sym]))

    if not elec_data:
        return {'n_elements': 0}

    log_sigma = np.array([math.log10(x[1]) for x in elec_data])
    theta_arr = np.array([x[2]['theta'] for x in elec_data])
    modes = [x[2]['mode'] for x in elec_data]

    # Correlation
    rho = np.corrcoef(theta_arr, log_sigma)[0, 1]
    leak_count = sum(1 for m in modes if m == 'leak')

    # Top 3 check
    top3_modes = [x[2]['mode'] for x in elec_data[:3]]
    top3_all_leak = all(m == 'leak' for m in top3_modes)

    return {
        'n_elements': len(elec_data),
        'correlation_theta_sigma': float(rho),
        'leak_mode_count': leak_count,
        'top3_all_leak': top3_all_leak,
        'top3': [(x[0], x[1], x[2]['mode']) for x in elec_data[:3]],
        'elements': [
            {'sym': sym, 'sigma': sigma, 'theta': d['theta'], 'mode': d['mode']}
            for sym, sigma, d in elec_data
        ],
    }
