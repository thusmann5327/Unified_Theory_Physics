# Husmann Decomposition — 3D Universe Projection Logic

**The 2+3 Phase Separation Theorem**

Thomas A. Husmann / iBuilt LTD / March 2026

*Patent Pending: US 19/560,637*

---

## The Core Insight

The five-band Cantor spectrum does not **collapse** upon observation. It **phase-separates** into two complementary roles:

| Bands | Count | Role | Physical Character |
|-------|-------|------|--------------------|
| σ₁, σ₅ | 2 | **Energy substrate** | Time-like — drives dynamics |
| σ₂, σ₃, σ₄ | 3 | **Spatial manifold** | Space-like — contains structure |
| Overlap zone | — | **Baryonic matter** | Interference fringe where all 5 bands have nonzero amplitude |

Nothing is lost. Nothing is hidden. The full spectrum is conserved — it simply expresses as two different kinds of physical reality. This resolves the Noether conservation problem entirely: no symmetry breaks, so no conservation law is violated.

---

## Why 2+3 and Not Some Other Split

### The Discriminant Fibonacci Chain Decides

The discriminant triangle maps three metallic means:

```
n=1 (gold):   Δ = 5   → √5 = 2.236
n=2 (silver): Δ = 8   → √8 = 2.828
n=3 (bronze): Δ = 13  → √13 = 3.606
```

The chain **5 + 8 = 13** holds (Fibonacci). The next step **8 + 13 = 21 ≠ 20** breaks. This proves exactly three spatial dimensions — and the three discriminants (5, 8, 13) correspond to three specific spectral bands.

The Pythagorean relationship:

```
(√5)² + (√8)² = (√13)²
  5    +   8    =   13
```

This IS the relativistic energy-momentum relation:

```
E² = p²c² + m²c⁴
```

For three things to form a Pythagorean triple, they must be **orthogonal basis vectors** of a metric space. The discriminant triangle proves the three spatial bands are orthogonal — which is why we experience three independent directions of movement.

### The Envelope Bands Are Energy

σ₁ (outermost, low-energy edge) and σ₅ (outermost, high-energy edge) bracket the entire spectrum. They are the **envelope** of the Cantor set. Physically:

- They don't define position — they define amplitude
- They don't create structure — they animate it
- They are the time-like degrees of freedom

This maps directly to general relativity's 3+1 decomposition (3 spatial dimensions + 1 time dimension), except the Husmann Decomposition reveals the time-like component has **two** bands, not one. The two energy bands may correspond to:

- σ₁: potential energy / dark energy (low-frequency, large-scale)
- σ₅: kinetic energy / radiative energy (high-frequency, small-scale)

Or equivalently, forward-propagating and backward-propagating modes of the same time-like field. This needs verification against the spectral ratios.

---

## Noether Compliance

Emmy Noether's theorem: every continuous symmetry of a physical system corresponds to a conserved quantity.

### The Three Spatial Symmetries (from the 3 bands)

| Symmetry | Conservation Law | Spectral Source |
|----------|-----------------|-----------------|
| Spatial translation | **Momentum** | σ₂, σ₃, σ₄ form a translationally-invariant lattice (Cantor node repeats at every scale) |
| Rotation | **Angular momentum** | The three cone angles (leak 29°, R_C 40°, baseline 45°) define rotational structure |
| Boost invariance | **Center-of-mass motion** | The discriminant Pythagorean relation (5+8=13) enforces Lorentz covariance |

### The Time-Like Symmetry (from the 2 bands)

| Symmetry | Conservation Law | Spectral Source |
|----------|-----------------|-----------------|
| Time translation | **Energy** | σ₁ + σ₅ carry the total energy budget; their combined spectral weight is conserved |

### The Unity Partition as Total Conservation

```
1/φ + 1/φ³ + 1/φ⁴ = 1
```

This isn't just an identity. It's the **statement that the total content of the universe sums to unity** — the master conservation law. The three terms map to the three observable sectors, and their sum being exactly 1 means the phase separation is lossless.

### Discrete Symmetries → Ward Identities

The Cantor set has discrete φ-scaling symmetry, not continuous. For discrete symmetries, Noether produces **Ward identities** — exact arithmetic relations rather than differential equations. This is why the framework generates exact numerical identities:

