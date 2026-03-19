# Speed of Light: What the Framework Can and Cannot Derive

**Thomas A. Husmann | iBuilt LTD**
**March 19, 2026**

**Status: CLOSED. The numerical value of c cannot be derived from the spectrum. This is proven, not a gap to be filled. Do not revisit.**

---

## 1. The Question

Can the speed of light c = 299,792,458 m/s be derived from the AAH spectrum at V = 2J, α = 1/φ, without inputting c through calibration of the lattice parameters l₀ and J?

## 2. The Answer

**No.** This was verified by adversarial analysis (Grok, xAI, March 19 2026) and confirmed by systematic exploration of seven independent approaches (Claude, Anthropic, March 18–19 2026).

The circularity is fundamental: Planck units contain c (l_P/t_P ≡ c), so any length/time bracket ratio recovers c trivially. No function f(φ, W, N) produces c without re-introducing Planck units or measured lengths/times.

## 3. What Was Tried

### 3.1 Bracket Ratio (CIRCULAR)

Pre-1983, the meter was defined by the Earth's quadrant and the second by the caesium-133 hyperfine transition. Both have bracket depths:

| Quantity | Bracket depth (n = log_φ(x/x_P)) |
|---|---|
| Earth quadrant (10,002 km) | 199.97 |
| Meter (1 m) | 166.48 |
| Bohr radius (0.529 Å) | 117.30 |
| Cs period (1.088×10⁻¹⁰ s) | 159.36 |
| One second | 207.04 |
| Cs energy (inverted) | 155.54 |

φ^(n_Earth − n_Cs) ≈ 3.067 × 10⁸ looks like c. But algebraically it IS c: L_Earth/(c × T_Cs) = φ^(n_L − n_Cs) by the definition of brackets. The Planck units have c baked in.

### 3.2 Planck Unit Constraint (TAUTOLOGICAL)

In Planck units: l₀ = n_φ l_P, J = m_φ E_P. Then c = 2m_φ n_φ (E_P l_P/ℏ) = 2m_φ n_φ c. This gives n_φ × m_φ = 1/2 — a constraint, not a derivation.

### 3.3 Entanglement vs Local Time (CIRCULAR)

Entangled channel: τ_corr = ℏ/J. Local channel: τ_prop = l₀/c. Ratio: τ_prop/τ_corr = Jl₀/(cℏ) = 1/2 by Lieb-Robinson. Gives c = 2Jl₀/ℏ again.

### 3.4 Spectral Bandwidth (DIMENSIONLESS)

The AAH bandwidth at D = 233 is 5.195 (in units of J). This is dimensionless. To get a physical energy requires J in eV, which requires a mass/energy scale, which requires c.

### 3.5 σ₄ Entropy for l₀ (PARTIAL — reduces to one parameter)

S(σ₄) = 0.6908 nats is a spectral quantity. Via Bekenstein-Hawking: l₀ = 2√S(σ₄) × l_P = 1.662 l_P. This eliminates one of two calibration parameters. But l_P contains c, so c remains as the single irreducible input.

### 3.6 Maxwell: c = 1/√(μ₀ε₀) (CIRCULAR)

ε₀ and μ₀ bracket depths require Planck-scale permittivity/permeability references, which loop through c. Maxwell's relation is definitional in the units.

### 3.7 Base Independence (CONFIRMED)

Any logarithmic base (e, 2, 10, φ) gives analogous bracket ratios that rescale to the same physical quantities. The φ base is motivated by the AAH spectrum (α = 1/φ criticality, Fibonacci scaling) and adds genuine predictive power for dimensionless quantities (α, Ω_b, etc.). But for c it adds nothing.

## 4. Why the Circularity Is Fundamental

c sets the ratio between length and time units. It is a dimensional conversion factor, not a dimensionless number. In natural units (ℏ = c = 1), c = 1 by definition and there is nothing to derive.

The question "why is c = 299,792,458 m/s?" is equivalent to "why did we define the meter and second the way we did?" The answer is historical convention (Earth's size, caesium transitions), not physics.

The physical question is: "why is the maximum signal speed FINITE, UNIVERSAL, and FRAME-INDEPENDENT?" That question the framework DOES answer (§5 below).

## 5. What the Framework DOES Derive About c

### 5.1 c Is Finite

The lattice has finite hopping energy J. An infinite J would give infinite c. The lattice structure imposes a speed limit. Standard physics states that c is finite but does not explain why.

### 5.2 c Is Universal

At V = 2J (the self-dual critical point), the AAH Hamiltonian has a unique Lieb-Robinson velocity that is the same at every site. At any other coupling (V ≠ 2J), the velocity depends on the local potential — different speeds in different regions. Self-duality at criticality FORCES a universal speed.

### 5.3 c Is Frame-Independent

The Cantor spectrum is self-similar at every scale. Zoom into any band → same Fibonacci structure → same gap fractions → same Lieb-Robinson velocity. No preferred frame exists because no preferred scale exists.

### 5.4 c Separates Entangled and Local Propagation

From the photon's frame (ds² = 0): it traverses all brackets simultaneously, sees the full Cantor structure at once, has zero entanglement entropy (pure state).

From the observer's frame: the photon hops one bracket per quantum clock tick (τ = ℏ/J), at speed l₀/τ = Jl₀/ℏ. The factor of 2 in c = 2Jl₀/ℏ comes from forward + backward hopping on the lattice.

c is the boundary: the fastest possible local signal that still has nonzero proper time. Below c, signals have timelike worldlines and positive entropy. At c, the worldline is null and entropy is zero. Above c, propagation would be non-local (entangled channel only).

## 6. The Framework's Parameter Count

| Parameter | Status |
|---|---|
| φ = (1+√5)/2 | Axiom (φ² = φ + 1) |
| W = 0.4671 | Computed from AAH spectrum |
| N = 294 | Bracket count (uses observed Hubble radius) |
| l₀ = 1.662 l_P | Computed from S(σ₄) — spectral quantity |
| c = 299,792,458 m/s | **Irreducible input** — dimensional anchor |

One axiom. One spectral constant (W). One cosmological input (N). One spectral calibration (l₀/l_P from σ₄ entropy). One dimensional anchor (c).

The dimensional anchor is irreducible. Any framework that makes predictions in physical units must input at least one dimensionful constant to set the scale. The Husmann framework uses c. Standard physics uses c, G, ℏ, e, and ~20 more.

## 7. What Would Change This Assessment

A derivation of c from the spectrum would require one of:

1. A way to compute the Planck length WITHOUT using c (i.e., from φ alone). This seems impossible since l_P = √(ℏG/c³) involves c by definition.

2. A dimensionless quantity that ENCODES c relative to some other speed. For example, if c/v_sound_in_vacuum had a φ-expression, that would do it. But there is no "speed of sound in vacuum" to compare to.

3. A reformulation of the framework in purely dimensionless terms where c never appears. This is possible (natural units) but then c = 1 by fiat, not by derivation.

None of these paths leads anywhere. The question is settled.

---

## References

Adversarial verification: Grok (xAI), March 19, 2026. Confirmed circularity of all seven approaches. Stated: "The α, cosmological, and atomic matches in the framework are genuine... But the c derivation you asked for is not there. It remains an input."

---

*© 2026 Thomas A. Husmann / iBuilt LTD. CC BY-NC-SA 4.0.*
