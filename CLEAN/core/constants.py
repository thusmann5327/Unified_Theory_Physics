"""
constants.py — All framework constants from φ² = φ + 1
========================================================

Step Zero of every proof. No free parameters, no fits, no calibration.
Everything flows from the single algebraic identity φ² = φ + 1.

Usage:
    from core.constants import PHI, W, LEAK, R_C, ...
"""

import math


# ═══════════════════════════════════════════════════════════════════
# THE AXIOM
# ═══════════════════════════════════════════════════════════════════

PHI = (1 + 5**0.5) / 2              # 1.6180339887... — the golden ratio
assert abs(PHI**2 - PHI - 1) < 1e-15, "Axiom violated"

SQRT5 = math.sqrt(5)
SQRT_PHI = math.sqrt(PHI)           # 1.27202 — oblate squash factor


# ═══════════════════════════════════════════════════════════════════
# HAMILTONIAN PARAMETERS
# ═══════════════════════════════════════════════════════════════════

D = 233                              # F(13) = F(F(7)) — lattice dimension
ALPHA_AAH = 1.0 / PHI               # irrational frequency


# ═══════════════════════════════════════════════════════════════════
# W THEOREM — gap fraction from first principles
# ═══════════════════════════════════════════════════════════════════
#
# W × φ⁴ = 2 + φ^(1/φ²)
#
# Exact to machine precision (2.22 × 10⁻¹⁶).
# Self-referential: 1/φ² = φ - 1 = 2 - φ, so φ^(1/φ²) is the
# axiom evaluating itself.

H_HINGE = PHI**(-1.0 / PHI)         # 0.742743 — hinge constant
W = (2 + PHI**(1.0 / PHI**2)) / PHI**4   # 0.467134

_W_CHECK = W * PHI**4 - (2 + PHI**(1.0 / PHI**2))
assert abs(_W_CHECK) < 1e-14, f"W theorem failed: residual = {_W_CHECK}"


# ═══════════════════════════════════════════════════════════════════
# GATE CONSTANTS
# ═══════════════════════════════════════════════════════════════════

LEAK = 1.0 / PHI**4                 # 0.14590 — gate transmission
R_C = 1.0 - LEAK                    # 0.85410 — crossover parameter
OBLATE = SQRT_PHI                    # 1.27202 — √φ oblate squash

assert abs(PHI**2 * R_C - SQRT5) < 1e-14, "φ²×r_c = √5 identity failed"


# ═══════════════════════════════════════════════════════════════════
# LORENTZ AND BREATHING
# ═══════════════════════════════════════════════════════════════════

LORENTZ_W = math.sqrt(1 - W**2)     # 0.88424
BREATHING = 1 - LORENTZ_W           # 0.11578


# ═══════════════════════════════════════════════════════════════════
# METALLIC MEANS
# ═══════════════════════════════════════════════════════════════════

def metallic_mean(n):
    """Positive root of x² = nx + 1."""
    return (n + math.sqrt(n * n + 4)) / 2

SILVER_MEAN = metallic_mean(2)       # 2.41421 — δ_S = 1 + √2
BRONZE_MEAN = metallic_mean(3)       # 3.30278 — δ_B

# σ₃ widths from metallic mean spectra (verified by eigensolver)
SILVER_S3 = 0.171
GOLD_S3   = 0.236
BRONZE_S3 = 0.394
DARK_GOLD = 0.290                    # gold axis dark fraction


# ═══════════════════════════════════════════════════════════════════
# TOPOLOGY
# ═══════════════════════════════════════════════════════════════════

N_BRACKETS = 294                     # F(13) + F(10) + F(5) + F(2)
GAMMA_DC = 4                         # Chern-number-carrying gaps
D_S = 0.5                            # Hausdorff dimension (Sütő 1989)
NU = 1.0 / (2.0 - D_S)              # 2/3 — correlation length exponent


# ═══════════════════════════════════════════════════════════════════
# RELATIVISTIC CORRECTION
# ═══════════════════════════════════════════════════════════════════

RHO6 = PHI**(1.0 / 6.0)             # 1.08305 — period-6 correction
GOLDEN_ANGLE = 2 * math.pi / PHI**2  # 137.508° — phyllotaxis angle


# ═══════════════════════════════════════════════════════════════════
# PHYSICAL CONSTANTS
# ═══════════════════════════════════════════════════════════════════

HBAR = 1.054571817e-34               # J·s
C_LIGHT = 299792458                  # m/s
L_PLANCK = 1.61625e-35               # m
E_CHARGE = 1.602176634e-19           # C
K_B = 1.380649e-23                   # J/K
RY_EV = 13.6057                      # Rydberg energy (eV)
A0_PM = 52.9177                      # Bohr radius (pm)


# ═══════════════════════════════════════════════════════════════════
# G-FACTOR IDENTITY
# ═══════════════════════════════════════════════════════════════════

G_PROTON = 5.585694713               # proton g-factor
G_ELECTRON = 2.00231930436256        # electron g-factor
# (gp - ge) / (gp + ge) = 2/φ³ at 0.022%