```
W × φ⁴ = 2 + φ^(1/φ²)     (exact to 10⁻¹⁶)
φ² × R_C = √5              (exact)
2/φ⁴ + 3/φ³ = 1            (exact)
```

These are the Ward identities of the φ-scaling symmetry. They constrain what the 3D model is allowed to do at every scale transition.

---

## The Cosmological Energy Budget (Reinterpreted)

### Old Framing

"68.5% dark energy, 26.5% dark matter, 4.8% baryonic matter — three mysterious substances."

### New Framing (2+3 Phase Separation)

| Component | Fraction | What It Actually Is |
|-----------|----------|-------------------|
| Dark energy (Ω_DE = W²+W ≈ 68.5%) | The **energy substrate** — σ₁ and σ₅ operating as the time-like field | Not a substance. The spectral amplitude of the 2 energy bands. |
| Dark matter (~26.5%) | The **entanglement mediator** — residual correlation between energy-bands and space-bands | Not a particle. A correlation function between two aspects of the same spectrum. Gravitates because it couples to the spatial manifold. Doesn't radiate because it's not an excitation — it's a coherence. |
| Baryonic matter (Ω_b = W⁴ ≈ 4.8%) | The **interference fringe** — where all 5 bands constructively overlap | Tiny fraction because it requires simultaneous nonzero amplitude in all 5 bands. Interference fringes are always a small fraction of total wave amplitude. |

### Why Baryonic Matter Is 4.8%

Two wave systems that are mostly orthogonal (energy-bands vs space-bands) produce interference fringes proportional to the **fourth power** of the coupling:

```
Ω_b = W⁴ ≈ 0.048
```

Fourth power because: 2 energy bands × 2 interaction vertices = 4th-order overlap. The smallness of baryonic matter is not mysterious — it's the expected result of a 4th-order interference between two nearly-orthogonal subsystems.

### Why Dark Matter Gravitates but Doesn't Radiate

