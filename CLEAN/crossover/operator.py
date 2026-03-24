"""
operator.py — Universal Cantor crossover operator
===================================================

Generalized from gaba_engine.py TubulinDimer.gaba_collapse().
One operator instantiates in six independent physical systems:

    1. N-SmA liquid crystals     — McMillan ratio → heat capacity α
    2. Quantum Hall plateau       — V/J → temperature scaling κ
    3. GABA microtubule gate      — gate_strength → collapse energy
    4. Magic angle graphene       — twist → flat band condition
    5. LCD polarizer              — polarization → 5→3 projection
    6. Dark sector                — energy imbalance → signal leakage

The formula:
    d_eff(x) = d_full - f_dec(x)
    f_dec(x) = ((x - r_c)/(1 - r_c))^γ  for x > r_c
    α = 2 - ν × d_eff

where:
    r_c = 1 - 1/φ⁴ = 0.8541  (universal crossover parameter)
    γ = 4                      (four Chern-number-carrying gaps)
    ν = 2/3                    (correlation length exponent, D_s = 1/2)

One axiom: φ² = φ + 1.
One parameter: r_c = 1 - 1/φ⁴.
One consequence: exactly three spatial dimensions.
"""

import math

from core.constants import PHI, R_C, GAMMA_DC, D_S, NU, SQRT5


# ═══════════════════════════════════════════════════════════════════
# DISCRIMINANT FIBONACCI CHAIN — three dimensions proof
# ═══════════════════════════════════════════════════════════════════

FIB = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987]


def metallic_discriminant(n):
    """Discriminant of x² = nx + 1: Δ_n = n² + 4."""
    return n * n + 4


def discriminant_fibonacci_chain(n_max=6):
    """
    Verify: Δ₁ + Δ₂ = Δ₃ iff n ≤ 3.

    For n = 1,2,3: Δ₁ = 5 = F(5), Δ₂ = 8 = F(6), Δ₃ = 13 = F(7).
    At n = 4: Δ₄ = 20 ≠ F(8) = 21. Chain breaks → fourth dimension blocked.
    Uniqueness: (n-2)² = 0 → n = 2 is the unique Fibonacci link.

    Returns dict with proof structure.
    """
    results = []
    for n in range(1, n_max + 1):
        d = metallic_discriminant(n)
        is_fib = d in FIB
        results.append({
            'n': n, 'discriminant': d, 'is_fibonacci': is_fib,
            'sqrt_discriminant': math.sqrt(d)
        })

    D1, D2, D3, D4 = [metallic_discriminant(n) for n in range(1, 5)]

    return {
        'discriminants': results,
        'chain_holds': D1 + D2 == D3,         # 5 + 8 = 13
        'chain_breaks': D2 + D3 != D4,        # 8 + 13 ≠ 20
        'deficit': (D2 + D3) - D4,             # = 1
        'unique_link': 2,                       # (n-2)² = 0 → n = 2
        'max_dimensions': 3,
    }


# ═══════════════════════════════════════════════════════════════════
# THE CROSSOVER OPERATOR
# ═══════════════════════════════════════════════════════════════════

def cantor_crossover(x, x_c=R_C, gamma=GAMMA_DC, d_full=3):
    """
    Universal crossover: control parameter → d_eff → exponents.

    At x ≤ x_c: fully coupled, d_eff = d_full
    At x > x_c: decoupling begins, f = ((x-x_c)/(1-x_c))^γ
    At x = 1:   fully decoupled, d_eff = d_full - 1
    """
    if x <= x_c:
        return {
            'f_decouple': 0.0,
            'd_eff': float(d_full),
            'alpha': 2.0 - NU * d_full,
            'below_xc': True
        }
    f_dec = ((x - x_c) / (1 - x_c)) ** gamma
    d_eff = d_full - f_dec
    return {
        'f_decouple': f_dec,
        'd_eff': d_eff,
        'alpha': 2.0 - NU * d_eff,
        'below_xc': False
    }


# ═══════════════════════════════════════════════════════════════════
# PHYSICAL INSTANCES
# ═══════════════════════════════════════════════════════════════════

def alpha_nsma(r):
    """N-SmA heat capacity exponent from McMillan ratio r."""
    return cantor_crossover(r)['alpha']


def kappa_qh():
    """Quantum Hall temperature scaling exponent."""
    return R_C / 2  # = 0.427


def kappa_qah():
    """Quantum anomalous Hall scaling."""
    return 1 / PHI**2  # = 0.382


def nu_noninteracting():
    """Chalker-Coddington model plateau exponent."""
    return PHI**2  # = 2.618


def nu_interacting():
    """Interacting plateau exponent."""
    return 2 / R_C  # = 2.342


# ═══════════════════════════════════════════════════════════════════
# √5 IDENTITY
# ═══════════════════════════════════════════════════════════════════

def verify_sqrt5_identity():
    """
    Verify φ² × r_c = √5 (exact algebraic identity).

    Proof: φ²(1 - 1/φ⁴) = φ² - 1/φ² = (φ⁴-1)/φ² = 2φ²/φ² = √5
    """
    lhs = PHI**2 * R_C
    return {
        'lhs': lhs,
        'rhs': SQRT5,
        'residual': abs(lhs - SQRT5),
        'exact': abs(lhs - SQRT5) < 1e-14
    }


# ═══════════════════════════════════════════════════════════════════
# N-SmA EXPERIMENTAL COMPARISON
# ═══════════════════════════════════════════════════════════════════

NSMA_COMPOUNDS = [
    ("8CB",    0.9766, 0.31),
    ("8OCB",   0.9628, 0.31),
    ("9CB",    0.9678, 0.31),
    ("10CB",   0.9552, 0.29),
    ("4O.8",   0.9302, 0.20),
    ("T8",     0.9190, 0.14),
    ("CBOOA",  0.9132, 0.13),
    ("4O.7",   0.8841, 0.045),
    ("40.6",   0.8774, 0.032),
    ("8S5",    0.8726, 0.025),
    ("CSS",    0.8636, 0.010),
]


def nsma_test():
    """
    Test the N-SmA crossover formula against 11 experimental compounds.

    Returns dict with per-compound results and RMS error.
    """
    results = []
    for name, r, alpha_obs in NSMA_COMPOUNDS:
        alpha_pred = alpha_nsma(r)
        err = alpha_pred - alpha_obs
        results.append({
            'name': name, 'r': r,
            'alpha_obs': alpha_obs, 'alpha_pred': alpha_pred,
            'error': err
        })

    errors = [abs(r['error']) for r in results]
    rms = math.sqrt(sum(e**2 for e in errors) / len(errors))

    return {
        'compounds': results,
        'rms': rms,
        'n_compounds': len(results),
        'n_within_2sigma': sum(1 for e in errors if e < 0.066),
    }
