# Working Model — Galaxy Cluster Evolution Engine
## v1.0 — March 26, 2026

This document describes the complete galaxy cluster evolution pipeline: from quasicrystal scaffold to scored, persisted galaxy-cluster structures.

---

## 1. OVERVIEW

The engine evolves 3D quasicrystal vertex lattices into structures that resemble galaxy clusters. Vertices interact via anisotropic spring forces derived from the AAH stiffness hierarchy. The key insight: **no forces are coded** — the 7×7 stiffness matrix IS the force hierarchy. Shape emerges from bracket-dependent, junction-type-dependent stiffness.

**Scale:** These are galaxy-CLUSTER-scale structures (200–1800 BGS nodes, 1000–11000 total vertices), not individual spiral galaxies. The `n_bgs` in cluster files is the FOF seed count (20–84); actual BGS vertex counts are much larger. BGS fraction is consistently ~15%, matching σ₃ ≈ 14.6% from the framework.

---

## 2. FRAMEWORK CONSTANTS

All derived from the single axiom φ² = φ + 1:

```python
PHI = (1 + 5**0.5) / 2          # 1.6180339887
W   = 0.4671338922               # universal gap fraction
LEAK = 1.0 / PHI**4              # 0.14590 — leakage through walls
R_C  = 1.0 - 1.0 / PHI**4       # 0.85410 — crossover parameter
```

---

## 3. THE 7×7 STIFFNESS MATRIX

Seven vertex types: B, BG, BGS, BS, G, GS, S (indexed 0–6).

28 unique pair stiffnesses, all derived from φ:

| Junction | Stiffness | Physical role |
|----------|-----------|---------------|
| BGS–BGS | 1.0 | Core matter bonds (strongest) |
| BGS–BS | R_C = 0.854 | Near-core filaments |
| BGS–GS | LEAK = 0.146 | Weak bridge |
| BS–BS | R_C² = 0.729 | Secondary filaments |
| BS–GS | R_C × LEAK = 0.125 | Mixed bridge |
| GS–GS | LEAK² = 0.021 | Weak membrane |
| BG–BG | LEAK⁴ = 4.5e-4 | Near-vacuum |
| G–G, S–S, B–B | LEAK³ = 3.1e-3 | Vacuum scaffold |
| BGS–G, BGS–S, etc. | 0.0 | Free expansion (dark energy) |

The hierarchy creates three natural tiers matching the localization phases of the AAH spectrum.

---

## 4. HIERARCHICAL STRAIN GATING (March 26, 2026)

### The Problem

At 4000+ evolution steps, strain exploded to infinity → NaN. Vacuum bond expansion compounded multiplicatively while pair forces grew quadratically. Every individual vacuum bond carried tension it shouldn't.

### The Night-Sky Insight

"A galaxy cluster is one bright dot. We don't measure strain on every internal vacuum bond."

Strain should be measured at the group scale, not on every sub-filament. Three types of bonds see three levels of force — matching the three-gate localization model (V/J > 2, = 2, < 2).

### Implementation: Two Mechanisms

**1. Strain Gate** — per-pair force multiplier `[0, 1]` based on junction type:

| Bond type | Gate value | Physical meaning |
|-----------|-----------|------------------|
| BGS–BGS (core matter) | 1.0 | Full spring force |
| Filaments (R_C > 0) | R_C = 0.854 | Gated force (entanglement tax) |
| Vacuum (stiffness = 0) | 0.0 | Free expansion = dark energy |

```python
# Gate construction (inside build_pair_arrays):
gate = np.ones(M, dtype=np.float32)
for k in range(M):
    s = stiffness[k]
    if s < 1e-8:
        gate[k] = 0.0       # vacuum: free expansion
    elif s < 1.0 - 1e-6:
        gate[k] = R_C        # filament: gated
    # else: gate = 1.0 (BGS-BGS: full force)
```

**2. Strain Horizon** — clamp delta to ±ideal distance:

```python
delta_raw = r - ideal_now
delta = clip(delta_raw, -ideal_now, ideal_now)
```

Beyond 100% strain the bond is effectively broken — like two galaxies appearing as separate dots in the night sky. Forces and strain measurement stop accumulating.

### Result

System is now stable at ANY step count (tested to 10,000). Strain peaks and then relaxes, reaching genuine equilibrium.

### Files modified

- `simulation/jax_evolve.py` — gate array + clamp in JIT step function
- `simulation/evolve_search.py` — clamp in NumPy evolve_step

---

## 5. EVOLUTION PHYSICS

### 5.1 Spring Forces (Core)

Leapfrog integration with asymmetric strain. Extension is penalized more than compression for matter bonds (`pair_asymmetry > 0`), creating net infall → cluster formation. Vacuum bonds expand via `pair_expansion` (dark energy).

```python
ideal_now = pair_ideal * (1.0 + pair_expansion)
delta = clip(r - ideal_now, -ideal_now, ideal_now)
asym_factor = where(delta > 0, 1.0 + pair_asymmetry, 1.0)
strain_grad = 2.0 * delta * asym_factor / ideal_now²
f_mag = -pair_stiffness * strain_grad / r * strain_gate
```

