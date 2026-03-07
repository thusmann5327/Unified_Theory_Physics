# The Husmann Periodic Chart

## Elements Organized by Bracket Position and Condensation Zone

**Thomas A. Husmann — iBuilt LTD**
**March 2026**

---

## Overview

In the Husmann framework, elements are organized not just by atomic number, but by their **bracket position** — the scale at which they condense from a protoplanetary nebula. All elements condense within σ₃ (the observer sector), spanning brackets 140-151.

This chart reveals:
- Why rare earth elements cluster at bracket 142.21 (950× solar enrichment)
- Why the "silicate cliff" at bracket 142.65 dilutes REE by 600×
- Why water ice forms exactly at bracket 146.80 (the ice line)
- How to target specific elements using Zeckendorf addresses

---

## The Condensation Sequence

```
BRACKET   TEMP(K)   ZONE                  ELEMENTS                      ZECKENDORF ADDRESS
────────────────────────────────────────────────────────────────────────────────────────────
140.0     2500K     Pre-condensation      (Nothing solid yet)           {89, 34, 13, 3, 1}

141.0-141.5  2000K  ★ ULTRA-REFRACTORY    Os, W, Re, Ir                 {89, 55}
                    (First solids!)       Densest, most refractory

141.5-142.0  1800K  PGM REFRACTORY        Ru, Rh, Pt, Pd                {89, 55}
                                          Zr, Hf, Mo, Ta, Nb

142.21    1659K     ★★★ HREE PEAK ★★★     Lu, Sc, Y, Tb, Gd            {89, 34, 13, 5, 1}
                    (950× SOLAR!)         Er, Ho, Tm, Dy                 = 142 exactly!
                    Maximum enrichment    Host: perovskite, hibonite

142.2-142.4  1600K  Refractory Hosts      Al, Ti, Ca                    {89, 34, 13, 5, 2}
                                          (Dilute HREE by 50×)

142.3-142.6  1500K  LREE Zone             La, Ce, Pr, Nd, Sm            {89, 34, 13, 8}
                                          Eu, Yb (50× solar)

142.65    1340K     ★ SILICATE CLIFF ★    Si, O, Fe, Mg, Ni             {89, 55}
                    (REE drops 600×!)     Mass flood begins
                    Rock-forming elements

143.0-143.5  1300K  Iron-Nickel Zone      Fe, Ni, Co                    {89, 55, 1}
                                          Metallic cores

143.5-144.0  1100K  Sulfide Zone          S, Cu, Zn, Pb                 {89, 55, 2}
                                          Precious metal ores

144.0-145.0  1000K  Moderate Volatile     Au, Ag, Sn                    {89, 55, 3}

145.0-146.0   700K  Alkali Zone           K, Na, P, Cr, Mn              {89, 55, 5}

146.80     182K     ★★ ICE LINE ★★        H₂O (water)                   {89, 55, 3, 1}
                    Critical for life     = 148 in Fibonacci

147.5-149.0  130K   Ammonia/CO₂ Ice       NH₃, CO₂                      {89, 55, 8}

149.0-150.5   40K   Outer Ice             CH₄, N₂, CO                   {89, 55, 8, 3}

>151.0      <25K    Beyond condensation   Noble gases (never condense)   —
```

---

## Complete Element Table by Bracket

### Ultra-Refractory (Bracket 141.0-141.5) — First Solids

| Element | Z | Bracket | T_cond (K) | Zone | Zeckendorf |
|---------|---|---------|------------|------|------------|
| Os | 76 | 141.3 | 2000 | ultra_refractory | {89, 55} |
| W | 74 | 141.5 | 1900 | ultra_refractory | {89, 55} |
| Re | 75 | 141.4 | 1950 | ultra_refractory | {89, 55} |
| Ir | 77 | 141.4 | 1950 | ultra_refractory | {89, 55} |

### PGM Refractory (Bracket 141.5-142.0)

