# Year 1, Unit 2: Forces & Newton's Laws
## *Why Things Move (Or Don't)*

**Duration:** 20 Days
**Grade Level:** 10th Grade
**Prerequisites:** Unit 1 (Kinematics)

---

## Anchoring Question

> *A Falcon 9 first stage lands on a drone ship after a 9-minute flight. What forces act on it during each phase — boost, coast, flip, reentry burn, landing burn — and how do those forces determine every moment of its trajectory?*

---

## Learning Objectives

By the end of this unit, you will be able to:
1. Draw accurate free-body diagrams for all force scenarios
2. State and apply all three of Newton's Laws with precision
3. Solve ΣF = ma problems in one and two dimensions
4. Analyze friction (static/kinetic) and inclined plane scenarios
5. Explain circular motion and centripetal force
6. Identify Newton's Third Law pairs and destroy the myth that they "cancel"

---

## Day 1-2: Newton's First Law — Inertia

### The Law

> *An object at rest stays at rest, and an object in motion stays in motion with the same velocity, unless acted upon by a net force.*

### Inertia: The Resistance to Change

**Inertia** is NOT a force — it's a property of matter. More mass = more inertia.

### SpaceX Hook: Why Does Falcon 9 Need Control?

A rocket sitting on the launch pad has enormous inertia (549,054 kg). But once moving, why does it need constant thrust vectoring and grid fin control?

**Answer:** Without active control, any small perturbation (wind, thrust imbalance, center of mass shift) will cause the rocket to tip. Once tipping starts, inertia keeps it going — straight into the ground.

The Falcon 9 booster makes **hundreds of micro-corrections per second** to stay vertical. This is Newton's First Law in action: small forces create small accelerations, which left unchecked, compound into disaster.

### Grid Fin Control History

Early Falcon 9 landing attempts failed due to control issues:
- **2014:** Roll rate exceeded attitude control capabilities
- **2018 (B1050):** Stalled grid fin hydraulic pump — the rocket compensated and soft-landed in water

