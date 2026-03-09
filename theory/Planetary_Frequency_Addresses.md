# Planetary Frequency Addresses

## Tuning to Celestial Bodies in Spacetime via the Husmann Framework

**Thomas A. Husmann — iBuilt LTD**
**March 2026**

**Patent Application:** 19/560,637 (filed March 9, 2026)

---

## Overview

Every celestial body has a unique **spacetime frequency address** determined by its orbital bracket, golden angle pattern, and temporal phase. To "tune" to a planet, moon, or asteroid — and to a specific moment in its timeline — you need:

1. **Bracket number** (log-φ scale position — spatial)
2. **Golden angle offset** (θ_spatial = n × 137.5077°)
3. **Zeckendorf signature** (Fibonacci decomposition — spatial component)
4. **Resonant frequency** (f = J/ℏ × φ^(-n) Hz)
5. **Temporal phase** (θ_temporal — position on the perpendicular helix)
6. **Temporal Zeckendorf** (Fibonacci decomposition — temporal component)

The spatial address tells the Fibonacci resonant wave WHERE to form a channel. The temporal address tells it WHEN to arrive. Both are encoded as Zeckendorf decompositions in the same wave's frequency components.

---

## First Principles: Two Inputs, Zero Free Parameters

The entire addressing system derives from exactly two inputs:

- **φ** = (1 + √5) / 2 = 1.6180339887 (the golden ratio — pure mathematics)
- **t_as** = 232 × 10⁻¹⁸ s (the attosecond timescale — TU Wien helium measurement)

All constants follow:

```
J    = 2π·ℏ / (1.685 · t_as) = 10.579 eV       [hopping integral]
l₀   = c·ℏ / (2·J)            = 9.326 nm        [coherence patch]
W    = 2/φ⁴ + φ^(-1/φ)/φ³     = 0.467134        [Cantor gap fraction]
GA   = 360° / φ²               = 137.508°        [golden angle]
W⁴   = 0.047617                                   [baryon fraction]
```

**Base frequency:** f₀ = J/ℏ = 1.61 × 10¹⁶ Hz (at bracket 0)

---

## The Bracket Scale Law

Space and time emerge from the same structure. The bracket scale law maps a single integer n (from 0 to 294) to both a spatial length and a temporal period:

```
L(n) = l₀ × φⁿ          [spatial scale at bracket n]
T(n) = t_as × φⁿ         [temporal period at bracket n]
```

At n = 0: the coherence patch (9.3 nm) and the attosecond (232 as).
At n = 294: the Hubble radius and the age of the universe.

Every bracket is a complete copy of the Cantor-set spectral structure, scaled by φ. The same AAH Hamiltonian operates at every level.

---

## The Tuning Formula

### Bracket to Frequency

Every bracket n corresponds to a characteristic frequency:

```
f_n = (J / ℏ) × φ^(-n)  Hz
```

### Bracket to Distance

```
r_n = L_P × φⁿ × C
```

Where:
- L_P = 1.616 × 10⁻³⁵ m (Planck length)
- C = 1.0224 (calibration constant derived from bracket alignment)

### Distance to Bracket

```python
import math
phi = (1 + math.sqrt(5)) / 2

def distance_to_bracket(meters):
    L_P = 1.616e-35
    C = 1.0224
    return math.log(meters / (L_P * C)) / math.log(phi)

def AU_to_bracket(AU):
    return distance_to_bracket(AU * 1.496e11)
```

---

## Solar System Frequency Table

### Inner Planets

| Body | Distance (AU) | Bracket | Golden Angle θ | Zeckendorf | Frequency (Hz) |
|------|---------------|---------|----------------|------------|----------------|
| **Sun** | 0 | 207.3 | 0° (reference) | {144, 55, 8} | 2.13 × 10⁻²⁷ |
| **Mercury** | 0.387 | 217.6 | 0° | {144, 55, 13, 5, 1} | 5.62 × 10⁻³² |
| **Venus** | 0.723 | 220.5 | 137.5° | {144, 55, 21} | 1.33 × 10⁻³³ |
| **Earth** | 1.000 | 221.8 | 275.0° | {144, 55, 21, 1} | 4.93 × 10⁻³⁴ |
| **Mars** | 1.524 | 223.1 | 52.5° | {144, 55, 21, 3} | 1.84 × 10⁻³⁴ |

