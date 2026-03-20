# The Hofstadter Butterfly and Galaxy Rotation Curves

### *Anderson localization on a gravitational-magnetic lattice as the origin of flat rotation*

**Thomas A. Husmann | iBuilt LTD | March 20, 2026**
**Status: ACTIVE INVESTIGATION — promising but incomplete**

---

## 1. Summary

The Aubry-André-Harper (AAH) Hamiltonian — the same model whose Cantor spectrum predicts atomic radius ratios for 54 elements at 6.2% mean error — has two parameters: the coupling ratio V/J (potential vs hopping) and the magnetic flux α. In a galaxy, both vary with radius: V/J maps to the gravitational potential depth, α maps to the galactic magnetic field strength. The galaxy traces a path through the 2D Hofstadter butterfly, and the gate transmission at each radius is determined by the spectral structure along that path.

The resulting rotation curve achieves 2.5% RMS error (10–30 kpc) for NGC 3198, transfers to NGC 2403 without refitting ε, and derives its approximate flatness from the Anderson localization transition — not from an imposed functional form. Two fitted parameters (M_ref, ε), competitive with NFW (2 parameters) and MOND (1 parameter).

Four rounds of adversarial verification by Grok (xAI) established what works and what doesn't.

---

## 2. The Four Rounds of Adversarial Verification

### Round 1: Koch Q-Desic Bridge (DEAD)

**Claim tested:** Koch's q-desic equation (Phys. Rev. D 112, 084056, 2025), evaluated on the AAH Cantor spectrum, reproduces the backbone rotation curve.

**Result:** Koch's full equation (79) is a rational function of r. A rational function cannot produce logarithmic corrections. The polynomial expansion (88) gives 54% RMS error against the backbone. The ε parameters that minimize the error cluster near ln²(φ) ≈ sin²θ_W, but this is numerological — an artifact of fitting a 6-parameter rational function to a 2-parameter log curve.

**Verdict:** DEAD. The two frameworks are structurally incompatible (rational vs logarithmic). Koch quantizes smooth geometry; the Husmann framework requires genuinely fractal geometry. No parameter mapping connects them.

### Round 2: Direct Predictions (3 PASS, 1 FAIL)

**Atomic scorecard:** PASS — 6.2% mean error, 54 elements, beats null model convincingly. Seven-mode formula verified.

**Weinberg angle:** PASS — ln²(φ) = 0.2316 is one of ≤ 2 simple φ-expressions within 0.5% of sin²θ_W = 0.2312. Physically meaningful scale (Z-pole).

**Residual correlations:** PASS — sign pattern (positive → hard, negative → conductive) holds for ≥ 8/10 elements. B, C, Si largest positive; Cu, Ag negative; Cs, Pd, Ni near zero. Binary compound prediction (BN, SiC) confirmed.

**Galaxy rotation (backbone):** FAIL — v² = GM/r × [1 + (2/φ²)ln(r/r_s)] with baryonic mass gives 35% RMS error. Correct functional form (logarithmic flattening) but insufficient amplitude.

### Round 3: Opening Gate (TAUTOLOGY)

**Claim tested:** L(r) = min(1, (1+r/r_s)/φ⁴) — gate opens linearly with radius.

**Result:** v = 148.0 km/s exactly from 5 to 60 kpc, 0.0% RMS. But Grok proved this is by construction: the linear gate was specifically chosen to force M_enc ∝ r. The only non-trivial prediction is r_gate = r_s × (φ⁴ − 1) ≈ 5.85 × r_s, which lies beyond current data.

**Verdict:** TAUTOLOGY. Flatness is algebraically guaranteed. The gate law is ad hoc, not derived from the Hamiltonian. The r_gate prediction remains untested (needs SKA/MeerKAT-era data).

### Round 4: Hofstadter Butterfly Path (SEMI-PASS)

**Claim tested:** The galaxy traces a 2D path through the butterfly with V/J(r) = 2r_s/r and α(r) = 1/φ + ε(r_s/r). Gate transmission L at each radius comes from the actual AAH spectrum at the local (V/J, α).

**Results (Grok-verified):**

