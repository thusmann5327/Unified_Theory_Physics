# Year 3, Unit 2: Rocket Propulsion
## *From Chemical to Nuclear to Electric*

**Duration:** 20 Days
**Grade Level:** 12th Grade
**Prerequisites:** Year 1-2, Unit 1 of Year 3, Calculus

---

## Anchoring Question

> *Chemical rockets are limited to ~4.5 km/s exhaust velocity. Nuclear thermal rockets could achieve 9 km/s. Ion engines reach 30+ km/s but with tiny thrust. What's the physics behind each propulsion type, and which is best for reaching Mars? The asteroid belt? Interstellar space?*

---

## Learning Objectives

By the end of this unit, you will be able to:
1. Analyze propulsion systems using thermodynamics
2. Calculate specific impulse for various propellants
3. Compare chemical, nuclear, and electric propulsion
4. Understand staging optimization
5. Evaluate the Parametric Cascade patent concept

---

## Day 1-2: Propulsion Fundamentals Review

### The Rocket Equation (Revisited)

```
Δv = v_e × ln(m₀/m_f) = I_sp × g₀ × ln(m₀/m_f)
```

### Specific Impulse

```
I_sp = v_e / g₀ = F / (ṁ × g₀)

Units: seconds (how long 1 kg of propellant produces 1 kg of thrust)
```

### Thrust

```
F = ṁ × v_e + (P_e - P_a) × A_e

Where:
  ṁ = mass flow rate
  v_e = exhaust velocity
  P_e = exit pressure
  P_a = ambient pressure
  A_e = exit area
```

---

## Day 3-4: Chemical Propulsion

### Combustion Chemistry

**Hydrogen-Oxygen (LOX/LH2):**
```
2H₂ + O₂ → 2H₂O + 572 kJ/mol
```

**Methane-Oxygen (LOX/CH4):**
```
CH₄ + 2O₂ → CO₂ + 2H₂O + 890 kJ/mol
```

**RP-1-Oxygen (Kerosene):**
```
2C₁₂H₂₆ + 37O₂ → 24CO₂ + 26H₂O + heat
```

### Theoretical Performance

| Propellant | O/F Ratio | T_c (K) | I_sp (s) |
|------------|-----------|---------|----------|
| LOX/LH2 | 6.0 | 3500 | 450 |
| LOX/CH4 | 3.6 | 3600 | 380 |
| LOX/RP-1 | 2.7 | 3700 | 350 |
| N₂O₄/UDMH | 2.1 | 3400 | 320 |

### Why Lighter Exhaust is Better

```
v_e = √(2 × η × ΔH / M_exhaust)

Lower molecular weight M → higher exhaust velocity
```

H₂O (M=18) is lighter than CO₂ (M=44), so hydrogen fuels have higher I_sp.

### SpaceX Raptor: Full-Flow Staged Combustion

**Unique features:**
- Both preburners use all propellant
- Fuel-rich preburner: CH₄ + some O₂ → CO + H₂ (hot gas to drive fuel turbopump)
- Oxidizer-rich preburner: O₂ + some CH₄ → hot O₂ (to drive LOX turbopump)
- All propellant reaches main chamber (no overboard dump)
- Highest efficiency cycle ever flown

**Performance:**
- Chamber pressure: 330 bar
- I_sp: 350 s (SL), 380 s (vacuum)
- Thrust: 230 tf (SL), 258 tf (vacuum)

---

## Day 5-6: Nuclear Thermal Propulsion

### The Concept

Heat propellant directly with nuclear reactor, no combustion:

```
Nuclear fission → Heat → Propellant expansion → Thrust
```

### NERVA Program (1955-1973)

- Tested 20+ reactors
- Best result: I_sp = 825 s (nearly 2× chemical!)
- Thrust: 334 kN
- Temperature limit: ~2700 K (reactor materials)

### Why Higher I_sp?

```
v_e = √(2c_pT / M)
```

Pure hydrogen (M = 2) with high temperature gives:
- I_sp ≈ 900 s theoretical
- 2× better than LOX/LH2 chemical

