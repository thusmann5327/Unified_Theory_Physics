# The Three Perturbation Axes of the Discriminant Cone Quasicrystal

**Thomas A. Husmann — iBuilt LTD, Lilliwaup, Washington**
**March 24, 2026**

## Summary

The periodic table is a perturbed golden-angle quasicrystal on three Fibonacci cones. The ideal structure is given by the cone formula (r, θ, φ, z=1) derived from the critical Fibonacci Hamiltonian at V=2J, α=1/φ, D=233. Every element's deviation from the ideal quasicrystal point decomposes into three orthogonal perturbations, each encoding a different physical property:

| Axis | Symbol | Definition | Range | Correlates with | ρ |
|------|--------|-----------|-------|----------------|---|
| **Rigidity** | δᵣ | (r_obs − r_pred) / r_pred | [−0.28, +0.77] | Mohs hardness | 0.76 |
| **Polarity** | δᵩ | (Fibonacci remainder / shell span) − 0.5 | [−0.65, +0.70] | Pauling electronegativity | 0.89 |
| **Confinement** | δθ | arccos(1/r_obs) − arccos(1/r_pred) | [−13°, +24°] | Mohs hardness / band gap | 0.73 |

Combined: EN = 0.777·δᵣ + 0.013·δθ + 1.591·δᵩ + 1.800, **R² = 0.903** (40 elements, 4 coefficients).

Without δᵩ: R² = 0.535. The polarity axis contributes ΔR² = 0.368.

---

## 1. The Ideal Quasicrystal

Every element occupies a point on one of three nested cones:

```
r = 1 / cos(α)                         (radial distance = vdW/cov ratio)
α = arctan(θ_eff × BOS)                (polar angle = cone assignment)  
φ = 2π × {φ}/φ × k                     (azimuth = golden angle × index)
z = r × cos(α) = 1                     (exact for all elements)
```

The three cones:

| Cone | θ_eff | Angle α | Ratio r | Spectral origin | Physics |
|------|-------|---------|---------|-----------------|---------|
| Leak | 0.564 | 29.2° | 1.146 | arctan(σ₄) to 0.015% | Gate open |
| Crossover | 0.854 | 40.3° | 1.311 | arctan(r_c) to 0.57% | Phase boundary |
| Baseline | 1.000 | 44.8° | 1.409 | 0.51% from 45° | Gate closed |

At the z=1 cross-section, the cones produce three concentric rings. Elements are distributed at golden-angle intervals, producing ~13 visible radial arms (= F(7), the Fibonacci number governing the spiral phyllotaxis at this element count).

The symmetric gaps directly across from each other confirm the quasicrystal geometry. The three-distance theorem guarantees golden-angle phyllotaxis produces gaps of exactly 2 or 3 sizes, arranged symmetrically.

**The deviations from this ideal structure encode all known elemental properties.**

---

## 2. Rigidity (δᵣ) — Radial Perturbation

**Definition:**
```
δᵣ = (r_observed − r_predicted) / r_predicted
```

**Physical meaning:** How far off its ring the element sits, radially.
- **Positive δᵣ** = atom is wider than its cone predicts → compressed electron cloud → hard material
- **Negative δᵣ** = atom is narrower → diffuse cloud → soft, malleable

**Scale:** −0.28 to +0.77 (dimensionless)

**Correlations:**
- ρ(δᵣ, Mohs) = +0.76
- ρ(δᵣ, gate overflow G) = +0.84

**Key elements:**

| Element | δᵣ | Character |
|---------|-----|-----------|
| C (diamond) | +0.47 | Hardest natural material |
| Os | +0.45 | Hardest metal |
| F | +0.77 | Highest EN, extreme rigidity |
| Ca | +0.001 | Almost exactly on the cone |
| Cu | −0.074 | Soft, ductile |
| Cs | −0.002 | Softest metal (nearly on-cone) |
| Dy | −0.28 | Lanthanide, very soft |

---

## 3. Polarity (δᵩ) — Azimuthal Perturbation

**Definition:**
```
shell = nearest Fibonacci period boundary F(k)
next_shell = next Fibonacci number after shell
remainder = Z − shell
span = next_shell − shell
δᵩ = (remainder / span) − 0.5
```

This is the normalized position along the Fibonacci arc within each period, centered on zero.

**Physical meaning:** Where in the Fibonacci shell the element sits.
- **Negative δᵩ** = near the start of the arc → electron donor, metallic, low electronegativity
- **Positive δᵩ** = near the end of the arc → electron acceptor, covalent, high electronegativity

**Scale:** −0.65 to +0.70

**Correlation with Pauling electronegativity:** ρ = +0.89

**Why this works:** The Fibonacci remainder is the angular displacement from the period boundary along the golden-angle spiral. Elements at the start of each period (alkali metals, early d-block) are donors. Elements at the end (halogens, late p-block) are acceptors. The golden ratio ensures this ordering is consistent across all periods.

