# Year 2, Unit 2: Rotational Mechanics
## *Spin, Angular Momentum, and Attitude Control*

**Duration:** 15 Days
**Grade Level:** 11th Grade
**Prerequisites:** Year 1 complete, Unit 1 of Year 2

---

## Anchoring Question

> *A spacecraft in orbit has no air resistance, no friction — how does it change its orientation? The answer involves angular momentum, reaction wheels, and gyroscopic physics. How do we control rotation in the vacuum of space?*

---

## Learning Objectives

By the end of this unit, you will be able to:
1. Define and calculate moment of inertia for various geometries
2. Apply Newton's second law for rotation (τ = Iα)
3. Use conservation of angular momentum
4. Analyze gyroscopic precession
5. Understand spacecraft attitude control systems

---

## Day 1-2: Angular Kinematics

### Rotational Variables

| Linear | Rotational | Relationship |
|--------|------------|--------------|
| x (position) | θ (angle) | x = rθ |
| v (velocity) | ω (angular velocity) | v = rω |
| a (acceleration) | α (angular acceleration) | a = rα |

### Rotational Kinematic Equations

```
ω = ω₀ + αt
θ = θ₀ + ω₀t + ½αt²
ω² = ω₀² + 2αθ
```

### Units

- Angle θ: radians (rad)
- Angular velocity ω: rad/s
- Angular acceleration α: rad/s²

---

## Day 3-4: Moment of Inertia

### Definition

Moment of inertia measures resistance to rotational acceleration:

```
I = Σmᵢrᵢ²  (discrete masses)
I = ∫r²dm   (continuous distribution)
```

### Common Geometries

| Object | Axis | Moment of Inertia |
|--------|------|-------------------|
| Point mass | Distance r | I = mr² |
| Thin rod (center) | Perpendicular | I = (1/12)ML² |
| Thin rod (end) | Perpendicular | I = (1/3)ML² |
| Solid cylinder | Central axis | I = ½MR² |
| Hollow cylinder | Central axis | I = MR² |
| Solid sphere | Diameter | I = (2/5)MR² |
| Hollow sphere | Diameter | I = (2/3)MR² |

### Parallel Axis Theorem

```
I = I_cm + Md²

Where d = distance from center of mass to new axis
```

---

## Day 5-6: Torque and Newton's Second Law

### Torque Definition

```
τ = r × F = rF sin θ

Magnitude: |τ| = rF sin θ (N·m)
```

### Newton's Second Law for Rotation

```
Στ = Iα

Net torque = moment of inertia × angular acceleration
```

### SpaceX Application: Grid Fin Control

Falcon 9 grid fins generate aerodynamic torque for attitude control during reentry:

```
Torque from grid fin = Force × moment arm

τ_fin = F_aero × d_fin
```

Each of the four fins can independently adjust, providing roll, pitch, and yaw control at hypersonic speeds.

---

## Day 7-8: Rotational Energy and Work

### Rotational Kinetic Energy

```
KE_rot = ½Iω²
```

### Work-Energy Theorem

```
W = τθ = ΔKE_rot
```

### Rolling Motion

For an object rolling without slipping:
```
v_cm = Rω
KE_total = ½mv² + ½Iω²
         = ½mv² + ½I(v/R)²
         = ½v²(m + I/R²)
```

---

## Day 9-10: Angular Momentum

### Definition

```
L = Iω  (for rigid body about fixed axis)
L = r × p = r × mv  (for point particle)
```

### Conservation of Angular Momentum

**If no external torque acts on a system:**
```
L_initial = L_final
I₁ω₁ = I₂ω₂
```

### Classic Example: Figure Skater

Arms extended: large I, small ω
Arms pulled in: small I, large ω
Same angular momentum!

### SpaceX Application: Reaction Wheels

Spacecraft use reaction wheels to change orientation:

1. **Spin up a flywheel** → spacecraft rotates opposite direction
2. **Angular momentum conserved** → L_wheel + L_spacecraft = constant
3. **No propellant used** → infinite small adjustments

Dragon spacecraft uses 4 reaction wheels for 3-axis stabilization plus redundancy.

---

## Day 11-12: Gyroscopic Effects

### Gyroscopic Precession

A spinning gyroscope doesn't fall over — it precesses:

