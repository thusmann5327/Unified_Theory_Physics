"""
gate_overflow.py — The Error IS the Prediction
================================================

Gate overflow G(Z) = discrepancy between predicted and observed
vdW/cov ratio. G < 0 means the electron cloud is MORE COMPACT
than predicted — energy redirected into bonding → HARD materials.
G > 0 means cloud extends further → SOFT, metallic.

One axiom: φ² = φ + 1. Zero free parameters.
"""

from atomic.periodic_table import predict_ratio
from atomic.elements import RADII, SYMBOLS


def gate_overflow(Z):
    """
    Compute gate overflow G(Z) for element Z.

    Returns dict with ratio_pred, ratio_obs, G (%), theta, mode,
    r_cov, r_vdw, and delta_R (pm).
    """
    if Z not in RADII or Z not in SYMBOLS:
        return None

    r_cov, r_vdw = RADII[Z]
    ratio_obs = r_vdw / r_cov
    ratio_pred, theta, per, n_p, n_d, n_f, n_s, blk, mode, cone = predict_ratio(Z)

    G = (ratio_obs - ratio_pred) / ratio_pred * 100
    delta_R = r_vdw - ratio_pred * r_cov  # pm

    return {
        'Z': Z,
        'sym': SYMBOLS[Z],
        'ratio_pred': ratio_pred,
        'ratio_obs': ratio_obs,
        'G': G,
        'delta_R': delta_R,
        'theta': theta,
        'mode': mode,
        'cone': cone,
        'r_cov': r_cov,
        'r_vdw': r_vdw,
        'period': per,
        'n_p': n_p,
        'n_d': n_d,
        'n_s': n_s,
        'block': blk,
    }


def gate_overflow_all():
    """Compute gate overflow for all elements with radii data."""
    results = {}
    for Z in sorted(RADII.keys()):
        if Z not in SYMBOLS:
            continue
        d = gate_overflow(Z)
        if d:
            results[d['sym']] = d
    return results
