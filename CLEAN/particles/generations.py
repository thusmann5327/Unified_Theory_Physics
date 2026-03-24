"""
generations.py — Three generations of fermion masses
=====================================================

Key results:
    t/c  = 136 = 4 × F(9)     (0.023%)  — gravity hierarchy exponent
    τ/μ  = W × 36              (0.002%)  — gap fraction × 36
    c/u  = N × 2 = 588         (0.006%)  — bracket count × 2
    s/d  = 5 × 4 = 20          (0.000%)  — exact integer

Koide formula:
    (m_e + m_μ + m_τ) / (√m_e + √m_μ + √m_τ)² = 2/3 = ν
    The Koide ratio IS the correlation length exponent of the
    Cantor lattice, where D_s = 1/2 (Sütő 1989).
"""

import math

from core.constants import PHI, W, N_BRACKETS, D, NU


# ═══════════════════════════════════════════════════════════════════
# EXPERIMENTAL MASSES (MeV/c²)
# ═══════════════════════════════════════════════════════════════════

LEPTON_MASSES = {'e': 0.51099895, 'mu': 105.6584, 'tau': 1776.86}
UP_QUARK_MASSES = {'u': 2.16, 'c': 1270.0, 't': 172760.0}
DOWN_QUARK_MASSES = {'d': 4.67, 's': 93.4, 'b': 4180.0}

# Neutrino mass-squared differences (eV²)
DM2_21 = 7.53e-5
DM2_32 = 2.453e-3


# ═══════════════════════════════════════════════════════════════════
# GENERATION MASS RATIOS
# ═══════════════════════════════════════════════════════════════════

def generation_ratios():
    """
    Compute all inter-generation mass ratios.

    Returns dict with each ratio, its value, best framework match,
    and error percentage.
    """
    ratios = {}

    # Lepton ratios
    mu_e = LEPTON_MASSES['mu'] / LEPTON_MASSES['e']
    tau_mu = LEPTON_MASSES['tau'] / LEPTON_MASSES['mu']
    tau_e = LEPTON_MASSES['tau'] / LEPTON_MASSES['e']

    # Up-type quark ratios
    c_u = UP_QUARK_MASSES['c'] / UP_QUARK_MASSES['u']
    t_c = UP_QUARK_MASSES['t'] / UP_QUARK_MASSES['c']

    # Down-type quark ratios
    s_d = DOWN_QUARK_MASSES['s'] / DOWN_QUARK_MASSES['d']
    b_s = DOWN_QUARK_MASSES['b'] / DOWN_QUARK_MASSES['s']

    # Neutrino
    dm2_ratio = DM2_32 / DM2_21

    # Framework constants for matching
    delta7 = (7 + math.sqrt(7**2 + 4)) / 2  # BCC metallic mean

    matches = {
        'mu/e': {
            'value': mu_e,
            'match': 'φ⁷ × δ₇',
            'predicted': PHI**7 * delta7,
        },
        'tau/mu': {
            'value': tau_mu,
            'match': 'W × 36',
            'predicted': W * 36,
        },
        'tau/e': {
            'value': tau_e,
            'match': 'φ¹³ × D/M',
            'predicted': PHI**13 * D / (D - 1),  # approximate
        },
        'c/u': {
            'value': c_u,
            'match': 'N × 2',
            'predicted': N_BRACKETS * 2,
        },
        't/c': {
            'value': t_c,
            'match': '4 × F(9) = 136',
            'predicted': 4 * 34,
        },
        's/d': {
            'value': s_d,
            'match': '5 × 4 = 20',
            'predicted': 20,
        },
        'b/s': {
            'value': b_s,
            'match': '21/W',
            'predicted': 21 / W,
        },
        'dm2_32/dm2_21': {
            'value': dm2_ratio,
            'match': 'D/δ₇',
            'predicted': D / delta7,
        },
    }

    for key, m in matches.items():
        m['error_pct'] = abs(m['value'] - m['predicted']) / m['value'] * 100

    return matches


# ═══════════════════════════════════════════════════════════════════
# t/c = 136 TEST
# ═══════════════════════════════════════════════════════════════════

def top_charm_ratio():
    """
    Test: t/c = 136 = 4 × F(9).

    The top-to-charm mass ratio encodes the gravity hierarchy exponent.
    Gravity: (√(1-W²)/φ)^136 = 10⁻³⁵·⁷
    Top quark: m_t = 136 × m_c

    Returns dict with ratio, target, and error.
    """
    ratio = UP_QUARK_MASSES['t'] / UP_QUARK_MASSES['c']
    target = 4 * 34  # = 136

    return {
        'ratio': ratio,
        'target': target,
        'formula': '4 × F(9) = 136',
        'error_pct': abs(ratio - target) / target * 100,
        'connection': 'gravity hierarchy exponent',
    }