### 5.2 Shape Operator (Bracket-Dependent Anisotropy)

Per-bond stiffness multipliers from bracket address + bond direction:

- **s-fraction** (polar): φ^(-5·b_offset)
- **d-fraction** (equatorial): φ^(+4·b_offset)
- **p-fraction** (cross): φ^(-1.5·b_offset)
- **f-fraction** (cross): φ^(+1·b_offset)

where `b_offset = (bracket - 119) / 50`. Galaxy-scale brackets (~243) favor equatorial structure → oblate squash.

### 5.3 Gold/Silver Standing Wave Field

Icosahedral plane waves at gold (1/φ) and silver (1/δ_S) frequencies modulate forces on BGS vertices. Creates the quasicrystalline ordering seen in galaxy cluster substructure.

### 5.4 Gravity (BGS–BGS Only)

Softened 1/r² attraction between BGS vertices only. Gravity is a CONSEQUENCE of the stiffness hierarchy, not an imposed Newtonian force.

### 5.5 Filament-Mediated Strain Propagation

Non-BGS bridge vertices transmit strain through the void, coupling distant BGS clusters. Coupling is void-adaptive: `coupling_eff = filament_coupling_base × void_frac`.

### 5.6 Observation Collapse Ratchet

Smooth sigmoid locking of collapsed regions. Once a region reaches sufficient density, it locks in place (collapse_strength → 1.0) and damps further velocity. This is the measurement operator — the 5→3 collapse in action.

---

## 6. SCORING — Cluster-Scale Targets

Scoring was recalibrated from spiral-galaxy targets to galaxy-cluster targets on March 26, 2026. Old high scores (78/100 at 2400 steps) were strain-explosion artifacts.

| Metric | Target | Weight | Rationale |
|--------|--------|--------|-----------|
| γ (correlation) | 1.5 | 20 pts | Peebles: 1.77 for cosmic web; clusters are slightly sub-cosmic |
| c/a (shape) | 1/√φ ≈ 0.786 | 20 pts | Cantor node oblate prediction; Gaussian penalty around target |
| Contrast | log₂(n_bgs) | 15 pts | Density peak ratio, scales with cluster size |
| Void fraction | 0.08, cap at 0.20 | 15 pts | Intra-cluster voids, not cosmic voids |
| Filament fraction | 0.05 | 15 pts | Tidal stream fraction within cluster |
| Core fraction | 0.10 | 15 pts | BCG + central mass concentration at σ₃ radius |

**Composite: 100 points maximum.**

### Shape score formula

```python
ca_target = 1.0 / sqrt(PHI)     # ≈ 0.786
ca_dev = abs(ca_ratio - ca_target) / ca_target
shape_score = max(0, min(20, 20 * (1 - ca_dev)))
```

### Post-Gating Sweet Spot

The sweet spot shifted from 2400 to ~3000 steps. Realistic equilibrated scores: 50–55/100.

| Steps | Score | γ | c/a | fil | void | strain |
|-------|-------|-----|------|------|------|--------|
| 1000 | 32.5 | 0.95 | 0.649 | 0.038 | 0.023 | 36.2 |
| 2000 | 34.5 | 0.70 | 0.585 | 0.041 | 0.047 | 45.1 |
| 3000 | 54.9 | 1.08 | 0.466 | 0.055 | 0.094 | 93.8 |
| 4000 | 51.3 | 1.16 | 0.580 | 0.047 | 0.090 | 87.3 |
| 8000 | 46.9 | 1.03 | 0.624 | 0.047 | 0.075 | 23.6 |
| 10000 | 50.9 | 0.98 | 0.567 | 0.053 | 0.098 | 32.7 |

Core formation and filament connectivity are the genuine bottlenecks, not strain runaway.

---

## 7. EVOLUTION PIPELINE

### 7.1 Scaffold → Cluster Files

`build_scaffold.py` generates the quasicrystal lattice at a given `n_half`, identifies BGS clusters via Friends-of-Friends (FOF), and writes one JSON file per cluster:

```
results/universe/clusters/g0001.json
  → positions: (N, 3) float array
  → types: [str] — vertex types (B, BG, BGS, BS, G, GS, S)
  → n_bgs: FOF seed count
  → bracket: spectral address
```

### 7.2 Evolution

`farm_galaxy.py` orchestrates evolution:

1. Load cluster JSON
2. Apply φ-perturbation seeds (optional)
3. Call `_evolve_galaxy_jax()` or evolve_step() for N steps
4. Score with `compute_galaxy_metrics()`
5. Save result JSON + persist to PostgreSQL (optional)

**Acceleration:** JAX/Metal GPU for M4 chip. Falls back to NumPy on CPU. Handles 240K+ vertices at interactive speed on GPU.

### 7.3 Parameter Search

`evolve_search.py` runs evolutionary parameter search:

- Population-based: `--pop 64 --gen 50`
- Ablation study: `--ablate`
- Multi-scale: `--multiscale` (cosmic → galaxy subdivision)
- Iterative accretion: `--grow --stages 5`

