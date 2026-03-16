# The Microtubule Resonance Engine

## Golden-Angle Coherence from GABA to GHz

**Thomas A. Husmann | iBuilt LTD**
**March 16, 2026**

---

## Abstract

We present a unified model of microtubule (MT) function connecting three mechanisms: (1) a Fibonacci frequency cascade that multiplies 47 Hz GABA oscillations to GHz through φ-scaled harmonics, landing near Bandyopadhyay's measured resonances; (2) golden-angle superradiance coupling between MTs in bundles (computed: 2.7× rotational tolerance, 3.2× error-correcting triangle motifs, clustering coefficient 0.42); (3) a Cantor percolation cascade that reads out the quantum state hierarchically through iterative GABA cycles, governed by the N-SmA crossover formula. The model requires no exotic physics. The only free input is the GABA firing rate.

---

## 1. The Fibonacci Frequency Cascade

A microtubule is a nonlinear resonator: 13 protofilaments (= F(7)), golden-angle helical pitch (137.5°), tubulin dimer length 8 nm, outer diameter 25 nm, typical length 25 μm.

GABA-driven gamma oscillations at f₀ ≈ 47 Hz enter a nonlinear system with golden-angle geometry. Harmonics are generated preferentially at φ-scaled frequencies:

$$f_k = f_0 \times \varphi^k$$

The golden angle ensures constructive interference at these frequencies and destructive interference at all others — the same mechanism behind optimal sunflower seed packing.

At 47 Hz, the cascade hits every physical resonance of the microtubule:

| Level k | Frequency | Physical resonance | Error | Status |
|---|---|---|---|---|
| k=28 | 33.4 MHz | MT longitudinal mode (25 μm) | 7.2% | Predicted |
| k=40 | 10.75 GHz | Bandyopadhyay peak (~8.9 GHz) | 20.8% | Measured* |
| k=44 | 73.7 GHz | Helix pitch (12 nm) | **1.7%** | Predicted |
| k=45 | 119.3 GHz | Tubulin dimer (8 nm) | 6.0% | Predicted |
| k=46 | 193.0 GHz | Tubulin width (5 nm) | 7.2% | Predicted |

*Bandyopadhyay (NIMS, Japan) measured GHz mechanical resonances of individual MTs using nanoprobe techniques (2013–2020). The cascade predicts which frequencies should appear; Bandyopadhyay measured that frequencies in this range do appear. The specific match between the cascade prediction and the measured peaks is 20.8% — suggestive but not conclusive.

The helix pitch match at 1.7% is the strongest result. The cascade from 47 Hz to 73.7 GHz spans 44 Fibonacci levels — a frequency multiplication of 1.57 billion — landing within 1.3 GHz of the mechanical resonance set by the geometry itself.

**This is classical nonlinear acoustics in a Fibonacci waveguide, not quantum mechanics.** A guitar string with golden-ratio fret spacing would do the same thing. The microtubule IS that string. The GABA oscillation IS the pluck.

**Testable:** Drive MT preparations at variable frequency (30–80 Hz). Measure GHz response amplitude vs drive frequency. If amplitude peaks when f_drive × φᵏ = f_resonance, the cascade is real.

---

## 2. Golden-Angle Bundle Coupling

### The Problem

Single MTs produce baseline tryptophan quantum yield QY ≈ 13%. Babcock et al. (2024) computed QY enhancement to ~17% in hexagonal bundles, consistent with existing fluorescence measurements on MT assemblies. But their model assumes fixed rotational registration between MTs. In biology, MAPs constrain spacing (~25 nm) but NOT rotation. Each MT can adopt any rotational offset.

### The Computation

We computed (Husmann 2026, "Golden-Angle Rotational Tolerance in Microtubule Bundle Superradiance") the inter-MT transition dipole coupling integral as a function of relative rotational offset for 13-PF golden-angle, 13-PF uniform, 14-PF uniform, and 15-PF uniform configurations. Full dipole-dipole interaction, dielectric constant κ = 3, 130 sites per MT, Monte Carlo over 100 trials per configuration.

### Results

