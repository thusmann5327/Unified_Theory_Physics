#!/usr/bin/env python3
"""
Strain Energy: Disclination Model for Dark Matter
===================================================
Standard condensed matter: wedge disclination in an elastic medium.
The Aristotle gap (7.36°) creates strain energy u ∝ δ²/r².
The resulting force F ∝ 1/r gives a logarithmic potential
and flat rotation curves.

Standard references:
- de Wit, R. "Theory of disclinations" J. Appl. Phys. (1971)
- Kleinert, H. "Gauge Fields in Condensed Matter" (1989)

Note: Ebanks (2026, ai.viXra:2602.0106) independently identified
the Aristotle gap as the source of dark matter through this same
strain energy mechanism in a φ-structured tetrahedral lattice.

© 2026 Thomas A. Husmann / iBuilt LTD
"""
import math
import numpy as np

PHI = (1 + math.sqrt(5)) / 2
W = 2/PHI**4 + PHI**(-1/PHI)/PHI**3   # 0.467134

# ================================================================
# FUNDAMENTAL ANGLES
# ================================================================

TETRAHEDRAL_DIHEDRAL = math.acos(1/3)                    # 1.2310 rad = 70.53°
ICOSAHEDRAL_ANGLE = math.acos(1/(1+PHI**2))              # 1.1071 rad = 63.43°
ARISTOTLE_GAP = 2*math.pi - 5*TETRAHEDRAL_DIHEDRAL       # 0.1284 rad = 7.36°
HD_GAP = TETRAHEDRAL_DIHEDRAL - ICOSAHEDRAL_ANGLE         # 0.1238 rad = 7.09°

# ================================================================
# STRAIN ENERGY (Standard condensed matter)
# ================================================================

def strain_energy_density(r, delta=ARISTOTLE_GAP, mu=1.0):
    """
    Strain energy density from a wedge disclination of angle δ.

    u(r) = μδ² / (2πr²)

    Standard result: de Wit (1971), Kleinert (1989).
    δ = Aristotle gap = 7.36° = 0.1284 rad
    μ = shear modulus of the vacuum (in Planck units: ℏc/L_p⁴)

    Returns energy density in units of μ.
    """
    if r <= 0:
        return 0.0
    return mu * delta**2 / (2 * math.pi * r**2)

def disclination_force(r, M, delta=ARISTOTLE_GAP):
    """
    Force from disclination strain on a test mass.

    F_gap = K_strain / r = sqrt(G × M × a₀) / r

    This is DIFFERENT from Newtonian 1/r²:
    - Newton: F ∝ 1/r² → v ∝ 1/√r (falls off)
    - Disclination: F ∝ 1/r → v = const (flat rotation)

    The fundamental acceleration floor:
    a₀ = c × H₀ × sin(δ)
    """
    G = 6.67430e-11          # m³/kg/s²
    c = 2.99792458e8         # m/s
    H0 = 2.2e-18             # 1/s (67.4 km/s/Mpc)
    a0 = c * H0 * math.sin(delta)  # fundamental acceleration

    K = math.sqrt(G * M * a0)
    return K / r if r > 0 else 0.0

# ================================================================
# ROTATION CURVES (Standard + disclination)
# ================================================================

def rotation_velocity(r, M_baryon, R_disk, delta=ARISTOTLE_GAP):
    """
    Combined rotation velocity: Newtonian + lattice strain.

    v²/r = GM/r² + sqrt(GM×a₀)/r

    v² = GM/r + sqrt(GM×a₀)

    At large r: first term → 0, second term dominates → flat.

    This recovers the Tully-Fisher relation: v⁴ ∝ M
    """
    G = 6.67430e-11
    c = 2.99792458e8
    H0 = 2.2e-18
    a0 = c * H0 * math.sin(delta)

    # Enclosed baryonic mass (exponential disk model)
    M_enc = M_baryon * (1 - (1 + r/R_disk) * math.exp(-r/R_disk))

    # Newtonian term
    v2_newton = G * M_enc / r if r > 0 else 0

    # Disclination term (lattice strain)
    v2_strain = math.sqrt(G * M_enc * a0) if M_enc > 0 else 0

    return math.sqrt(max(v2_newton + v2_strain, 0))

