# Year 1, Unit 6: Electricity & Circuits
## *Powering Spacecraft and Civilization*

**Duration:** 20 Days
**Grade Level:** 10th Grade
**Prerequisites:** Units 1-5

---

## Anchoring Question

> *The ISS has eight large solar panel arrays generating 84–120 kW of power. The station uses roughly 75 kW continuously. Where does the extra energy go? Where does power come from on the night side of the orbit?*

---

## Learning Objectives

By the end of this unit, you will be able to:
1. Explain electric charge and Coulomb's Law
2. Calculate electric field and potential
3. Apply Ohm's Law to analyze circuits
4. Solve series and parallel circuit problems
5. Calculate power consumption and efficiency

---

## Day 1-2: Electric Charge

### Fundamental Properties

- Two types: positive (+) and negative (-)
- Like charges repel; opposite charges attract
- Charge is quantized: smallest unit is e = 1.602 × 10⁻¹⁹ C
- Charge is conserved (cannot be created or destroyed)

### Coulomb's Law

The force between two charges:

```
F = k × (q₁ × q₂) / r²

Where:
  k = 8.99 × 10⁹ N·m²/C²
  q₁, q₂ = charges (Coulombs)
  r = distance (meters)
```

### SpaceX Application: Spacecraft Charging

In the plasma environment of space, spacecraft accumulate charge:
- Sunlit surfaces: positive (photoelectric effect ejects electrons)
- Shadowed surfaces: negative (collect ambient electrons)

This differential charging can cause electrostatic discharge (ESD) — arcing that damages electronics.

**Protection strategies:**
- Conductive coatings to equalize potential
- Faraday cages around sensitive electronics
- Bleed resistors to drain accumulated charge

---

## Day 3-4: Electric Fields

### Field Definition

```
E = F/q = k × Q / r²   (units: N/C or V/m)
```

The electric field is the force per unit charge at any point in space.

### Field Lines

- Point away from positive charges
- Point toward negative charges
- Never cross
- Density indicates field strength

### SpaceX Application: Solar Panel Efficiency

Solar panels convert photon energy to electrical energy via the photoelectric effect. The electric field inside the semiconductor junction is critical:

```
P = η × A × I

Where:
  P = power output
  η = efficiency (~20-25% for space-grade panels)
  A = area
  I = solar intensity (1361 W/m² at Earth orbit)
```

ISS solar panels:
- Total area: ~2,500 m²
- Efficiency: ~14% (older technology)
- Max power: 2,500 × 0.14 × 1361 × cos(angle) ≈ 120 kW

---

## Day 5-6: Electric Potential (Voltage)

### Potential Definition

Voltage is electric potential energy per unit charge:

```
V = PE/q = k × Q / r   (units: Volts = J/C)
```

### Potential Difference

Current flows due to potential DIFFERENCE (voltage drop):

```
ΔV = V_high - V_low
```

### SpaceX Application: ISS Bus Voltage

The ISS operates at **120V DC** for main power distribution.

**Why 120V instead of lower voltage?**

```
Power = Voltage × Current
P = V × I

For P = 75,000 W:
  At 28V: I = 75,000/28 = 2,679 A (massive cables needed!)
  At 120V: I = 75,000/120 = 625 A (still large, but manageable)
```

Higher voltage means lower current for the same power, which means:
- Smaller cables (less mass!)
- Lower resistive losses (P_loss = I²R)

---

## Day 7-8: Current and Resistance

### Current

Current is the flow of charge:

```
I = Q/t   (units: Amperes = C/s)
```

### Resistance

Resistance opposes current flow:

```
R = ρ × L / A

Where:
  ρ = resistivity of material
  L = length
  A = cross-sectional area
```

| Material | Resistivity (Ω·m) |
|----------|-------------------|
| Copper | 1.7 × 10⁻⁸ |
| Aluminum | 2.8 × 10⁻⁸ |
| Silicon | 6.4 × 10² |
| Glass | 10¹⁰ - 10¹⁴ |

### SpaceX Application: Wire Selection

Spacecraft use **aluminum wire** instead of copper despite higher resistivity. Why?

Density comparison:
- Copper: 8,960 kg/m³
- Aluminum: 2,700 kg/m³

For the same conductance (same R), aluminum wire is ~50% lighter!

Mass is everything in spaceflight. Every kg saved in wiring can be additional payload.

---

## Day 9: Lab — Mapping Electric Fields

### Procedure

1. Set up conducting paper with electrodes
2. Apply voltage across electrodes
3. Use voltmeter to measure potential at grid points
4. Plot equipotential lines
5. Sketch electric field lines (perpendicular to equipotentials)

---

## Day 10-11: Ohm's Law

### The Relationship

```
V = I × R

Voltage = Current × Resistance
```

### Ohmic vs. Non-Ohmic Materials

- **Ohmic:** R constant (metals at constant temperature)
- **Non-Ohmic:** R varies (diodes, semiconductors, heated filaments)

### Problem Solving Strategy