```
Ω = τ / L = Mgr / (Iω)

Where:
  Ω = precession rate
  τ = gravitational torque
  L = spin angular momentum
```

### Gyroscopic Stability

Spinning objects resist changes to their rotation axis. This explains:
- Why bicycles are stable when moving
- How rifling stabilizes bullets
- Why spacecraft use spin stabilization

### SpaceX Application: Starlink Spin Stabilization

During deployment, Starlink satellites are released in a spinning "stack":
- Spin provides gyroscopic stability
- Reduces attitude control fuel needed
- Satellites de-spin and deploy solar panels individually

---

## Day 13: Lab — Reaction Wheel Demonstration

### Building a Simple Reaction Wheel

**Materials:**
- Rotating platform (lazy Susan)
- Bicycle wheel with handles
- Stopwatch

**Procedure:**
1. Stand on platform holding bicycle wheel not spinning
2. Spin the wheel and observe platform rotation
3. Flip the wheel axis and observe reversal
4. Quantify angular momentum transfer

**Calculations:**
```
L_wheel = I_wheel × ω_wheel
L_person = I_person × ω_person

Conservation: L_wheel + L_person = 0
```

---

## Day 14-15: Spacecraft Attitude Control Systems

### Control Methods

1. **Reaction Wheels**
   - Pros: No propellant, precise control
   - Cons: Momentum saturation, mechanical wear

2. **Control Moment Gyroscopes (CMGs)**
   - Pros: Higher torque than reaction wheels
   - Cons: Complex, potential gimbal lock

3. **Thrusters (RCS)**
   - Pros: High torque, momentum dumping
   - Cons: Uses propellant, imprecise

4. **Magnetorquers**
   - Pros: No moving parts, no propellant
   - Cons: Only works in magnetic field, low torque

### ISS Attitude Control

The ISS uses CMGs for routine attitude control and thrusters for momentum dumping:
- 4 CMGs provide ~258 N·m torque each
- Thrusters fire periodically to desaturate CMGs

---

## Unit Summary

| Concept | Key Equation | Application |
|---------|--------------|-------------|
| Moment of inertia | I = Σmr² | Rotational mass |
| Torque | τ = rF sin θ | Rotational force |
| Newton's 2nd (rot) | τ = Iα | Rotational dynamics |
| Angular momentum | L = Iω | Conservation |
| Rotational KE | KE = ½Iω² | Energy analysis |
| Precession | Ω = τ/L | Gyroscopic motion |

---

## Problem Sets

### Tier 1: Foundation (Must Do)

1. A solid cylinder (M = 5 kg, R = 0.2 m) rotates at 10 rad/s. Calculate its (a) moment of inertia, (b) angular momentum, (c) rotational kinetic energy.

2. A torque of 50 N·m is applied to a wheel with I = 2 kg·m². Calculate the angular acceleration.

3. A skater spins at 2 rev/s with arms extended (I = 4 kg·m²). She pulls her arms in (I = 2 kg·m²). What is her new angular velocity?

### Tier 2: Application (Should Do)

4. A reaction wheel (I = 0.1 kg·m²) spins up from rest to 3000 rpm in 10 seconds. If the spacecraft has I = 500 kg·m², what is its angular velocity change?

5. Falcon 9's first stage (modeled as a cylinder, M = 25,000 kg, R = 1.83 m) needs to rotate 180° in 30 seconds for landing burn. What torque is required?

### Tier 3: Challenge (Want to Try?)

6. **CMG Analysis:** A Control Moment Gyroscope has flywheel I = 0.5 kg·m² spinning at 6000 rpm. The gimbal rotates at 1 rad/s. Calculate the output torque using τ = L × Ω_gimbal.

7. **φ-Symmetry in Rotation:** The moment of inertia of a thin rod about its center is (1/12)ML². About its end, it's (1/3)ML². The ratio is 4. For what geometry would the ratio of moments about two perpendicular axes equal φ?

---

## Resources

### Demonstrations
- MIT Gyroscope demonstrations (YouTube)
- NASA ISS attitude control videos

### References
- Kleppner & Kolenkow: "An Introduction to Mechanics"
- Wertz: "Spacecraft Attitude Determination and Control"

---

*© 2026 Thomas A. Husmann / iBuilt LTD. All rights reserved.*
*Licensed under CC BY-NC-SA 4.0 for academic and research use.*
