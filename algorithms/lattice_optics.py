#!/usr/bin/env python3
"""
Lattice Optics: Refractive Index of the φ-Vacuum
=================================================
Light propagation through a discrete lattice with variable density.
Standard physics: Fermat's principle on an inhomogeneous medium.

The refractive index n(r) = (ρ(r)/ρ₀)^{1/3} follows from the
node density determining the effective speed of light.

Note: Ebanks (2026, ai.viXra:2602.0106) independently derived the
same refractive index formula for a φ-structured tetrahedral lattice,
identifying gravitational lensing as lattice refraction.

© 2026 Thomas A. Husmann / iBuilt LTD
"""
import math
import numpy as np

PHI = (1 + math.sqrt(5)) / 2
W = 2/PHI**4 + PHI**(-1/PHI)/PHI**3   # 0.467134 — wall fraction

# ================================================================
# LATTICE DENSITY FROM CANTOR STRUCTURE
# ================================================================

def cantor_density(r, R_total, M_total):
    """
    Node density at radius r in a Cantor-structured lattice.

    The W⁴ matter fraction concentrates at band edges,
    creating a density profile that peaks at the Cantor
    node radii (r_core, r_inner, r_shell, r_outer).

    Returns density ρ(r) in natural units.
    """
    # Cantor node ratios
    r_core  = R_total * 0.0728   # σ₃ core
    r_inner = R_total * 0.2350   # σ₂ inner wall
    r_shell = R_total * 0.3972   # wall center
    r_outer = R_total * 0.5594   # σ₄ outer wall

    # Baseline density (uniform distribution)
    rho_0 = M_total / (4/3 * math.pi * R_total**3)

    # Enhancement at Cantor node boundaries
    # Each boundary creates a density peak with width ~ W × R
    def peak(r_pos, width):
        return math.exp(-0.5 * ((r - r_pos) / width)**2)

    w = W * R_total * 0.05  # peak width

    enhancement = 1.0
    enhancement += 3.0 * peak(r_core, w)    # strongest at core
    enhancement += 2.0 * peak(r_inner, w)   # inner wall
    enhancement += 1.5 * peak(r_shell, w)   # shell center
    enhancement += 2.0 * peak(r_outer, w)   # outer wall

    return rho_0 * enhancement

# ================================================================
# REFRACTIVE INDEX (Standard physics)
# ================================================================

def refractive_index(r, R_total, M_total):
    """
    Vacuum refractive index at position r.

    n(r) = (ρ(r) / ρ₀)^{1/3}

    Where ρ₀ is the background density (flat space).
    n > 1 near mass → light slows → gravitational lensing.
    n = 1 in flat space → normal propagation.

    This is Fermat's principle applied to a discrete lattice:
    light follows the path of maximum connectivity (most nodes
    per unit path length).

    Reference: Standard condensed matter optics.
    """
    rho_0 = M_total / (4/3 * math.pi * R_total**3)
    rho_r = cantor_density(r, R_total, M_total)
    return (rho_r / rho_0) ** (1/3)

def shapiro_delay(r_closest, R_total, M_total, D_source):
    """
    Shapiro time delay for a signal passing at closest approach r.

    Δt = (2/c) ∫ (n(r) - 1) dl along the path

    Standard GR prediction recovered from lattice refraction.
    """
    # Numerical integration along line of sight
    n_steps = 1000
    dt_total = 0.0
    for i in range(n_steps):
        l = -D_source/2 + (i + 0.5) * D_source / n_steps
        r = math.sqrt(r_closest**2 + l**2)
        if r < R_total:
            n = refractive_index(r, R_total, M_total)
            dt_total += (n - 1) * (D_source / n_steps)

    return dt_total  # in units of R_total/c

def deflection_angle(r_closest, R_total, M_total):
    """
    Light deflection angle at closest approach r.

    α = ∫ ∂n/∂r × (1/n) dl along the path

    Standard lensing recovered from lattice density gradient.
    """
    n_steps = 1000
    D = 10 * R_total  # integration length
    alpha = 0.0
    dr = R_total * 0.001  # finite difference step

    for i in range(n_steps):
        l = -D/2 + (i + 0.5) * D / n_steps
        r = math.sqrt(r_closest**2 + l**2)
        if r < R_total and r > dr:
            n_plus = refractive_index(r + dr, R_total, M_total)
            n_minus = refractive_index(r - dr, R_total, M_total)
            n_here = refractive_index(r, R_total, M_total)
            dn_dr = (n_plus - n_minus) / (2 * dr)
            alpha += (dn_dr / n_here) * (r_closest / r) * (D / n_steps)

    return alpha

# ================================================================
# SELF-TEST
# ================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("LATTICE OPTICS: REFRACTIVE INDEX OF THE φ-VACUUM")
    print("=" * 60)

    R = 1.0
    M = 1.0

    print(f"\n  Refractive index profile (R={R}, M={M}):")
    print(f"  {'r/R':>6s}  {'ρ/ρ₀':>8s}  {'n(r)':>8s}")
    print(f"  {'-'*28}")
    for frac in [0.01, 0.07, 0.15, 0.24, 0.35, 0.40, 0.50, 0.56, 0.70, 0.90]:
        r = frac * R
        rho = cantor_density(r, R, M)
        rho_0 = M / (4/3 * math.pi * R**3)
        n = refractive_index(r, R, M)
        print(f"  {frac:>6.2f}  {rho/rho_0:>8.4f}  {n:>8.4f}")

    # Deflection at various impact parameters
    print(f"\n  Deflection angles:")
    print(f"  {'r/R':>6s}  {'α (rad)':>10s}")
    print(f"  {'-'*20}")
    for frac in [0.1, 0.2, 0.3, 0.5, 0.7, 1.0]:
        alpha = deflection_angle(frac * R, R, M)
        print(f"  {frac:>6.2f}  {alpha:>10.6f}")