1. Identify voltage source
2. Identify resistances
3. Apply V = IR to find unknowns
4. Check: Does the answer make physical sense?

---

## Day 12-13: Series Circuits

### Series Connection

Components connected end-to-end (same current through all):

```
I_total = I₁ = I₂ = I₃

R_total = R₁ + R₂ + R₃

V_total = V₁ + V₂ + V₃
```

### Voltage Divider

```
V₁ = V_total × (R₁ / R_total)
```

### SpaceX Application: Battery Stacking

Li-ion battery cells are about 3.7V each. To get the 28V typical of small satellite buses:

```
28V / 3.7V ≈ 8 cells in series
```

But series connection means: if ONE cell fails, the whole string fails.

---

## Day 14-15: Parallel Circuits

### Parallel Connection

Components connected across the same two points (same voltage across all):

```
V_total = V₁ = V₂ = V₃

I_total = I₁ + I₂ + I₃

1/R_total = 1/R₁ + 1/R₂ + 1/R₃
```

### Current Divider

```
I₁ = I_total × (R_total / R₁)
```

### SpaceX Application: Solar Panel Configuration

ISS solar panels use **parallel strings** of series-connected cells:

```
Series: Adds voltages → achieves bus voltage
Parallel: Adds currents → achieves total power

Also: Parallel provides redundancy — one string failure doesn't kill the panel
```

---

## Day 16-17: Lab — Build and Measure Circuits

### Part A: Series Circuit

1. Connect three resistors in series
2. Measure total resistance
3. Apply voltage, measure current
4. Verify: R_total = R₁ + R₂ + R₃ and V = IR

### Part B: Parallel Circuit

1. Connect same three resistors in parallel
2. Measure total resistance
3. Apply voltage, measure current
4. Verify: 1/R_total = 1/R₁ + 1/R₂ + 1/R₃

---

## Day 18-19: Electrical Power

### Power Equations

```
P = I × V = I²R = V²/R   (units: Watts)
```

### Energy Consumption

```
E = P × t   (units: Joules, or kWh for billing)
```

### Answering the Anchoring Question

**Where does the extra ISS power go?**

The ISS generates 84-120 kW but uses ~75 kW. The excess goes to:
1. **Battery charging:** During sunlit periods (52 min of 92 min orbit), batteries charge for night-side operation
2. **System losses:** Resistive heating in wires, conversion losses
3. **Thermal control:** Some power deliberately converted to heat for temperature regulation

**Night-side power:**
During the 40 minutes in Earth's shadow, solar panels produce zero power. The batteries (lithium-ion, ~120 kWh capacity) provide all power.

```
Energy needed for 40 minutes: 75 kW × (40/60) hr = 50 kWh
Battery capacity: 120 kWh
Margin: 70 kWh for safety
```

### SpaceX Application: Arc Flash Safety

In pure oxygen environments (like early spacecraft), electrical arcing is catastrophic. The Apollo 1 fire (1967) killed three astronauts due to an electrical fault in a pure O₂ atmosphere.

Modern spacecraft use:
- Reduced oxygen partial pressure
- Arc-resistant wiring insulation
- Circuit breakers and fault protection
- Fire suppression systems

---

## Day 20: Review and Assessment

### Unit Summary

| Concept | Key Equation | SpaceX Connection |
|---------|--------------|-------------------|
| Coulomb's Law | F = kq₁q₂/r² | Spacecraft charging |
| Electric field | E = kQ/r² | Solar cell design |
| Voltage | V = IR | Bus voltage selection |
| Series | R_total = ΣR | Battery stacking |
| Parallel | 1/R = Σ(1/R) | Panel redundancy |
| Power | P = IV | Power budget |

---

## Problem Sets

### Tier 1: Foundation (Must Do)

1. Calculate the force between two 1 μC charges separated by 10 cm.

2. A 100 Ω resistor has 12 V across it. Calculate: (a) current, (b) power dissipated.

3. Three 100 Ω resistors are connected: (a) all in series, (b) all in parallel. Calculate total resistance for each.

### Tier 2: Application (Should Do)

4. The ISS draws 75 kW at 120 V. Calculate: (a) current, (b) power lost in a 0.1 Ω cable resistance.

5. Design a battery pack for a CubeSat: needs 12V, 10Ah capacity. Li-ion cells are 3.7V, 3Ah each. How many cells, in what configuration?

### Tier 3: Challenge (Want to Try?)

6. **Solar Panel Degradation:** ISS solar panels lose ~1% efficiency per year due to radiation damage. After 20 years, what fraction of original power do they produce? If they started at 120 kW, what power now?

7. **φ-Connection:** The fine structure constant α ≈ 1/137 governs electromagnetic interactions. Calculate the force between an electron and proton at the Bohr radius (5.29 × 10⁻¹¹ m). Then calculate F × (Bohr radius)² / (k × e²). What do you get? Why is this significant?

---

*© 2026 Thomas A. Husmann / iBuilt LTD. All rights reserved.*
*Licensed under CC BY-NC-SA 4.0 for academic and research use.*