### Modern Concepts

**DRACO (DARPA):**
- Nuclear thermal demonstrator
- Launch planned 2027
- Could cut Mars transit time in half

### Challenges

- Reactor shielding mass
- Radioactive exhaust (must not fire near Earth)
- Political/regulatory hurdles
- Ground testing difficulties

---

## Day 7-8: Electric Propulsion

### Types of Electric Propulsion

1. **Electrothermal:** Heat propellant electrically (resistojet, arcjet)
2. **Electrostatic:** Accelerate ions with electric field (ion, Hall)
3. **Electromagnetic:** Use magnetic field (MPD, VASIMR)

### Ion Engine Physics

```
v_e = √(2eV / m)

Where:
  e = electron charge
  V = accelerating voltage
  m = ion mass
```

For xenon at 1000 V:
```
v_e = √(2 × 1.6×10⁻¹⁹ × 1000 / 2.2×10⁻²⁵) = 38,000 m/s
I_sp = 38,000 / 9.81 = 3,900 s!
```

### The Tradeoff: Thrust vs. Efficiency

```
Power = ½ × ṁ × v_e²

For fixed power P:
- High v_e → low ṁ → low thrust
- Low v_e → high ṁ → high thrust
```

### Comparison Table

| System | I_sp (s) | Thrust | Power Source | Application |
|--------|----------|--------|--------------|-------------|
| Chemical | 300-450 | High | Chemical | Launch, maneuvers |
| Nuclear Thermal | 800-1000 | Medium | Fission | Interplanetary |
| Ion Engine | 3000-5000 | Very Low | Solar/Nuclear | Deep space |
| Hall Thruster | 1500-3000 | Low | Solar | Station keeping |
| VASIMR | 3000-30000 | Adjustable | Nuclear | Proposed |

### SpaceX Starlink Hall Thrusters

- Krypton propellant (cheaper than xenon)
- I_sp ≈ 1500 s
- Used for orbit raising and station keeping
- 6000+ satellites using electric propulsion

---

## Day 9-10: Staging Optimization

### Why Stage?

Carrying empty tanks wastes propellant. Staging discards dead mass.

### Optimal Staging

For identical stages with same I_sp:
```
Δv_per_stage = Δv_total / n

Mass ratio per stage: μ = e^(Δv_per_stage / v_e)
```

### Structural Coefficient

```
ε = m_structure / (m_structure + m_propellant)

Real rockets: ε ≈ 0.05-0.15
```

### Payload Fraction

```
λ = m_payload / m_initial

Higher I_sp → higher λ
More stages → higher λ (but more complexity)
```

### Example: Falcon 9 vs. Starship

**Falcon 9:**
- 2 stages
- Payload to LEO: ~23 tons
- λ ≈ 4%

**Starship (expendable):**
- 2 stages
- Payload to LEO: ~150 tons
- λ ≈ 2.5% (worse, but reusable design)

---

## Day 11-12: Mission Design Application

### Mars Mission Δv Budget

| Segment | Δv (km/s) |
|---------|-----------|
| LEO → Earth escape | 3.2 |
| Hohmann transfer | 2.5 |
| Mars capture | 0.9 |
| Mars landing | 1.5 |
| **Total to Mars surface** | **8.1** |
| Mars ascent | 4.1 |
| Mars escape | 2.5 |
| Return transfer | 2.5 |
| Earth capture (aerobrake) | 0 |
| **Total round trip** | **17.2** |

### Propulsion Comparison for Mars

**Chemical only (Starship):**
- Δv capability: ~6 km/s per fueling
- Needs orbital refueling at Earth AND Mars

**Nuclear thermal:**
- Δv capability: ~12 km/s single stage
- Could reach Mars without refueling

**Nuclear electric:**
- I_sp: 5000+ s
- Very long transit time (low thrust)
- Best for cargo, not crew

---

## Day 13-14: The Parametric Cascade Concept

### Patent 63/995,816 Overview

**The Claim:** A spacecraft propulsion system incorporating:
1. Multiple engine chambers of φ-scaled sizes
2. Sequential ignition following Fibonacci timing
3. Thrust vector distribution optimized for structural φ-ratio spacing

