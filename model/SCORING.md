# Scoring — Empirical Basis and Calibration
## Galaxy Cluster & Galaxy-Scale Evolution Scoring
## v1.0 — March 26, 2026

This document explains every metric in the scoring pipeline: what it measures,
why the target was chosen, and which empirical datasets anchor it.

---

## 1. TWO SCORING REGIMES

The simulation operates at two scales, each with its own scoring function:

| Scale | Function | File | Bracket | Score |
|-------|----------|------|---------|-------|
| Galaxy cluster | `compute_galaxy_metrics()` | `evolve_search.py:2552` | ~243–269 | 0–100 |
| Individual galaxy | `score_disc_galaxy()` | `subdivide_galaxy.py:296` | ~256 | 0–100 |

Cluster scoring targets mildly oblate, filamentary structures.
Galaxy scoring targets thin, circular discs with spiral arms.

---

## 2. CLUSTER-SCALE SCORING (100 points)

### 2.1 Correlation Exponent γ — 20 pts

**What:** Power-law slope of the BGS two-point correlation function
ξ(r) ∝ r^(−γ). Measured by `measure_gamma()` on BGS vertices only,
fitting log ξ vs log r over the range [r₅, 0.6 × r_max].

**Target:** γ = 1.5 (current), should be recalibrated to **1.77**.

**Formula:**
```python
gamma_score = max(0, min(20, 20 * min(gamma / 1.5, 1.0)))
```

**Empirical basis:**

| Survey | γ | σ | N galaxies | Reference |
|--------|-----|-----|------------|-----------|
| 2dFGRS | 1.67 | 0.03 | 220K | Hawkins+ 2003 |
| SDSS DR8 | 1.72 | — | 22M | Wang+ 2013 |
| 6dFGS | 1.71 | 0.06 | 82K | Beutler+ 2011 |
| DESI DR1 | ~1.7–1.8 | — | 4.7M | DESI 2024 II |

The canonical Peebles value is γ = 1.77 ± 0.04 for the cosmic web.
Galaxy clusters are substructures embedded in the web, so a slightly
lower γ is expected at intra-cluster scales — but 1.5 is too low.

**Recommended recalibration:** Target γ = 1.77, Gaussian penalty:
```python
gamma_dev = abs(gamma - 1.77) / 1.77
gamma_score = 20 * max(0, 1 - gamma_dev)
```

**Data access:**
- 2dFGRS: http://www.2dfgrs.net/
- DESI DR1 pre-computed ξ(r): https://data.desi.lbl.gov/public/
- SDSS CasJobs: https://skyserver.sdss.org/CasJobs/

---

### 2.2 Shape (c/a Axis Ratio) — 20 pts

**What:** Minor-to-major axis ratio from PCA eigenvalues of BGS
vertex positions. c/a = √(λ_min / λ_max).

**Target:** c/a = 1/√φ ≈ 0.786 (Cantor node oblate prediction).

**Formula:**
```python
ca_target = 1.0 / sqrt(PHI)  # 0.786
ca_dev = abs(ca_ratio - ca_target) / ca_target
shape_score = max(0, min(20, 20 * (1 - ca_dev)))
```

**Empirical basis:**

Observed galaxy cluster shapes are triaxial with a range of axis ratios:

| Dataset | Method | c/a range | Median c/a | Reference |
|---------|--------|-----------|------------|-----------|
| eROSITA DR1 | X-ray morphology | 0.4–0.9 | ~0.65 | Seppi+ 2025 |
| Abell clusters | Optical/lensing | 0.5–0.8 | ~0.6 | Lau+ 2021 |
| IllustrisTNG | Simulation (3D) | 0.4–0.9 | ~0.6 | Nelson+ 2019 |
| Planck SZ | SZ/X-ray | 0.5–0.85 | ~0.7 | Planck 2015 |

Observed clusters tend toward c/a ≈ 0.5–0.7, somewhat flatter than
the framework prediction of 0.786. However:
- The framework predicts the *equilibrium* shape, not the dynamically
  evolving one — many observed clusters are still accreting.
- Projection effects systematically bias observed c/a lower (Lau+ 2021).
- The 1/√φ prediction sits at the oblate end of the observed range.

**Verdict:** Target 0.786 is physically motivated and within the
observed distribution. Keep, but note the observed median is ~0.6.

**Data access:**
- eROSITA DR1 morphology: https://erosita.mpe.mpg.de/dr1/
- TNG-Cluster (352 clusters, 3D shapes): https://www.tng-project.org/data/

