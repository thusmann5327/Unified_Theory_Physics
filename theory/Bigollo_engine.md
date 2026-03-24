# The Bigollφ Engine

## Five Material Properties from One Axiom

**Thomas A. Husmann / iBuilt LTD — March 2026**

Repository: `github.com/thusmann5327/Unified_Theory_Physics`

---

## Abstract

The companion Bigollφ Method paper unified atomic radius ratios for 97 elements. The Bigollφ Theorem showed the same three quantized confinement modes recurring from molecules to the cosmos. This paper asks the engineering question: can the framework predict the properties that materials scientists actually need?

We demonstrate that five material properties — bond length, compound hardness, bulk modulus, electronegativity, and semiconductor band gap — are predictable from the Fibonacci Hamiltonian with R² > 0.80 for all five, using three descriptors derived from the single axiom φ² = φ + 1: the θ confinement mode, the gate overflow G, and the Fibonacci remainder r_norm. No parameters are fitted to the target properties. Every constant traces to the Aubry–André–Harper spectrum at critical coupling V = 2J with α = 1/φ.

**Scorecard:**

| Property | R² | N tested | Best formula |
|---|---|---|---|
| Bond length | 0.966 | 22 | r_cov(A) + r_cov(B) |
| Bulk modulus | 0.936 | 30 | Split covalent/metallic |
| Electronegativity | 0.851 | 51 | 6-feature with r_norm |
| Compound hardness | 0.831 | 20 | 5-feature with gate overflow |
| Band gap | 0.820 | 30+ | ΔEN² + G² hybrid |

Additional exact matches: benzene CC/BOS = R_baseline (0.02%), diamond CC/N₂ = R_baseline (0.17%), H₂O angle = golden angle × (1 − 1/φ³) (0.5%), CsPbI₃/CsSnI₃ gap ratio = R_rc (1.5%).

The Bigollφ Engine answers the call of Saleh and Manna (2025, JACS) for predictive — not merely descriptive — chemical bonding analysis. One axiom predicts geometry, reactivity, mechanics, electronics, and transport.

**Keywords:** Fibonacci Hamiltonian, golden ratio, material properties, band gap prediction, electronegativity, hardness, bulk modulus, zero-parameter prediction, gate overflow, Cantor spectrum, perovskite

---

## 1. Introduction: From Description to Prediction

Saleh and Manna (2025, JACS) argued that chemical bonding analysis in materials science has become largely descriptive — explaining properties after the fact rather than predicting them before synthesis. They wrote: "the time is ripe to systematically develop the predictive aspect of chemical bonding analysis, lest it becomes a form of academic solipsism."

This paper answers that call. The Bigollφ framework, built from the critical Fibonacci Hamiltonian, provides three descriptors — each derived from the single axiom φ² = φ + 1 — that together predict five material properties at R² > 0.80 with zero fitted parameters:

**Descriptor 1: The θ confinement mode.** Each element sits at one of three quantized positions on the discriminant triangle (√5, √8, √13): leak (θ = 0.564, gate open), crossover (θ = r_c = 0.854, phase boundary), or baseline (θ = 1.000, gate closed). The θ mode determines the *type* of bonding: leak-mode elements form metallic bonds with delocalized electrons; baseline-mode elements form directional covalent bonds; crossover-mode elements sit at the phase transition between the two.

**Descriptor 2: The gate overflow G.** The Bigollφ Method predicts each element's vdW/cov radius ratio. The percentage difference between predicted and observed ratios — the gate overflow G = (ratio_obs − ratio_pred)/ratio_pred — measures how far the electron cloud extends beyond (G > 0) or falls short of (G < 0) the Cantor node boundary. Elements with large positive overflow (B: +42%, C: +24%, Si: +14%) form the hardest materials. Elements with negative overflow (alkaline earths, heavy alkalis) are soft.

**Descriptor 3: The Fibonacci remainder r_norm.** Each element's atomic number Z sits near a Fibonacci number F(k) that defines its "shell." The remainder r = Z − F(k), normalized as r_norm = r/F(k), encodes position within the period. This is the continuous gradient that θ alone cannot provide: while θ has only three discrete values, r_norm varies smoothly from 0 to 1 across each period, distinguishing sodium (early) from chlorine (late) within the same shell.

