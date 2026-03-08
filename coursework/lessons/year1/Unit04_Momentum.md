# Year 1, Unit 4: Momentum & Collisions
## *Conservation Laws That Build Spacecraft*

**Duration:** 12 Days
**Grade Level:** 10th Grade
**Prerequisites:** Units 1-3

---

## Anchoring Question

> *When Dragon capsule docks with the ISS, it approaches at 0.03 m/s relative to the station. If Dragon has a mass of 12,000 kg and the ISS has a mass of 420,000 kg, what happens to the ISS's velocity when they dock?*

---

## Learning Objectives

By the end of this unit, you will be able to:
1. Calculate momentum (p = mv) for objects and systems
2. Apply the impulse-momentum theorem
3. Use conservation of momentum for collisions and explosions
4. Distinguish elastic vs. inelastic collisions
5. Analyze 2D momentum problems (conceptual level)

---

## Day 1-2: Momentum Definition

### What is Momentum?

**Momentum** is "mass in motion" — a measure of how hard it is to stop a moving object.

```
p = m × v

Momentum = mass × velocity (a vector!)
```

### Units

Momentum has units of kg·m/s (no special name).

### SpaceX Example: ISS Momentum

The ISS:
- Mass: 420,000 kg
- Velocity: 7,660 m/s

```
p = 420,000 × 7,660 = 3.22 × 10⁹ kg·m/s
```

**Compare to a car:**
- Mass: 2,000 kg
- Velocity: 30 m/s (highway speed)
- p = 60,000 kg·m/s

The ISS has 50,000× more momentum than a speeding car!

---

## Day 3-4: Impulse-Momentum Theorem

### Impulse

**Impulse** is the change in momentum caused by a force over time:

```
J = F × Δt = Δp = m × Δv

Impulse = Force × time = change in momentum
```

### The Key Insight for Landing

To stop a moving object (Δv = -v), you need impulse J = -mv.

**You can achieve this with:**
- Large force, short time: F × Δt = constant → high impact
- Small force, long time: F × Δt = constant → gentle landing

### SpaceX Application: Landing Leg Crush Cores

Falcon 9 landing legs contain **crush cores** — aluminum honeycomb structures that collapse on impact.

**Purpose:** Extend the impact time Δt, reducing peak force F.

```
Example:
- Booster mass: 25,000 kg
- Landing velocity: 2 m/s
- Required impulse: J = 25,000 × 2 = 50,000 kg·m/s

Without crush cores (Δt = 0.01 s):
F = J/Δt = 50,000 / 0.01 = 5,000,000 N = 5 MN

With crush cores (Δt = 0.1 s):
F = J/Δt = 50,000 / 0.1 = 500,000 N = 0.5 MN
```

The crush cores reduce peak force by 10×!

---

## Day 5-6: Conservation of Momentum

### The Law

In a closed system with no external forces:

```
p_initial = p_final

m₁v₁ᵢ + m₂v₂ᵢ = m₁v₁f + m₂v₂f
```

### Answering the Anchoring Question

Dragon (m₁ = 12,000 kg) approaches ISS (m₂ = 420,000 kg) at v_rel = 0.03 m/s.

In the ISS reference frame:
- v₁ᵢ = 0.03 m/s (Dragon approaching)
- v₂ᵢ = 0 m/s (ISS stationary)

After docking (perfectly inelastic collision):
```
m₁v₁ᵢ + m₂v₂ᵢ = (m₁ + m₂)v_f

12,000 × 0.03 + 420,000 × 0 = (12,000 + 420,000) × v_f

360 = 432,000 × v_f

v_f = 0.000833 m/s = 0.833 mm/s
```

The ISS moves backward at less than 1 mm/s!

**But this tiny change matters.** Over months without reboost, even 0.8 mm/s would cause significant orbital decay.

---

## Day 7: Lab — Cart Collisions

### Procedure

1. Set up two carts on a low-friction track
2. Measure masses
3. Record velocities before and after collision using motion sensors
4. Calculate total momentum before and after
5. Verify conservation

### Data Table

| Trial | m₁ | v₁ᵢ | m₂ | v₂ᵢ | v₁f | v₂f | p_before | p_after | % diff |
|-------|----|----|----|----|----|----|---------|---------|--------|
| 1 | | | | | | | | | |
| 2 | | | | | | | | | |

---

## Day 8-9: Elastic vs. Inelastic Collisions

### Definitions

**Elastic collision:** Kinetic energy is conserved
```
½m₁v₁ᵢ² + ½m₂v₂ᵢ² = ½m₁v₁f² + ½m₂v₂f²
```