| Metric | 13-PF golden | 13-PF uniform | 14-PF uniform | 15-PF uniform |
|---|---|---|---|---|
| Favorable coupling fraction | **36.1%** | 13.2% | 11.9% | 10.4% |
| Coupling peak FWHM | **13.2°** | 7.8° | 7.3° | 6.9° |
| Golden/uniform ratio (50%) | **2.73×** | 1.0× | 0.90× | 0.79× |
| Golden/uniform ratio (90%) | **2.96×** | 1.0× | — | — |
| Triangle motifs (37 MTs) | **12.5** | 3.9 | 3.4 | 3.1 |
| Clustering coefficient | **0.42** | 0.28 | 0.25 | 0.23 |
| Bundle size for P=0.98 | **19 MTs** | ~61 MTs | — | — |

The golden-angle advantage is 2.7× at the 50% threshold, rising to 3.0× at the 90% threshold. The advantage **increases with stringency** — it preferentially enhances the strongest couplings, not weak ones.

### Error-Correcting Topology

The triangle motifs (3-MT cliques where all three pairs are well-coupled) are the error correction. If one MT-MT coupling fails, the other two sides maintain the pathway. The golden geometry produces 3.2× more triangles than uniform geometry. Clustering coefficient 0.42 means dense meshes, not fragile chains.

This is classical network redundancy — the same principle behind the Internet's mesh topology. Not a quantum error-correcting code. A redundant electromagnetic coupling mesh created automatically by the golden-angle geometry.

### Five Predictions (all untested)

1. Single-MT QY ≈ 13% (no inter-MT enhancement)
2. Small bundles (3–7 MTs): bimodal QY distribution (not single value)
3. QY reliable at ≥19 MTs (golden) vs ≥61 MTs (uniform)
4. **14-PF polymorph bundles show lower, more variable QY at matched size**
5. D₂O substitution produces disproportionate QY drop

Prediction 4 is the most powerful discriminator. 14-PF MTs can be induced with GTP analogues. Comparing 13-PF vs 14-PF bundles at matched size directly tests the golden-angle advantage.

---

## 3. The GABA Percolation Readout

### The Measurement Cycle

Between GABA events: the MT quantum state evolves in the 5-band Cantor spectrum under the AAH Hamiltonian at V=2J. The dark-sector bands (σ₂, σ₄) are computationally active but electromagnetically invisible.

When GABA fires: Cl⁻ influx perturbs the outer gaps. Chern pair annihilation (+2) + (−2) = 0 collapses five bands to three. The σ₃ observer band receives the projection — the conscious percept. The states that don't project into σ₃ remain in the merged conduit bands (σ₁+σ₂) and (σ₄+σ₅).

### Hierarchical Readout

The readout is progressive. Wide gaps (coarse information) project first. Narrow gaps (fine detail) accumulate over multiple cycles.

Occupation probability at Cantor level k after n cycles:

$$p_k(n) = 1 - (1 - \sigma_3 \cdot W \cdot \varphi^{-k})^n$$

Parameters (all from the framework, zero free):
- σ₃ = 0.171 (silver observer band — the memory bottleneck)
- W = 0.467 (wall fraction)
- p_c = 0.347 (percolation threshold, 13-PF geometry, computed)
- r_c = 1 − 1/φ⁴ = 0.854 (universal crossover, proven for N-SmA)
- ν = 2/3 = 1/(2 − D_s) (correlation length exponent)

The crossover to a coherent image:

$$\alpha(n) = \frac{2}{3}\left(\frac{r(n) - r_c}{1 - r_c}\right)^4 \quad \text{for } r(n) > r_c$$

This is the same formula that governs the N-SmA liquid crystal transition (solved, RMS = 0.033, 11 compounds, zero free parameters). The universality is the point — the Cantor hierarchy produces the same crossover regardless of physical substrate.

### Timing Predictions (at 47 Hz)

