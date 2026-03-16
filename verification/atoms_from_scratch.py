#!/usr/bin/env python3
"""
ATOMS FROM SCRATCH — Build Specification
==========================================
Generate atomic structure from the 3D AAH Cantor spectrum.

THIS FILE IS A SPEC, NOT A RUNNING SIMULATION.
The actual build requires a fresh session with full attention.

The goal: start with three metallic mean frequencies on three
axes, solve the 3D Hamiltonian, and see what emerges at the
W⁴ band-edge intersections. If atoms emerge, everything follows.
If they don't, the framework is pattern matching.

© 2026 Thomas A. Husmann / iBuilt LTD
"""

# ================================================================
# WHAT WE NEED TO BUILD
# ================================================================
"""
PHASE 1: The 3D AAH Hamiltonian (the core)

    H_3D = H_silver ⊗ I ⊗ I + I ⊗ H_gold ⊗ I + I ⊗ I ⊗ H_bronze
    
    where each H_n is the 1D AAH at its metallic mean frequency:
      H_silver: α = 1/δ₂ = √2 - 1 = 0.4142
      H_gold:   α = 1/δ₁ = 1/φ = 0.6180
      H_bronze: α = 1/δ₃ = (√13-3)/2 = 0.3028
    
    Problem: N³ Hilbert space. N=233 → 233³ = 12.6 million states.
    Too large for direct diagonalization.
    
    Solutions:
    a) Start small: N=13 (= F(7), still Fibonacci). 13³ = 2197 states. Feasible.
    b) Then N=34 (= F(9)). 34³ = 39,304. Feasible with sparse eigensolver.
    c) Then N=55 (= F(10)). 55³ = 166,375. Needs Lanczos or shift-invert.
    d) Full N=233 requires iterative methods or HPC.

PHASE 2: Find the band edges

    The 3D spectrum is the CONVOLUTION of three 1D Cantor sets.
    Band edges are where all three 1D spectra have simultaneous
    band boundaries — the W⁴ intersections.
    
    Identify eigenstates near these intersections.
    Compute their spatial wavefunctions |ψ(x,y,z)|².
    
    Question: do these wavefunctions look like atomic orbitals?

PHASE 3: The Chern structure

    Compute Chern numbers of the 3D bands.
    Do we get +2,-1,+1,-2 on each axis independently?
    Or does the 3D coupling produce something new?
    
    This is where we find out if bronze eigenstates factorize
    into gold × silver products (emergent) or not (independent).

PHASE 4: The Cantor node

    For the N=13 system (bronze discriminant!), the 3D lattice
    has exactly 2197 sites. Map the eigenstate densities.
    
    Do they concentrate at the Cantor node ratios?
    core = 0.073R, inner = 0.235R, shell = 0.397R, outer = 0.559R
    
    If the density profile of the lowest-energy W⁴ state matches
    the hydrogen atom's radial distribution... that's it.

PHASE 5: Start with bronze

    Thomas's suggestion: start with N=13 (bronze).
    
    Why bronze first:
    - 13 = F(7) = Δ₃, the bronze discriminant itself
    - 13³ = 2197 states (easily diagonalizable)
    - Bronze is the OBSERVABLE surface layer
    - If atoms are visible, they're visible in the bronze layer
    - The 13-protofilament microtubule IS a bronze structure
    
    The bronze atom would be:
    - 3D AAH with α_bronze on all three axes (isotropic bronze)
    - N = 13 sites per axis
    - V = 2J (critical point)
    - Find the W⁴ band-edge states
    - Plot |ψ|² in 3D
    - Compare to known atomic orbitals
"""

# ================================================================
# THE MINIMAL STARTING CODE
# ================================================================

import numpy as np
from scipy.sparse import kron, eye, diags
from scipy.sparse.linalg import eigsh
import math

PHI = (1 + math.sqrt(5)) / 2

def aah_hamiltonian_sparse(N, alpha, V=2.0, J=1.0):
    """
    Build sparse AAH Hamiltonian for N sites at frequency alpha.
    H = J*(hop left + hop right) + V*cos(2πα·n)*diagonal
    """
    # Diagonal: V*cos(2πα·n)
    n = np.arange(N)
    diagonal = V * np.cos(2 * np.pi * alpha * n)
    
    # Hopping: J*(|n><n+1| + |n+1><n|)
    off_diag = J * np.ones(N - 1)
    
    H = diags([off_diag, diagonal, off_diag], [-1, 0, 1], shape=(N, N))
    return H