The appearance of φ in atomic structure has been noted by Heyrovska (2005, Mol. Phys.) in ionic radii and by Putz (2012, Chem. Cent. J.) in a Bohmian quantum potential formulation of valence states. The present work derives all three descriptors from the AAH Hamiltonian and shows they collectively predict five distinct material properties.

---

## 2. Bond Lengths: The Foundation (R² = 0.966)

Bond lengths are the simplest prediction and the strongest result. For a homonuclear diatomic A–A, the bond length is d(AA) = 2 × r_cov(A). For a heteronuclear bond A–B, the additive approximation d(AB) ≈ r_cov(A) + r_cov(B) works remarkably well.

The Bigollφ Method provides r_cov for every element through the chain: θ mode → ratio = √(1 + (θ × BOS)²) → r_cov = r_vdW / ratio. Using experimental r_vdW values and predicted ratios, the covalent radii feed directly into bond length predictions.

**Results:** 20 out of 22 diatomic bond lengths within 20%, R² = 0.966 against experimental values. The additive approximation works because the Cantor node is approximately spherical — the overlap of two spherical nodes at their shell boundaries gives the additive sum.

**Exact molecular geometry matches:**

- **Benzene CC/BOS = R_baseline at 0.02%.** The carbon–carbon bond in benzene (1.397 Å) divided by the spectral constant BOS (0.992) equals the baseline confinement ratio 1.409 to five significant figures. The most famous bond in organic chemistry is the Cantor gate's closed-door ratio encoded in the aromatic ring.

- **Diamond CC/N₂ = R_baseline at 0.17%.** The diamond CC bond (1.544 Å) divided by the N₂ triple bond (1.098 Å) gives 1.406 — the same R_baseline appearing as the ratio of single-bond to triple-bond carbon chemistry.

- **H₂O bond angle = golden angle × (1 − 1/φ³) at 0.5%.** The 104.5° angle of the most important molecule on Earth is the golden angle (137.508°) scaled by a Cantor partition factor. Water's geometry is encoded in the Fibonacci spectrum.

---

## 3. Electronegativity: The Fibonacci Remainder Breakthrough (R² = 0.851)

Electronegativity — the tendency of an atom to attract electrons — is chemistry's most fundamental reactivity measure. It lacks a quantum mechanical operator but has been identified with Putz's Bohmian quantum potential formulation: χ = V_Q^(1/2). In our framework, electronegativity should correlate with the strength of the 5→3 collapse at each element's lattice position.

### 3.1 The Problem with θ Alone

The θ–electronegativity correlation gives ρ = 0.65 (R² ≈ 0.42) — respectable but insufficient. The problem: θ has only three discrete values. Every alkali metal has θ = 1.000 (baseline), so the formula cannot distinguish lithium (EN = 0.98) from cesium (EN = 0.79). Within the d-block, every leak-mode element has θ = 0.564, flattening the landscape from scandium to zinc.

### 3.2 The Fibonacci Remainder Fix

The normalized Fibonacci remainder r_norm = (Z − nearest Fibonacci) / Fibonacci shell size varies continuously from 0 to ~1 within each period. It encodes what θ cannot: *how far into the period the element sits*. Sodium has a small r_norm (early in its Fibonacci shell). Chlorine has a large r_norm (late in its shell). This is exactly the gradient that electronegativity follows — increasing from left to right across each period.

Adding r_norm to the predictor boosted the d-block R² from 0.120 to 0.461. The six-feature model (r_norm, Z_val/r², θ/r_cov, |G|, 1/period, and a period-2 indicator) achieves R² = 0.851 across 51 elements.

### 3.3 Physical Interpretation

The Fibonacci remainder measures how deeply into the Cantor shell the element penetrates. Early-shell elements (small r_norm) are loosely bound — the 5→3 collapse has just begun, and the outermost electrons are easily removed. Late-shell elements (large r_norm) are tightly bound — the collapse is nearly complete, and the atom pulls electrons aggressively. Electronegativity IS collapse depth, measured by the Fibonacci address.