Source: [Wikipedia - Falcon 9 Landing Tests](https://en.wikipedia.org/wiki/Falcon_9_first-stage_landing_tests)

---

## Day 3-4: Free-Body Diagrams

### The Most Important Tool in Physics

A **free-body diagram (FBD)** shows ALL forces acting on ONE object.

### Rules for Drawing FBDs

1. Draw the object as a dot or simple shape
2. Draw ALL forces as arrows FROM the object
3. Label each force (Weight W, Normal N, Friction f, Tension T, etc.)
4. Choose a coordinate system

### Falcon 9 FBDs at Different Phases

**On the Pad:**
```
        ↑ N (Normal from pad)
        |
       [R]
        |
        ↓ W = mg = 5.4 MN
```

**At Liftoff:**
```
        ↑ F_thrust = 7.6 MN
        |
       [R]
        |
        ↓ W = 5.4 MN

ΣF = 7.6 - 5.4 = 2.2 MN (upward)
a = ΣF/m = 2,200,000 / 549,054 = 4.01 m/s²
```

**At Max-Q (maximum drag):**
```
        ↑ F_thrust = 7.6 MN
        |
       [R]
        |
        ↓ W + D = 5.4 + 1.5 MN = 6.9 MN

ΣF = 7.6 - 6.9 = 0.7 MN
a = 0.7 MN / (reduced mass) ≈ 2 m/s²
```

---

## Day 5-6: Newton's Second Law — ΣF = ma

### The Law

> *The acceleration of an object equals the net force divided by its mass.*

```
a = ΣF / m

Or equivalently:
ΣF = ma
```

### SpaceX Calculation: Falcon 9 Liftoff

**Given:**
- Thrust: F_thrust = 7,607,000 N
- Mass: m = 549,054 kg
- Weight: W = mg = 549,054 × 9.8 = 5,380,729 N

**Calculate initial acceleration:**
```
ΣF = F_thrust - W = 7,607,000 - 5,380,729 = 2,226,271 N

a = ΣF / m = 2,226,271 / 549,054 = 4.05 m/s²
```

### Why Acceleration Increases During Flight

As fuel burns, mass decreases. Near MECO (Main Engine Cut-Off):
- Mass ≈ 125,000 kg (mostly structure + second stage)
- Thrust: Still ~7,000,000 N (slightly reduced)
- Weight: 125,000 × 9.8 = 1,225,000 N

```
ΣF = 7,000,000 - 1,225,000 = 5,775,000 N
a = 5,775,000 / 125,000 = 46.2 m/s² ≈ 4.7g
```

**This is why G-forces peak near the end of burns, not the beginning!**

---

## Day 7-8: Newton's Third Law — Action-Reaction

### The Law

> *For every action, there is an equal and opposite reaction.*

### The Critical Understanding

Action-reaction pairs:
- Act on **DIFFERENT objects**
- Are **equal in magnitude**
- Are **opposite in direction**
- **NEVER cancel** (because they're on different objects)

### Rocket Propulsion: The Perfect Example

**The exhaust pushing down IS the rocket pushing up — same force, different objects.**

```
Action:  Rocket pushes exhaust gas downward with force F
Reaction: Exhaust gas pushes rocket upward with force F
```

The rocket doesn't push against the ground or the air. It pushes against its own exhaust. This is why rockets work in vacuum!

### Common Misconception

**Wrong:** "The rocket pushes against the air"
**Right:** "The rocket pushes exhaust backward; exhaust pushes rocket forward"

In space, there's no air to push against — but rockets work perfectly because they carry their own reaction mass (exhaust).

---

## Day 9: Lab — Verify ΣF = ma

### Procedure

1. Set up cart on horizontal track with force probe
2. Measure mass of cart
3. Apply constant force with hanging mass over pulley
4. Record acceleration using motion sensor
5. Verify: a = F_net / m_total

### Data Analysis

| Trial | Mass (kg) | Force (N) | Measured a (m/s²) | Predicted a (m/s²) | Error |
|-------|-----------|-----------|-------------------|-------------------|-------|
| 1 | 0.50 | 0.98 | | | |
| 2 | 0.50 | 1.96 | | | |
| 3 | 1.00 | 0.98 | | | |
| 4 | 1.00 | 1.96 | | | |

---

## Day 10-11: Friction

### Static vs. Kinetic Friction

```
f_s ≤ μ_s × N  (static — prevents motion)
f_k = μ_k × N  (kinetic — opposes motion)

Always: μ_s > μ_k (it takes more force to start than to keep moving)
```

### SpaceX Application: Why Ablative Liners?

Raptor engines run at 300 bar and 3,500°C. At these conditions, the exhaust creates enormous shear forces on the nozzle walls. This "friction" (more accurately: high-speed gas-wall interaction) would erode most materials instantly.

**Solution:** Ablative liners that deliberately erode, carrying heat away with the ablated material.

---

## Day 12-13: Inclined Planes

### Force Decomposition

On an incline at angle θ:
```
Weight component parallel to slope: W_∥ = mg sin θ
Weight component perpendicular: W_⊥ = mg cos θ
Normal force: N = mg cos θ
```

### Problem: Block on Ramp

A 10 kg block sits on a ramp at 30°. If μ_s = 0.6, will it slide?

```
W_∥ = 10 × 9.8 × sin(30°) = 49 N (down the ramp)
N = 10 × 9.8 × cos(30°) = 84.9 N
f_s,max = 0.6 × 84.9 = 50.9 N

Since f_s,max (50.9 N) > W_∥ (49 N), the block does NOT slide.
```

---

## Day 14-15: Tension and Atwood Machines

### Tension in Ropes

Tension is a pulling force transmitted through a rope, string, or cable.

**Key insight:** For a massless rope, tension is the same throughout.

### SpaceX Application: Launch Umbilical Tension

Before liftoff, the launch umbilical cord provides fuel, oxidizer, electrical power, and data to the rocket. The tension in this umbilical must be carefully managed:
- Too much tension: Cord doesn't release cleanly
- Too little: Cord drags and creates asymmetric forces

### Atwood Machine

Two masses connected by a rope over a pulley:

```
For m₁ > m₂:
a = (m₁ - m₂)g / (m₁ + m₂)
T = 2m₁m₂g / (m₁ + m₂)
```

---

## Day 16-17: Circular Motion

### The Key Insight: Acceleration Toward Center

An object moving in a circle at constant speed is **accelerating** — because its direction is constantly changing.

```
Centripetal acceleration: a_c = v²/r (toward center)
Centripetal force: F_c = mv²/r (toward center)
```

### There Is No "Centrifugal Force"

**Centrifugal force is a fictitious force** — it appears only in a rotating reference frame. In an inertial frame, there is only centripetal force.

### The ISS: Circular Motion in Action

The ISS orbits at 400 km altitude, moving at 7,660 m/s. It is NOT "held up" — it is in continuous free fall.

**The calculation:**
```
r = 6,371,000 + 400,000 = 6,771,000 m
v = 7,660 m/s

Centripetal acceleration:
a_c = v²/r = (7,660)² / 6,771,000 = 8.67 m/s²

Gravitational acceleration at 400 km:
g = 9.8 × (6,371/6,771)² = 8.67 m/s²

They match! Gravity provides exactly the centripetal force needed.
```

**Orbit is not magic. It is falling around the Earth instead of into it.**

---

## Day 18: Design Challenge — Egg Drop

### The Physics

Landing a Falcon 9 booster is like landing an egg — but at 10,000× the scale.

Design a structure that:
- Protects an egg dropped from 5 meters
- Uses only paper and tape
- Minimizes total mass

### The Key Concept: Impulse

```
Impulse = F × Δt = Δp

To reduce peak force F, increase contact time Δt.
```

This is exactly what Falcon 9's landing legs do — their crush cores extend the impact time, reducing peak force.

---

## Day 19-20: Review and Exam

### Unit Summary

| Concept | Key Equation | SpaceX Connection |
|---------|--------------|-------------------|
| First Law | No net force → constant velocity | Active control needed |
| Second Law | ΣF = ma | Liftoff acceleration |
| Third Law | Action = Reaction | Rocket propulsion |
| Friction | f = μN | Ablative liners |
| Circular motion | F_c = mv²/r | Orbital mechanics |

### Exit Ticket

*"Write one sentence explaining why the ISS doesn't fall down, using only concepts from this unit."*

---

## Problem Sets

### Tier 1: Foundation (Must Do)

1. Draw FBDs for a Falcon 9 at: (a) on the pad, (b) liftoff, (c) in orbit.

2. A 2 kg book sits on a table. What force does the table exert on the book? What force does the book exert on the table? Are these an action-reaction pair?

3. Calculate the centripetal acceleration of a car going 25 m/s around a curve of radius 50 m.

### Tier 2: Application (Should Do)

4. A Falcon 9 booster (mass 25,000 kg after fuel depletion) decelerates at 3g during landing burn. Calculate the required thrust.

5. A 5 kg block sits on a 20° ramp with μ_s = 0.4. (a) Will it slide? (b) If pushed with 10 N up the ramp, what is its acceleration?

### Tier 3: Challenge (Want to Try?)

6. **Grid Fin Physics:** A grid fin produces 50,000 N of drag force at an angle of 15° from the rocket axis. Decompose this into axial and lateral components. If the booster mass is 25,000 kg, what lateral acceleration does this produce?

7. **Bracket Connection:** The centripetal acceleration for Earth orbit at 400 km is 8.67 m/s². At what altitude is a_c = φ × 9.8 m/s²? (Hint: Use the formula g = g₀(R_E/r)² and a_c = v²/r with v from orbital mechanics.)

---

*© 2026 Thomas A. Husmann / iBuilt LTD. All rights reserved.*
*Licensed under CC BY-NC-SA 4.0 for academic and research use.*
