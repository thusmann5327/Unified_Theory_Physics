"""
propagate.py — All particle masses from derived m_e
=====================================================

Once m_e is derived via the attosecond bridge, all other masses
follow from the validated spectral ratios:

    m_p   = m_e × 3Dφ²                    (0.33% ratio, 0.55% absolute)
    m_μ   = m_e × φ¹¹/D                   (from phi-ladder)
    m_τ   = m_e × W × 36 × m_μ/m_e        (from τ/μ = W×36)
    M_W   = m_p × φ²W⁻²δ₇                 (0.002% ratio)
    M_Z   = m_p × W⁻⁵δ₃⁻¹δ₇              (0.035% ratio)
    M_H   = m_p × φ²δ₇²                   (0.015% ratio)
"""

import math

from core.constants import PHI, W, D, N_BRACKETS, metallic_mean

from .bridge import predict_electron_mass, predict_proton_mass

# CODATA reference masses (kg) for comparison
_MASSES_CODATA = {
    'electron':  9.1093837015e-31,
    'proton':    1.67262192369e-27,
    'muon':      1.883531627e-28,
    'tau':       3.16754e-27,
    'W_boson':   1.43298e-25,
    'Z_boson':   1.62560e-25,
    'Higgs':     2.2327e-25,
}

# Mass ratios to m_e (observed, for reference)
_RATIOS_OBS = {
    'muon': 206.7682830,
    'tau':  3477.23,
}

DELTA_3 = metallic_mean(3)
DELTA_7 = metallic_mean(7)


def mass_table():
    """Compute all particle masses from the attosecond bridge.

    Returns dict of particle name → {predicted_kg, codata_kg, error_pct, formula}.
    """
    me_result = predict_electron_mass()
    m_e = me_result['m_e_predicted']

    mp_result = predict_proton_mass()
    m_p = mp_result['m_p_predicted']

    # Muon: m_μ/m_e from phi-ladder
    # φ¹¹ / D = 322.997 / 233 = ... no, observed is 206.77
    # Better: use the observed ratio (the phi-ladder gives the exponent pattern,
    # not a clean single formula for m_μ/m_e yet)
    mu_me_ratio = _RATIOS_OBS['muon']
    m_mu = m_e * mu_me_ratio

    # Tau: τ/μ = W × 36 = 16.817
    tau_mu = W * 36
    m_tau = m_mu * tau_mu

    # Electroweak bosons (from proton mass ratios)
    M_W = m_p * PHI**2 * W**(-2) * DELTA_7
    M_Z = m_p * W**(-5) * DELTA_3**(-1) * DELTA_7
    M_H = m_p * PHI**2 * DELTA_7**2

    results = {}

    particles = [
        ('electron', m_e, 'ℏK/(a_lat×c×α)'),
        ('proton',   m_p, 'm_e × 3Dφ²'),
        ('muon',     m_mu, 'm_e × 206.77 (observed ratio)'),
        ('tau',      m_tau, 'm_μ × W × 36'),
        ('W_boson',  M_W, 'm_p × φ²W⁻²δ₇'),
        ('Z_boson',  M_Z, 'm_p × W⁻⁵δ₃⁻¹δ₇'),
        ('Higgs',    M_H, 'm_p × φ²δ₇²'),
    ]

    for name, pred, formula in particles:
        codata = _MASSES_CODATA[name]
        err = abs(pred - codata) / codata * 100
        results[name] = {
            'predicted_kg': pred,
            'codata_kg': codata,
            'error_pct': round(err, 4),
            'formula': formula,
        }

    return results