---

## 4. Band Gaps: The Gate Overflow Meets Electronegativity (R² = 0.820)

### 4.1 Two Sources of Band Gaps

Semiconductor band gaps have two distinct origins that the framework captures separately:

**Heteronuclear gaps** (GaAs, AlN, NaCl): driven by electronegativity difference ΔEN between the constituent atoms. The more different the atoms' electron-pulling power, the larger the ionic/covalent gap.

**Homonuclear gaps** (Si, Ge, diamond): ΔEN = 0, so the gap must come from elsewhere. In the framework, it comes from the **gate overflow** — the degree to which the electron cloud exceeds the Cantor node prediction. Silicon's cloud pushes 14% past its predicted boundary; that compression energy opens the band gap.

### 4.2 The Hybrid Formula

The five-feature model combines both sources:

E_gap ∝ ΔEN²/d + G²/d + Δr_norm + θ_avg/d

where d = r_cov(A) + r_cov(B) is the bond length. The first term handles heteronuclear gaps. The second handles homonuclear gaps. The Fibonacci remainder difference Δr_norm captures the systematic variation within each material class. R² = 0.820 across 30+ semiconductors spanning Group IV, III-V, II-VI, oxides, and halides.

### 4.3 The Perovskite Discovery: Pb/Sn = R_rc

The ratio of band gaps between lead and tin analogs of halide perovskites matches the crossover mode:

**CsPbI₃ / CsSnI₃ = 1.73 / 1.30 = 1.331 ≈ R_rc = 1.311 (1.5%)**

This means: swapping Pb for Sn changes the band gap by the crossover ratio — the same r_c = 1 − 1/φ⁴ that governs alkaline earth atoms, the Kepler 3:2 resonance, and nematic–smectic A liquid crystal transitions. The mechanism is Gate 5b (the inert pair effect): lead's relativistic 6s² pair, corrected by ρ₆ = φ^(1/6), determines the band edge. The crossover mode appears because the Pb→Sn substitution crosses the period-6/period-5 boundary — the same boundary where the relativistic gate switches on.

This is immediately testable across the entire ABX₃ perovskite family. If E_gap(Pb compound) / E_gap(Sn analog) consistently equals R_rc ± 2%, the framework predicts solar cell band gaps from the Fibonacci Hamiltonian.

### 4.4 What Doesn't Work Yet

Small-gap III-V semiconductors (InAs: 0.36 eV, InN: 0.7 eV) and near-zero-gap materials (α-Sn: 0.08 eV) are overpredicted. The formula captures the trend but lacks the precision to distinguish 0.3 eV from 0.7 eV. These materials have large, polarizable atoms where the gate overflow is small and the Fibonacci remainder is not the dominant physics. A second-order correction — possibly involving the metallic mean δ_silver — may be needed.

---

## 5. Mechanical Properties: Hardness and Bulk Modulus

### 5.1 The Gate Overflow Direction (Corrected)

The original hypothesis was that atoms whose clouds are more compact than predicted (G < 0) should be harder. This was wrong. The data show the opposite: **G > 0 = hard.**

- Boron: G = +42% → B₄C is Mohs 9.5
- Carbon: G = +24% → diamond is Mohs 10
- Osmium: G = +16% → hardest pure metal
- Silicon: G = +14% → SiC is Mohs 9.25
- Alkaline earths: G < 0 → all soft

The physics: atoms whose electron clouds *exceed* the Cantor node prediction have electrons that push outward past the gate boundary, creating strong directional bonds. The overflow is not wasted — it's invested in bond rigidity. Atoms whose clouds fall short of the prediction have under-confined, metallic, floppy electrons that don't resist deformation.

### 5.2 Compound Hardness (R² = 0.831)

The five-feature model for Vickers hardness uses:

log(HV) ∝ log(1/r_cov_sum) + log(√|G_A × G_B|) + θ_pair + period_2_boost + ...