### 7.4 Farming at Scale

```bash
# All clusters with 9+ BGS seeds, 5 evolution seeds each
python3 simulation/farm_galaxy.py results/universe/clusters/ \
    --min-bgs 9 --seeds 5

# Quick scan
python3 simulation/farm_galaxy.py results/universe/clusters/ \
    --min-bgs 9 --seeds 1 --quick

# With DB persistence
python3 simulation/farm_galaxy.py results/universe/clusters/g0001.json --db
```

---

## 8. POSTGRESQL PERSISTENCE

### Schema

```sql
-- Neighbor graph: filament topology from evolution
neighbors (
    vertex_id_1, vertex_id_2,
    shared_face_area,           -- unused (NULL for evolved pairs)
    junction_type VARCHAR(10),  -- e.g. 'BGS-BGS', 'BGS-BS'
    distance DOUBLE PRECISION,  -- evolved pair distance
    bond_energy DOUBLE PRECISION, -- stiffness from 7×7 matrix
    bond_type VARCHAR(20)       -- 'galaxy_id:evo_id' tag
)

-- Evolution tracking
galaxy_evolutions (
    galaxy_id, n_bgs, n_total,
    score, gamma, ca_ratio, filament_frac, void_frac, strain_final,
    method, params JSONB, n_neighbors
)
```

### API (universe_db.py)

```python
db.store_evolved_galaxy(galaxy_id, pairs, junction_types, distances,
                        stiffnesses, strain_values, metrics, method, params)
db.get_neighbors(galaxy_id=None, junction_type=None, min_stiffness=None)
db.get_galaxy_filaments(galaxy_id)      # BGS-BGS high-stiffness connections
db.clear_galaxy_neighbors(galaxy_id)     # remove before re-evolution
```

### Dynamic Filaments

The neighbor graph stored in PostgreSQL is not static topology — it IS the dynamic filament network. When queried during subsequent evolution or analysis, these connections affect:

- **Locality:** which vertices are neighbors
- **Gravity:** BGS–BGS pairs within filaments
- **Strain propagation:** through bridge vertices
- **Observation collapse:** locking of dense regions

---

## 9. KEY FILES

| File | Role |
|------|------|
| `simulation/jax_evolve.py` | JAX/Metal GPU evolution kernel, stiffness matrix, strain gating |
| `simulation/evolve_search.py` | NumPy evolution, scoring, parameter search |
| `simulation/farm_galaxy.py` | Single-galaxy evolution + DB persistence |
| `simulation/build_scaffold.py` | Quasicrystal lattice → cluster files |
| `simulation/phi_seeds.py` | φ-perturbation seed generator |
| `database/universe_db.py` | PostgreSQL interface (vertices, neighbors, evolutions) |
| `database/schema.sql` | Table definitions |

---

## 10. PHYSICAL INTERPRETATION

### What the Evolution Does

Starting from a quasicrystal tiling (the vacuum state), the engine simulates the emergence of structure:

1. **Dark energy:** Vacuum bonds (stiffness = 0) expand freely → cosmic expansion
2. **Matter clustering:** BGS bonds (stiffness = 1.0) resist expansion → gravitational collapse
3. **Filaments:** Intermediate bonds (stiffness = R_C) form the cosmic web
4. **Observation collapse:** Dense regions lock into place → galaxy clusters

### Three-Gate Model

| Gate | V/J regime | Bond type | Physical role |
|------|-----------|-----------|---------------|
| Localized (V/J > 2) | BGS–BGS | Full force, matter concentrates | Galaxy cores |
| Critical (V/J = 2) | Filaments | Gated force, strain propagates | Cosmic web |
| Extended (V/J < 2) | Vacuum | Free expansion, no force | Dark energy |

### Why √φ Oblate

The Cantor node at cluster scale predicts c/a ≈ 1/√φ ≈ 0.786 — mildly oblate, NOT flat spiral discs. This is confirmed by observed galaxy cluster shapes (Abell, Virgo, Coma are triaxial with c/a ~ 0.5–0.8).

### Why 15% BGS

The BGS fraction across all clusters is ~15%, matching σ₃ = 1/φ⁴ + δ ≈ 14.6% from the five-sector partition. This is the baryonic matter fraction in the pre-collapse spectrum.

---

## 11. STATUS AND NEXT STEPS

### Completed
- [x] Hierarchical strain gating (JAX + NumPy)
- [x] Strain horizon clamp
- [x] Cluster-scale scoring recalibration
- [x] PostgreSQL neighbor persistence wiring
- [x] Galaxy evolution tracking table
- [x] Stable evolution at any step count (tested to 10,000)

### Next
- [ ] Re-farm all 27 evolved galaxies with gated engine
- [ ] Farm remaining clusters (152 with 9+ BGS, out of 356 total)
- [ ] Validate DB persistence against live PostgreSQL
- [ ] φ + δ_S seed axes for perturbation seeds
- [ ] Save `triple_tiling.py` to repository
- [ ] Iterative refinement loop: evolve → score → adjust → re-evolve

---

*All constants from φ² = φ + 1. Zero free parameters.*