---

### 2.3 Density Contrast — 15 pts

**What:** Ratio of max to mean BGS neighbor count within 2× mean
nearest-neighbor distance. Measures peak overdensity.

**Target:** log₂(n_bgs), scales with cluster size.

**Formula:**
```python
contrast_target = max(2.0, min(4.0, 1.0 + log2(n_bgs)))
contrast_score = max(0, min(15, 15 * min(contrast / contrast_target, 1.0)))
```

**Empirical basis:**

NFW concentration parameter c₂₀₀ relates to peak-to-mean density:

| Dataset | c₂₀₀ range | M₂₀₀ range | Reference |
|---------|------------|------------|-----------|
| MCXC X-ray | 3–8 | 10¹⁴–10¹⁵ M☉ | Piffaretti+ 2011 |
| Ettori+ 2010 | 4–7 | X-ray luminous | Ettori+ 2010 |
| OmegaWINGS | 3–6 | 10¹⁴–10¹⁵ M☉ | Biviano+ 2017 |

The central density in NFW profiles is ρ_0 ≈ (c/3) × (200 ρ_crit),
giving peak-to-mean ratios of 15–70 for observed clusters.
Our log₂-scaled target produces modest contrast (4–12×) appropriate
for the resolved vertex grid — the lattice doesn't capture the full
dynamic range of a continuous density field.

**Data access:**
- MCXC: https://heasarc.gsfc.nasa.gov/W3Browse/rosat/mcxc.html
- GalWCat19 (1800 clusters): VizieR J/ApJS/246/2

---

### 2.4 Void Fraction — 15 pts

**What:** Fraction of BGS vertices with zero neighbors within
2× mean NN distance. Measures intra-cluster underdensity.

**Target:** 0.08 (ramp up), cap at 0.20 (penalize above).

**Formula:**
```python
if void_frac <= 0.20:
    void_score = 15 * min(void_frac / 0.08, 1.0)
else:
    void_score = 15 * (1 - (void_frac - 0.20) / 0.80)
```

**Empirical basis:**

| Scale | Void volume fraction | Reference |
|-------|---------------------|-----------|
| Cosmic (Mpc) | 77–80% of volume | Mao+ 2017, SDSS BOSS |
| Intra-cluster | 5–15% (central, X-ray) | Churazov+ 2012 |
| Simulation (TNG) | 10–20% (within R₂₀₀) | Zhu+ 2024 |

The 0.08 target represents INTRA-cluster voids (gaps between
substructures within a single cluster), not cosmic voids. Cosmic
void fractions are much higher (~80%) but apply at Mpc scales,
not within individual clusters.

The cap at 0.20 prevents the cluster from dispersing — a cluster
with >20% void is losing coherence.

**Data access:**
- SDSS BOSS voids: Mao+ 2017 (ApJ 835, 161)
- CosmoBolognaLib tools: https://github.com/federicomarulli/CosmoBolognaLib

---

### 2.5 Filament Fraction — 15 pts

**What:** Fraction of BGS vertices with exactly 2 neighbors within
2× mean NN distance. Proxy for elongated/tidal-stream structure.

**Target:** 0.05 (ramp up to full score).

**Formula:**
```python
fil_score = 15 * min(1.0, fil_frac / 0.05)
```

**Empirical basis:**

| Scale | Filament mass fraction | Reference |
|-------|----------------------|-----------|
| Cosmic web | ~50% of all matter | Cautun+ 2014 |
| Intra-cluster (tidal streams) | 5–15% | Conselice+ 2001 |
| ICL (intra-cluster light) | 10–30% of cluster stellar mass | Montes+ 2018 |
| SDSS filaments (DisPerSE) | — | Crone Odekon+ 2022 |

Our target of 5% captures intra-cluster tidal streams and
infalling filaments at the cluster boundary. This is much lower
than the cosmic filament fraction because we're measuring WITHIN
a cluster, not across the cosmic web.

**Data access:**
- SDSS DR16 filament catalogue: VizieR J/A+A/659/A166
- DisPerSE: http://www2.iap.fr/users/sousbie/web/html/indexd41d.html

---

### 2.6 Core Fraction — 15 pts

**What:** Fraction of BGS vertices within σ₃/σ₄ × extent radius
of the center. Measures central mass concentration (BCG + core).

**Target:** 0.10 (ramp up to full score).