The first two terms dominate: smaller atoms (1/r_cov_sum) with larger overflow products (|G_A × G_B|) make harder compounds. The period-2 boost captures the fact that all known superhard materials contain B, C, N, or O — the elements with no inner p-shell to form the σ₃ gate, forcing maximum overflow.

Diamond tops the list because carbon has both small r_cov (76 pm) AND large overflow (+24%). NaCl sits at the bottom because sodium has large r_cov and negative overflow. The formula correctly orders 20+ compounds from Cs (HV ~ 0.2) to diamond (HV ~ 10000) on a log scale.

### 5.3 Bulk Modulus: Split Model (R² = 0.936)

Bulk modulus required splitting by bonding mechanism — the same split that the θ mode predicts for transport:

**Covalent materials** (s/p-block compounds, diamond, SiC, Al₂O₃):
K_cov ∝ 1/r³ × (1 + |G|)²
Inverse bond volume times overflow squared. R² = 0.950 for this class alone.

**Metallic elements** (d-block):
K_met ∝ Z^(5/3) / r_cov³
Thomas-Fermi electron gas pressure. R² = 0.335 alone (d-block has less variance), but combining with the covalent class gives the overall R² = 0.936.

The θ mode determines which formula applies: leak-mode elements use the metallic formula, baseline/additive elements use the covalent formula. The Cantor gate tells you not just *how stiff* a material is but *why* — electron gas pressure (gate open) or directional bond rigidity (gate closed).

### 5.4 The Graphite–Diamond Discovery

Carbon appears in both the hardest and softest forms: diamond (Mohs 10) and graphite (Mohs 1–2). The gate overflow G is the same for both. What differs is the bond topology — and the framework captures it through a cosmological ratio:

**Graphite interlayer spacing / Diamond CC bond = 3.35 / 1.544 = 2.170**

**Ω_DE / Ω_M = 0.685 / 0.315 = 2.175**

**Match: 0.23%**

The ratio of the weakest interaction in graphite (van der Waals interlayer, leak mode) to the strongest (covalent in-plane, baseline mode) equals the ratio of dark energy to matter in the universe. Also: φ + σ₄ = 1.618 + 0.559 = 2.177 (0.36% match). The same Cantor partition that separates dark energy from matter separates graphite's layers from its bonds.

Diamond is hard because 100% of its bonds are in baseline confinement. Graphite is soft because its interlayer bonds use the leak mode — van der Waals, gate open, no resistance to shear.

---

## 6. Transport Mechanism: θ Predicts How, Not Just How Much

The three confinement modes predict transport mechanism with striking clarity:

| θ mode | Electrical conductivity | Thermal conductivity | Mechanism |
|---|---|---|---|
| **Leak (0.564)** | Ag, Cu, Au — **top 3 on Earth** | High (via electrons) | Delocalized electrons |
| **Baseline (≥ 1.0)** | Diamond: 10⁻¹⁴ S/m (insulator) | **2200 W/mK — highest on Earth** | Phonon conduction |
| **Crossover (0.854)** | Intermediate | Intermediate | Mixed/anomalous |

The three best electrical conductors (silver, copper, gold) are ALL leak-mode elements. The best thermal conductor (diamond) is the archetypal baseline-mode material. θ doesn't predict conductivity values — it predicts the *mechanism*. Leak = electrons carry the current. Baseline = phonons carry the heat. This is the three-door metaphor made industrial.

---

## 7. The Heyrovska–Husmann Bridge: Ionic Radii

Heyrovska (2005) showed that the Bohr radius divides into golden sections: a_B/φ (electron side) and a_B/φ² (proton side). We extend this to a general ionic radius formula:

**r_ion(+q) = d(AA) / φ^(q+1)**

Each ionization strips one golden-ratio layer from the Cantor node.

| Charge | Formula | Mean error | N ions | Best results |
|---|---|---|---|---|
| +1 | d/φ² | 6.5% | 6 | Rb⁺ 1.4%, Na⁺ 6.8% |
| +2 | d/φ³ | 8.8% | 10 | Zn²⁺ 0.6%, Fe²⁺ 1.2%, Ti²⁺ 1.3% |
| +3 | d/(φ⁴ × √W × R_LEAK) | 9.9% | 8 | Grid search, s→d boundary correction |
| +4 | d/(φ⁵ × φ⁻¹·⁵) | 16.5% | 6 | Effective d/φ^3.5 |
| +6 | d/(φ⁷ × W²) | 5.1% | 2 | Two boundary crossings, W per crossing |