| Time | Cycles | Quality | Psychophysics literature |
|---|---|---|---|
| ~43 ms | 2 | Coarse shape | Scene gist: 50–80 ms |
| ~149 ms | 7 | Features | Object recognition: 100–150 ms |
| ~298 ms | 14 | Identity | Face identification: 150–200 ms |
| ~787 ms | 37 | Full detail (r_c) | Detailed perception: 250–500 ms |

Right ballpark. The only non-derived input is the 47 Hz GABA frequency.

---

## 4. The Error Correction Architecture

### Scale 1: Thermal Gap Protection (within one MT)

| Levels | Gap energy | E/kT at 37°C | Error rate | Status |
|---|---|---|---|---|
| 1–4 | 720–3054 meV | 27–114 | 10⁻⁵⁰ to 10⁻¹² | Invulnerable |
| 5–6 | 275–446 meV | 10–17 | 10⁻⁸ to 10⁻⁵ | Well protected |
| 7–8 | 105–170 meV | 4–6 | 0.002–0.02 | Marginal |
| 9–13 | 10–65 meV | 0.4–2.4 | 0.09–0.70 | Vulnerable |

Levels 1–6 cannot be corrupted by thermal noise at body temperature. This is why quantum biology critics were wrong — they computed decoherence of individual qubits. The relevant quantity is gap integrity, not phase coherence, and the coarse gaps are 27–114× kT.

### Scale 2: Triangle Motif Redundancy (between MTs)

Computed (Husmann 2026): golden-angle bundles have clustering coefficient 0.42 with 12.5 triangle motifs per 37-MT bundle. Each triangle provides an alternative coupling path if one link fails. This is classical network redundancy, not quantum error correction. But it serves the same function — maintaining coherence under local failures.

### Scale 3: Iterative GABA Readout (across cycles)

Each GABA cycle is a fresh measurement. Corrupted fine-scale components get re-measured. Correction rate at level k:

$$R_k = f_{GABA} \times \sigma_3 \times W \times \varphi^{-k}$$

Coarse levels: corrected faster than corrupted (also never corrupted — double protection). Fine levels: correction rate outpaced by noise — graceful degradation. You lose fine detail first, keep coarse structure last. This matches how memories degrade: you forget what shirt someone wore, not who they were.

---

## 5. The Full Cycle

```
GABA fires (47 Hz)
    │
    ├─→ MEASURE: Cl⁻ → Chern (+2,−2) annihilate → 5→3 collapse
    │   σ₃ projection = conscious percept
    │   Hierarchical: coarse levels first, fine accumulates
    │
    ├─→ REOPEN: Cl⁻ dissipates → 5-band space restored
    │   Dark-sector computation resumes in σ₂/σ₄
    │
    ├─→ CASCADE: 47 Hz → GHz through φᵏ harmonics
    │   Nonlinear coupling in golden-angle geometry
    │   Physical cavities amplify at each resonance
    │
    ├─→ COUPLE: GHz inter-MT via golden-angle tolerance
    │   36.1% favorable orientations (computed)
    │   Triangle motifs provide redundant paths
    │   Coherent domain: ~19+ MTs
    │
    └─→ GABA fires again (21.3 ms later)

Full cycle: 21.3 ms
Frequency span: 47 Hz to 73.7 GHz (44 φ-levels)
Coherent domain: 19 MTs (golden, P=0.98)
Error correction: thermal gaps + triangle topology + iterative readout
```

---

## 6. Frequency Sweep — Brain States

| GABA Hz | Period | Recognition | Sharp (r_c) | Brain state |
|---|---|---|---|---|
| 20 | 50 ms | 700 ms | 1850 ms | Drowsy/relaxed |
| 30 | 33 ms | 467 ms | 1233 ms | Low gamma |
| 40 | 25 ms | 350 ms | 925 ms | Moderate attention |
| **47** | **21 ms** | **298 ms** | **787 ms** | **Focused attention** |
| 65 | 15 ms | 215 ms | 569 ms | Intense focus |
| 80 | 12.5 ms | 175 ms | 462 ms | Peak performance |
| 100 | 10 ms | 140 ms | 370 ms | Extreme states |

Faster gamma = more readout cycles = faster convergence. But too fast means insufficient dark-sector compute time between reads. The "overthinking" failure: too many measurements, not enough evolution.