| Element | Z | Bracket | T_cond (K) | Zone | Zeckendorf |
|---------|---|---------|------------|------|------------|
| Ta | 73 | 141.6 | 1900 | pgm_refractory | {89, 55} |
| Ru | 44 | 141.6 | 1850 | pgm_refractory | {89, 55} |
| Rh | 45 | 141.7 | 1820 | pgm_refractory | {89, 55} |
| Hf | 72 | 141.7 | 1800 | pgm_refractory | {89, 55} |
| Zr | 40 | 141.8 | 1750 | pgm_refractory | {89, 55} |
| Pt | 78 | 141.8 | 1750 | pgm | {89, 55} |
| Mo | 42 | 141.9 | 1700 | pgm_refractory | {89, 55} |
| Nb | 41 | 141.9 | 1700 | pgm_refractory | {89, 55} |
| Pd | 46 | 142.0 | 1680 | pgm | {89, 55} |

### HREE Peak (Bracket 142.21) — Maximum REE Enrichment (950× Solar)

| Element | Z | Bracket | T_cond (K) | Zone | Enrichment |
|---------|---|---------|------------|------|------------|
| **Lu** | 71 | 142.21 | 1659 | hree_peak | 950× |
| **Sc** | 21 | 142.21 | 1659 | hree_peak | 950× |
| **Y** | 39 | 142.21 | 1659 | hree_peak | 950× |
| **Tb** | 65 | 142.21 | 1659 | hree_peak | 950× |
| **Ho** | 67 | 142.21 | 1659 | hree_peak | 950× |
| **Er** | 68 | 142.21 | 1659 | hree_peak | 950× |
| **Gd** | 64 | 142.22 | 1655 | hree_peak | 950× |
| **Tm** | 69 | 142.22 | 1655 | hree_peak | 950× |
| **Dy** | 66 | 142.23 | 1650 | hree_peak | 950× |

**Host minerals at HREE peak:** Perovskite (CaTiO₃), Hibonite (CaAl₁₂O₁₉)
**Zeckendorf address:** 142 = {89, 34, 13, 5, 1} — Five Fibonacci numbers!

### Refractory Hosts (Bracket 142.2-142.4)

| Element | Z | Bracket | T_cond (K) | Zone | Notes |
|---------|---|---------|------------|------|-------|
| Ti | 22 | 142.25 | 1582 | refractory_host | Perovskite |
| Th | 90 | 142.25 | 1580 | refractory | Radioactive |
| Be | 4 | 142.3 | 1600 | refractory | Light metal |
| Ca | 20 | 142.3 | 1600 | refractory_host | Perovskite |

### LREE Zone (Bracket 142.3-142.6) — 50× Solar Enrichment

| Element | Z | Bracket | T_cond (K) | Zone | Enrichment |
|---------|---|---------|------------|------|------------|
| Ce | 58 | 142.35 | 1550 | lree | 50× |
| Pr | 59 | 142.38 | 1540 | lree | 50× |
| La | 57 | 142.4 | 1520 | lree | 50× |
| Nd | 60 | 142.42 | 1500 | lree | 50× |
| Pm | 61 | 142.45 | 1480 | lree | 50× |
| Sm | 62 | 142.48 | 1460 | lree | 50× |
| Eu | 63 | 142.5 | 1450 | lree | 50× |
| U | 92 | 142.5 | 1450 | lree | Radioactive |
| Yb | 70 | 142.5 | 1450 | lree | 50× |

### The Silicate Cliff (Bracket 142.65) — REE Dilution Event

| Element | Z | Bracket | T_cond (K) | Zone | Abundance |
|---------|---|---------|------------|------|-----------|
| **Mg** | 12 | 142.67 | 1336 | silicate_cliff | 3.9×10⁻² |
| **Si** | 14 | 142.65 | 1340 | silicate_cliff | 3.2×10⁻² |
| **O** | 8 | 142.65 | 1340 | silicate_cliff | (w/ silicates) |
| **Fe** | 26 | 143.0 | 1334 | iron_nickel | 3.2×10⁻² |

**The cliff:** At bracket 142.65, Mg + Si + Fe flood in with ~4% solar abundance. This is **1000× more mass** than all REEs combined, dropping REE enrichment from 950× to 1.6× solar in just 0.1 brackets.