# ═══════════════════════════════════════════════════════════════════
# KOIDE FORMULA
# ═══════════════════════════════════════════════════════════════════

def koide_formula():
    """
    Koide formula: (m_e + m_μ + m_τ) / (√m_e + √m_μ + √m_τ)² = 2/3.

    Framework connection:
        ν = 1/(2 - D_s) = 1/(2 - 0.5) = 2/3
        D_s = 1/2 is the Hausdorff dimension of the AAH spectrum (Sütő 1989).
        The Koide ratio IS the correlation length exponent of the Cantor lattice.
    """
    m_e = LEPTON_MASSES['e']
    m_mu = LEPTON_MASSES['mu']
    m_tau = LEPTON_MASSES['tau']

    numerator = m_e + m_mu + m_tau
    denominator = (math.sqrt(m_e) + math.sqrt(m_mu) + math.sqrt(m_tau))**2
    Q = numerator / denominator

    return {
        'Q': Q,
        'target': 2.0 / 3.0,
        'nu': NU,
        'error_pct': abs(Q - 2.0/3.0) / (2.0/3.0) * 100,
        'framework': 'ν = 1/(2 - D_s), D_s = 1/2 (Sütő 1989)',
    }


# ═══════════════════════════════════════════════════════════════════
# φ-POWER HYPOTHESIS
# ═══════════════════════════════════════════════════════════════════

def phi_power_exponents():
    """
    If m₂/m₁ = φ^a, find a = ln(ratio)/ln(φ) for each generation pair.

    Notable: μ/e ≈ φ¹¹, τ/μ ≈ φ⁶, τ/e ≈ φ¹⁷.
    Lepton ladder: 11 + 6 = 17 (additive consistency).
    """
    ln_phi = math.log(PHI)

    pairs = {
        'mu/e': LEPTON_MASSES['mu'] / LEPTON_MASSES['e'],
        'tau/mu': LEPTON_MASSES['tau'] / LEPTON_MASSES['mu'],
        'tau/e': LEPTON_MASSES['tau'] / LEPTON_MASSES['e'],
        'c/u': UP_QUARK_MASSES['c'] / UP_QUARK_MASSES['u'],
        't/c': UP_QUARK_MASSES['t'] / UP_QUARK_MASSES['c'],
        's/d': DOWN_QUARK_MASSES['s'] / DOWN_QUARK_MASSES['d'],
        'b/s': DOWN_QUARK_MASSES['b'] / DOWN_QUARK_MASSES['s'],
    }

    results = {}
    for name, ratio in pairs.items():
        a = math.log(ratio) / ln_phi
        nearest = round(a)
        phi_err = abs(ratio - PHI**nearest) / ratio * 100
        results[name] = {
            'ratio': ratio,
            'exponent': a,
            'nearest_int': nearest,
            'phi_int_error_pct': phi_err,
        }

    # Check lepton additivity: a(τ/e) ≈ a(μ/e) + a(τ/μ)
    a_sum = results['mu/e']['nearest_int'] + results['tau/mu']['nearest_int']
    results['lepton_additivity'] = {
        'sum': a_sum,
        'tau_e_nearest': results['tau/e']['nearest_int'],
        'consistent': a_sum == results['tau/e']['nearest_int'],
    }

    return results


# ═══════════════════════════════════════════════════════════════════
# FORMATTED REPORT
# ═══════════════════════════════════════════════════════════════════

def print_generations_report():
    """Print generation mass ratio analysis."""
    ratios = generation_ratios()

    print("  Generation mass ratios:")
    for name, r in ratios.items():
        stars = "★★★" if r['error_pct'] < 0.05 else "★★" if r['error_pct'] < 1 else "★"
        print(f"    {name:>15s} = {r['value']:>10.2f}  →  {r['match']:>20s}"
              f"  = {r['predicted']:.2f}  ({r['error_pct']:.3f}%)  {stars}")

    tc = top_charm_ratio()
    print(f"\n  t/c = {tc['ratio']:.4f} = {tc['formula']}  ({tc['error_pct']:.3f}%)")

    k = koide_formula()
    print(f"\n  Koide: Q = {k['Q']:.6f}  (target 2/3 = {k['target']:.6f},"
          f" error {k['error_pct']:.4f}%)")
    print(f"         ν = {k['nu']:.6f}  ({k['framework']})")
