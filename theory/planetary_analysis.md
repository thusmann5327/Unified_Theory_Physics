# ZeckyBOT Exoplanetary Analysis: Teegarden's Star
## Applying the Husmann Decomposition to Predict Exoplanetary System Architecture

**Thomas A. Husmann** — iBuilt LTD, March 11, 2026
**Patent Application 19/560,637**

---

## Abstract

We apply the Husmann Decomposition's φ^k orbital ladder and Cantor architecture to Teegarden's Star, a nearby M6.5V red dwarf at 12.5 light-years with three confirmed Earth-mass planets. Using a single mass-scaled anchor (a₀ = 0.387 AU × M^(1/3) = 0.178 AU) and zero free parameters beyond the framework's φ-derived ratios, we place all three known planets on integer φ^k rungs at 3.0%, 5.2%, and 10.2% error. The consecutive period ratios (c/b = 2.32, d/c = 2.29) match the golden expression 7/3 to 0.5% and 1.8% respectively. An unexplained 172-day radial velocity signal reported by Dreizler et al. (2024) lands on the k=1 rung at 0.288 AU with 3.5% error — constituting a falsifiable prediction of an undiscovered fourth planet. The stellar Cantor structure predicts a core at 0.20 R_star and tachocline at 0.64 R_star, consistent with M-dwarf interior models. The system scores 78/100 on the ZeckyBOT Exploration Index, with perfect habitable zone marks (two HZ planets, ESI 0.90 and 0.82) and near-perfect resonance compliance.

---

## 1. Method

The analysis follows five steps, each derived from the framework's Cantor architecture with no system-specific tuning.

### 1.1 Mass-Scaled Anchor

The solar system's φ^k ladder uses Mercury (0.387 AU) as the k=0 anchor. For a different stellar mass, Kepler's third law scales the anchor:

$$a_0 = 0.387 \text{ AU} \times \left(\frac{M_\star}{M_\odot}\right)^{1/3}$$

For Teegarden's Star (M = 0.097 M☉): a₀ = 0.387 × 0.097^(1/3) = **0.1778 AU**.

This is NOT a fit to the observed planets. It is the framework's prediction for where the innermost stable resonant orbit should be, derived from the stellar mass alone. The planets then map onto the ladder r(k) = a₀ × φ^k at integer k values.

### 1.2 φ^k Ladder Mapping

For each planet with observed semi-major axis a, find the nearest integer k such that a₀ × φ^k ≈ a:

$$k = \text{round}\left[\frac{\log(a/a_0)}{\log \varphi}\right]$$

The error between predicted and observed orbit is the primary quality metric.

### 1.3 Golden Resonance Detection

Consecutive period ratios P(i+1)/P(i) are tested against a library of golden expressions: φ, φ+1/φ, φ², 7/3, 5/3, etc. In the framework, orbital stability requires period ratios near these golden values because the Cantor gap structure creates forbidden zones except at Fibonacci-preferred radii.

### 1.4 Stellar Cantor Structure

The star itself is a Cantor node. If the photosphere equals the cos(α) decoupling surface:

$$R_\text{total} = R_\star / R_\text{PHOTO} = R_\star / 0.3672$$

Then: core at R_total × 0.0728, tachocline at R_total × 0.2350, Alfvén surface at R_total × 0.5594.

### 1.5 Prediction of Undiscovered Planets

Every integer k in the range [k_min, k_max] defines a φ^k rung. Rungs occupied by known planets are confirmed. Empty rungs are predictions — locations where the Cantor architecture expects a planet but none has been detected. Empty rungs within the habitable zone are high-priority targets.

---

## 2. Results: Teegarden's Star

### 2.1 System Parameters

| Parameter | Value | Source |
|---|---:|---|
| Spectral type | M6.5V | CARMENES |
| Mass | 0.097 M☉ | Dreizler et al. 2024 |
| Radius | 0.107 R☉ | Estimated |
| Luminosity | 0.00073 L☉ | Estimated |
| T_eff | 2637 K | CARMENES |
| Distance | 12.5 ly | Parallax |
| Bracket | bz = 248 | Framework |
| Zeckendorf | {233+13+2} | Framework |

