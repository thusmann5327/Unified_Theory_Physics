"""
bridge.py — The attosecond bridge to absolute mass
=====================================================

The lattice-to-Bohr conversion constant:

    K = 24 / φ³ = 5.6656

converts a_lattice = c × t_hop into the Bohr radius:

    a_B = a_lattice / K

Then:
    m_e = ℏ / (a_B × c × α)
        = ℏ × K × N × W / (a_lattice × c)

Inputs:
    φ         — axiom
    N, W      — from spectrum
    t_hop     — 1 attosecond (one measurement)
    ℏ, c      — SI defined constants

No empirical m_e or a_B anywhere in the chain.
"""

import math

from core.constants import (
    PHI, W, N_BRACKETS, D,
    HBAR, C_LIGHT, RHO6,
)

# ── The one physical measurement ─────────────────────────────────
T_HOP = 1.0e-18                           # 1 attosecond
A_LATTICE = C_LIGHT * T_HOP               # = 2.998e-10 m

# ── The bridge constant ──────────────────────────────────────────
K_BRIDGE = 24.0 / PHI**3                   # = 5.6656 (0.007% from target)

# ── α from spectrum ──────────────────────────────────────────────
ALPHA_PRED = 1.0 / (N_BRACKETS * W)        # = 1/137.34

# ── CODATA reference values (for comparison ONLY) ────────────────
_M_E_CODATA = 9.1093837015e-31            # kg
_A_BOHR_CODATA = 5.29177210903e-11        # m
_M_P_CODATA = 1.67262192369e-27           # kg
_MP_ME_RATIO = _M_P_CODATA / _M_E_CODATA  # 1836.15


def predict_bohr_radius():
    """Predict the Bohr radius from a_lattice / K.

    a_B = c × t_hop / (24/φ³)

    Returns dict with prediction, CODATA value, and error.
    """
    a_B = A_LATTICE / K_BRIDGE
    error_pct = abs(a_B - _A_BOHR_CODATA) / _A_BOHR_CODATA * 100
    return {
        'a_B_predicted': a_B,
        'a_B_codata': _A_BOHR_CODATA,
        'error_pct': round(error_pct, 4),
        'formula': 'c × t_hop × φ³ / 24',
        'K': K_BRIDGE,
    }


def predict_electron_mass():
    """Predict m_e from the attosecond bridge.

    m_e = ℏ × K / (a_lattice × c × α)
        = ℏ × 24 × N × W / (φ³ × c² × t_hop)

    Returns dict with prediction, CODATA value, and error.
    """
    m_e = HBAR * K_BRIDGE / (A_LATTICE * C_LIGHT * ALPHA_PRED)
    error_pct = abs(m_e - _M_E_CODATA) / _M_E_CODATA * 100

    # Decompose the error: how much comes from K vs α
    # If we used CODATA α, what would m_e be?
    alpha_codata = 1.0 / 137.035999084
    m_e_with_codata_alpha = HBAR * K_BRIDGE / (A_LATTICE * C_LIGHT * alpha_codata)
    err_from_K = abs(m_e_with_codata_alpha - _M_E_CODATA) / _M_E_CODATA * 100

    return {
        'm_e_predicted': m_e,
        'm_e_codata': _M_E_CODATA,
        'error_pct': round(error_pct, 4),
        'error_from_K_alone': round(err_from_K, 4),
        'error_from_alpha': round(error_pct - err_from_K, 4),
        'formula': 'ℏ × 24 × N × W / (φ³ × c² × t_hop)',
        'alpha_used': ALPHA_PRED,
    }


def predict_proton_mass():
    """Predict m_p using the framework proton/electron ratio.

    m_p/m_e ≈ 3 × D × φ² = 1830.0  (0.33% from 1836.15)

    Returns dict with prediction, CODATA value, and error.
    """
    m_e = predict_electron_mass()['m_e_predicted']
    mp_me_framework = 3 * D * PHI**2
    m_p = m_e * mp_me_framework
    error_pct = abs(m_p - _M_P_CODATA) / _M_P_CODATA * 100

    return {
        'm_p_predicted': m_p,
        'm_p_codata': _M_P_CODATA,
        'error_pct': round(error_pct, 4),
        'mp_me_framework': round(mp_me_framework, 2),
        'mp_me_observed': round(_MP_ME_RATIO, 2),
        'mp_me_error_pct': round(
            abs(mp_me_framework - _MP_ME_RATIO) / _MP_ME_RATIO * 100, 3),
        'formula': 'm_e × 3 × D × φ²',
    }


def alternative_K_formulas():
    """All K formulas within 0.3% of target, ranked by error.

    These are independent routes to K — any one suffices.
    """
    from core.spectrum import R_MATTER, R_INNER, R_PHOTO, R_SHELL, R_OUTER
    from core.constants import LORENTZ_W, BREATHING, metallic_mean

    DELTA_7 = metallic_mean(7)
    K_target = A_LATTICE / _A_BOHR_CODATA

    formulas = [
        ('24/φ³', 24.0 / PHI**3),
        ('N^(1/3)/ρ₆²', N_BRACKETS**(1/3) / RHO6**2),
        ('φ⁴ × BREATHING × δ₇', PHI**4 * BREATHING * DELTA_7),
        ('5π × R_PHOTO', 5 * math.pi * R_PHOTO),
        ('(D-1)^(1/3)/ρ₆', (D-1)**(1/3) / RHO6),
        ('5/LORENTZ_W', 5.0 / LORENTZ_W),
        ('D^(1/3)/ρ₆', D**(1/3) / RHO6),
    ]

    results = []
    for name, val in formulas:
        err = abs(val - K_target) / K_target * 100
        results.append({'formula': name, 'value': round(val, 6), 'error_pct': round(err, 4)})

    results.sort(key=lambda x: x['error_pct'])
    return results