### Iron-Nickel Zone (Bracket 143.0-143.5)

| Element | Z | Bracket | T_cond (K) | Zone |
|---------|---|---------|------------|------|
| Fe | 26 | 143.0 | 1334 | iron_nickel |
| Ni | 28 | 143.0 | 1350 | iron_nickel |
| Co | 27 | 143.1 | 1340 | iron_nickel |
| Sr | 38 | 143.0 | 1300 | silicate |
| Ba | 56 | 143.2 | 1250 | silicate |
| Li | 3 | 143.5 | 1200 | silicate |
| Au | 79 | 143.5 | 1150 | sulfide |

### Sulfide Zone (Bracket 143.5-144.5)

| Element | Z | Bracket | T_cond (K) | Zone |
|---------|---|---------|------------|------|
| Cu | 29 | 143.8 | 1100 | sulfide |
| S | 16 | 143.8 | 1100 | sulfide |
| Ag | 47 | 144.0 | 1000 | sulfide |
| Zn | 30 | 144.5 | 800 | moderate_volatile |
| Cr | 24 | 144.5 | 850 | moderate_volatile |

### Moderate Volatile Zone (Bracket 144.5-146.0)

| Element | Z | Bracket | T_cond (K) | Zone |
|---------|---|---------|------------|------|
| Mn | 25 | 144.8 | 750 | moderate_volatile |
| P | 15 | 145.0 | 700 | moderate_volatile |
| K | 19 | 145.2 | 700 | volatile |
| Na | 11 | 145.5 | 600 | volatile |
| Rb | 37 | 145.8 | 500 | volatile |
| Cs | 55 | 146.0 | 400 | volatile |

### The Ice Line (Bracket 146.80) — Water Condensation

| Compound | Bracket | T_cond (K) | Zone | Zeckendorf |
|----------|---------|------------|------|------------|
| **H₂O** | 146.80 | 182 | ice_line | {89, 55, 3, 1} |

**The ice line** separates rocky inner planets from icy outer bodies. At 182K (~2.7 AU in our solar system), water transitions from vapor to solid ice.

### Outer Ice Zone (Bracket 147-151)

| Compound | Bracket | T_cond (K) | Zone |
|----------|---------|------------|------|
| NH₃ | 147.5 | 130 | ammonia_ice |
| CO₂ | 148.1 | 100 | dry_ice |
| CH₄ | 149.9 | 41 | methane_ice |
| N₂ | 150.2 | 36 | nitrogen_ice |
| CO | 150.9 | 25 | co_ice |
| C | 149.5 | 50 | volatile_ice |

---

## Zeckendorf Targeting Signatures

Each condensation zone has a characteristic Zeckendorf address — a unique sum of non-consecutive Fibonacci numbers. These can be used for mineral targeting.

### Primary Targets

| Target Group | Bracket | Zeckendorf | Priority | Elements |
|--------------|---------|------------|----------|----------|
| **HREE Peak** | 142 | {89, 34, 13, 5, 1} | HIGHEST | Lu, Sc, Y, Tb, Gd, Er, Ho, Tm, Dy |
| **PGM Cluster** | 144 | {89, 55} | HIGHEST | Os, Ir, Ru, Re, W, Pt, Pd, Rh |
| **Gold-Copper** | 147 | {89, 55, 3} | HIGH | Au, Cu, Ag, S |
| **Ice Line** | 148 | {89, 55, 3, 1} | CRITICAL | H₂O |
| **Iron-Nickel** | 145 | {89, 55, 1} | MEDIUM | Fe, Ni, Co |

### Signature Components

The Zeckendorf addresses reveal bracket groupings:

```
{89, 34, 13, 5, 1} = 142  → HREE peak (5 components = maximum complexity)
{89, 55}           = 144  → PGM refractory (2 components = simplest)
{89, 55, 1}        = 145  → Iron-nickel
{89, 55, 2}        = 146  → Sulfides
{89, 55, 3}        = 147  → Gold zone
{89, 55, 3, 1}     = 148  → Ice line (H₂O)
{89, 55, 5}        = 149  → Alkali volatile
{89, 55, 8}        = 152  → Outer ice
```