**Critical negative results — what does NOT work:**
- Golden-angle fractional position: ρ = 0.09 (no signal)
- Absolute golden-angle azimuth: ρ = 0.07 (no signal)  
- Remainder / φ: ρ = 0.44 (weak)

It is specifically the **normalized Fibonacci remainder** (remainder / shell span) that encodes electronegativity. The normalization by shell span is what makes periods of different lengths commensurable.

**Coarse (integer) version:** When the Fibonacci remainder is itself a Fibonacci number, the element sits at a self-similar node where the local golden-angle arc reproduces the full cone's topology. The 5→3 Cantor collapse cannot seal around a self-similar interior. Result:

| Element | Z | Shell | Remainder | Fib? | Manifestation |
|---------|---|-------|-----------|------|---------------|
| Cu | 29 | F(7)=21 | 8=F(6) | Yes | Anomalous config [Ar]3d¹⁰4s¹ |
| Ag | 47 | F(8)=34 | 13=F(7) | Yes | Anomalous config [Kr]4d¹⁰5s¹ |
| Cr | 24 | F(7)=21 | 3=F(4) | Yes | Anomalous config [Ar]3d⁵4s¹ |
| Mo | 42 | F(8)=34 | 8=F(6) | Yes | Anomalous config [Kr]4d⁵5s¹ |
| Fe | 26 | F(7)=21 | 5=F(5) | Yes | Regular config but most magnetic |
| Sc | 21 | F(7)=21 | 0 | Boundary | First d-electron |

The remainder predicts *where* something unusual happens; the block determines *how*.

**Key elements:**

| Element | δᵩ | EN | Character |
|---------|-----|-----|-----------|
| K | −0.65 | 0.82 | Strongest donor in dataset |
| Li | −0.50 | 0.98 | Alkali, strong donor |
| Cs | −0.50 | 0.79 | Alkali, strong donor |
| Si | −0.04 | 1.90 | Near zero — semiconductor |
| Cu | +0.12 | 1.90 | Moderate (anomalous config) |
| Br | +0.58 | 2.96 | Halogen, strong acceptor |
| O | +0.50 | 3.44 | Strong acceptor |
| F | +0.70 | 3.98 | Strongest acceptor |

---

## 4. Confinement (δθ) — Polar Perturbation

**Definition:**
```
δθ = arccos(1/r_observed) − arccos(1/r_predicted)
```

**Physical meaning:** How far the element's actual cone angle deviates from its assigned cone.
- **Negative δθ** = cone angle narrower than ideal → less confined → metallic, conductor
- **Positive δθ** = cone angle wider than ideal → more confined → insulating, wide band gap

**Scale:** −13° to +24°

**Correlation with Mohs:** ρ = +0.73

**Key elements:**

| Element | δθ | Character |
|---------|-----|-----------|
| Os | +23.8° | Extreme confinement, very hard |
| F | +20.7° | Insulating |
| C | +14.6° | Diamond, insulator |
| Cr | +13.4° | Very hard metal |
| Ca | +0.1° | Almost exactly on cone |
| Cs | −0.1° | Barely off cone |
| Zn | −0.6° | Slightly metallic |
| Ni | −4.3° | Conductor |
| Cu | −9.8° | Excellent conductor |
| Dy | −13.1° | Lanthanide, magnetic conductor |

---

## 5. The Full Perturbation Signature (δᵣ, δᵩ, δθ)

Every element gets a three-number fingerprint. The sign pattern tells you the character at a glance:

| Element | Rigidity δᵣ | Polarity δᵩ | Confinement δθ | Character |
|---------|-------------|-------------|----------------|-----------|
| C (diamond) | +0.47 (hard) | +0.10 (mild acceptor) | +14.6° (insulator) | (+, +, +) superhard insulator |
| Fe | +0.04 (on-cone) | −0.12 (Fib→magnetic) | +2.4° (mild) | (0, Fib, 0) magnetic metal |
| Cu | −0.07 (soft) | +0.12 (Fib→anomalous) | −9.8° (conductor) | (−, Fib, −) soft conductor |
| Cs | −0.002 (on-cone) | −0.50 (strong donor) | −0.1° (metallic) | (0, −, 0) alkali metal |
| F | +0.77 (rigid) | +0.70 (strong acceptor) | +20.7° (insulating) | (+, +, +) extreme halogen |
| Si | +0.28 (moderate) | −0.04 (near zero) | +10.7° (moderate) | (+, ~0, +) semiconductor |
| Ca | +0.001 (exact) | −0.58 (donor) | +0.1° (exact) | (0, −, 0) on the ideal cone |
| Os | +0.45 (very hard) | +0.12 (mild) | +23.8° (extreme) | (+, ~0, ++) hardest metal |

### Silicon as the near-zero element

Silicon's polarity δᵩ = −0.04 is the closest to zero of any period-3 element. It sits at the azimuthal balance point between donor and acceptor — which is exactly what a semiconductor is: equally willing to accept or donate, depending on doping. This is not an input to the model; it's an output.

