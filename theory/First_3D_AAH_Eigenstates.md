# 3D AAH Eigenstates — N=13 vs N=34 Comparison

## Experimental Record — March 16, 2026

**Thomas A. Husmann | iBuilt LTD**

---

## Setup

3D AAH at V=2J, tensor sum of three 1D Hamiltonians. Two configurations at each N:

- **Isotropic bronze:** α = 0.3028 on all three axes
- **Anisotropic:** α_silver = 0.4142 (x), α_gold = 0.6180 (y), α_bronze = 0.3028 (z)

Eigenstates nearest E = 0 via shift-invert Lanczos. Radial density from lattice center.

---

## N = 13 (2,197 states, 0.2s)

### Isotropic Bronze — E = 0.003 (degenerate)

| r/R | ρ(r) |
|---|---|
| 0.042 | 0.000002 |
| 0.208 | 0.000097 |
| 0.375 | 0.000289 |
| **0.458** | **0.000940** ← peak |
| 0.625 | 0.000601 |
| 0.792 | 0.000379 |
| 0.958 | 0.000217 |

Peak at r/R ≈ 0.46. Broad distribution, middle-to-outer.

### Anisotropic — E = 0.001, −0.003, −0.004 (broken degeneracy)

| r/R | ρ(r) |
|---|---|
| 0.042 | 0.000016 |
| 0.375 | 0.000118 |
| 0.625 | 0.000527 |
| **0.792** | **0.000922** ← peak |
| 0.958 | 0.000443 |

Peak at r/R ≈ 0.79. Pushed outward.

---

## N = 34 (39,304 states, 19–39s)

### Isotropic Bronze — E = 0.000 (degenerate, closer to zero)

| r/R | ρ(r) |
|---|---|
| **0.029** | **0.000479** ← peak 1 |
| 0.088 | 0.000355 |
| 0.147 | 0.000267 |
| 0.206 | 0.000127 |
| 0.265 | 0.000431 |
| **0.324** | **0.000587** ← peak 2 |
| 0.382 | 0.000192 |
| 0.500 | 0.000124 |
| 0.618 | 0.000042 |
| 0.794 | 0.000011 |
| 0.971 | 0.000003 |

Two peaks: core (r/R ≈ 0.03) and shell (r/R ≈ 0.32). Monotonic falloff beyond. State localizes at center.

### Anisotropic — E ≈ 0.000 (near-degenerate)

| r/R | ρ(r) |
|---|---|
| 0.029 | 0.000000 |
| 0.206 | 0.000000 |
| 0.382 | 0.000002 |
| 0.559 | 0.000004 |
| 0.676 | 0.000014 |
| 0.794 | 0.000028 |
| 0.912 | 0.000021 |
| **0.971** | **0.000048** ← peak |

Density at the edge. Monotonic increase center to surface. This is a surface/edge state.

---

## Observations

1. **N=13 and N=34 give qualitatively different profiles.** The N=13 result is not a scaled version of N=34. The Cantor hierarchy changes character as more levels develop.

2. **Isotropic bronze at N=34 localizes at center with two peaks.** Peaks at r/R ≈ 0.03 and ≈ 0.32. Suggestive of core + shell structure. Does not align precisely with Cantor ratios 0.073 and 0.235 — resolution may be insufficient, or the structure may be different from the 1D prediction.

3. **Anisotropic at N=34 is a surface state.** When three different frequencies are used, the E ≈ 0 state localizes at the lattice boundary. This may be a topological edge state or finite-size artifact.

4. **Eigenvalues converge to E = 0 with increasing N.** N=13: E ≈ 0.003. N=34: E ≈ 0.000. Band-edge states sharpen as Cantor hierarchy deepens.

5. **The two configurations diverge at N=34.** At N=13 they overlapped. At N=34 they are qualitatively different (center-localized vs edge-localized). Bronze may not factorize at sufficient depth.

---

## Next Steps

- N = 55 (166K states, ~5–10 min): do the two peaks in isotropic bronze sharpen toward Cantor ratios?
- N = 89 (705K states, ~1 hr): full convergence test
- Angular profiles: does the anisotropic state show orbital-like angular structure?
- Multiple eigenstates: are there s-like, p-like, d-like states in the near-E=0 spectrum?
- Chern numbers of the 3D bands

---

*Recorded March 16, 2026.*
*Code: atoms_from_scratch.py, atoms_n34.py*