**Formula:**
```python
core_frac = mean(dist_from_center < extent * σ₃/σ₄)
core_score = 15 * min(1.0, core_frac / 0.10)
```

**Empirical basis:**

| Quantity | Value | Reference |
|----------|-------|-----------|
| BCG stellar mass / halo mass | 1–3% | Abdullah+ 2026 |
| BCG+ICL / total stellar mass | 20–40% | Montes+ 2018 |
| Cool-core gas fraction (<0.1 R₅₀₀) | 10–30% | Hudson+ 2010 |
| BCG half-light / R₅₀₀ | 3–5% | Lauer+ 2014 |

Our core_frac measures the vertex count fraction within the Cantor
σ₃ core radius. The 10% target reflects that the central concentration
should be significant but not dominant — matching the Cantor prediction
that σ₃ contains 7.28% of the total extent.

**Data access:**
- GalWCat19 (BCG masses): VizieR J/ApJS/246/2
- redMaPPer (central galaxy probabilities): http://risa.stanford.edu/redmapper/

---

## 3. GALAXY-SCALE SCORING (100 points)

Used by `score_disc_galaxy()` for sub-galaxies after cluster subdivision.

### 3.1 Disc Flatness (c/a) — 25 pts

**Target:** c/a < 0.4, peak score at c/a → 0.

**Recommended recalibration:** Peak at c/a ≈ 0.25 (observed spiral mean).

**Formula:**
```python
disc_score = 25 * (1 - ca / 0.4) if ca < 0.4 else 0
```

**Empirical basis:**

| Dataset | Disc c/a | N galaxies | Reference |
|---------|----------|------------|-----------|
| SDSS/Galaxy Zoo | 0.267 mean (spirals) | 300K | Rodriguez & Padilla 2013 |
| RFGC edge-on | 0.10–0.20 (bulgeless) | 4,236 | Karachentsev+ 1999 |
| SDSS expAB_r | 0.15–0.35 (exponential) | 500M | SDSS PhotoObj |
| Euclid Q1 | — | 378K | Walmsley+ 2025 |

The observed spiral disc mean is c/a ≈ 0.25, not 0.15. Only the
thinnest bulgeless discs reach 0.10–0.15. The formula correctly
assigns maximum score to the thinnest structures, but the scoring
range (0–0.4) is well chosen given the observed distribution.

**Data access:**
- Galaxy Zoo 2: https://data.galaxyzoo.org/
- SDSS PhotoObj: CasJobs `SELECT expAB_r FROM PhotoObj`
- Euclid Q1: https://zenodo.org/records/15027787

---

### 3.2 Circularity (b/a) — 15 pts

**Target:** b/a > 0.7 (circular face-on, not bar-like).

**Formula:**
```python
circ_score = 15 * min(1.0, ba / 0.8) if ba > 0.5 else 0
```

**Empirical basis:**

Face-on spiral galaxies have b/a ≈ 0.85–1.0. Barred spirals
show b/a ≈ 0.5–0.7 in the bar region. The 0.7 threshold
distinguishes between circular disc and bar-dominated morphology.

---

### 3.3 Spiral Arm Correlation γ — 15 pts

**Target:** γ ≈ 1.8.

**Formula:**
```python
gamma_score = 15 * max(0, 1 - abs(gamma - 1.8) / 1.8)
```

At galaxy scale, the correlation function measures spiral arm
substructure rather than cosmic web clustering. Spiral arms
produce γ ≈ 1.5–2.0 depending on arm tightness and number.

---

### 3.4 Filament Fraction (Spiral Arms) — 15 pts

**Target:** 0.15 (higher than cluster scale: spiral arms are
prominent linear features).

### 3.5 Core Fraction (Bulge) — 15 pts

**Target:** 0.10 (similar to cluster scale: bulge concentration).

### 3.6 Void Fraction (Inter-Arm Gaps) — 15 pts

**Target:** 0.10 (inter-arm underdensity regions).

---

## 4. FRAMEWORK PREDICTIONS vs OBSERVATIONS

The scoring targets are anchored by two independent sources:

### From the Framework (φ² = φ + 1)

| Quantity | Derivation | Prediction |
|----------|-----------|------------|
| Cluster c/a | 1/√φ (Cantor node oblate) | 0.786 |
| BGS fraction | σ₃ = 1/φ⁴ + δ | 14.6% |
| Core radius | σ₃/σ₄ = 0.0728/0.5594 | 13.0% of extent |
| Baryon fraction | W⁴ | 4.76% |