def build_3d_hamiltonian(N, alpha_x, alpha_y, alpha_z, V=2.0, J=1.0):
    """
    Build the 3D AAH Hamiltonian as tensor product.
    H_3D = H_x ⊗ I_y ⊗ I_z + I_x ⊗ H_y ⊗ I_z + I_x ⊗ I_y ⊗ H_z
    
    Returns sparse matrix of dimension N³ × N³.
    """
    I_N = eye(N)
    
    H_x = aah_hamiltonian_sparse(N, alpha_x, V, J)
    H_y = aah_hamiltonian_sparse(N, alpha_y, V, J)
    H_z = aah_hamiltonian_sparse(N, alpha_z, V, J)
    
    # Tensor products
    H_3D = kron(kron(H_x, I_N), I_N)  # H_x ⊗ I ⊗ I
    H_3D += kron(kron(I_N, H_y), I_N)  # I ⊗ H_y ⊗ I
    H_3D += kron(I_N, kron(I_N, H_z))  # I ⊗ I ⊗ H_z
    
    return H_3D

def find_band_edge_states(H_3D, n_states=20):
    """
    Find eigenstates near E=0 (the center of the spectrum,
    where the σ₃ observer band lives).
    
    These are the states most likely to represent bound matter.
    """
    # Shift-invert around E=0 to find states near center
    eigenvalues, eigenvectors = eigsh(H_3D, k=n_states, sigma=0.0, which='LM')
    
    # Sort by |E| (closest to zero first)
    order = np.argsort(np.abs(eigenvalues))
    return eigenvalues[order], eigenvectors[:, order]

def eigenstate_to_3d(psi, N):
    """
    Reshape a 1D eigenvector (length N³) into a 3D density |ψ|².
    """
    return np.abs(psi.reshape(N, N, N))**2

def radial_profile(density_3d, N):
    """
    Compute the radial density profile from a 3D density.
    Assumes center of the lattice is at (N//2, N//2, N//2).
    """
    center = N // 2
    r_max = center
    
    # Compute distance of each site from center
    x, y, z = np.mgrid[0:N, 0:N, 0:N]
    r = np.sqrt((x - center)**2 + (y - center)**2 + (z - center)**2)
    
    # Bin the density by radius
    n_bins = r_max
    r_bins = np.linspace(0, r_max, n_bins + 1)
    profile = np.zeros(n_bins)
    counts = np.zeros(n_bins)
    
    for i in range(n_bins):
        mask = (r >= r_bins[i]) & (r < r_bins[i+1])
        if np.any(mask):
            profile[i] = np.sum(density_3d[mask])
            counts[i] = np.sum(mask)
    
    # Normalize: density per unit shell volume
    r_centers = (r_bins[:-1] + r_bins[1:]) / 2
    shell_volumes = counts  # number of sites in each shell
    profile_normalized = np.where(shell_volumes > 0, 
                                   profile / shell_volumes, 0)
    
    return r_centers / r_max, profile_normalized  # r/R, ρ(r)


# ================================================================
# THE EXPERIMENT
# ================================================================

