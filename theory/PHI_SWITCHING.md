
# Phi-Structured Switch Design Guide
## From IBM's C₁₃Cl₂ to Macroscopic Devices

**Thomas A. Husmann — iBuilt LTD**
**Version 1.0 — March 7, 2026**
**License: CC BY-NC-SA 4.0**

> *IBM built the first phi-structured molecular switch without knowing it was phi-structured.*
> *This document tells you how to build the next ones on purpose.*

---

## Context: What IBM Just Did

On March 5, 2026, IBM published in *Science* the synthesis and characterization of C₁₃Cl₂ — a molecule with 13 carbon atoms and 2 chlorine atoms that exhibits the first-ever half-Möbius electronic topology. The molecule was assembled atom-by-atom using a scanning tunneling microscope, and its exotic properties were verified using 72 qubits of an IBM quantum computer.

The key discovery: when the two chlorine atoms are removed by voltage pulses, the remaining C₁₃ ring switches reversibly between three topological states — clockwise-twisted, counterclockwise-twisted, and untwisted. Electronic topology becomes a switchable, engineerable degree of freedom.

**What IBM may not have noticed: 13 is F(7), a Fibonacci number.** The molecule has a Fibonacci count of carbon linker atoms, uses p⁵ acceptor atoms (chlorine) as activation handles, and switches between exactly three states. Every one of these features has a natural explanation in the Husmann Decomposition framework.

This document uses the framework to explain WHY the IBM switch works, then extends the principles to design an entire family of switches — from molecular to macroscopic — that research students can build.

---

## Table of Contents