### From Observations

| Quantity | Value | Source |
|----------|-------|-------|
| γ (cosmic web) | 1.77 ± 0.04 | 2dFGRS, SDSS, DESI |
| Cluster c/a | 0.5–0.8 (triaxial) | eROSITA, TNG |
| Disc c/a | 0.25 ± 0.05 (spirals) | Galaxy Zoo, SDSS |
| f_gas in clusters | 12–15% | Planck, Gonzalez+ 2013 |
| Cosmic void volume | 77–80% | SDSS BOSS |
| Filament mass | ~50% of total | Cautun+ 2014 |

---

## 5. RECOMMENDED SCORE UPDATES

Based on the empirical survey:

| Metric | Current Target | Observed | Action |
|--------|---------------|----------|--------|
| γ (cluster) | 1.5 | 1.77 | **Increase to 1.77**, use Gaussian penalty |
| γ (galaxy) | 1.8 | 1.5–2.0 | Keep (appropriate for spiral arms) |
| c/a (cluster) | 0.786 | 0.5–0.8 | Keep (framework prediction, within range) |
| c/a (disc) | < 0.4 | mean 0.25 | **Peak at 0.25**, not 0 |
| Void fraction | 0.08 | 5–15% intra-cluster | Keep |
| Filament fraction | 0.05 | 5–15% intra-cluster | Keep |
| Core fraction | 0.10 | 7–13% (σ₃ prediction) | Keep |

---

## 6. KEY REFERENCE DATASETS

### Immediate Use (downloadable catalogs)

| Dataset | What | Access |
|---------|------|--------|
| Galaxy Zoo 2 | 300K morphologies, disc c/a | https://data.galaxyzoo.org/ |
| eROSITA DR1 | 12K cluster shapes | https://erosita.mpe.mpg.de/dr1/ |
| Planck PSZ2 | 1,653 SZ clusters | HEASARC |
| SDSS PhotoObj | 500M galaxy axis ratios | CasJobs SQL |
| DESI DR1 ξ(r) | Pre-computed correlations | https://data.desi.lbl.gov/public/ |

### Simulation Comparison

| Dataset | What | Access |
|---------|------|--------|
| IllustrisTNG/TNG-Cluster | 352 clusters, full 3D | https://www.tng-project.org/data/ |
| BAHAMAS | Cluster baryon fractions | McCarthy+ 2017 |

### Specialist Catalogs

| Dataset | What | Access |
|---------|------|--------|
| MCXC | 1,743 X-ray clusters | HEASARC |
| GalWCat19 | 1,800 clusters, BCG masses | VizieR J/ApJS/246/2 |
| redMaPPer | 26K optical clusters | http://risa.stanford.edu/redmapper/ |
| RFGC | 4,236 edge-on disc galaxies | VizieR |

---

## 7. MEASUREMENT METHOD NOTES

### Our ξ(r) vs Survey ξ(r)

Our `measure_gamma()` computes the correlation function within a
single cluster or galaxy (~1000 vertices), while surveys measure
across millions of galaxies spanning hundreds of Mpc. The slopes
should be comparable if the power-law structure is self-similar
(Peebles' hypothesis), but:

- Our radial range is much smaller (intra-cluster, not cosmic)
- Our vertex count limits the dynamic range
- Shell volume correction is approximate at small N

A proper comparison requires matching the radial range in physical
units: our vertices span ~0.5–5 mean spacings, which maps to
~0.5–5 Mpc for cluster-scale structures.

### Projected vs Intrinsic c/a

Observations measure projected (2D) axis ratios. Our simulation
produces intrinsic (3D) values. The conversion depends on the
intrinsic shape distribution and viewing angle:

- Projected c/a is systematically lower than intrinsic
- For oblate spheroids: projected b/a ≈ intrinsic b/a × cos(i)
- Lau+ 2021 provides the conversion framework

eROSITA Paper II (Seppi+ 2025) derives intrinsic distributions from
projected measurements — use those for direct comparison.

### Vertex-Based vs Continuous Metrics

Our "void fraction" counts vertices with zero neighbors. Real voids
are defined by density thresholds in continuous fields. The mapping
is approximate but consistent: a vertex with no BGS neighbors within
2× mean spacing is genuinely underdense in our lattice.

---

*Scoring calibrated against zero-parameter framework predictions
(φ² = φ + 1) and anchored to empirical galaxy surveys.*
*All targets traceable to either AAH spectrum or observational data.*