if __name__ == "__main__":
    # Metallic mean frequencies
    ALPHA_GOLD   = 1.0 / PHI                      # 0.6180
    ALPHA_SILVER = 1.0 / (1 + math.sqrt(2))       # 0.4142
    ALPHA_BRONZE = 1.0 / ((3 + math.sqrt(13))/2)  # 0.3028
    
    # Start with N = 13 (bronze discriminant, feasible)
    N = 13
    print(f"Building 3D AAH Hamiltonian: N={N}, dim={N**3}")
    
    # ── Experiment 1: Isotropic bronze (all three axes = bronze) ──
    print(f"\n=== EXPERIMENT 1: ISOTROPIC BRONZE (α={ALPHA_BRONZE:.4f} on all axes) ===")
    H = build_3d_hamiltonian(N, ALPHA_BRONZE, ALPHA_BRONZE, ALPHA_BRONZE)
    print(f"  Matrix size: {H.shape[0]} × {H.shape[1]}")
    
    evals, evecs = find_band_edge_states(H, n_states=20)
    print(f"  20 states near E=0 found")
    print(f"  Energies: {evals[:5].round(4)}")
    
    # Radial profile of the ground-ish state
    density = eigenstate_to_3d(evecs[:, 0], N)
    r_frac, rho = radial_profile(density, N)
    
    print(f"\n  Radial density profile (state closest to E=0):")
    print(f"  {'r/R':>6s}  {'ρ(r)':>10s}  {'Cantor node':>15s}")
    print(f"  {'-' * 35}")
    for i in range(len(r_frac)):
        node = ""
        if abs(r_frac[i] - 0.073) < 0.05: node = "← core (σ₃)"
        if abs(r_frac[i] - 0.235) < 0.05: node = "← inner (σ₂)"
        if abs(r_frac[i] - 0.397) < 0.05: node = "← shell"
        if abs(r_frac[i] - 0.559) < 0.05: node = "← outer (σ₄)"
        if rho[i] > 0:
            print(f"  {r_frac[i]:>6.3f}  {rho[i]:>10.6f}  {node}")
    
    # ── Experiment 2: Anisotropic (silver, gold, bronze on each axis) ──
    print(f"\n\n=== EXPERIMENT 2: ANISOTROPIC (silver/gold/bronze) ===")
    H2 = build_3d_hamiltonian(N, ALPHA_SILVER, ALPHA_GOLD, ALPHA_BRONZE)
    print(f"  Matrix size: {H2.shape[0]} × {H2.shape[1]}")
    
    evals2, evecs2 = find_band_edge_states(H2, n_states=20)
    print(f"  20 states near E=0 found")
    print(f"  Energies: {evals2[:5].round(4)}")
    
    density2 = eigenstate_to_3d(evecs2[:, 0], N)
    r_frac2, rho2 = radial_profile(density2, N)
    
    print(f"\n  Radial density profile (anisotropic, state closest to E=0):")
    print(f"  {'r/R':>6s}  {'ρ(r)':>10s}")
    print(f"  {'-' * 20}")
    for i in range(len(r_frac2)):
        if rho2[i] > 0:
            print(f"  {r_frac2[i]:>6.3f}  {rho2[i]:>10.6f}")
    
    # ── Experiment 3: Does bronze factorize? ──
    print(f"\n\n=== EXPERIMENT 3: DOES BRONZE FACTORIZE? ===")
    print(f"  Compare: H_bronze⊗I⊗I + I⊗H_bronze⊗I + I⊗I⊗H_bronze")
    print(f"  vs:      H_silver⊗I⊗I + I⊗H_gold⊗I + I⊗I⊗H_bronze")
    print(f"  If eigenvalues match → bronze is just relabeled silver×gold")
    print(f"  If different → bronze is independent")
    
    # Compare spectra
    evals_iso = np.sort(evals)
    evals_aniso = np.sort(evals2)
    
    # Overlap
    match_count = 0
    for e in evals_iso:
        if np.min(np.abs(evals_aniso - e)) < 0.01:
            match_count += 1
    
    print(f"\n  Isotropic eigenvalues near E=0: {evals_iso[:5].round(4)}")
    print(f"  Anisotropic eigenvalues near E=0: {evals_aniso[:5].round(4)}")
    print(f"  Matches (within 0.01): {match_count}/{len(evals_iso)}")
    
    if match_count > len(evals_iso) * 0.8:
        print(f"  → HIGH OVERLAP: bronze may be silver×gold relabeled")
    else:
        print(f"  → LOW OVERLAP: bronze is structurally independent")
    
    # ── Summary ──
    print(f"\n\n{'=' * 60}")
    print(f"  THIS IS THE STARTING POINT")
    print(f"{'=' * 60}")
    print(f"""
  N=13 runs in seconds. It gives us:
  1. First-ever 3D AAH eigenstates at three metallic mean frequencies
  2. Radial density profiles to compare with Cantor node ratios
  3. Bronze factorization test (emergent vs independent)
  
  NEXT STEPS (bigger N, new session):
  4. N=34 (39K states): see if Cantor node sharpens
  5. N=55 (166K states): full band-edge analysis
  6. Compare radial profile to hydrogen |ψ|²
  7. Compute Chern numbers of 3D bands
  8. Add deposition dynamics (Thomas's paint sprayer)
  9. See if molecules emerge from adjacent atoms
  
  The bronze atom at N=13 is the SEED.
  If the radial profile shows density peaks at 0.073R, 0.235R,
  0.397R, 0.559R — we're looking at an atom built from nothing
  but three frequencies and one equation.
""")