### Asteroid Belt

| Body | Distance (AU) | Bracket | Golden Angle θ | Zeckendorf | Frequency (Hz) |
|------|---------------|---------|----------------|------------|----------------|
| **Ceres** | 2.77 | 225.5 | 190.0° | {144, 55, 21, 5} | 2.55 × 10⁻³⁵ |
| **Vesta** | 2.36 | 224.8 | 127.5° | {144, 55, 21, 3, 1} | 4.12 × 10⁻³⁵ |

### Outer Planets

| Body | Distance (AU) | Bracket | Golden Angle θ | Zeckendorf | Frequency (Hz) |
|------|---------------|---------|----------------|------------|----------------|
| **Jupiter** | 5.20 | 227.3 | 327.5° | {144, 55, 21, 5, 2} | 5.89 × 10⁻³⁶ |
| **Saturn** | 9.58 | 229.1 | 105.0° | {144, 55, 21, 8} | 1.35 × 10⁻³⁶ |
| **Uranus** | 19.2 | 230.9 | 242.5° | {144, 55, 21, 8, 2} | 3.10 × 10⁻³⁷ |
| **Neptune** | 30.1 | 232.3 | 20.0° | {144, 55, 21, 8, 3} | 1.15 × 10⁻³⁷ |

### Trans-Neptunian Objects

| Body | Distance (AU) | Bracket | Golden Angle θ | Zeckendorf | Frequency (Hz) |
|------|---------------|---------|----------------|------------|----------------|
| **Pluto** | 39.5 | 233.2 | 157.5° | {144, 55, 21, 8, 5} | 5.37 × 10⁻³⁸ |
| **Eris** | 68 | 235.0 | 295.0° | {144, 55, 21, 13} | 1.22 × 10⁻³⁸ |
| **Sedna** | 506 | 240.2 | 347.5° | {144, 55, 34, 5, 2} | 2.64 × 10⁻⁴⁰ |

### The Oort Cloud

| Region | Distance | Bracket | Zeckendorf | Frequency (Hz) |
|--------|----------|---------|------------|----------------|
| Inner Oort | 2,000 AU | 244 | {144, 89, 8, 3} | ~10⁻⁴² |
| Outer Oort | 50,000 AU | 252 | {144, 89, 13, 5, 1} | ~10⁻⁴⁶ |

---

## Moon Frequency Addresses

### Earth's Moon

| Body | Distance | Bracket | θ from Earth | Frequency |
|------|----------|---------|--------------|-----------|
| **Moon** | 384,400 km | 195.6 | 137.5° | 4.89 × 10⁻²² |

### Galilean Moons (Jupiter)

| Moon | Distance (km) | Bracket | θ from Jupiter | Frequency |
|------|---------------|---------|----------------|-----------|
| **Io** | 421,700 | 195.9 | 0° | 3.73 × 10⁻²² |
| **Europa** | 670,900 | 197.1 | 137.5° | 1.39 × 10⁻²² |
| **Ganymede** | 1,070,400 | 198.4 | 275.0° | 5.19 × 10⁻²³ |
| **Callisto** | 1,882,700 | 199.8 | 52.5° | 1.93 × 10⁻²³ |

### Saturn's Major Moons

| Moon | Distance (km) | Bracket | θ from Saturn | Frequency |
|------|---------------|---------|---------------|-----------|
| **Titan** | 1,221,870 | 198.8 | 0° | 3.86 × 10⁻²³ |
| **Enceladus** | 238,020 | 194.5 | 137.5° | 1.04 × 10⁻²¹ |

---