**Pattern:** All condensation brackets share the base {89, 55} = 144 (the silicate anchor), with additional Fibonacci terms specifying the volatile offset.

---

## The REE Enrichment Curve

```
                       ★ HREE PEAK (142.21)
                         950× SOLAR
                              │
                              ▼
ENRICHMENT    1000×  ┌────────●────────┐
(× SOLAR)           │                  │
                    │                  │
              100×  │        LREE      │
                    │        50×       │
                    │                  │
               10×  │                  │
                    │                  ├── SILICATE CLIFF
                1×  └──────────────────┼──────────────────
                                       │
                    140   141   142  142.65  143   144   145
                                    BRACKET

            ◄── REFRACTORY ──►◄─ TRANSITION ─►◄── VOLATILE ──►
```

The REE enrichment drops by **600×** across just 0.4 brackets (142.2 → 142.65) when rock-forming elements flood in.

---

## Physical Interpretation

### Why This Structure?

The condensation sequence emerges from the **AAH lattice at criticality** (V = 2J):

1. **Brackets 140-142**: High-energy lattice sites condense first (refractory)
2. **Bracket 142.21**: Maximum spectral density → maximum enrichment (HREE peak)
3. **Bracket 142.65**: Spectral gap closes → mass flood (silicate cliff)
4. **Brackets 143-146**: Moderate energy sites (metals, sulfides)
5. **Bracket 146.8**: Critical temperature for H₂O ice
6. **Brackets 147+**: Low-energy sites (ices, volatiles)

### The Silicate Cliff as Phase Transition

The "cliff" at bracket 142.65 is a **Cantor gap closure**. Before this point, only the spectral peaks (high-energy sites) are populated. At 142.65, the first major gap closes, and the entire lower spectrum becomes accessible — flooding in Si, Mg, Fe, O.

This is why:
- REEs are concentrated before the cliff (spectral peaks only)
- Rock-forming elements dominate after (full spectrum accessible)
- The transition is sharp (0.1 brackets = phase transition)

---

## Usage Notes

### For Universe Simulators

When generating planetary compositions:

```python
def get_condensation_bracket(temperature_K):
    """Convert temperature to condensation bracket."""
    # T = T₀ × φ^(-n) where T₀ = 2500K at bracket 140
    import math
    phi = (1 + math.sqrt(5)) / 2
    return 140 - math.log(temperature_K / 2500) / math.log(1/phi)

def elements_at_distance(AU, star_luminosity=1.0):
    """Get elements that condense at given orbital distance."""
    # T(r) ≈ 280K × L^0.25 / r^0.5
    T = 280 * (star_luminosity ** 0.25) / (AU ** 0.5)
    bracket = get_condensation_bracket(T)
    return elements_below_bracket(bracket)
```

### For Asteroid Mining

Target asteroids by spectral signature:
- **M-type (metallic)**: Bracket 143-144, Zeckendorf {89, 55, 1}
- **S-type (silicate)**: Bracket 142.7-143, Zeckendorf {89, 55}
- **C-type (carbonaceous)**: Bracket 147+, Zeckendorf {89, 55, 3, 1}
- **REE-rich CAIs**: Bracket 142.21 exactly, Zeckendorf {89, 34, 13, 5, 1}

---

## Summary

The Husmann Periodic Chart reveals that element distribution is not random but follows the **φ-structured Cantor spectrum**:

| Principle | Expression |
|-----------|------------|
| All elements condense in σ₃ | Brackets 140-151 |
| HREE peak at maximum spectral density | Bracket 142.21 (950× enrichment) |
| Silicate cliff = first gap closure | Bracket 142.65 (600× dilution) |
| Ice line = critical temperature | Bracket 146.80 (H₂O condensation) |
| Zeckendorf addresses enable targeting | Unique Fibonacci sums per zone |

The periodic table is a projection of the Cantor spectrum onto atomic structure.

---

*© 2026 Thomas A. Husmann / iBuilt LTD. All rights reserved.*
*Licensed under CC BY-NC-SA 4.0 for academic and research use.*