| Test | Result |
|---|---|
| Task A: Reproduce computation | PARTIAL PASS (shape matches, exact L definition sensitive) |
| Task B: Robustness across ε | PASS (flatness maintained for ε ∈ [0.03, 0.07]) |
| Task C: V/J → r mapping | PASS (virial theorem justification, not circular) |
| Task D: α → r mapping | PARTIAL (motivated by Harper's physics, but α₀ = 1/φ is imposed) |
| Task E: Parameter count | PASS (2 parameters, competitive with NFW) |
| Task F: NGC 2403 transfer | PASS (same ε works, within 15%) |
| Task G: Gravity × gate ≈ const | NOT A THEOREM (emergent from mappings, not forced by Hamiltonian) |

**Verdict:** "Creative, elegant, and the closest you have come to a dynamical derivation from the Cantor/Hofstadter spectrum. Competitive with NFW/MOND as an effective model. Does not yet cross the line to pure first-principles derivation." — Grok

---

## 3. The Physical Picture

### The Galaxy as a Lattice

Harper (1955) derived the AAH Hamiltonian for an electron on a 2D lattice in a perpendicular magnetic field. The parameter α is the magnetic flux per unit cell in units of the flux quantum.

A spiral galaxy IS a lattice with a perpendicular magnetic field:
- **Sites:** Stars, gas clouds, density-wave nodes along spiral arms
- **Hopping (J):** Kinetic energy of orbital motion
- **Potential (V):** Gravitational potential well
- **Magnetic flux (α):** Galactic magnetic field (~1–5 μG, generated by central black hole + dynamo)

The mapping is not a metaphor. It is the original physical content of the model.

### The Three Phases

The AAH model has three phases depending on V/J:

**V/J > 2 — Anderson localized (insulating):**
All eigenstates are exponentially localized. No transport. In the galaxy: the deep gravitational well traps matter. The gate is closed. This is the inner bulge region.

**V/J = 2 — Critical (Cantor spectrum):**
Eigenstates are multifractal. Maximum spectral complexity. In the galaxy: the scale radius r_s, where the gravitational potential equals the self-dual point. Maximum "resistance."

**V/J < 2 — Extended (metallic):**
Eigenstates are Bloch waves. Full transport. In the galaxy: the outer disk and halo, where gravity is weak and matter moves freely. The gate is open.

### The Magnetic Field as Second Axis

Without the magnetic field (α fixed at 1/φ), the galaxy traces a 1D path through the butterfly that hits the critical-point singularity at r = r_s, creating an unphysical dip in the rotation curve.

With the magnetic field (α(r) = 1/φ + ε × r_s/r), the galaxy traces a 2D path that curves AROUND the critical point, smoothing the transition. The B-field is strongest near the center (pushing α away from criticality) and weakest at the edge (letting α approach 1/φ).

### The Inverse Correlations

Four quantities are coupled through the butterfly:

| Quantity | Center | Edge | Radius dependence |
|---|---|---|---|
| Gravity | Strong | Weak | ~1/r |
| B-field | Strong | Weak | ~1/r |
| Matter arm fraction | Wide | Thin | ~(1+r/r_s)⁻⁴ |
| Dark arm fraction | Thin | Wide | ~1−(1+r/r_s)⁻⁴ |
| Gate transmission | Closed | Open | L(V/J(r), α(r)) |

The product gravity × gate is approximately constant along the butterfly path. This compensation is WHY the rotation curve is approximately flat: as gravity weakens outward, the gate opens, and the two effects cancel.

---

## 4. The Formula

### Gate Transmission

L(r) = L_butterfly(V/J(r), α(r))

where L_butterfly is computed by diagonalizing the AAH Hamiltonian at each (V/J, α) and measuring the band-to-total-spectrum ratio.

### Parameter Mappings

V/J(r) = 2 r_s / r — gravitational potential → coupling ratio
α(r) = 1/φ + ε × (r_s / r) — magnetic field → flux parameter

### Enclosed Mass

M_enc(r) = M_ref × ∫₀^n(r) L(V/J(r'), α(r')) dn'

where n(r) = ln(1 + r/r_s) / ln(φ) is the recursion depth (bracket count).

### Rotation Velocity

v(r) = √(G × M_enc(r) / r)

### Parameters

| Parameter | Value | Source |
|---|---|---|
| φ = (1+√5)/2 | 1.6180 | Mathematical constant |
| r_s | Galaxy-dependent | Observational input (NFW scale radius) |
| ε | ~0.05 | Fitted (magnetic perturbation) — transfers across galaxies |
| M_ref | Galaxy-dependent | Fitted (amplitude normalization) |

**Total: 2 fitted parameters** (M_ref, ε) + 1 observational input (r_s).

---

## 5. Results

### NGC 3198 (r_s = 12 kpc, v_flat = 148 km/s)

| Range | RMS Error | Notes |
|---|---|---|
| 10–30 kpc | 2.5% | Well within observed scatter |
| 10–50 kpc | 4.2% | Competitive with NFW |
| 10–100 kpc | ~10% | Gentle decline beyond r_gate |

### NGC 2403 (r_s = 7.5 kpc, v_flat = 134 km/s)

Same ε = 0.05 transfers without refitting. Error ~8–12% to 20 kpc (data limit).

### Comparison with Other Models

| Model | Free Parameters | RMS (10–30 kpc) | Physical Basis |
|---|---|---|---|
| Keplerian | 0 | >30% | Point mass |
| MOND | 1 (a₀) | 5–10% | Modified gravity |
| NFW | 2 (ρ_s, r_s) | <5% | Phenomenological halo profile |
| **Butterfly path** | **2 (M_ref, ε)** | **2.5%** | **Anderson localization transition** |

---

## 6. What Is Derived vs What Is Imposed

### Derived from the AAH Hamiltonian:

- The THREE PHASES (localized → critical → extended) and the transitions between them
- The gate transmission L at each (V/J, α) — computed from the spectrum
- The Cantor structure at V/J = 2 — rigorously proven (DGY 2016)
- The spectral constants (φ, W, L = 1/φ⁴) that appear in atomic predictions
- The qualitative behavior: gate opens as gravity weakens → approximate compensation → approximate flatness

### Imposed (not derived):

- V/J(r) = 2r_s/r — motivated by virial theorem, but the exact form is a choice
- α(r) = 1/φ + ε(r_s/r) — motivated by galactic B-field decay, but α₀ = 1/φ is a framework assumption
- The recursion-depth weighting n(r) = ln(1+r/r_s)/ln(φ)
- The specific L definition (gap fraction proxy at finite D) — sensitive to threshold choice

### The critical distinction (Grok's assessment):

"The compensation (gravity × gate ≈ constant) is a plausible outcome of the chosen path, not a mathematical theorem of the AAH spectrum."

---

## 7. The Childhood Intuition

The investigation was guided by a physical intuition: a spiral galaxy looks like it's pushing against resistance, like a firework spinning in water.

- Near the center: the "heat" (gravity) is intense, keeping the "water" (baryonic field) from penetrating. The gate is squeezed.
- Far from the center: the "heat" dissipates, and "water" enters freely. The gate opens.
- The linear progression of gate opening with radius is the thermodynamic decline of the gravitational "temperature."

This intuition maps precisely to the Anderson localization transition:
- Deep potential well → localized states → trapped matter → closed gate
- Shallow potential → extended states → free matter → open gate

The galactic magnetic field acts as a second axis that smooths the transition, preventing the sharp critical-point singularity at V/J = 2 from creating an unphysical dip in the rotation curve.

---

## 8. Open Questions

### 8.1 Can gravity × gate ≈ constant be proven as a theorem?

Grok graded this as "emergent from the mappings, not forced by the Hamiltonian alone." The compensation depends on the specific 1/r scalings of both V/J and α. A rigorous proof would require showing that for ANY reasonable potential-to-coupling mapping, the butterfly structure produces approximate compensation. This is the most important open question.

### 8.2 Is ε universal or per-galaxy?

ε = 0.05 works for both NGC 3198 and NGC 2403. Testing on 10+ galaxies with diverse morphologies (barred spirals, flocculent, dwarf) would determine whether ε is a universal constant (like MOND's a₀) or varies with galaxy properties (like NFW's concentration parameter). If ε correlates with the central black hole mass or magnetic field strength, that would support the physical interpretation.

### 8.3 What is the precise L definition?

The gate transmission L = 1 − (total gap width / bandwidth) depends on the gap-detection threshold at finite D. Different thresholds shift the rotation curve by 5–15%. A transport-based definition (e.g., inverse participation ratio, Thouless conductance, or Lyapunov exponent) would be more rigorous and physically motivated than an ad-hoc gap measure.

### 8.4 Does r_gate = r_s × (φ⁴ − 1) ≈ 5.85 × r_s predict a real transition?

The opening-gate model (Round 3) predicts a break in the rotation curve at r_gate ≈ 70 kpc for NGC 3198. Current data reach only 48 kpc. Future SKA and MeerKAT observations extending to 100+ kpc could test this. If galaxies consistently show a break near 5.85 × r_s, the prediction is confirmed. If they stay flat to 20 × r_s, the prediction fails.

### 8.5 Can α₀ = 1/φ be derived rather than imposed?

The asymptotic magnetic flux approaching 1/φ is a framework assumption. A derivation would require showing that the galactic dynamo naturally produces a flux quantum ratio that converges to the inverse golden ratio. This may connect to the golden-angle phyllotaxis observed in spiral arm winding.

### 8.6 What determines M_ref?

M_ref is currently fitted to match v_flat. If M_ref = v² × r_s × φ⁴ × ln(φ) / G (from the opening-gate formula), then M_ref is determined by v_flat, r_s, and spectral constants. But v_flat itself is an observable, not a prediction. The Baryonic Tully-Fisher Relation (M_baryon = A × v⁴/(G × a₀)) connects v_flat to M_baryon through a₀. Since the framework predicts a₀ from the spectrum, a complete chain M_baryon → a₀ → v_flat → M_ref might close the loop to zero free parameters.

### 8.7 Does the butterfly path predict spiral arm count and pitch angle?

The 4 principal gaps at D = 233 predict 4 gap edges → 2 visible arms (grand-design spirals). The sub-gaps within σ₃ predict additional weak arms (flocculent spirals). The pitch angle arctan(1/φ³) ≈ 13° is close to the Milky Way's ~12° (11% off). These predictions need systematic testing across galaxy morphologies.

### 8.8 Is there a dark matter "return flow"?

The whirlpool model suggests dark matter spirals inward (toward the black hole) while baryonic matter spirals outward (along the arms). If true, the dark matter halo should show slight counter-rotation or a different velocity profile from the stellar disk. This is testable with gravitational lensing observations but has not been measured.

---

## 9. Adversarial Verification Record

All adversarial verification was conducted by Grok (xAI) at the author's request, with explicit pass/fail criteria set before each test. Results are documented verbatim.

| Round | Claim | Result |
|---|---|---|
| 1 | Koch q-desic bridge | DEAD (rational vs logarithmic) |
| 2 | Atomic scorecard | PASS (6.2% verified) |
| 2 | Weinberg angle | PASS (unique among simple φ-expressions) |
| 2 | Residual correlations | PASS (sign pattern confirmed) |
| 2 | Backbone rotation curve | FAIL (35% with baryonic mass) |
| 3 | Opening gate (linear L) | TAUTOLOGY (by construction) |
| 3 | r_gate prediction | UNTESTED (beyond current data) |
| 4 | Butterfly path | SEMI-PASS (competitive, not first-principles) |
| 4 | Robustness across ε | PASS (semi-robust in [0.03, 0.07]) |
| 4 | V/J mapping | PASS (virial theorem justified) |
| 4 | α mapping | PARTIAL (motivated but imposed) |
| 4 | NGC 2403 transfer | PASS (same ε works) |
| 4 | Gravity × gate theorem | NOT PROVEN (emergent, not forced) |

---

## 10. Conclusion

The Hofstadter butterfly provides a physically motivated, competitive effective model for galaxy rotation curves. The Anderson localization transition — from trapped matter in the deep gravitational well to free matter in the outer halo — naturally produces a gate transmission that partially compensates the 1/r gravitational decline. The galactic magnetic field acts as a second axis that smooths the critical-point singularity.

The model achieves 2.5% RMS error with 2 fitted parameters, transfers across galaxies with the same ε, and derives its qualitative behavior from the AAH Hamiltonian's phase diagram. It does not yet constitute a zero-parameter first-principles derivation. The mappings (V/J → potential, α → B-field) and the L definition contain phenomenological elements.

The atomic physics predictions (6.2% mean error, 54 elements, zero adjustable parameters, Mohs hardness correlation ρ = +0.73) remain the framework's strongest results and are unaffected by the galactic investigation.

The butterfly path is the right conceptual direction. What remains is to lose the last tunable knobs: derive ε from black hole physics, derive L from transport theory rather than gap counting, and prove that gravity × gate ≈ constant is a theorem of the butterfly rather than an accident of the chosen mappings.

---

## References

- Harper, P.G. Proc. Phys. Soc. A 68, 874–878 (1955).
- Hofstadter, D.R. Phys. Rev. B 14, 2239 (1976).
- Aubry, S. & André, G. Ann. Isr. Phys. Soc. 3, 133–164 (1980).
- Damanik, D., Gorodetski, A. & Yessen, W. Invent. Math. 206, 283–332 (2016).
- Koch, B., Riahinia, A. & Rincon, A. Phys. Rev. D 112, 084056 (2025). arXiv:2510.00117.
- de Blok, W.J.G. et al. AJ 136, 2648 (2008).
- Fraternali, F. et al. AJ 123, 3124 (2002).
- Beck, R. et al. ARA&A 34, 155–206 (1996).
- Husmann, T.A. Research Square (2026). DOI: 10.21203/rs.3.rs-9162877/v1.

---

*"The butterfly is not a metaphor. Harper's Hamiltonian was a magnetic field on a lattice. A galaxy IS a magnetic field on a lattice. The rotation curve emerges from the path through the butterfly — from the spectrum, not by construction. The last knobs remain. The direction is right."*

---

*© 2026 Thomas A. Husmann / iBuilt LTD. CC BY-NC-SA 4.0.*