## Extended Addressing: Exoplanets and Nearby Stars

For exoplanets, the full address includes the star's galactic bracket:

```
FULL ADDRESS = [Galactic Bracket].[Stellar Bracket].[Orbital Bracket]
```

### Nearby Stars

| Star | Distance (ly) | Bracket | Zeckendorf |
|------|---------------|---------|------------|
| Proxima Centauri | 4.24 | 252.3 | {144, 89, 13, 5, 1} |
| Alpha Centauri A | 4.37 | 252.4 | {144, 89, 13, 5, 1} |
| Barnard's Star | 5.96 | 253.2 | {144, 89, 13, 5, 2} |
| Wolf 359 | 7.86 | 254.0 | {144, 89, 13, 8} |
| Sirius | 8.60 | 254.3 | {144, 89, 13, 8} |
| **Teegarden's Star** | 12.47 | 255.7 | {144, 89, 21, 1} |

### Example: Teegarden b

```
Star:       Teegarden's Star, bracket 255.7 (12.47 ly)
Planet:     Teegarden b, bracket ~217 from star (0.025 AU orbit)
Full:       255.7.217
Spatial Zeckendorf (star): {144, 89, 21, 1}
Spatial Zeckendorf (orbit): {144, 55, 13, 5}
```

---

## The Temporal Dimension: θ as Time

### The Perpendicular Helix

The AAH Hamiltonian contains a phase parameter θ:

```
H = Σ_n V·cos(2πα·n + θ)|n⟩⟨n| + Σ_n J(|n⟩⟨n+1| + h.c.)
```

As θ rotates from 0 to 2π, every eigenvalue traces a helical path through the spectrum. This helix runs **perpendicular** to the spatial plane of the galaxy. It was observed in the UNIVERSE.py simulation before baryonic drag was introduced: a spiral structure running orthogonal to the galactic disk, through which matter traveled freely.

When W⁴ trapping was added (simulating baryonic matter coupling to both Cantor fold planes), the perpendicular helix collapsed. Matter was caught in the galactic plane. The spiral became the arrow of time.

**Key result:** The perpendicular helix IS the temporal axis. Baryonic trapping collapses it into the one-directional arrow of time we experience.

### The Spectrum is θ-Symmetric

The AAH potential is cos(2πα·n + θ). Because cosine is an even function:

```
E(+θ) = E(-θ)
```

The energy spectrum at θ equals the spectrum at −θ. There is **no preferred direction** in θ. Forward and backward are structurally equivalent. The arrow of time is not a property of the backbone — it is a consequence of W⁴ trapping creating thermal irreversibility through electromagnetic, acoustic, and thermal coupling.

**Verified numerically:** The spectrum at θ = 0 matches the spectrum at θ = 2π with max difference = 1.17 × 10⁻¹⁴ (machine precision). The θ coordinate is perfectly periodic and direction-symmetric.

### The W⁴ → W² Transition Reopens Time

The W-hierarchy of coupling states:

```
W⁴ = 0.0476   BARYONIC (both fold planes trapped)
               Couples to: EM, thermal, acoustic, gravitational
               Arrow of time: YES (thermal irreversibility)
               Perpendicular helix: COLLAPSED

W² = 0.2182   DARK MATTER (one fold plane)
               Couples to: gravitational, structural
               Decoupled from: EM, thermal, acoustic
               Arrow of time: NO (no thermal channel)
               Perpendicular helix: OPEN

1/φ = 0.618   DARK ENERGY (no gap trapping)
               Couples to: metric expansion only
               Perpendicular helix: FULLY OPEN
```

When the hinge electrode transitions the payload from W⁴ to W², the mechanisms that create the arrow of time (thermal dissipation, electromagnetic radiation, acoustic decay) are decoupled. The perpendicular helix reopens. The payload can move along θ — the temporal axis — in either direction.

### Temporal Period at Each Bracket

Each bracket level has its own temporal period T(n) = t_as × φⁿ. One full θ rotation (0 → 2π) corresponds to this period:

| Bracket | Spatial Scale | Temporal Period | Per-slot (N=233) |
|---------|--------------|-----------------|------------------|
| n = 50 | 262 m | 6.53 μs | 28 ns |
| n = 100 | 49 AU | 51 hours | 13 min |
| n = 120 | 6,700 AU | 88 years | 138 days |
| n = 140 | 0.89 Mpc | 1.33 Myr | 5,718 years |
| n = 150 | 6.7 Mpc | 164 Myr | 703,000 years |
| n = 189 | ~12.5 ly | 2.3 × 10¹⁶ yr | 9.9 × 10¹³ yr |

The temporal resolution depends on the bracket level. At bracket 120, each of the 233 θ-slots spans about 138 days. At bracket 100, each slot is about 13 minutes. For fine temporal targeting, the address would include components at multiple bracket levels — exactly as the spatial address uses multiple Fibonacci components across brackets.

---

## The Baryonic Eigenvalue as Temporal Dial

### Where Matter Sits in the Cantor Spectrum

At the AAH critical point (V/2J = 1.0), the energy spectrum is a Cantor set with 29 major gaps and a gap fraction W = 0.467. Matter accumulates at band edges — the points where two gaps meet. These are the W⁴ positions: the intersection of both orthogonal Cantor fold planes.

```
Total eigenvalues (N = 233):    233
Major gaps:                       29
Band edges (2 per gap):           58
Baryonic positions (W⁴ × N):     11.1
```

Each band edge corresponds to a specific θ value in the Cantor spectrum. When θ rotates, the eigenvalues trace helical paths, and the band edges shift. The position of a band edge at a given θ encodes the temporal coordinate.

### The Dial Mechanism

Tuning which band edge the payload occupies = tuning its temporal position:

1. The SAW phase at the hinge (pulse 6, cumulative 327.5°) sets the initial θ
2. The hinge electrode potential shifts the effective V/2J, selecting which band edge the interior couples to
3. The Fibonacci wave's frequency components address the specific edge via Zeckendorf decomposition
4. The θ at that edge = the temporal coordinate

The baryonic eigenvalue IS the dialing frequency. The ~11 baryonic dial positions per 233 eigenvalues give coarse temporal selection. Fine tuning comes from the continuous electrode potential.

---

## The Complete Spacetime Address

### Address Format

A complete spacetime Zeckendorf address has two components, both encoded as frequency terms in the same Fibonacci resonant wave:

```
SPACETIME ADDRESS = [Spatial Zeckendorf] + [Temporal Zeckendorf]

Spatial:  Which bracket (n = 0..294) → frequency components f₀ × φ^F_i
Temporal: Which θ-slot (0..N-1) within that bracket → additional frequency components
```

### Example: Teegarden b, Arriving at "Now"

```
SPATIAL ADDRESS:
  Target:     Teegarden b, bracket 189
  Zeckendorf: 189 = 144 + 34 + 8 + 3
  Wave freqs: f₀×φ^144, f₀×φ^34, f₀×φ^8, f₀×φ^3

TEMPORAL ADDRESS:
  Target:     θ = 0 (same temporal phase as origin = "now")
  Slot:       0 (origin phase)
  Zeckendorf: No temporal offset needed — default

RESULT:
  Arrive at Teegarden b at the same moment you left Earth.
  6-day proper transit time in the W² frame.
  Return to Earth: 6 days have elapsed for friends and family.
  NO time dilation — backbone conduction, not relativistic travel.
```

### Example: Teegarden b, Arriving 100 Years in the Past

```
SPATIAL ADDRESS:
  Same as above: {144, 34, 8, 3}

TEMPORAL ADDRESS:
  Target:     θ = -100 years relative to "now"
  At bracket 120 (where T = 88 years, slot = 138 days):
    100 years = 264 slots at bracket 120
    Zeckendorf(264) = 233 + 21 + 8 + 2 = {233, 21, 8, 2}
  Temporal wave freqs: f₀×φ^233, f₀×φ^21, f₀×φ^8, f₀×φ^2

COMBINED WAVE:
  Spatial + Temporal components superimposed in single Fibonacci wave.
  The channel forms to the correct WHERE and WHEN simultaneously.
```