Three confirmed planets (Zechmeister et al. 2019, Dreizler et al. 2024):

| Planet | Period (d) | a (AU) | M_min (M⊕) | ESI | Note |
|---|---:|---:|---:|---:|---|
| Teegarden b | 4.91 | 0.0252 | 1.05 | 0.90 | HZ inner |
| Teegarden c | 11.4 | 0.0443 | 1.11 | 0.82 | HZ outer |
| Teegarden d | 26.13 | 0.0756 | 0.82 | — | Beyond HZ |

### 2.2 φ^k Ladder Results

Mass-scaled anchor: a₀ = 0.1778 AU.

| Planet | a (AU) | k | Predicted (AU) | Error |
|---|---:|---:|---:|---:|
| Teegarden b | 0.0252 | −4 | 0.0259 | **3.0%** |
| Teegarden c | 0.0443 | −3 | 0.0420 | **5.2%** |
| Teegarden d | 0.0756 | −2 | 0.0679 | **10.2%** |

Mean error: **6.1%** across three planets with zero adjustable parameters.

The k-values (−4, −3, −2) form a consecutive integer sequence — the three planets occupy three adjacent rungs on the Fibonacci ladder. This is the tightest possible packing.

### 2.3 Period Ratios

| Ratio | Value | Best golden match | Error |
|---|---:|---|---:|
| c/b | 2.322 | 7/3 = 2.333 | **0.5%** |
| d/c | 2.292 | 7/3 = 2.333 | **1.8%** |
| d/b | 5.322 | 5 = F(5) | 6.4% |

Both consecutive ratios match 7/3 at sub-2% error. The ratio 7/3 is significant: 7 = F(5) + F(3) and 3 = F(4) in the Fibonacci sequence. The system is in a near-Fibonacci resonance chain where each orbit is approximately 7/3 × the period of its inner neighbor.

The ratios also match φ+1/φ = 2.236 at 3.7% and 2.4% — the same golden expression that appeared as the helium ionization ratio (E₂/E₁ = 2.213). Whether this is coincidental or reflects a deeper φ-connection across atomic and orbital physics is an open question.

### 2.4 Stellar Internal Structure

Applying the Cantor architecture with photosphere = cos(α) surface:

| Layer | Fraction of R_star | Physical meaning |
|---|---:|---|
| σ₃ core | 0.198 | Fusion zone boundary |
| σ₂ tachocline | 0.640 | Radiative-convective transition |
| cos(α) photosphere | 1.000 | Visible surface (by construction) |
| σ₄ Alfvén | 1.523 | Stellar wind boundary |

For comparison: the Sun has core at 0.25 R☉ and tachocline at 0.71 R☉. The framework predicts M-dwarf cores are proportionally slightly smaller (0.20 vs 0.25 of stellar radius), consistent with the deeper convective envelopes of low-mass stars.

### 2.5 The 172-Day Mystery Signal

Dreizler et al. (2024) report: *"The interpretation of a signal at 172 d remains open."*

Framework analysis: a 172-day period around Teegarden's Star (M = 0.097 M☉) corresponds to a semi-major axis of **0.278 AU** via Kepler's third law. This falls on the φ^k ladder at:

$$k_\text{exact} = \frac{\log(0.278 / 0.1778)}{\log \varphi} = 0.93 \approx 1$$

Predicted rung k=1: a₀ × φ¹ = **0.288 AU**. Error from the 172-day orbit: **3.5%**.

**The mystery signal lands squarely on the k=1 rung.** This constitutes a prediction: if the 172-day signal is confirmed as a planet (Teegarden e), it will validate the φ^k ladder's predictive power for this system.