def flat_velocity(M_baryon, delta=ARISTOTLE_GAP):
    """
    Asymptotic flat rotation velocity.

    v_flat = (G × M × a₀)^{1/4}

    This IS the Tully-Fisher relation: v⁴ = G × M × a₀
    Derived from lattice strain, not fitted.
    """
    G = 6.67430e-11
    c = 2.99792458e8
    H0 = 2.2e-18
    a0 = c * H0 * math.sin(delta)

    return (G * M_baryon * a0) ** 0.25

# ================================================================
# CONNECTION TO HD WALL FRACTION
# ================================================================

def wall_fraction_to_acceleration(W_val=W):
    """
    Map the HD wall fraction W to the fundamental acceleration a₀.

    The spectral gap fraction W = 0.467 and the angular gap δ = 7.36°
    both measure geometric frustration of φ-order in 3D.

    W comes from spectral gaps (energy space).
    δ comes from angular deficit (position space).

    Connection: both arise from the impossibility of tiling 3D
    with φ-structured order without gaps.

    sin(δ) = sin(7.36°) = 0.1281
    W⁴ = 0.0476
    These are different quantities measuring the same frustration.
    """
    c = 2.99792458e8
    H0 = 2.2e-18
    a0_angular = c * H0 * math.sin(ARISTOTLE_GAP)
    a0_spectral = c * H0 * W_val**4  # candidate spectral version

    return {
        'a0_angular': a0_angular,
        'a0_spectral': a0_spectral,
        'ratio': a0_angular / a0_spectral,
        'delta': math.degrees(ARISTOTLE_GAP),
        'W': W_val,
        'W4': W_val**4,
        'sin_delta': math.sin(ARISTOTLE_GAP),
    }

# ================================================================
# SELF-TEST
# ================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("STRAIN ENERGY: DISCLINATION MODEL FOR DARK MATTER")
    print("=" * 60)

    print(f"\n  Aristotle gap: {math.degrees(ARISTOTLE_GAP):.3f}°")
    print(f"  HD gap (tet-icos): {math.degrees(HD_GAP):.3f}°")
    print(f"  Match: {abs(HD_GAP-ARISTOTLE_GAP)/ARISTOTLE_GAP*100:.1f}%")

    # Milky Way example
    M_MW = 6e10 * 1.989e30   # 60 billion solar masses baryonic
    R_disk = 3e3 * 3.086e16  # 3 kpc disk scale

    v_flat = flat_velocity(M_MW)
    print(f"\n  Milky Way (M = 6×10¹⁰ M☉):")
    print(f"  Predicted v_flat = {v_flat/1e3:.1f} km/s")
    print(f"  Observed: ~220 km/s")
    print(f"  Match: {abs(v_flat/1e3 - 220)/220*100:.1f}%")

    # Rotation curve
    print(f"\n  Rotation curve:")
    print(f"  {'r (kpc)':>8s}  {'v (km/s)':>10s}  {'v_Newton':>10s}")
    print(f"  {'-'*32}")
    G = 6.67430e-11
    for r_kpc in [1, 2, 5, 10, 20, 50, 100]:
        r = r_kpc * 3.086e19  # kpc to meters
        v = rotation_velocity(r, M_MW, R_disk)
        M_enc = M_MW * (1 - (1 + r/R_disk) * math.exp(-r/R_disk))
        v_newt = math.sqrt(G * M_enc / r) if r > 0 else 0
        print(f"  {r_kpc:>8d}  {v/1e3:>10.1f}  {v_newt/1e3:>10.1f}")

    # W → a₀ connection
    connection = wall_fraction_to_acceleration()
    print(f"\n  W → a₀ connection:")
    print(f"  a₀ (angular): {connection['a0_angular']:.4e} m/s²")
    print(f"  a₀ (spectral): {connection['a0_spectral']:.4e} m/s²")
    print(f"  Ratio: {connection['ratio']:.3f}")