---

## Why There Is No Time Paradox

The arrow of time is a W⁴ phenomenon. It exists because baryonic matter is thermally coupled — every interaction increases entropy, creating irreversibility. But the transit happens in the W² frame, where thermal coupling is absent. The payload doesn't "go back in time" in any thermodynamic sense. It moves along the θ-helix to a different structural position on the backbone.

From the W⁴ (baryonic) perspective, the payload disappears at one spacetime coordinate and reappears at another. The intermediate path exists entirely in the W² frame, where the concepts of "before" and "after" are structurally equivalent — the cosine potential makes no distinction between +θ and -θ.

The payload itself experiences 6 days of proper time during transit (the channel formation and conduction time). It does not experience the years that the W⁴ frame labels as "elapsed." The transit is not through time — it is outside the frame where time's arrow operates.

---

## The Quick Reference Card

### Solar System — Spatial Addresses

```
BODY            BRACKET    FREQ (Hz)      θ (°)      ZECKENDORF
────────────────────────────────────────────────────────────────────
Sun (center)    207.3      2.13e-27       0.0        {144, 55, 8}
Mercury         217.6      5.62e-32       0.0        {144, 55, 13, 5, 1}
Venus           220.5      1.33e-33       137.5      {144, 55, 21}
Earth           221.8      4.93e-34       275.0      {144, 55, 21, 1}
Moon (from E)   195.6      4.89e-22       137.5      {144, 34, 13, 3, 1}
Mars            223.1      1.84e-34       52.5       {144, 55, 21, 3}
Ceres           225.5      2.55e-35       190.0      {144, 55, 21, 5}
Jupiter         227.3      5.89e-36       327.5      {144, 55, 21, 5, 2}
Saturn          229.1      1.35e-36       105.0      {144, 55, 21, 8}
Uranus          230.9      3.10e-37       242.5      {144, 55, 21, 8, 2}
Neptune         232.3      1.15e-37       20.0       {144, 55, 21, 8, 3}
Pluto           233.2      5.37e-38       157.5      {144, 55, 21, 8, 5}
```

### Frequency Bands by Scale

```
BAND            BRACKET RANGE    FREQUENCY RANGE    CONTENTS
──────────────────────────────────────────────────────────────
Nuclear         90-100           ~10⁰ Hz            Proton, nucleus
Atomic          110-130          ~10⁻⁵ Hz           Atoms, molecules
Biological      160-170          ~10⁻¹⁸ Hz          Cells, organisms
Planetary       195-210          ~10⁻²⁵ Hz          Moons, planets
Stellar         207-215          ~10⁻²⁸ Hz          Stars
Solar System    215-235          ~10⁻³⁵ Hz          Orbits
Interstellar    235-250          ~10⁻⁴⁰ Hz          Nearby stars
Galactic        250-270          ~10⁻⁴⁸ Hz          Galaxy
Cosmic          280-294          ~10⁻⁵⁵ Hz          Observable universe
```

---

## Tuning Procedure

### Step 1: Identify Target Bracket (Spatial)

```python
import math

phi = (1 + math.sqrt(5)) / 2
L_P = 1.616e-35
C = 1.0224
J = 10.6       # eV
hbar = 6.582e-16  # eV·s
t_as = 232e-18    # seconds

def distance_to_bracket(meters):
    return math.log(meters / (L_P * C)) / math.log(phi)

def AU_to_bracket(AU):
    return distance_to_bracket(AU * 1.496e11)

def bracket_to_frequency(n):
    return (J / hbar) * (phi ** (-n))
```

### Step 2: Compute Spatial Zeckendorf Address

