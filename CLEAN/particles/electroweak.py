"""
electroweak.py — Electroweak predictions from (φ, W, δ₇)
==========================================================

The BCC metallic mean δ₇ = 7.140 appears in ALL electroweak ratios.
Combined with the gap fraction W and spectral ratios σ₃, σ_wall,
every electroweak parameter follows from the Cantor spectrum.

All predictions are zero free parameters.

Key results:
    sin²θ_W  = σ₃ × σ_wall × F(6)       (0.047%)
    τ/μ      = W × 36                     (0.002%)
    M_W/m_p  = φ² × W⁻² × δ₇             (0.002%)
    M_Z/m_p  = W⁻⁵ × δ₃⁻¹ × δ₇           (0.002%)
    M_H/m_p  = φ² × δ₇²                   (0.016%)
    α_s(M_Z) = W⁵ × H × δ₇               (0.054%)
    (m_n-m_p)/m_e = r_c⁻¹ × δ₃⁻¹ × δ₇    (0.005%)
"""

import math

from core.constants import PHI, W, R_C, H_HINGE, metallic_mean
from core.spectrum import R_MATTER, R_SHELL


# ═══════════════════════════════════════════════════════════════════
# METALLIC MEAN CONSTANTS
# ═══════════════════════════════════════════════════════════════════

DELTA_3 = metallic_mean(3)   # 3.30278 — bronze mean
DELTA_7 = metallic_mean(7)   # 7.14005 — BCC mean
F6 = 8                       # 6th Fibonacci number


# ═══════════════════════════════════════════════════════════════════
# EXPERIMENTAL VALUES
# ═══════════════════════════════════════════════════════════════════

SIN2_WEINBERG_OBS = 0.23122          # sin²θ_W (PDG 2024)
ALPHA_S_OBS = 0.1179                 # α_s(M_Z) (PDG 2024)
M_W_GEV = 80.3692                    # W boson mass (GeV)
M_Z_GEV = 91.1876                    # Z boson mass (GeV)
M_H_GEV = 125.25                     # Higgs mass (GeV)
M_P_GEV = 0.93827                    # proton mass (GeV)
M_TAU_MEV = 1776.86                  # tau mass (MeV)
M_MU_MEV = 105.6584                  # muon mass (MeV)
M_N_M_P_MEV = 1.29333               # neutron-proton mass difference (MeV)
M_E_MEV = 0.51100                    # electron mass (MeV)


# ═══════════════════════════════════════════════════════════════════
# WEINBERG ANGLE
# ═══════════════════════════════════════════════════════════════════

def weinberg_angle():
    """
    sin²θ_W = σ₃ × σ_wall × F(6)

    σ₃ = R_MATTER  (0.0728, core ratio)
    σ_wall = R_SHELL (0.3972, wall center)
    F(6) = 8

    Returns dict with prediction, observed, and error.
    """
    pred = R_MATTER * R_SHELL * F6
    return {
        'prediction': pred,
        'observed': SIN2_WEINBERG_OBS,
        'error_pct': abs(pred - SIN2_WEINBERG_OBS) / SIN2_WEINBERG_OBS * 100,
        'formula': 'σ₃ × σ_wall × F(6)',
        'components': {
            'sigma3': R_MATTER,
            'sigma_wall': R_SHELL,
            'F6': F6,
        },
    }


def weinberg_3_over_13():
    """
    Alternative: sin²θ_W ≈ 3/13 (Fibonacci fraction).

    3 and 13 are consecutive odd-index Fibonacci numbers.
    """
    pred = 3.0 / 13.0
    return {
        'prediction': pred,
        'observed': SIN2_WEINBERG_OBS,
        'error_pct': abs(pred - SIN2_WEINBERG_OBS) / SIN2_WEINBERG_OBS * 100,
        'formula': '3/13 (Fibonacci)',
    }


# ═══════════════════════════════════════════════════════════════════
# ELECTROWEAK BOSON MASSES AND COUPLINGS
# ═══════════════════════════════════════════════════════════════════