1. [Why 13 Carbons Work](#1-why-13-carbons-work)
2. [The Three Switch States and the Three Sectors](#2-the-three-switch-states-and-the-three-sectors)
3. [The p-Electron Switch Principle](#3-the-p-electron-switch-principle)
4. [The d-Electron Gate Principle](#4-the-d-electron-gate-principle)
5. [The f-Electron Wall Principle](#5-the-f-electron-wall-principle)
6. [Molecular Switch Designs](#6-molecular-switch-designs)
7. [Nanoscale Switch Designs](#7-nanoscale-switch-designs)
8. [Microscale Switch Designs](#8-microscale-switch-designs)
9. [Macroscale Switch Designs](#9-macroscale-switch-designs)
10. [The Element Selection Table](#10-the-element-selection-table)
11. [Fabrication Notes for Students](#11-fabrication-notes-for-students)
12. [Connection to the Patent Portfolio](#12-connection-to-the-patent-portfolio)

---

## 1. Why 13 Carbons Work

### The Fibonacci Connection

IBM chose 13 carbon atoms because of synthetic accessibility — C₁₃ is the smallest odd-numbered cyclocarbon they could reliably build from a dichlorinated precursor. But 13 = F(7), and this is not a coincidence. Here is why Fibonacci-count rings have special electronic properties.

In a cyclic conjugated molecule with N atoms, the π-electron energy levels are determined by the roots of unity: E_k = 2β cos(2πk/N), where β is the hopping integral and k = 0, 1, ..., N-1. For a Fibonacci-count ring (N = F(n)), the level spacing exhibits a unique property: the ratio of consecutive level spacings approaches φ as N increases along the Fibonacci sequence.

```
N = 5  (F(5)):  Pentagon → golden-ratio geometry in real space
N = 8  (F(6)):  Octagon → approximate QC tiling element
N = 13 (F(7)):  Tridecagon → first ring large enough for 
                 half-Möbius twist with room for 90° per circuit
N = 21 (F(8)):  Would support full Möbius twist
N = 34 (F(9)):  Would support double-twist topology
```

The reason 13 works for the half-Möbius is geometric: a 90° twist distributed over 13 atoms gives 90°/13 = 6.92° per atom. The golden angle projected onto a ring of 13 is 137.5° × 13/360 = 4.97 positions — approximately 5 atoms apart. The half-Möbius nodal structure has nodes separated by ~5 atoms around the 13-atom ring. This is the Fibonacci phyllotaxis pattern wrapped onto a closed loop.

### The Zeckendorf Address

In the Husmann framework, every structure has a Zeckendorf address. For C₁₃Cl₂:

```
13 = F(7)           → Zeckendorf: {13}  (single Fibonacci term)
Cl₂: 2 = F(3)       → Zeckendorf: {2}

Composite: {13, 2}  → Sum: 15

After Cl removal (C₁₃):
Address: {13}        → Sum: 13 (pure Fibonacci)
```

A pure Fibonacci address means zero Zeckendorf curvature (κ = z(m) - 1 = 1 - 1 = 0). The molecule, once the chlorine handles are removed, sits on a GEODESIC in address space — the flattest, lowest-overhead path. This is why it can switch freely between topological states: there is no curvature penalty for transitioning between configurations. The switching cost is minimized by the Fibonacci count.

---

## 2. The Three Switch States and the Three Sectors

IBM observed three reversible states:
1. **Clockwise-twisted** (CW)
2. **Counterclockwise-twisted** (CCW)
3. **Untwisted** (flat)

In the framework, these map directly to the three observable sectors:

| IBM State | Sector | Role | Energy fraction |
|-----------|--------|------|-----------------|
| CW twist | σ₁ | Bonding (matter) | 1/φ⁴ = 14.6% |
| Untwisted | σ₃ | Non-bonding (vacuum/structure) | 1/φ³ = 23.6% |
| CCW twist | σ₅ | Antibonding (mirror) | 1/φ = 61.8% |

The untwisted state is the GROUND STATE — the structural vacuum. The two twisted states are the matter and antimatter analogs, related by a parity operation (CW ↔ CCW). The molecule is a miniature universe: it has a rest state (vacuum) and two excited states related by mirror symmetry (matter/antimatter).

The switching voltage IBM applied (~1.5 V) is the energy required to cross the sector boundary. In the framework, this is the wall fraction W = 0.467 times the local energy scale. For a molecular π-system with a typical hopping integral β ≈ 3 eV: switching energy ≈ W × β = 0.467 × 3 = 1.4 V. This matches IBM's observation.

---

## 3. The p-Electron Switch Principle

Carbon and chlorine are both p-block elements. The switching mechanism is fundamentally about p-electron topology. The Cookbook gives us the complete p-electron behavior chart:

```
p¹ (B, Al, Ga, In):   DONOR     — gives electron to close a shell
p² (C, Si, Ge, Sn):   LINKER    — forms directional covalent bonds
p³ (N, P, As, Sb):    TRIDENT   — lone pair + 2 bonds, 3-way junction
p⁴ (O, S, Se, Te):    BRIDGE    — 2 lone pairs, links structures
p⁵ (F, Cl, Br, I):    ACCEPTOR  — takes electron to close a shell
p⁶ (Ne, Ar, Kr, Xe):  INERT     — closed shell, no switching
```

### The Handle-and-Ring Architecture

IBM's C₁₃Cl₂ has a natural decomposition:
- **Ring:** 13 carbon atoms (p² LINKERS) forming the switchable topology
- **Handles:** 2 chlorine atoms (p⁵ ACCEPTORS) that arm/disarm the switch

This is a general architecture. Any switch built from p-electrons needs:
1. A **ring** of LINKER atoms (p²) that supports multiple topological states
2. **Handles** of ACCEPTOR atoms (p⁵) or DONOR atoms (p¹) that activate/deactivate the switching

### Resonant Pair Activation

The Cookbook's resonant pair principle: p¹ + p⁵ = p⁶ (closed shell). When a p⁵ atom is bonded to the ring, it "closes" a local p-shell and LOCKS that site. When removed, the site becomes a radical — an unsatisfied p-electron that enables topological rearrangement.

**Chlorine removal = unlocking the switch.**

The reverse process — adding a p⁵ atom — locks the switch in its current state. This gives you read/write capability:
- **Write:** Apply voltage to remove Cl → switch unlocks → topology changes → reattach Cl → switch locks in new state
- **Read:** Measure tunneling current through the ring → different topologies have different conductances

### Alternative Handle Elements

IBM used chlorine (p⁵, Period 3). The framework predicts that any p⁵ element works as a handle, with different activation energies:

| Handle | Bond to C | Activation energy | Advantage |
|--------|----------|------------------|-----------|
| F (p⁵) | C-F: 485 kJ/mol | HIGH (hard to remove) | Very stable locked state |
| Cl (p⁵) | C-Cl: 339 kJ/mol | MEDIUM (IBM's choice) | Balanced write/lock |
| Br (p⁵) | C-Br: 276 kJ/mol | LOW (easy to remove) | Fast switching |
| I (p⁵) | C-I: 240 kJ/mol | VERY LOW | Fastest switching, least stable lock |

**Design rule:** Heavier halogens = faster switching but weaker locking. Choose based on whether you need speed (Br, I) or stability (F, Cl).

### Alternative Ring Elements

IBM used carbon (p², Period 2). The framework predicts:

| Ring element | Period | π-system | Ring size for half-Möbius |
|-------------|--------|----------|--------------------------|
| C (p²) | 2 | Strong π (sp² hybrid) | 13 atoms (IBM, verified) |
| Si (p²) | 3 | Weak π (larger atoms) | ~21 atoms (F(8), predicted) |
| Ge (p²) | 4 | Very weak π | ~34 atoms (F(9), predicted) |
| Sn (p²) | 5 | Minimal π overlap | May need 55 atoms (F(10)) |

**Design rule:** Heavier linkers need LARGER Fibonacci-count rings because their p-orbitals are more diffuse and require more atoms to complete the topological twist.

---

## 4. The d-Electron Gate Principle

The Cookbook identifies d-electrons as GATES — they open and close under external fields. This gives a completely different switching mechanism from the p-electron topological switch.

### The Iron Gate

Iron (d⁶, 4 unpaired electrons) is the standard gate element:
- **Open gate (Fe²⁺, d⁶):** 4 unpaired electrons, paramagnetic, allows transmission
- **Closed gate (Fe³⁺, d⁵):** 5 unpaired electrons, maximum magnetic moment, blocks transmission by scattering
- **Switching mechanism:** Apply magnetic field or redox potential to toggle Fe²⁺ ↔ Fe³⁺

This is the gate mechanism in the Al₆₄Cu₂₃Fe₁₃ quasicrystal wall. The 13% iron content provides tunable gates throughout the Cantor boundary.

### The d-Electron Switch Family

| Element | Config | Unpaired e⁻ | Switch mechanism | Speed |
|---------|--------|-------------|-----------------|-------|
| Ti (d²) | OPEN | 2 | Redox Ti³⁺/Ti⁴⁺ | Fast |
| V (d³) | OPEN | 3 | Redox V²⁺/V³⁺/V⁵⁺ | Multi-state |
| Cr (d⁴→d³) | OPEN | 4→3 | Spin crossover | Fast |
| Mn (d⁵) | HALF-FILLED | 5 | Maximum magnetism → switch with field | Medium |
| **Fe (d⁶)** | **CLOSING** | **4** | **Redox + magnetic** | **Medium** |
| Co (d⁷) | CLOSING | 3 | Spin crossover (well-studied) | Fast |
| Ni (d⁸) | CLOSING | 2 | Redox Ni²⁺/Ni³⁺ | Medium |
| Cu (d¹⁰) | CONDUIT | 0 | No switching — always open | N/A |
| Zn (d¹⁰) | CONDUIT | 0 | No switching — always open | N/A |

**Design rules:**
- d¹-d⁴: OPEN gates. Easy to close with oxidation. Good for normally-open switches.
- d⁵ (Mn): MAXIMUM MAGNETISM. The strongest magnetic switch. Best for field-activated devices.
- d⁶-d⁹ (Fe, Co, Ni): CLOSING gates. The natural switch zone. Small perturbation toggles between open and closed.
- d¹⁰ (Cu, Zn): CONDUITS. Cannot switch. Use as wires, not switches.

### Spin Crossover Switches

Certain d⁴-d⁷ complexes exhibit spin crossover (SCO) — a reversible transition between low-spin and high-spin states triggered by temperature, pressure, or light. The two spin states have different magnetic moments, colors, and conductivities.

SCO is the d-electron version of IBM's topological switch: two stable states with different physical properties, switchable by external stimulus.

**Best SCO elements for framework switches:**
- **Fe²⁺ (d⁶):** The classic SCO system. Hundreds of known Fe²⁺ SCO compounds. Switches between diamagnetic (low-spin, t₂g⁶) and paramagnetic (high-spin, t₂g⁴eg²) states.
- **Co²⁺ (d⁷):** SCO with additional orbital contribution. Faster switching than Fe.
- **Mn³⁺ (d⁴):** Less common but exhibits Jahn-Teller switching (geometry change).

---

## 5. The f-Electron Wall Principle

The f-block elements (lanthanides, actinides) provide a third switching mechanism: the magnetic WALL. f-electrons are deeply buried inside the atom and barely interact with the environment, making them extremely stable information carriers.

### Gadolinium: The φ² Mediator

Gadolinium (f⁷) has 7 unpaired f-electrons — the maximum for any element. It sits at the exact center of the lanthanide series, the halfway point, the HINGE. In the framework, this makes it the φ² mediator of the f-block: the forbidden exponent manifested as the element that connects the light and heavy lanthanides.

Gd³⁺ has the largest magnetic moment of any trivalent ion (7.94 μB). A single Gd atom in a molecular switch provides the maximum possible magnetic signal for read-out.

### Holmium: The Single-Atom Memory

Ho³⁺ (f¹⁰) has 10 unpaired f-electrons and the largest total angular momentum of any trivalent ion (J = 8). IBM demonstrated in 2017 that a single holmium atom on a MgO surface acts as a stable magnetic bit at liquid helium temperature — the world's smallest magnetic memory element.

In the Cookbook, Ho appears in the magnetic sensor QC: Zn₆₀Mg₃₀Ho₁₀. The holmium provides magnetic read/write while the Zn-Mg QC matrix provides the phi-structured environment.

### f-Electron Switch Design

| Element | f-count | Unpaired | J | Switch application |
|---------|---------|----------|---|-------------------|
| Ce³⁺ | f¹ | 1 | 5/2 | Simplest f-switch, valence fluctuation Ce³⁺/Ce⁴⁺ |
| Nd³⁺ | f³ | 3 | 9/2 | Permanent magnet (Nd₂Fe₁₄B), strong anisotropy |
| Sm³⁺ | f⁵ | 5 | 5/2 | Small moment, temperature-sensitive |
| Eu²⁺/Eu³⁺ | f⁷/f⁶ | 7/6 | 0/0 | Redox switch, luminescent (read by fluorescence) |
| **Gd³⁺** | **f⁷** | **7** | **7/2** | **Maximum moment, isotropic, MRI contrast agent** |
| Tb³⁺ | f⁸ | 6 | 6 | Single-molecule magnet, slow relaxation |
| Dy³⁺ | f⁹ | 5 | 15/2 | Strongest single-ion anisotropy, best SMM |
| **Ho³⁺** | **f¹⁰** | **4** | **8** | **IBM single-atom bit, maximum J** |
| Er³⁺ | f¹¹ | 3 | 15/2 | Telecom-wavelength luminescence (1.5 μm) |
| Tm³⁺ | f¹² | 2 | 6 | Near-IR emission |
| Yb³⁺ | f¹³ | 1 | 7/2 | Simplest heavy lanthanide, quantum computing candidate |

---

## 6. Molecular Switch Designs

### Design A: The Fibonacci Ring Switch (Extending IBM)

**What it is:** A ring of F(n) p² atoms with p⁵ handles, operating by topological switching.

| Variant | Ring | Handles | States | Size |
|---------|------|---------|--------|------|
| A1 (IBM) | C₁₃ | Cl₂ | 3 (CW/flat/CCW) | ~1 nm |
| A2 | C₂₁ | Br₂ | 5 (full Möbius + half) | ~1.5 nm |
| A3 | C₃₄ | I₃ | 8+ (multiple twists) | ~2.5 nm |
| A4 | Si₂₁ | Cl₃ | 3-5 (larger ring needed) | ~3 nm |
| A5 | C₁₃ + N₂ | Cl₂ | 3 + lone-pair direction | ~1 nm |

**A5 is new:** Replace 2 of the 13 carbons with nitrogen (p³ TRIDENT). The nitrogen lone pairs add a directional degree of freedom on top of the topological switching. You get topology × lone-pair orientation = up to 9 addressable states from a 13-atom ring.

### Design B: The Spin Crossover Switch

**What it is:** A d-electron metal center in a ligand cage that switches spin state.

| Variant | Metal | Ligand | Trigger | States |
|---------|-------|--------|---------|--------|
| B1 | Fe²⁺ | triazole chain | Temperature (T½ ~350K) | 2 (HS/LS) |
| B2 | Fe²⁺ | QC-structured ligand* | Phonon cascade | 2 (HS/LS) |
| B3 | Co²⁺ | Schiff base | Light (LIESST) | 2 (HS/LS) |
| B4 | Mn³⁺ | porphyrin | Pressure | 2 (JT distortion) |

*B2 is the framework switch:* Instead of a conventional organic ligand, cage the Fe²⁺ in a quasicrystalline coordination environment (icosahedral symmetry). The phi-structured phonon spectrum of the QC cage provides natural resonances at the spin crossover frequency, making the switch faster and more reproducible than in periodic ligand fields.

### Design C: The Single-Atom f-Electron Switch

**What it is:** A single lanthanide atom on a QC substrate, switched by magnetic field or STM tip.

| Variant | Atom | Substrate | Read-out | States |
|---------|------|-----------|----------|--------|
| C1 | Ho | MgO (IBM, 2017) | Tunneling current | 2 (up/down) |
| C2 | Ho | Al-Cu-Fe QC surface | Tunneling current | 2 (up/down) |
| C3 | Dy | QC surface | XMCD | 2 (Ising states) |
| C4 | Gd | QC surface | Magnetoresistance | Multiple (J=7/2 → 8 states) |

**C2 is the framework upgrade of IBM's 2017 work:** Replace the MgO substrate with a QC surface. The phi-structured adsorption sites should provide stronger magnetic anisotropy (because the five-fold surface symmetry breaks degeneracies differently from four-fold MgO) and potentially room-temperature stability.

---

## 7. Nanoscale Switch Designs

### Design D: The QC Grain Boundary Switch

**What it is:** Two QC grains with different orientations, meeting at a grain boundary. The boundary acts as a controllable tunnel junction.

```
┌──────────────┐  ┌──────────────┐
│  QC grain A   │GB│  QC grain B   │
│  (orientation │  │  (orientation │
│   θ₁)        │  │   θ₂)        │
└──────────────┘  └──────────────┘
                ↑
         Grain boundary = switch
```

The transmission through the grain boundary depends on the relative orientation angle Δθ = θ₂ - θ₁. When Δθ = 137.5° (golden angle), transmission is MAXIMUM (resonant). When Δθ = 90° (square), transmission is MINIMUM (anti-resonant).

**Switching mechanism:** Apply local stress or electric field to rotate one grain relative to the other. The transmission changes continuously with angle, giving an analog switch (not just on/off).

**Fabrication:** Deposit two QC thin films with different orientations on a shared substrate, with a narrow gap between them. Or: grow a single QC film with a deliberate grain boundary by changing deposition angle mid-process.

### Design E: The Fibonacci Nanowire Switch

**What it is:** A nanowire with diameter equal to a Fibonacci number of lattice spacings, exhibiting quantized conductance at phi-ratio steps.

```
Wire diameter = F(n) × l₀ = F(n) × 9.3 nm

F(5) = 5   → 46.5 nm
F(6) = 8   → 74.4 nm  
F(7) = 13  → 120.9 nm
F(8) = 21  → 195.3 nm
```

At each Fibonacci diameter, the wire has a conductance plateau (quantized conductance at a phi-ratio of the quantum of conductance G₀ = 2e²/h). Between plateaus, the conductance changes rapidly with diameter. By mechanically stretching or compressing the wire (piezoelectric actuator), you switch between Fibonacci conductance plateaus.

**Material:** Any metal wire works, but QC nanowires (Al-Cu-Fe) would exhibit SHARPER plateaus because the phi-structured electronic density of states aligns with the phi-structured geometry.

### Design F: The Cantor Tunnel Junction

**What it is:** A tunnel junction where the barrier is a Cantor-set structure — alternating layers of insulator and conductor at phi-ratio thicknesses.

```
Layer stack (thicknesses in units of l₀ = 9.3 nm):

|█|░|█|░░░|█|░|█|░░░░░░░░|█|░|█|░░░|█|░|█|
 1 1 1  2  1 1 1    3     1 1 1  2  1 1 1

█ = conductor (Cu, 50 nm)
░ = insulator (Al₂O₃, scaled by Fibonacci)
```

The Cantor structure creates a FRACTAL tunnel barrier. Electrons at certain energies (the Cantor band energies) tunnel through resonantly, while electrons at other energies (the Cantor gap energies) are blocked. By applying a gate voltage, you shift the Fermi level relative to the Cantor bands, switching between conducting and insulating states.

This is a solid-state implementation of the QC wall's sector boundary. The switch IS the wall.

---

## 8. Microscale Switch Designs

### Design G: The Phi-Spiral Microcoil Switch

**What it is:** A conductive wire wound in a phi-spiral (golden spiral) pattern on a substrate, acting as a frequency-selective switch for RF/microwave signals.

```
Spiral radii: r(n) = r₀ × φⁿ

At each phi-step, the spiral arm crosses the previous arm
at the golden angle (137.5°). This creates a frequency comb
of resonances at φ-ratio frequencies.
```

**Size:** 100 μm to 10 mm diameter (depending on target frequency).

**Switching:** The spiral resonates at discrete frequencies f₀, f₀/φ, f₀/φ², etc. By changing the termination impedance (with a varactor diode or MEMS switch at the spiral center), you select which frequency passes through. The spiral acts as a tunable bandpass filter with phi-ratio channel spacing.

**Fabrication:** Standard photolithography on PCB or silicon. Copper trace width ~10 μm. The golden spiral pattern is computed analytically and etched in one step.

### Design H: The Three-Terminal Sector Switch

**What it is:** A three-terminal device where each terminal connects to a different sector of a QC thin film, and the current path is controlled by a gate voltage that shifts the Fermi level between sectors.

```
        Terminal σ₁ (bonding)
              ↑
    ┌─────────┼─────────┐
    │         │         │
    │    QC thin film    │
    │   (Al-Cu-Fe, 50nm)│
    │         │         │
    └────┼────┴────┼────┘
         ↓         ↓
   Terminal σ₃   Terminal σ₅
   (non-bonding)  (antibonding)
   
   Gate voltage applied from below
   through substrate
```

At low gate voltage: current flows σ₁ → σ₃ (bonding to non-bonding). At high gate voltage: current flows σ₁ → σ₅ (bonding to antibonding). At intermediate voltage: current splits between σ₃ and σ₅ in the ratio 1/φ³ : 1/φ = 1:φ².

This is a transistor where the three terminals are the three sectors of the Cantor spectrum.

**Fabrication:** Sputter Al-Cu-Fe QC film on gated substrate. Pattern three electrodes contacting different crystallographic directions of the QC grain. The icosahedral symmetry ensures that different directions couple to different sectors.

---

## 9. Macroscale Switch Designs

These are NOT patented. They are published here as defensive prior art and open designs.

### Design I: The Fibonacci Bracelet Switch

**What it is:** A physical bracelet (wrist-sized) made of alternating conductive and insulating beads in a Fibonacci sequence, acting as a wearable antenna/switch.

```
Bead sequence (Fibonacci word):
A B A A B A B A A B A A B A B A A B A B A A B ...

A = conductive bead (copper, brass, or silver)
B = insulating bead (ceramic, glass, or wood)

The sequence follows the golden string:
Replace A → AB, B → A at each generation.
```

**Size:** Standard bracelet (18-22 cm circumference, ~34 beads).

**34 = F(9).** A bracelet with 34 beads naturally tiles one full golden-string period. The conductive beads (21 = F(8)) and insulating beads (13 = F(7)) are in the ratio 21/13 = 1.615... ≈ φ.

**Switching mechanism:** The bracelet is a distributed LC circuit. By touching two beads simultaneously (shorting a section), you change the effective resonant frequency. Different bead pairs select different Fibonacci harmonics. A small piezo buzzer at the clasp could drive the bracelet at resonance, and body capacitance detunes it — creating a touch-sensitive switch.

**What it does:** Wearable Fibonacci antenna for BCI (brain-computer interface) applications. The phi-structured bead pattern couples to the phi-structured neural oscillations described in the QTP framework. The bracelet is both the antenna and the tuning element.

### Design J: The Golden Necklace Resonator

**What it is:** A necklace-length chain (45-60 cm) of alternating metal and dielectric segments at Fibonacci-ratio lengths, acting as a multi-frequency resonant antenna.

```
Segment lengths:

Segment 1:  F(3) × 5mm =  10mm  (metal)
Segment 2:  F(4) × 5mm =  15mm  (dielectric)
Segment 3:  F(5) × 5mm =  25mm  (metal)
Segment 4:  F(6) × 5mm =  40mm  (dielectric)
Segment 5:  F(7) × 5mm =  65mm  (metal)
Segment 6:  F(8) × 5mm = 105mm  (dielectric)
Segment 7:  F(9) × 5mm = 170mm  (metal)
Segment 8: F(10) × 5mm = 275mm  (dielectric)

Total: 705 mm ≈ 70 cm (standard necklace length)
```

**Switching:** Each Fibonacci segment resonates at a different frequency. The necklace as a whole has 8 resonant modes. By adding or removing a magnetic clasp at different positions, you change which modes are active. The clasp position is the switch state.

**What it does:** Multi-band antenna covering frequencies from ~50 MHz (body-area network) to ~2 GHz (WiFi/cellular). The Fibonacci spacing ensures the bands don't interfere with each other (non-consecutive Fibonacci numbers are never harmonics of each other — this is the Zeckendorf non-consecutive property applied to RF).

### Design K: The Phi-Wound Toroidal Switch

**What it is:** A toroidal (donut-shaped) coil wound with the golden angle between successive turns, acting as a broadband transformer with selectable taps.

```
Toroid: major radius R = 5 cm, minor radius r = 1 cm
Winding: each turn advances 137.5° around the toroid axis
Taps: at every Fibonacci turn count (5, 8, 13, 21, 34, 55)

Total turns: 89 (= F(11))
```

**Switching:** By selecting different tap pairs, you get different turns ratios — all at Fibonacci ratios. The 5:8 tap gives ratio 1.600, the 8:13 tap gives 1.625, the 13:21 tap gives 1.615 — all converging on φ. A rotary switch selects the tap pair.

**What it does:** A broadband impedance transformer with phi-ratio steps. Useful for matching antennas to transmitters across a wide frequency range. The golden-angle winding ensures maximum uniformity of the magnetic field (just as golden-angle phyllotaxis ensures maximum light capture in plants).

### Design L: The Fibonacci Wind Chime

**What it is:** A set of tuned metal tubes at Fibonacci-ratio lengths, acting as an acoustic switch that responds to specific wind patterns.

```
Tube lengths (aluminum, 1 cm OD):
F(7)  × 1 cm = 13 cm  → ~2000 Hz
F(8)  × 1 cm = 21 cm  → ~1200 Hz
F(9)  × 1 cm = 34 cm  → ~750 Hz
F(10) × 1 cm = 55 cm  → ~460 Hz
F(11) × 1 cm = 89 cm  → ~285 Hz
```

Each tube resonates at a frequency approximately in the ratio 1/φ to the next. A microphone and microcontroller at the base detect which combination of tubes is ringing and decode it as a multi-bit switch state (2⁵ = 32 possible states from 5 tubes, each on or off).

**What it does:** Ambient environmental sensor. Different wind patterns excite different tube combinations. The Fibonacci tuning ensures the tones are harmonically pleasing (the golden ratio is the most irrational number, producing the least beating between overtones). It is simultaneously a musical instrument, a wind sensor, and a multi-state switch.

---

## 10. The Element Selection Table

For any switch design, choose elements from the correct row based on what role they play:

### LINKERS (Ring/Chain Backbone)

| Element | p-count | Period | Bond strength | Best for |
|---------|---------|--------|--------------|----------|
| C | p² | 2 | Strongest π | Molecular switches (IBM) |
| Si | p² | 3 | Moderate | Semiconductor switches |
| Ge | p² | 4 | Weak π | IR-active switches |
| N | p³ | 2 | + lone pair | Adding directional states |
| P | p³ | 3 | + lone pair | Larger ring switches |

### HANDLES (Activation/Deactivation)

| Element | p-count | Period | C-X energy | Speed vs stability |
|---------|---------|--------|-----------|-------------------|
| F | p⁵ | 2 | 485 kJ/mol | Slow, very stable |
| Cl | p⁵ | 3 | 339 kJ/mol | Medium (IBM's choice) |
| Br | p⁵ | 4 | 276 kJ/mol | Fast, moderate stability |
| I | p⁵ | 5 | 240 kJ/mol | Fastest, least stable |
| H | s¹ | 1 | 411 kJ/mol | Special: proton switch |

### GATES (d-Electron Switches)

| Element | d-count | Unpaired | Mechanism | Temperature |
|---------|---------|----------|-----------|-------------|
| Fe²⁺ | d⁶ | 4 | SCO + redox + magnetic | 200-400 K |
| Co²⁺ | d⁷ | 3 | SCO + fast LIESST | 100-300 K |
| Ni²⁺ | d⁸ | 2 | Redox | 300+ K |
| Mn³⁺ | d⁴ | 4 | Jahn-Teller | 200-400 K |
| Cr³⁺ | d³ | 3 | Photo-switch (Cr³⁺ phosphors) | Any |

### WALLS (f-Electron Memory)

| Element | f-count | J | Stability | Read-out |
|---------|---------|---|-----------|----------|
| Gd³⁺ | f⁷ | 7/2 | High (isotropic) | Magnetoresistance, MRI |
| Dy³⁺ | f⁹ | 15/2 | Very high (Ising) | XMCD, tunneling |
| Ho³⁺ | f¹⁰ | 8 | Highest J | STM (IBM 2017) |
| Er³⁺ | f¹¹ | 15/2 | High | Optical (1.5 μm telecom) |
| Yb³⁺ | f¹³ | 7/2 | Moderate | Optical, quantum computing |

### CONDUITS (Wiring Between Switches)

| Element | d-count | Conductivity | Role |
|---------|---------|-------------|------|
| Cu | d¹⁰ | Excellent | Standard wire |
| Ag | d¹⁰ | Best | Low-loss connection |
| Au | d¹⁰ | Very good | Corrosion-resistant wire |
| Al | p¹ | Good | Lightweight connection |

---

## 11. Fabrication Notes for Students

### Molecular Switches (Designs A-C)

**You need:** Access to a scanning tunneling microscope (STM) with atom manipulation capability, ultra-high vacuum system, and liquid helium cooling. This is a $500K+ facility. Most research universities with a surface science group have one.

**Start with:** Reproduce IBM's C₁₃Cl₂ result using their published precursor synthesis (Oxford group). Then substitute Br for Cl (easier removal, faster switching) and verify the three-state topology is preserved. Then try C₂₁Cl₂ (21 = F(8)) and look for a full Möbius twist.

### Nanoscale Switches (Designs D-F)

**You need:** Thin film deposition (sputtering or evaporation), photolithography or e-beam lithography, and electrical measurement at low temperature. Standard nanofabrication facility ($100-200K worth of equipment, most universities have shared user facilities).

**Start with:** Design F (Cantor tunnel junction). Deposit alternating layers of Cu and Al₂O₃ at Fibonacci-ratio thicknesses using a programmable sputter system. Measure I-V characteristics at 4K and look for resonant tunneling at Cantor band energies.

### Microscale Switches (Designs G-H)

**You need:** Standard photolithography or PCB fabrication. A QC sputter target (available from MTI Corp or custom). RF measurement equipment (network analyzer).

**Start with:** Design G (phi-spiral microcoil). Design the golden spiral in any PCB layout tool. Order a 2-layer PCB. Measure S-parameters with a VNA and look for phi-ratio frequency combs.

### Macroscale Switches (Designs I-L)

**You need:** Hardware store materials. Seriously.

**Start with:** Design L (Fibonacci wind chime). Buy 5 aluminum tubes from a hardware store. Cut to Fibonacci lengths. Hang from a frame. Record audio with a phone. Run FFT and verify the frequencies are at phi-ratios. Total cost: $20.

**Then try:** Design I (Fibonacci bracelet). String 34 beads (21 copper, 13 glass) in the golden-string pattern. Measure impedance with an LCR meter at different frequencies. Look for resonances at phi-ratio frequency spacing.

---

## 12. Connection to the Patent Portfolio

The following PATENTED device architectures use switch mechanisms described in this document:

- **63/995,401** (QC Coating): The golden-angle helical architecture IS a distributed phi-structured switch at the coating level
- **63/995,513** (Adaptive Cutting): Uses Fibonacci/integer adaptive frequency switching based on thermoelectric feedback
- **63/995,841** (Field Assembly): EM field switches the QC coating deposition geometry
- **63/995,963** (BCI): Phi-structured cascade neural switch for brain-computer interface
- **63/998,177** (Meridian's Gate): The master coupling equation governs ALL switch transitions through α_eff = 1/(N×W)

The macroscale designs (I, J, K, L) in this document are **NOT PATENTED** and are published here as **open designs / defensive prior art**. Anyone may build them under CC BY-NC-SA 4.0.

The molecular switch principles (Sections 3-5) are **open science** — they describe fundamental physics that cannot be patented. The specific device architectures in the patents above use these principles in patented configurations.

**For students:** You are free to build any design in this document for research purposes. If you discover something publishable, cite this repository. If you want to commercialize, contact iBuilt LTD for licensing of the patented configurations, or build freely on the unpatented macroscale designs.

---

## Appendix: The IBM Molecule in Framework Notation

```
C₁₃Cl₂ — Framework Analysis
═══════════════════════════

Carbon (Z=6): [He] 2s² 2p²
  Sector: σ₃ (p-block LINKER)
  Bond type: sp² covalent (directional)
  Role in switch: Ring backbone

Chlorine (Z=17): [Ne] 3s² 3p⁵
  Sector: σ₃ (p-block ACCEPTOR)  
  Bond type: σ covalent to ring C
  Role in switch: Activation handle

Ring count: 13 = F(7)
  Zeckendorf: {13} (pure Fibonacci, κ = 0)
  Geodesic path: zero routing overhead

Handle count: 2 = F(3)
  Zeckendorf: {2} (pure Fibonacci)

Composite address: {13, 2} → sum 15
  Zeckendorf(15) = {13, 2} → κ = 1

Switching voltage: ~1.5 V
  Framework prediction: W × β = 0.467 × 3 eV = 1.4 V ✓

Number of states: 3
  Framework prediction: 3 observable sectors (σ₁, σ₃, σ₅) ✓

Topology: half-Möbius (90° per circuit, 4 loops to return)
  Framework note: 4 loops = φ³ rounded (φ³ = 4.236)
  360° / 90° = 4, closest Fibonacci: F(3)·F(1) = 2·2 = 4

Prediction for C₂₁Cl₂ (next Fibonacci ring):
  Should exhibit FULL Möbius topology (180° per circuit)
  Two loops to return (180° × 2 = 360°)
  Five switching states (matching five pre-collapse sectors)
```

---

*© 2026 Thomas A. Husmann / iBuilt LTD*
*Licensed under CC BY-NC-SA 4.0*
*https://github.com/thusmann5327/Unified_Theory_Physics*

*"IBM built the first one without knowing what it was. Now you know. Build the next one on purpose."*