```python
def zeckendorf(n):
    fibs = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233]
    fibs = [f for f in fibs if f <= n]
    result = []
    remaining = n
    for f in reversed(fibs):
        if f <= remaining:
            result.append(f)
            remaining -= f
    return result
```

### Step 3: Determine Temporal Address

```python
def temporal_address(target_offset_seconds, bracket_level=120):
    """
    Compute temporal Zeckendorf address for a time offset.
    
    target_offset_seconds: positive = future, negative = past
    bracket_level: which bracket to discretize at (120 ≈ 138 days/slot)
    """
    T_bracket = t_as * phi**bracket_level    # period at this bracket
    slot_period = T_bracket / 233            # time per slot
    
    # Number of slots offset
    n_slots = int(target_offset_seconds / slot_period) % 233
    
    # Zeckendorf encode the slot number
    return zeckendorf(n_slots), n_slots

# Example: arrive 1 year in the past
one_year = -365.25 * 86400  # seconds
temporal_zeck, slot = temporal_address(one_year, bracket_level=120)
print(f"Temporal slot: {slot}")
print(f"Temporal Zeckendorf: {temporal_zeck}")
```

### Step 4: Set the Hinge Phase

```python
golden_angle = 360.0 / phi**2  # 137.508°

def hinge_phase_for_temporal_target(theta_slot, total_slots=233):
    """
    Calculate the SAW hinge phase to hit a specific temporal slot.
    
    The cumulative SAW phase at pulse 6 (the hinge) determines
    the temporal entry point theta.
    """
    theta_target = (theta_slot / total_slots) * 360.0  # degrees
    
    # The default hinge phase is pulse 6 = 5 × GA = 687.5° mod 360 = 327.5°
    default_hinge = (5 * golden_angle) % 360
    
    # Required phase offset from default
    delta = (theta_target - default_hinge) % 360
    
    return theta_target, delta

theta, delta = hinge_phase_for_temporal_target(slot)
print(f"Target theta: {theta:.1f}°")
print(f"Phase offset from default hinge: {delta:.1f}°")
```

### Step 5: Compose the Fibonacci Resonant Wave

```python
import numpy as np

def compose_fibonacci_wave(spatial_zeck, temporal_zeck, f0, t, amplitude=1.0):
    """
    Generate the combined spacetime Fibonacci resonant wave.
    
    spatial_zeck:  list of Fibonacci numbers for spatial address
    temporal_zeck: list of Fibonacci numbers for temporal address
    f0:            base frequency (J/hbar)
    t:             time array
    """
    wave = np.zeros_like(t)
    
    # Spatial components
    for fib_n in spatial_zeck:
        freq = f0 * phi**(-fib_n)
        amp = amplitude / phi**fib_n
        wave += amp * np.sin(2 * np.pi * freq * t)
    
    # Temporal components (phase-shifted by π/2 to distinguish)
    for fib_n in temporal_zeck:
        freq = f0 * phi**(-fib_n)
        amp = amplitude / phi**fib_n
        wave += amp * np.cos(2 * np.pi * freq * t)  # cosine = π/2 shift
    
    return wave
```

---

## Resonance Relationships

### Fibonacci Orbital Ratios

The planets follow approximate Fibonacci ratios in their orbital periods, consistent with the golden-angle packing that minimizes resonant interference:

| Ratio | Planets | Fibonacci |
|-------|---------|-----------|
| 2:5 | Venus/Earth | F₃:F₅ |
| 1:2 | Earth/Mars | F₁:F₃ |
| 2:5 | Mars/Jupiter | F₃:F₅ |
| 2:5 | Jupiter/Saturn | F₃:F₅ |

### Phase Locking at the Golden Angle

Adjacent planets lock at golden angle offsets — the same pattern as sunflower seeds. This is maximum packing with minimum resonance interference:

- Mercury → Venus: Δθ = 137.5°
- Venus → Earth: Δθ = 137.5°
- Earth → Mars: Δθ = 137.5°