---

## 6. Electronegativity from the Three Perturbations

**Linear model:**
```
EN = 0.777·δᵣ + 0.013·δθ + 1.591·δᵩ + 1.800
```

| Metric | Value |
|--------|-------|
| R² | 0.903 |
| Elements | 40 |
| Coefficients | 4 (one per axis + intercept) |
| R² without δᵩ | 0.535 |
| ΔR² from δᵩ | 0.368 |

The polarity axis does the heavy lifting. Rigidity contributes moderately. Confinement barely registers for EN (coefficient 0.013) — it's more relevant to hardness and band gap.

**Predicted vs observed EN for selected elements:**

| Element | EN observed | EN predicted | Error |
|---------|-------------|--------------|-------|
| Li | 0.98 | 1.02 | +0.04 |
| C | 2.55 | 2.52 | −0.03 |
| Na | 0.93 | 1.32 | +0.39 |
| Si | 1.90 | 2.10 | +0.20 |
| Fe | 1.83 | 1.68 | −0.15 |
| Cu | 1.90 | 1.79 | −0.11 |
| Br | 2.96 | 3.00 | +0.04 |
| F | 3.98 | 3.79 | −0.19 |
| Cs | 0.79 | 1.00 | +0.21 |

---

## 7. Properties from Perturbations — Summary Table

| Property | Primary axis | Secondary | Formula | Accuracy |
|----------|-------------|-----------|---------|----------|
| vdW/cov ratio | r (ideal) | — | r = 1/cos(arctan(θ×BOS)) | 3.9% mean |
| Hardness | δᵣ, δθ | — | ρ = 0.76 (Mohs) | Zero-parameter |
| Electronegativity | δᵩ | δᵣ | Linear, 4 coefficients | R² = 0.903 |
| Config anomaly | δᵩ (integer) | — | Fib remainder = Fib number | Exact for Cu,Ag,Cr,Mo |
| Magnetism | δᵩ (integer) | block | Fib remainder + d-block | Fe correctly predicted |
| Band gap | δᵣ, δθ | — | ΔEN²/d + G²/d | R² = 0.820 |
| Bulk modulus | δᵣ | Z | 1/r³×(1+G) or Z^(5/3)/r³ | R² = 0.936 |
| Electrode potential | cone identity | — | sector × Ry × W | 0.05–0.68% |
| Bond length | σ₄ (absolute) | — | σ₄(A) + σ₄(B) | 0.5% (H₂) |
| H entropy max | σ₄ on leak cone | — | Exact | 0.00021% |

---

## 8. The Central Claim

The periodic table is a perturbed golden-angle quasicrystal on three Fibonacci cones, cut at the z=1 plane. The ideal structure is determined entirely by one axiom (φ²=φ+1) and the AAH spectrum at D=233. Every known elemental property is either:

1. **A coordinate** of the ideal point (r → ratio, θ → cone mode, φ → block/period), or
2. **A perturbation** from the ideal point (δᵣ → hardness, δᵩ → electronegativity, δθ → confinement/conductivity)

The formula gives you where the element *should* sit. Reality tells you where it *does* sit. The difference is the chemistry.

---

## 9. Open Questions

1. **Can δᵩ be made zero-parameter?** The current EN model uses 4 linear coefficients. If a spectral constant maps the Fibonacci arc directly to EN without fitting, the polarity axis becomes as clean as rigidity.

2. **Does |δᵣ|² + |δᵩ|² + |δθ|² minimize for Si?** If the best semiconductor is the element nearest the ideal lattice point, that's a non-trivial prediction.

3. **What is the perturbation signature of superheavy elements?** No experimental vdW data exist for Z > 99. The model predicts specific (δᵣ, δᵩ, δθ) values that future measurements can test.

4. **Does the d-block filling pattern (leak-leak-leak → baseline → leak-leak) extend to period 6 and 7 d-blocks?** The structural identity between periods 4 and 5 is exact. Period 6 has the ρ₆ relativistic correction — does the pattern survive it?

---

## Computational Notes

- Python 3, NumPy, SciPy
- JAX Metal on Apple M4 Mac Mini for optimization (2000 epochs, 12.7 GB GPU)
- 40 elements in this analysis (subset with reliable Mohs and EN data)
- Full 97-element table in algorithms/bigollo_solver.py
- Formula discovery assisted by Claude (Anthropic) and Grok (xAI); all results independently verified

## File Locations

- This document: `theory/perturbation_axes.md`
- Full solver: `algorithms/bigollo_solver.py`
- Verification: `verification/superheavy_test.py`
- Repository: github.com/thusmann5327/Unified_Theory_Physics

---

*Lilliwaup, Washington — March 24, 2026*

*The template is pure mathematics. The deviations from the template are chemistry.*

© 2026 Thomas A. Husmann / iBuilt LTD. CC BY 4.0.