**Inelastic collision:** Kinetic energy is NOT conserved (some goes to heat, sound, deformation)

**Perfectly inelastic:** Objects stick together (maximum KE loss)

### SpaceX Application: Stage Separation

Stage separation is a **reverse collision** — an "explosion" where the stages push apart.

Falcon 9 stage separation:
- Before: Combined mass M at velocity v
- After: Stage 1 (m₁) at v₁, Stage 2 (m₂) at v₂

Momentum is conserved:
```
Mv = m₁v₁ + m₂v₂
```

The separation is achieved by:
1. Pneumatic pushers (cold gas actuators)
2. Stage 2 engine ignition (provides main separation force)

### DART Mission: Kinetic Impactor

NASA's DART mission (2022) demonstrated asteroid deflection by momentum transfer:

- DART spacecraft mass: 550 kg
- Impact velocity: 6.1 km/s
- Dimorphos asteroid mass: 4.8 × 10⁹ kg

Momentum transferred:
```
Δp = m_DART × v = 550 × 6100 = 3.36 × 10⁶ kg·m/s
```

Change in asteroid velocity:
```
Δv = Δp / m_asteroid = 3.36 × 10⁶ / 4.8 × 10⁹ = 0.0007 m/s
```

Only 0.7 mm/s! But this changed the orbital period by 33 minutes — enough to validate the deflection concept.

---

## Day 10-11: 2D Momentum (Conceptual)

### Vector Nature of Momentum

Momentum is a vector. In 2D collisions, we must conserve momentum separately in x and y directions:

```
p_x,before = p_x,after
p_y,before = p_y,after
```

### Spacecraft Attitude Control

Reaction wheels change spacecraft orientation without expelling mass:

```
Angular momentum: L = Iω

To rotate spacecraft clockwise: spin reaction wheel counterclockwise
```

Total angular momentum is conserved — the wheel and spacecraft always have equal and opposite L.

---

## Day 12: Design Challenge

### Impulse Device for Egg Drop

Design a device that:
- Protects a raw egg from a 3-meter drop
- Maximizes impulse time Δt
- Minimizes total system mass

**Physics principles:**
- J = FΔt = mΔv (impulse equation)
- Longer Δt → lower F
- Soft, compressible materials extend impact time

---

## Unit Summary

| Concept | Key Equation | SpaceX Connection |
|---------|--------------|-------------------|
| Momentum | p = mv | ISS orbital momentum |
| Impulse | J = FΔt = Δp | Landing leg crush cores |
| Conservation | p_before = p_after | Docking, stage separation |
| Elastic | KE conserved | Theoretical limit |
| Inelastic | KE not conserved | Real collisions |
| DART | Δv = Δp/m | Asteroid deflection |

---

## Problem Sets

### Tier 1: Foundation (Must Do)

1. Calculate the momentum of: (a) a 70 kg astronaut floating at 2 m/s, (b) the ISS at 7,660 m/s.

2. A 5 kg ball moving at 10 m/s collides with a wall and rebounds at 8 m/s. Calculate the impulse delivered to the ball.

3. Two ice skaters push off each other. Skater A (50 kg) moves at 3 m/s. If Skater B is 75 kg, how fast does she move?

### Tier 2: Application (Should Do)

4. A Falcon 9 landing burn reduces booster velocity from 200 m/s to 2 m/s in 30 seconds. If the booster mass is 25,000 kg, calculate: (a) the impulse, (b) the average force.

5. In a perfectly inelastic collision, two objects (m₁ = 3 kg at 5 m/s, m₂ = 2 kg at -3 m/s) stick together. Calculate: (a) final velocity, (b) kinetic energy lost.

### Tier 3: Challenge (Want to Try?)

6. **DART Analysis:** The DART impact actually changed Dimorphos's velocity by more than the simple calculation predicts (0.7 mm/s became ~4 mm/s). This "momentum enhancement" came from ejecta (debris flying off). If the enhancement factor β = 4, how much mass was ejected at what average velocity? (Assume ejecta velocity = 1 km/s)

7. **Reaction Wheel Design:** A 500 kg satellite needs to rotate at 1°/s. If the reaction wheel has moment of inertia I = 0.5 kg·m², what angular velocity must the wheel reach? If it takes 10 seconds to spin up, what average torque is needed?

---

*© 2026 Thomas A. Husmann / iBuilt LTD. All rights reserved.*
*Licensed under CC BY-NC-SA 4.0 for academic and research use.*
