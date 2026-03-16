# First 3D AAH Eigenstates at Metallic Mean Frequencies

## Experimental Record — March 16, 2026

**Thomas A. Husmann | iBuilt LTD**

---

## Setup

Three-dimensional Aubry-André-Harper Hamiltonian at the self-dual critical point V = 2J, constructed as the tensor sum of three 1D AAH Hamiltonians:

$$H_{3D} = H_x \otimes I \otimes I + I \otimes H_y \otimes I + I \otimes I \otimes H_z$$

Each 1D Hamiltonian:

$$H\psi(n) = J[\psi(n+1) + \psi(n-1)] + V\cos(2\pi\alpha \cdot n)\psi(n)$$

with J = 1, V = 2 (critical point).

Lattice size: N = 13 sites per axis (13³ = 2197 total states).

N = 13 was chosen because 13 = F(7), the seventh Fibonacci number and the discriminant of the bronze metallic mean (Δ₃ = 3² + 4 = 13).

## Frequencies

| Axis | Metallic mean | n | Frequency α = 1/δ_n |
|---|---|---|---|
| x | Silver | 2 | 0.4142 (= √2 − 1) |
| y | Gold | 1 | 0.6180 (= 1/φ) |
| z | Bronze | 3 | 0.3028 (= (√13−3)/2) |

## Method

- Sparse matrix construction using `scipy.sparse.kron` and `scipy.sparse.diags`
- 20 eigenstates nearest to E = 0 found via shift-invert Lanczos (`scipy.sparse.linalg.eigsh`, sigma=0)
- Eigenvectors reshaped to 3D density |ψ(x,y,z)|²
- Radial profile computed from lattice center (site 6,6,6), binned by distance

## Experiment 1: Isotropic Bronze

All three axes set to α_bronze = 0.3028.

**Eigenvalues nearest E = 0:**

0.0033, 0.0033, 0.0033, 0.0033, 0.0033

(Five-fold near-degeneracy at E ≈ 0.003)

**Radial density profile (state closest to E = 0):**

| r/R | ρ(r) | Cantor node ratio |
|---|---|---|
| 0.083 | 0.000001 | 0.073 (core) |
| 0.250 | 0.000094 | 0.235 (inner wall) |
| 0.417 | 0.000342 | 0.397 (shell) |
| 0.583 | 0.000533 | 0.559 (outer wall) |
| 0.750 | 0.000436 | — |
| 0.917 | 0.000174 | — |

**Observation:** Density increases from core to outer wall, peaks at r/R ≈ 0.583 (near the Cantor outer wall ratio 0.559), then decreases beyond.

## Experiment 2: Anisotropic (Silver / Gold / Bronze)

x-axis: α_silver = 0.4142, y-axis: α_gold = 0.6180, z-axis: α_bronze = 0.3028.

**Eigenvalues nearest E = 0:**

0.0013, −0.0032, −0.0036, −0.0081, −0.0081

(Degeneracy broken — five distinct eigenvalues)

**Radial density profile (state closest to E = 0):**

| r/R | ρ(r) |
|---|---|
| 0.083 | 0.000016 |
| 0.250 | 0.000021 |
| 0.417 | 0.000132 |
| 0.583 | 0.000308 |
| 0.750 | 0.000608 |
| 0.917 | 0.000565 |

**Observation:** Density peaks at r/R ≈ 0.750, shifted outward compared to isotropic case. The three different frequencies break spherical symmetry.

## Experiment 3: Factorization Test

Question: Are the eigenvalues of the isotropic bronze Hamiltonian (α_bronze on all three axes) the same as the anisotropic Hamiltonian (α_silver, α_gold, α_bronze)?

**Result:** 20/20 eigenvalues near E = 0 matched within tolerance 0.01.

**Observation:** At N = 13, the near-zero eigenvalues of the isotropic and anisotropic systems overlap. This is consistent with bronze being a combination of silver and gold, but N = 13 provides only 6 radial bins and minimal Cantor hierarchy depth. The test needs repetition at N = 34 and N = 55 to be conclusive.

## What Was Computed

- First-ever 3D AAH eigenstates at three distinct metallic mean frequencies
- Radial density profiles of the lowest-energy states near E = 0
- Comparison between isotropic (single frequency) and anisotropic (three frequencies) configurations
- Eigenvalue overlap test between configurations

## What Was Not Computed

- Chern numbers of the 3D bands
- Higher-N convergence (N = 34, 55, 233)
- Angular density profiles (orbital structure)
- Comparison with hydrogen radial wavefunctions
- Band-edge identification in the full 3D spectrum
- Time evolution or dynamics

## Code

The computation is fully contained in `atoms_from_scratch.py` (Python 3, requires NumPy and SciPy). Runs in < 1 second on any modern machine at N = 13.

Repository: https://github.com/thusmann5327/Unified_Theory_Physics

---

*Recorded March 16, 2026. No interpretation beyond the stated observations.*