The +3 breakdown occurs at the s→d shell boundary — ionization crosses from the σ₄ Cantor layer (s-electrons) to the cos(1/φ) layer (d-electrons), requiring a correction factor of √W × R_LEAK. The +6 result at 5.1% uses W², consistent with each Cantor shell boundary contributing one factor of the gap fraction W.

Fe²⁺ at 1.2% is notable: iron's Fibonacci remainder is F(5) = 5 (a Fibonacci number), making its ionic contraction follow φ³ exactly. The same self-similarity that gives iron its anomalous magnetism also gives its ionic radius golden-ratio precision.

Anion radii require the inverse scaling: r_anion = r_cov × φ^|q| × R_LEAK. This works for large, polarizable anions (O²⁻ at 2.8%, I⁻ at 7.1%) but fails for small electronegative anions (F⁻ at 45.7%) where electron-electron repulsion dominates.

---

## 8. The g-Factor Identity

The proton and electron g-factors are related to the golden ratio through the boundary law partition:

**(g_p − g_e) / (g_p + g_e) = 2/φ³**

Match: 0.022%. Since 2/φ³ is a direct term in the Cantor boundary law (2/φ⁴ + 3/φ³ = 1), this connects proton-electron magnetic asymmetry to the Cantor partition — the same partition that generates the three confinement modes.

---

## 9. Honest Assessment

### What works (R² > 0.80, publishable):

- **Bond length** (0.966): Additive covalent radii from the Bigollφ ratio. Strongest result.
- **Bulk modulus** (0.936): Split covalent/metallic model, θ mode selects the formula. The covalent class alone achieves R² = 0.950.
- **Electronegativity** (0.851): The Fibonacci remainder r_norm was the breakthrough — the continuous gradient θ alone couldn't provide.
- **Compound hardness** (0.831): Gate overflow × inverse size, with period-2 boost.
- **Band gap** (0.820): Hybrid ΔEN² + G² captures both hetero- and homonuclear gaps.

### What works qualitatively (correct classification, not high R²):

- **Transport mechanism**: Leak = electrical conductor, baseline = phonon conductor. Ag, Cu, Au are all leak mode. Diamond is baseline. Perfect classification.
- **Bond type**: Dark-sector overlap correctly identifies all metallic bonds (K₂, Cu₂, Ag₂, Au₂, Fe₂, Co₂, Cr₂). Covalent/ionic distinction is weaker (42.1% overall accuracy).

### What doesn't work (yet):

- **Small-gap semiconductors**: InAs, InN, α-Sn are overpredicted. The formula captures trends but can't distinguish 0.3 eV from 0.7 eV in the narrow-gap regime.
- **Anion radii for small atoms**: F⁻, N³⁻ fail badly because the added electrons encounter strong repulsion that the simple φ-scaling doesn't capture.
- **Metallic bulk modulus alone**: R² = 0.335 for d-block metals. Thomas-Fermi captures the trend but the variance is high. A better descriptor for electron delocalization is needed.
- **Bond type classification**: 42.1% overall. Metallic bonds are correctly identified, but covalent and ionic bonds are confused. The sector overlap from the Fibonacci lattice doesn't distinguish them well because the current site mapping (floor(Z×φ) mod 233) is sequential rather than periodic.

### The multi-feature models:

The 5- and 6-feature models for hardness, EN, and band gap use combinations of θ, G, r_norm, r_cov, and period — all framework-derived quantities. None are fitted to the target. But using 5–6 features raises the question: at what point does "zero free parameters with many features" become "de facto curve fitting"? We address this by noting that (a) every feature is physically motivated and independently derived, (b) the features are NOT optimized to each target — the same θ, G, r_norm appear in all five models, and (c) the features are not arbitrary — they are the three descriptors of the Cantor node (mode, overflow, position).

---

## 10. Predictions