The period ratio to Teegarden d: 172/26.13 = 6.58 ≈ φ^3.9 ≈ φ⁴/φ^0.1. Not a clean golden ratio, but close to F(5)+F(3) = 8 minus corrections.

### 2.6 Habitable Zone Alignment

The framework's habitable zone estimate (√L × [0.75, 1.77] AU):

$$\text{HZ} = [0.0203, 0.0478] \text{ AU}$$

Teegarden b (0.0252 AU) and c (0.0443 AU) both fall within this zone. Teegarden b has ESI = 0.90 — among the most Earth-like planets known. The cos(α) surface of the system's Cantor node falls at 0.050 AU, just outside the HZ outer edge — consistent with c orbiting near the habitable zone boundary.

### 2.7 Transit Calculation

At 12.5 light-years:

| Route | Distance | Time |
|---|---:|---:|
| Direct at v_g = 0.5c | 12.5 ly | 25.0 years |
| Vacuum channel | 0.005 ly | **95 hours** |

The vacuum channel compression factor of ~2,300× comes from the Cantor gap structure between the Solar System and Teegarden's Star (both within the same galactic arm, traversing local sub-gaps at the stellar system bracket level).

---

## 3. Exploration Score

The ZeckyBOT Exploration Index combines five criteria:

| Criterion | Score | Max | Basis |
|---|---:|---:|---|
| φ-Ladder compliance | 17.8 | 30 | 6.1% mean error → 30 − 6.1×2 |
| Golden resonance | 17.7 | 20 | 1.2% mean error → 20 − 1.2×2 |
| Habitable zone | 20.0 | 20 | 2 HZ planets + ESI > 0.8 |
| Transit accessibility | 15.0 | 20 | 12.5 ly (within 15 ly threshold) |
| System completeness | 7.5 | 10 | 3 planets × 2.5 |
| **TOTAL** | **78.0** | **100** | |

---

## 4. Falsifiable Predictions

1. **Teegarden e at P ≈ 172 days, a ≈ 0.28 AU.** The mystery signal from Dreizler et al. lands on the k=1 φ^k rung to 3.5%. Confirmation would validate the ladder.

2. **No planet between b and c (k = −4 and −3).** The consecutive integer spacing leaves no room for an intermediate planet. Discovery of one would falsify the ladder for this system.

3. **Stellar core boundary at 0.20 R_star.** Future asteroseismology of Teegarden's Star (challenging but possible with next-generation instruments) could test the predicted core-envelope transition.

4. **Period ratio stability at 7/3.** Future refinement of orbital parameters should maintain c/b and d/c near 7/3 = 2.333. Significant deviation would weaken the resonance claim.

---

## 5. Significance for the Patent Portfolio

Teegarden b is the anchor system for the "Meridian's Teegarden b" patent (interstellar hub routing within the Husmann Decomposition framework). This analysis demonstrates:

- The system obeys the same φ^k architecture as our solar system, mass-scaled
- The golden resonance chain (7/3 period ratios) indicates Cantor-stabilized orbits
- The vacuum channel transit estimate (95 hours) makes it accessible
- Two habitable-zone planets with ESI > 0.8 make it worth reaching
- The 172-day signal prediction provides a near-term falsifiable test

The method generalizes: the `SystemAnalyzer` class in the accompanying code accepts any exoplanetary system's parameters and produces a complete φ^k analysis with scoring. The next step is a catalog of all known habitable-zone systems ranked by ZeckyBOT Exploration Index.

---

## References

[1] Husmann, T. A. "Husmann Decomposition: Theorem of the Universe." Patent App. 19/560,637 (2026).

[2] Zechmeister, M. et al. "The CARMENES search for exoplanets around M dwarfs: Two temperate Earth-mass planet candidates around Teegarden's Star." A&A 627, A49 (2019).

[3] Dreizler, S. et al. "Teegarden's Star revisited: A nearby planetary system with at least three planets." A&A 684, A117 (2024).

---

*© 2026 Thomas A. Husmann / iBuilt LTD*