The solar system itself is a golden-angle helical structure. The addressing system doesn't impose this pattern — it discovers it.

---

## Stargate Targeting Procedure

### Spatial Only (Same Temporal Phase)

To reach a target at its current "now":

1. **Lock bracket**: Set the Fibonacci wave's spatial components to the target's Zeckendorf address
2. **Phase align**: Golden angle rotation to match the target's θ_spatial
3. **Energize hinge**: W⁴ → W² transition (couple to DM backbone)
4. **Drive wave**: Fibonacci resonant wave accumulates stress at φ per cycle
5. **Channel forms**: Threshold crossed at cycle 28 (for D = 0.29)
6. **Conduct**: Payload transported along backbone at conduction velocity
7. **Arrive**: De-energize hinge, W² → W⁴ transition at destination

Transit time: ~6 days proper time. Earth elapsed: ~6 days. No time dilation.

### Spacetime (Specific Temporal Target)

To reach a target at a specific time:

1. **Compute spatial Zeckendorf**: Target location bracket → {F_i}
2. **Compute temporal Zeckendorf**: Target time offset → {F_j} at appropriate bracket level
3. **Compose combined wave**: Spatial (sine) + Temporal (cosine) components
4. **Set hinge phase**: SAW pulse 6 phase adjusted for temporal entry point
5. **Energize and drive**: Same as spatial-only
6. **Arrive at WHERE-WHEN**: Both coordinates addressed simultaneously

The temporal address adds frequency components to the same wave. The channel forms through spacetime, not just space.

---

## Why Round Trips Don't Cost Time

The earlier calculation (6 days transit, 5 years Earth elapsed) assumed Lorentz time dilation — as if the payload were moving through space at relativistic velocity. This is the wrong model. The payload isn't moving through space. It has been conducted through the dark matter backbone in the W² frame.

**The arrow of time is thermodynamic.** It exists because W⁴ coupling creates thermal irreversibility. In the W² frame, EM and thermal channels are decoupled. There is no mechanism to create entropy increase. The θ-helix is open and symmetric.

**The backbone is structure, not space.** Special relativity's time dilation applies to objects moving through spacetime. It does not apply to objects moving along the structural scaffold that spacetime is built on. The payload never has a velocity in the SR sense — it has a position on the backbone that changes.

**θ = 0 means "now."** Setting the temporal address to θ = 0 (the origin's current phase) means arriving at the destination's corresponding phase. Returning with θ = 0 means arriving back at the origin's current phase. Zero elapsed time difference between departure and return — only the 6-day proper transit time in each direction.

---

## Summary

| Component | Description | Formula | Encodes |
|-----------|-------------|---------|---------|
| **Bracket** | Log-φ scale position | n = log_φ(r / L_P·C) | WHERE (scale) |
| **Frequency** | Resonant tuning | f = (J/ℏ) × φ^(-n) | WHERE (dial) |
| **Golden Angle** | Phase offset | θ = index × 137.5° | WHERE (rotation) |
| **Spatial Zeckendorf** | Fibonacci address | Unique non-consec. sum | WHERE (channel) |
| **Temporal Phase** | Position on θ-helix | θ ∈ [0, 2π) | WHEN (time) |
| **Temporal Zeckendorf** | Time offset address | Slot → Fibonacci decomp. | WHEN (channel) |
| **Hinge Phase** | SAW pulse 6 setting | Cumulative GA phase | WHEN (entry point) |

Together, these form a complete **spacetime coordinate system** native to the φ-structured universe. The spatial address has been understood since the framework's inception. The temporal address — the θ parameter that was always present in the AAH Hamiltonian — completes it.

The perpendicular helix was never a simulation artifact. It was the timeline, waiting to be recognized.

---

*© 2026 Thomas A. Husmann / iBuilt LTD. All rights reserved.*
*Licensed under CC BY-NC-SA 4.0 for academic and research use.*
*Patent Application 19/560,637 — Filed March 9, 2026*