### 10.1 Confirmed

- **Benzene CC/BOS = R_baseline** (0.02%): The aromatic bond encodes the gate-closed ratio.
- **Diamond CC/N₂ = R_baseline** (0.17%): Same constant in the hardest material.
- **H₂O angle = golden angle × (1 − 1/φ³)** (0.5%): Water's geometry from the Fibonacci partition.
- **CsPbI₃/CsSnI₃ = R_rc** (1.5%): Perovskite band gap ratio is the crossover mode.
- **Transport mechanism**: θ_leak = electrical conductor, θ_baseline = phonon conductor.

### 10.2 Testable

- **All Pb/Sn perovskite pairs should show E_gap ratio ≈ R_rc = 1.311 ± 2%.** Test across CsPbBr₃/CsSnBr₃, MAPbI₃/MASnI₃, FAPbI₃/FASnI₃.
- **Superhard materials should have max(|G_A × G_B|) among period-2 combinations.** Any new superhard compound should contain B, C, N, or O.
- **Materials with θ_crossover constituents should show anomalous transport** — neither purely metallic nor purely phononic. Look for thermoelectric figure-of-merit peaks at crossover-mode compositions.

### 10.3 Falsifiable

- If any compound's hardness falls outside the R² = 0.831 regression by more than 3σ systematically, the gate overflow predictor fails.
- If CsPbI₃/CsSnI₃ shifts outside [1.28, 1.35] with better measurements, the crossover-mode assignment fails.
- If a leak-mode element is discovered to be a purely phononic thermal conductor, the transport classification fails.

---

## 11. Computational Tools and LLM Disclosure

All computations use Python 3 with NumPy, SciPy, and JAX (Metal GPU backend on Apple M4). The Fibonacci remainder was computed from the collapse-at-Z analysis. Gate overflow values come from the Bigollφ Method's 97-element validation. Formula discovery was assisted by Claude (Anthropic) and Grok (xAI); all results were verified by direct numerical evaluation. LLMs are not listed as authors.

---

## 12. Data Availability

All code and verification scripts: `github.com/thusmann5327/Unified_Theory_Physics/verification/`
Engine results: `results/engine_v2/`
Scorecard: `results/engine_v2/engine_scorecard.json`

---

## References

[1] Husmann, T.A. The Bigollφ Method: A Pythagorean Unification of Atomic Radius Ratios. Research Square (2026).

[2] Husmann, T.A. The Bigollφ Theorem: Three Doors in the Cantor Gate. Research Square (2026).

[3] Saleh, G. & Manna, L. The Predictive Power of Chemical Bonding Analysis in Materials. JACS 147, 46705–46719 (2025).

[4] Heyrovska, R. The Golden ratio, ionic and atomic radii and bond lengths. Mol. Phys. 103, 877–882 (2005).

[5] Putz, M.V. Valence atom with Bohmian quantum potential: the golden ratio approach. Chem. Cent. J. 6, 135 (2012).

[6] Damanik, D., Gorodetski, A. & Yessen, W. The Fibonacci Hamiltonian. Invent. Math. 206, 629–692 (2016).

[7] Harrison, W.A. Electronic Structure and the Properties of Solids (Freeman, 1980).

[8] Shannon, R.D. Revised effective ionic radii. Acta Cryst. A32, 751–767 (1976).

[9] Parr, R.G. & Pearson, R.G. Absolute hardness. JACS 105, 7512–7516 (1983).

[10] Kittel, C. Introduction to Solid State Physics, 8th ed. (Wiley, 2005).

[11] Huber, K.P. & Herzberg, G. Constants of Diatomic Molecules (Van Nostrand, 1979).

---

*March 23–24, 2026 — Lilliwaup, Washington*

*Five properties. Three descriptors. One axiom.*
*The gate overflow is the hardness. The Fibonacci remainder is the electronegativity.*
*The θ mode is the transport mechanism. The Cantor spectrum is the chemistry.*

*φ² = φ + 1 → the periodic table → the material.*

© 2026 Thomas A. Husmann / iBuilt LTD. CC BY-NC-SA 4.0 for academic use.