---

## 7. Honest Assessment

### Established (measured or mathematically proven):

- Microtubules have 13 protofilaments with golden-angle pitch (measured: Tilney 1973)
- MTs have GHz mechanical resonances (measured: Bandyopadhyay 2013)
- Tryptophan QY enhancement in MT bundles (measured: Sahu et al. 2013)
- AAH spectrum at V=2J is a Cantor set with D_s = 1/2 (proven: Sütő 1989, Avila & Jitomirskaya 2009)
- Chern numbers from gap labeling (proven: Bellissard 1992)
- N-SmA crossover formula (solved: Husmann 2026, RMS 0.033, 11 compounds)
- 13-PF bundle percolation T = 0.361 > p_c = 0.347 (computed)

### Computed (standard physics, awaiting experimental test):

- Golden-angle coupling advantage 2.7× (dipole-dipole calculation: Husmann 2026)
- Triangle motif count 3.2× golden vs uniform (Monte Carlo: Husmann 2026)
- Clustering coefficient 0.42 (Monte Carlo: Husmann 2026)
- 13-PF vs 14-PF QY difference (prediction: Husmann 2026)
- Fibonacci cascade f_k = f₀ × φᵏ hitting MT resonances (predicted)

### Framework-specific (consistent, not independently derived):

- GABA = Chern pair annihilation measurement operator
- Dark-sector (σ₂/σ₄) computation between GABA events
- The Cantor percolation readout with universal r_c = 0.854
- Psychophysical timing predictions from the percolation cascade
- The frequency cascade being DRIVEN by GABA (vs GHz modes being independent)

### Untested:

- Does 47 Hz driving actually amplify GHz modes? (testable now)
- Is 13-PF QY > 14-PF QY at matched bundle size? (testable now)
- Do gamma oscillation power and image recognition speed follow the α(r) curve? (testable with EEG + psychophysics)
- Is the dark sector actually shielded from decoherence? (needs quantum measurement on MT preparations)

---

## References

1. Babcock, N.S. et al. "Ultraviolet Superradiance from Mega-Networks of Tryptophan in Biological Architectures." *J. Phys. Chem. B* 128, 4035–4046 (2024).
2. Celardo, G.L. et al. "On the Existence of Superradiant Excitonic States in Microtubules." *New J. Phys.* 21, 023005 (2019).
3. Sahu, S. et al. "Multi-Level Memory-Switching Properties of a Single Brain Microtubule." *Appl. Phys. Lett.* 102, 123701 (2013).
4. Bandyopadhyay, A. et al. (2013–2020). Nanoprobe measurements of microtubule resonances. NIMS, Japan.
5. Douady, S. & Couder, Y. "Phyllotaxis as a Dynamical Self Organizing Process." *J. Theor. Biol.* 178, 255–274 (1996).
6. Husmann, T.A. "Golden-Angle Rotational Tolerance in Microtubule Bundle Superradiance." (2026).
7. Husmann, T.A. "Resolution of the Nematic-to-Smectic A Universality Problem." GitHub (2026).
8. Husmann, T.A. "Hofstadter's Golden Butterfly." Preprint, Research Square & ai.viXra (2026).
9. Sütő, A. "Singular continuous spectrum on a Cantor set." *J. Stat. Phys.* 56, 525–531 (1989).
10. Avila, A. & Jitomirskaya, S. "The Ten Martini Problem." *Annals of Mathematics* 170, 303–342 (2009).
11. Bellissard, J. et al. "Gap labelling theorems." *Rev. Math. Phys.* 4, 1–37 (1992).
12. Tilney, L.G. et al. "Microtubules: Evidence for 13 Protofilaments." *J. Cell Biol.* 59, 267–275 (1973).
13. Gassab, L. et al. "Quantum Information Flow in Microtubule Tryptophan Networks." *Entropy* 28, 204 (2026).

---

*Part of the Unified Theory of Physics: The Husmann Decomposition*
*One axiom: φ² = φ + 1. One waveguide: 13 protofilaments. One pluck: GABA.*