### Physics Basis

**Established:**
- φ-spaced structures minimize resonance coupling
- Quasiperiodic forcing avoids constructive interference
- Fibonacci timing creates self-similar thrust profiles

**The Novel Claim:**
- Combining these in a propulsion system provides structural benefit
- May reduce pogo-like instabilities
- Optimizes thrust distribution across vehicle frame

### Critical Evaluation Questions

1. What evidence supports φ-spacing reducing resonance?
2. How would you test this experimentally?
3. What would refute the claim?
4. Is the benefit worth the complexity?

---

## Day 15-18: Simulation Project

### Assignment

Using `propulsion_sim.py`:

1. **Chemical Baseline:** Design a Mars mission with LOX/CH4 (I_sp = 350 s)
2. **Nuclear Thermal:** Redesign with I_sp = 850 s
3. **Hybrid:** Chemical for launch, nuclear for transfer
4. **Compare:** Total mass, transit time, complexity

### Simulation Framework

```python
import numpy as np

def mission_delta_v(segments):
    """Calculate total Δv for mission"""
    return sum(segments.values())

def mass_ratio(delta_v, isp):
    """Calculate mass ratio using rocket equation"""
    v_e = isp * 9.81
    return np.exp(delta_v / v_e)

def propellant_mass(payload, delta_v, isp, structural_fraction=0.1):
    """Calculate propellant needed for given payload and Δv"""
    MR = mass_ratio(delta_v, isp)
    # m_initial / m_final = MR
    # m_final = payload + structure
    # structure = structural_fraction * propellant
    # Solve iteratively...

mars_mission = {
    'leo_escape': 3200,
    'transfer': 2500,
    'capture': 900,
    'landing': 1500
}

total_dv = mission_delta_v(mars_mission)
print(f"Mars mission Δv: {total_dv} m/s")
```

---

## Day 19-20: Assessment

### Unit Summary

| Propulsion Type | I_sp (s) | Best Use | Limitation |
|-----------------|----------|----------|------------|
| Chemical | 300-450 | Launch, fast maneuvers | Low efficiency |
| Nuclear Thermal | 800-1000 | Interplanetary | Radiation, politics |
| Ion/Hall | 1500-5000 | Station keeping, cargo | Low thrust |
| Nuclear Electric | 3000+ | Deep space | Power/mass ratio |

---

## Problem Sets

### Tier 1: Foundation (Must Do)

1. A rocket engine has thrust 2 MN and propellant flow rate 650 kg/s. Calculate I_sp.

2. Compare mass ratios needed for Δv = 9 km/s using (a) I_sp = 350 s, (b) I_sp = 900 s.

3. An ion engine uses 3000 V to accelerate argon ions (mass 6.6×10⁻²⁶ kg). Calculate exhaust velocity.

### Tier 2: Application (Should Do)

4. Design a two-stage rocket to deliver 10 tons to LEO (Δv = 9.4 km/s). Both stages use I_sp = 330 s and structural fraction 0.08. What is the launch mass?

5. A nuclear thermal stage with I_sp = 850 s must provide Δv = 4 km/s. If payload is 50 tons and structural fraction is 0.15, what propellant mass is needed?

### Tier 3: Challenge (Want to Try?)

6. **Optimal I_sp:** For fixed power P, show that maximum acceleration occurs when I_sp is chosen such that thrust equals the rate of propellant kinetic energy increase. Derive the optimal exhaust velocity.

7. **Parametric Cascade:** If engine chambers are sized in ratio φ and ignited in Fibonacci-timed sequence, what is the resulting thrust profile? Model this and compare to simultaneous ignition.

---

## Resources

### NASA Technical
- NERVA program reports
- Ion Propulsion System documentation

### Videos
- Everyday Astronaut: "Ion Engines"
- Scott Manley: "Nuclear Rockets"

---

*© 2026 Thomas A. Husmann / iBuilt LTD. All rights reserved.*
*Licensed under CC BY-NC-SA 4.0 for academic and research use.*
