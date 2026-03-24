"""
predictions.py — Cosmological predictions from (φ, W, N)
==========================================================

Four hierarchy predictions from three constants:
    1. Fine structure:    α⁻¹ = N × W = 137.3           (0.22%)
    2. Baryon fraction:   Ω_b = W⁴ = 0.048              (2.8%)
    3. Gravity weakness:  (√(1-W²)/φ)^136 = 10⁻³⁵·⁷     (1.1% log)
    4. Cosmological Λ:    (1/φ)^588 = 10⁻¹²²·⁹           (0.7% log)

Plus: W-polynomial dark energy budget (sums to exactly 1).
Plus: MOND acceleration a₀ = c²/(l_P × φ^295).

Physical mechanism:
    EM:      counts Cantor walls → linear    → α⁻¹ = N×W = 137
    Gravity: propagates through channels → exponential → 10⁻³⁶
    Vacuum:  decays through bare lattice → deeper exponential → 10⁻¹²³
"""

import math

from core.constants import (
    PHI, W, LORENTZ_W, N_BRACKETS,
    C_LIGHT, L_PLANCK
)


# ═══════════════════════════════════════════════════════════════════
# FINE STRUCTURE CONSTANT
# ═══════════════════════════════════════════════════════════════════

def fine_structure():
    """α⁻¹ = N × W where N = 294 (bracket count), W = gap fraction."""
    pred = N_BRACKETS * W
    obs = 137.036
    return {
        'prediction': pred,
        'observed': obs,
        'error_pct': abs(pred - obs) / obs * 100,
        'formula': 'N × W = 294 × 0.4671'
    }


# ═══════════════════════════════════════════════════════════════════
# W-POLYNOMIAL COSMOLOGICAL BUDGET
# ═══════════════════════════════════════════════════════════════════

def w_polynomial_budget():
    """
    Dark energy budget as a W-polynomial (sums to exactly 1).

    Ω_DE = W² + W    = 0.6853  (Planck: 0.685, 0.05%)
    Ω_b  = W⁴        = 0.0476  (Planck: 0.049, 2.8%)
    Ω_DM = 1-W⁴-W²-W = 0.2671  (Planck: 0.266, 0.4%)
    """
    omega_de = W**2 + W
    omega_b = W**4
    omega_dm = 1 - omega_b - W**2 - W

    return {
        'omega_de': omega_de,
        'omega_b': omega_b,
        'omega_dm': omega_dm,
        'total': omega_de + omega_b + omega_dm,
        'planck_de': 0.685,
        'planck_b': 0.049,
        'planck_dm': 0.266,
        'err_de_pct': abs(omega_de - 0.685) / 0.685 * 100,
        'err_b_pct': abs(omega_b - 0.049) / 0.049 * 100,
        'err_dm_pct': abs(omega_dm - 0.266) / 0.266 * 100,
    }


# ═══════════════════════════════════════════════════════════════════
# GRAVITY HIERARCHY
# ═══════════════════════════════════════════════════════════════════

def gravity_hierarchy():
    """
    G/F_EM = (√(1-W²)/φ)^(4×F(9)) = (√(1-W²)/φ)^136

    Physical basis: gravity propagates through 136 acoustic channels
    (4 × 34 gaps = 4 × F(9)), each attenuating by √(1-W²)/φ.
    """
    transmission = LORENTZ_W / PHI
    exponent = 4 * 34  # = 136
    ratio = transmission ** exponent

    return {
        'ratio': ratio,
        'log10': math.log10(ratio),
        'observed_log10': -36.1,
        'error_log_pct': abs(math.log10(ratio) - (-36.1)) / 36.1 * 100,
        'transmission_per_bracket': transmission,
        'exponent': exponent,
    }


# ═══════════════════════════════════════════════════════════════════
# COSMOLOGICAL CONSTANT
# ═══════════════════════════════════════════════════════════════════

def cosmological_constant():
    """
    Λ/Λ_Planck = (1/φ)^(2N) = (1/φ)^588

    Physical basis: vacuum energy decays through 2N = 588 brackets
    of bare lattice, each damping by 1/φ.
    """
    exponent = 2 * N_BRACKETS  # = 588
    ratio = (1.0 / PHI) ** exponent

    return {
        'ratio': ratio,
        'log10': math.log10(ratio),
        'observed_log10': -122.0,
        'error_log_pct': abs(math.log10(ratio) - (-122.0)) / 122.0 * 100,
        'exponent': exponent,
    }


# ═══════════════════════════════════════════════════════════════════
# MOND ACCELERATION
# ═══════════════════════════════════════════════════════════════════

def mond_acceleration():
    """
    a₀ = c²/(l_P × φ^(N+1)) = c²/(l_P × φ^295)

    Bracket N+1 = first bracket beyond Hubble horizon.
    """
    a0 = C_LIGHT**2 / (L_PLANCK * PHI**(N_BRACKETS + 1))
    obs = 1.2e-10

    return {
        'a0': a0,
        'observed': obs,
        'error_pct': abs(a0 - obs) / obs * 100,
    }


# ═══════════════════════════════════════════════════════════════════
# FORMATTED REPORT
# ═══════════════════════════════════════════════════════════════════

def print_cosmology_report():
    """Print all cosmological predictions."""
    fs = fine_structure()
    budget = w_polynomial_budget()
    grav = gravity_hierarchy()
    cosmo = cosmological_constant()
    mond = mond_acceleration()

    print(f"  Fine structure:    1/alpha = {fs['prediction']:.3f}  "
          f"(CODATA: {fs['observed']}, {fs['error_pct']:.2f}%)")

    print(f"\n  W-polynomial budget (sums to 1.000):")
    print(f"    Omega_DE = W^2+W = {budget['omega_de']:.4f}  "
          f"(Planck: {budget['planck_de']}, {budget['err_de_pct']:.2f}%)")
    print(f"    Omega_DM         = {budget['omega_dm']:.4f}  "
          f"(Planck: {budget['planck_dm']}, {budget['err_dm_pct']:.1f}%)")
    print(f"    Omega_b  = W^4   = {budget['omega_b']:.5f}  "
          f"(Planck: {budget['planck_b']}, {budget['err_b_pct']:.1f}%)")
    print(f"    Total            = {budget['total']:.6f}")

    print(f"\n  Gravity hierarchy:")
    print(f"    G/F_EM = (sqrt(1-W^2)/phi)^136 = 10^{grav['log10']:.1f}  "
          f"(observed: 10^{grav['observed_log10']}, {grav['error_log_pct']:.1f}% log)")

    print(f"\n  Cosmological constant:")
    print(f"    Lambda/Lambda_P = (1/phi)^588 = 10^{cosmo['log10']:.1f}  "
          f"(observed: 10^{cosmo['observed_log10']}, {cosmo['error_log_pct']:.1f}% log)")

    print(f"\n  MOND acceleration:")
    print(f"    a0 = c^2/(l_P*phi^295) = {mond['a0']:.3e} m/s^2  "
          f"(observed: {mond['observed']:.1e}, {mond['error_pct']:.1f}%)")