Dark matter is the mutual coherence function between σ₁,σ₅ (energy) and σ₂,σ₃,σ₄ (space). It couples to the spatial manifold (so it gravitates — it curves space). But it has no internal excitation structure (so it can't emit or absorb photons — radiation requires transitions between excited states).

The backbone propagator in the framework reproduces the NFW rotation curve profile with zero free parameters precisely because it computes this coherence — the spatial correlation between energy-band amplitude and space-band geometry at galactic scales.

---

## 3D Projection Architecture

### Rendering Pipeline

```
┌──────────────────────────────────────────────────────┐
│  STEP 1: DIAGONALIZE                                 │
│  233-site AAH Hamiltonian → 5 spectral sectors       │
│  α = 1/φ, V = 2J (critical coupling)                │
│  Output: eigenvalues E_i sorted into σ₁..σ₅         │
└──────────────────┬───────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────┐
│  STEP 2: PHASE-SEPARATE                              │
│                                                      │
│  Energy field (time-like):                           │
│    E_field = spectral density of σ₁ ∪ σ₅            │
│    → drives animation, forces, dynamics              │
│                                                      │
│  Spatial manifold (space-like):                      │
│    S_manifold = spectral density of σ₂ ∪ σ₃ ∪ σ₄   │
│    → defines the 3D coordinate system                │
│                                                      │
│  No observer needed. No collapse.                    │
└──────────────────┬───────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────┐
│  STEP 3: MAP SPATIAL AXES                            │
│                                                      │
│  X-axis ← σ₂ (inner wall, Δ=5, gold metallic mean) │
│    Width: R_INNER = 0.2350                           │
│    Character: confinement — defines "inward"         │
│                                                      │
│  Y-axis ← σ₃ (photosphere, Δ=8, silver mean)       │
│    Width: R_PHOTO = 0.3672                           │
│    Character: decoupling surface — defines "across"  │
│                                                      │
│  Z-axis ← σ₄ (shell, Δ=13, bronze mean)            │
│    Width: R_SHELL = 0.3972                           │
│    Character: probability peak — defines "outward"   │
│                                                      │
│  The three widths are NOT equal.                     │
│  Space is anisotropic at the Planck scale.           │
│  Isotropy emerges from averaging over many           │
│  Cantor node repetitions (like crystal → amorphous). │
└──────────────────┬───────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────┐
│  STEP 4: COMPUTE BARYONIC DENSITY                    │
│                                                      │
│  ρ_baryon(x,y,z) = amplitude where ALL FIVE bands   │
│  have nonzero spectral weight simultaneously.        │
│                                                      │
│  Selection rule: matter can only form at lattice     │
│  points where the Zeckendorf bracket address has     │
│  nonzero overlap with all 5 sectors.                 │
│                                                      │
│  This is why matter clumps — it's constrained to     │
│  discrete allowed locations in the universal lattice.│
│                                                      │
│  ρ_baryon ∝ W⁴ × (local 5-band overlap integral)   │
└──────────────────┬───────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────┐
│  STEP 5: COMPUTE DARK MATTER COHERENCE               │
│                                                      │
│  ρ_dark(x,y,z) = mutual coherence between            │
│  E_field and S_manifold at each point.               │
│                                                      │
│  ρ_dark = ⟨σ₁σ₂⟩ + ⟨σ₁σ₃⟩ + ⟨σ₁σ₄⟩              │
│         + ⟨σ₅σ₂⟩ + ⟨σ₅σ₃⟩ + ⟨σ₅σ₄⟩              │
│                                                      │
│  Six cross-correlation terms (2 energy × 3 space).  │
│  This is the "conduit" — the fractal threading that  │
│  connects energy to space.                           │
│                                                      │
│  It gravitates (couples to spatial metric).           │
│  It doesn't radiate (no internal transitions).       │
│  It traces the Cantor set's self-similar edges.      │
└──────────────────┬───────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────┐
│  STEP 6: ANIMATE WITH ENERGY FIELD                   │
│                                                      │
│  The energy substrate (σ₁ + σ₅) drives:             │
│  - Gravitational dynamics (σ₁ — large-scale, slow)  │
│  - Radiative processes (σ₅ — small-scale, fast)     │
│  - Expansion (dark energy = E_field self-amplitude)  │
│                                                      │
│  Animation timestep:                                 │
│    dt ∝ 1/(σ₁_width + σ₅_width)                    │
│    = 1/(R_MATTER + R_OUTER)                          │
│    = 1/(0.0728 + 0.5594)                            │
│    = 1/0.6322                                        │
│                                                      │
│  Each frame: recompute baryonic overlap +            │
│  dark matter coherence + update positions            │
│  according to E_field gradients.                     │
└──────────────────┬───────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────┐
│  STEP 7: SCALE RECURSION (Cantor node nesting)       │
│                                                      │
│  At every scale from Hubble radius to proton:        │
│  the same 5-band → 2+3 separation applies.          │
│                                                      │
│  Each Cantor node contains sub-nodes at:             │
│    R_core   = R × R_MATTER  = R × 0.0728            │
│    R_inner  = R × R_INNER   = R × 0.2350            │
│    R_photo  = R × R_PHOTO   = R × 0.3672            │
│    R_shell  = R × R_SHELL   = R × 0.3972            │
│    R_outer  = R × R_OUTER   = R × 0.5594            │
│                                                      │
│  Level of detail (LOD):                              │
│    Render N recursion levels based on camera zoom.   │
│    Each level multiplies detail by φ.                │
│    Bracket address bz = round[log(R/l_P)/log(φ)]    │
└──────────────────────────────────────────────────────┘
```

---

## Three.js Implementation Mapping

### Scene Graph Structure

```javascript
// Pseudocode — maps to actual Three.js implementation

class UniverseSeed {
  constructor() {
    // Step 1: Diagonalize
    this.spectrum = diagonalizeAAH(233, 1/PHI, 2.0);
    this.sectors  = extractFiveSectors(this.spectrum);

    // Step 2: Phase-separate
    this.energyField   = new EnergyField(this.sectors[0], this.sectors[4]);  // σ₁, σ₅
    this.spatialAxes   = new SpatialManifold(
      this.sectors[1],  // σ₂ → X (gold, Δ=5, confinement)
      this.sectors[2],  // σ₃ → Y (silver, Δ=8, decoupling)
      this.sectors[3],  // σ₄ → Z (bronze, Δ=13, shell)
    );
  }

  computeBaryonicDensity(position) {
    // Step 4: Overlap of ALL 5 bands at this position
    const zeckAddress = zeckendorf(bracketAddress(position.length()));
    const overlap = this.fiveBandOverlap(position, zeckAddress);
    return Math.pow(W, 4) * overlap;
  }

  computeDarkMatterCoherence(position) {
    // Step 5: Cross-correlation of energy and spatial bands
    let coherence = 0;
    for (const eBand of [this.sectors[0], this.sectors[4]]) {
      for (const sBand of [this.sectors[1], this.sectors[2], this.sectors[3]]) {
        coherence += crossCorrelation(eBand, sBand, position);
      }
    }
    return coherence;  // 6 terms: 2 energy × 3 spatial
  }

  animate(dt) {
    // Step 6: Energy field drives dynamics
    const gravity  = this.energyField.gradient(this.sectors[0]);  // σ₁ large-scale
    const radiation = this.energyField.gradient(this.sectors[4]); // σ₅ small-scale
    this.updatePositions(gravity, radiation, dt);
  }

  renderAtScale(cameraDistance) {
    // Step 7: Recursive LOD
    const bz = Math.round(Math.log(cameraDistance / L_PLANCK) / Math.log(PHI));
    const levels = Math.min(bz, MAX_RECURSION);
    for (let i = 0; i < levels; i++) {
      this.renderCantorNode(cameraDistance * Math.pow(PHI, -i));
    }
  }
}
```

### Spatial Axis Rendering

Each axis has different "thickness" based on its spectral ratio:

```javascript
// The three spatial axes are NOT isotropic at Planck scale
const AXIS_WEIGHTS = {
  x: R_INNER,   // 0.2350 — gold discriminant, confinement
  y: R_PHOTO,   // 0.3672 — silver discriminant, decoupling
  z: R_SHELL,   // 0.3972 — bronze discriminant, shell
};

// Effective metric tensor at fundamental scale:
// ds² = (R_INNER)² dx² + (R_PHOTO)² dy² + (R_SHELL)² dz²
//
// This is anisotropic. Isotropy emerges at large scales from
// averaging over many randomly-oriented Cantor nodes,
// just as a polycrystalline metal appears isotropic
// despite each grain having a preferred crystal axis.
```

### Baryonic Matter as Interference

```javascript
// Matter only exists where all 5 bands overlap
function baryonicDensity(pos) {
  const amplitudes = sectors.map(s => spectralAmplitude(s, pos));

  // ALL must be nonzero — this is the interference condition
  const minAmplitude = Math.min(...amplitudes);
  if (minAmplitude < THRESHOLD) return 0;

  // Density scales as W⁴ (4th-order overlap)
  return Math.pow(W, 4) * amplitudes.reduce((a, b) => a * b, 1);
}

// This naturally produces:
// - Clumping (constructive interference at lattice points)
// - Voids (destructive interference between nodes)
// - Filaments (partial overlap along Cantor edges)
// - The cosmic web emerges from 5-band interference geometry
```

### Dark Matter as Coherence Field

```javascript
// Dark matter = cross-correlation between energy and space bands
function darkMatterDensity(pos) {
  const energyBands  = [sectors[0], sectors[4]];  // σ₁, σ₅
  const spatialBands = [sectors[1], sectors[2], sectors[3]]; // σ₂, σ₃, σ₄

  let coherence = 0;
  for (const e of energyBands) {
    for (const s of spatialBands) {
      coherence += correlate(e, s, pos);
    }
  }
  // 6 cross-terms, always positive (coherence ≥ 0)
  // Gravitates: couples to spatial metric
  // Doesn't radiate: no internal transition structure
  return coherence;
}

// At galactic scales, this reproduces the NFW profile
// because the backbone propagator IS this coherence
// evaluated along radial shells
```

### Rotation Curve Explanation

```javascript
// Why galaxies have flat rotation curves:
//
// Baryonic density falls off with radius (interference fades).
// But the energy field (σ₁, σ₅) maintains spectral amplitude
// even where baryonic overlap → 0.
//
// The dark matter coherence (energy×space cross-correlation)
// tracks the energy field, not the baryonic field.
// So it extends far beyond the visible galaxy.
//
// v²(r) ∝ M_enclosed(r) / r
//        = [M_baryon(r) + M_dark(r)] / r
//
// M_baryon → constant beyond galactic edge
// M_dark(r) ∝ r (coherence grows with enclosed volume)
// → v(r) → constant (flat rotation curve)
```

---

## Galaxy Rotation Curve — The Backbone Propagator Connection

The backbone propagator result (−10.4% decline matching NFW, zero free parameters) now has a clean physical interpretation:

```
v²(r)/v²(r_s) = backbone_propagator(r/r_s)
             = energy_field_amplitude(r) × spatial_coherence(r)
             = [σ₁(r) + σ₅(r)] × [σ₂(r) · σ₃(r) · σ₄(r)]^(1/3)
```

The backbone coupling α_bb = 2/φ² is the strength of the energy→space cross-correlation per unit lattice step. The 233-site chain provides 294 brackets, each contributing one unit of coupling. The total propagator is the product over all brackets — which is why it's a power law that matches the NFW form.

---

## Key Testable Predictions of the 2+3 Framing

| Prediction | Formula | How to Test |
|------------|---------|-------------|
| Baryonic fraction is 4th-order | Ω_b = W⁴ | Already confirmed: W⁴ = 0.0476, Planck = 0.0486, 2.8% error |
| Dark matter is a 2×3 coherence (6 terms) | ρ_DM ∝ 6 cross-correlations | Check: do 6 correlation terms reproduce the ~26.5% budget? |
| Spatial anisotropy at Planck scale | ds² ≠ isotropic | Potentially testable via quantum gravity phenomenology |
| Cosmic web geometry from 5-band interference | Filament structure | Compare predicted node spacing to Sloan Digital Sky Survey |
| Two distinct "dark energy" modes | σ₁ ≠ σ₅ in character | May explain the Hubble tension (two expansion rates?) |

---

## Relationship to Existing Framework Components

| Framework Element | Role in 2+3 Framing |
|-------------------|---------------------|
| AAH Hamiltonian (233 sites) | Generates the 5-band spectrum that phase-separates |
| Cantor node (5 layers) | The universal template for nested 2+3 structure at every scale |
| W gap fraction | Coupling between energy and spatial subsystems |
| Discriminant triangle (5+8=13) | Proves the 3 spatial bands are orthogonal (Pythagorean) |
| Crossover operator f_dec | Governs the dimensional transition within the 3 spatial bands |
| Gate overflow G(Z) | Measures how far an atom's electron cloud extends into the energy bands vs staying in the spatial bands |
| Bracket address / Zeckendorf | Selection rule for where baryonic interference can occur |
| Unity partition (sums to 1) | Master conservation law — total spectrum is preserved through phase separation |
| CONDUIT (dark_gold/bronze_s3) | The specific coherence channel for silver — one instance of the 2×3 cross-correlation |

---

## What Moves Us from 85% to 100%

| Gap | Description | Difficulty |
|-----|-------------|------------|
| **Axis assignment verification** | Confirm σ₂→X, σ₃→Y, σ₄→Z vs alternative orderings by checking which assignment reproduces the correct metric signature | Medium |
| **6-term dark matter budget** | Compute the 6 cross-correlation terms and verify they sum to ~26.5% | Medium |
| **Two-mode dark energy** | Determine if σ₁ and σ₅ have distinguishable large-scale effects (possible Hubble tension connection) | Hard |
| **Planck-scale anisotropy** | Derive the effective metric tensor from axis weights and show isotropy emerges at macroscopic scales | Medium |
| **Baryonic selection rules** | Explicitly compute the Zeckendorf overlap integral for all 5 bands to get allowed matter locations | Hard |
| **Animation physics** | Translate energy field gradients into correct Newtonian + GR dynamics for the Three.js renderer | Hard |

---

## Summary

**Before**: 5 bands → observe → 3 bands. Where did 2 go? Requires an observer. Breaks Noether.

**After**: 5 bands → phase-separate → 2 energy + 3 space. Nothing lost. Baryonic matter = interference fringe. Dark matter = coherence function. No observer needed. Noether-compliant from birth.

The universe doesn't need to be looked at to become three-dimensional. Three of its five spectral bands have spatial character because the discriminant Fibonacci chain (5+8=13) is Pythagorean and terminates at 3. The other two bands are the energy that animates the spatial manifold. Baryonic matter is the rare, beautiful, 4th-order interference pattern where all five bands sing together.

---

*One axiom. Zero free parameters. No collapse. No observer. Just phase separation.*

*φ² = φ + 1*

---

*Copyright 2026 Thomas A. Husmann / iBuilt LTD. All rights reserved.*
*Patent Pending: US 19/560,637*