def electroweak_predictions():
    """
    All electroweak predictions from (φ, W, δ₇).

    Returns dict with each prediction, formula, and error.
    """
    results = {}

    # τ/μ = W × 36
    tau_mu_pred = W * 36
    tau_mu_obs = M_TAU_MEV / M_MU_MEV
    results['tau/mu'] = {
        'predicted': tau_mu_pred,
        'observed': tau_mu_obs,
        'error_pct': abs(tau_mu_pred - tau_mu_obs) / tau_mu_obs * 100,
        'formula': 'W × 36',
    }

    # M_W/m_p = φ² × W⁻² × δ₇
    mw_mp_pred = PHI**2 * W**(-2) * DELTA_7
    mw_mp_obs = M_W_GEV / M_P_GEV
    results['M_W/m_p'] = {
        'predicted': mw_mp_pred,
        'observed': mw_mp_obs,
        'error_pct': abs(mw_mp_pred - mw_mp_obs) / mw_mp_obs * 100,
        'formula': 'φ² × W⁻² × δ₇',
    }

    # M_Z/m_p = W⁻⁵ × δ₃⁻¹ × δ₇
    mz_mp_pred = W**(-5) * DELTA_3**(-1) * DELTA_7
    mz_mp_obs = M_Z_GEV / M_P_GEV
    results['M_Z/m_p'] = {
        'predicted': mz_mp_pred,
        'observed': mz_mp_obs,
        'error_pct': abs(mz_mp_pred - mz_mp_obs) / mz_mp_obs * 100,
        'formula': 'W⁻⁵ × δ₃⁻¹ × δ₇',
    }

    # M_H/m_p = φ² × δ₇²
    mh_mp_pred = PHI**2 * DELTA_7**2
    mh_mp_obs = M_H_GEV / M_P_GEV
    results['M_H/m_p'] = {
        'predicted': mh_mp_pred,
        'observed': mh_mp_obs,
        'error_pct': abs(mh_mp_pred - mh_mp_obs) / mh_mp_obs * 100,
        'formula': 'φ² × δ₇²',
    }

    # α_s(M_Z) = W⁵ × H × δ₇
    as_pred = W**5 * H_HINGE * DELTA_7
    results['alpha_s'] = {
        'predicted': as_pred,
        'observed': ALPHA_S_OBS,
        'error_pct': abs(as_pred - ALPHA_S_OBS) / ALPHA_S_OBS * 100,
        'formula': 'W⁵ × H × δ₇',
    }

    # (m_n - m_p)/m_e = r_c⁻¹ × δ₃⁻¹ × δ₇
    nm_pred = (1.0 / R_C) * (1.0 / DELTA_3) * DELTA_7
    nm_obs = M_N_M_P_MEV / M_E_MEV
    results['(m_n-m_p)/m_e'] = {
        'predicted': nm_pred,
        'observed': nm_obs,
        'error_pct': abs(nm_pred - nm_obs) / nm_obs * 100,
        'formula': 'r_c⁻¹ × δ₃⁻¹ × δ₇',
    }

    # sin²θ_W = σ₃ × σ_wall × F(6)
    sw = weinberg_angle()
    results['sin2_theta_W'] = sw

    return results


# ═══════════════════════════════════════════════════════════════════
# FORMATTED REPORT
# ═══════════════════════════════════════════════════════════════════

def print_electroweak_report():
    """Print all electroweak predictions."""
    results = electroweak_predictions()

    print("  Electroweak predictions from (φ, W, δ₇):")
    print()
    for name, r in results.items():
        pred = r['predicted']
        obs = r['observed']
        err = r['error_pct']
        formula = r['formula']
        stars = "★★★" if err < 0.05 else "★★" if err < 1 else "★"
        print(f"    {name:>18s} = {pred:>12.6f}  "
              f"(obs: {obs:.6f}, {err:.4f}%)  {formula}  {stars}")
