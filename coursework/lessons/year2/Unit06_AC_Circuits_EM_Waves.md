# Year 2, Unit 6: AC Circuits & Electromagnetic Waves
## *RLC Resonance, Phased Arrays, and Starlink*

**Duration:** 15 Days
**Grade Level:** 11th Grade
**Prerequisites:** Year 1 complete, Units 1-5 of Year 2

---

## Anchoring Question

> *A Starlink satellite communicates with millions of ground terminals using electronically steered phased arrays — antennas that can point their beams without moving parts. How do AC circuits, resonance, and electromagnetic wave physics make this possible?*

---

## Learning Objectives

By the end of this unit, you will be able to:
1. Analyze AC circuits with resistors, capacitors, and inductors
2. Calculate impedance and phase relationships
3. Understand resonance in RLC circuits
4. Derive EM wave properties from Maxwell's equations (conceptually)
5. Explain phased array beam steering

---

## Day 1-2: AC Circuit Fundamentals

### Alternating Current

```
V(t) = V₀ cos(ωt)
I(t) = I₀ cos(ωt + φ)

Where:
  V₀, I₀ = peak values
  ω = 2πf = angular frequency
  φ = phase angle between V and I
```

### RMS Values

```
V_rms = V₀/√2 ≈ 0.707 V₀
I_rms = I₀/√2 ≈ 0.707 I₀
```

Power calculations use RMS values.

### Phasors

Represent AC quantities as rotating vectors:
- Length = amplitude
- Angle = phase
- Useful for adding AC signals

---

## Day 3-4: Reactance and Impedance

### Resistor (R)

```
V_R = IR
Voltage and current in phase
```

### Capacitor (C)

```
V_C = I × X_C
X_C = 1/(ωC) = 1/(2πfC)

Current LEADS voltage by 90° ("ICE")
```

### Inductor (L)

```
V_L = I × X_L
X_L = ωL = 2πfL

Voltage LEADS current by 90° ("ELI")
```

### Impedance (Z)

For series RLC circuit:
```
Z = √(R² + (X_L - X_C)²)

Phase angle: tan φ = (X_L - X_C)/R
```

### Generalized Ohm's Law

```
V = IZ
```

---

## Day 5-6: RLC Resonance

### Resonant Frequency

When X_L = X_C, impedance is minimum (Z = R):

```
ωL = 1/(ωC)
ω₀ = 1/√(LC)
f₀ = 1/(2π√(LC))
```

### At Resonance

- Current is maximum
- Impedance equals R
- Voltage and current are in phase
- Q = ω₀L/R = 1/(ω₀CR)

### Bandwidth

```
Δf = f₀/Q
```

Higher Q = narrower bandwidth = sharper tuning

### Applications

- Radio tuners select stations
- Filters pass/block frequency ranges
- Oscillators generate specific frequencies

---

## Day 7-8: Power in AC Circuits

### Instantaneous Power

```
P(t) = V(t) × I(t)
```

### Average Power

```
P_avg = V_rms × I_rms × cos φ
      = I²_rms × R

Where cos φ = power factor
```

### Reactive Power

```
Q = V_rms × I_rms × sin φ (in VAR)
```

Reactive power oscillates between source and reactive components but does no net work.

### Apparent Power

```
S = V_rms × I_rms (in VA)
S² = P² + Q²
```

---

## Day 9-10: Electromagnetic Waves

### Maxwell's Equations (Conceptual)

1. **Gauss (E):** Electric field lines originate on charges
2. **Gauss (B):** No magnetic monopoles
3. **Faraday:** Changing magnetic field creates electric field
4. **Ampère-Maxwell:** Currents and changing electric fields create magnetic fields

### The Wave Equation

Maxwell showed that E and B fields satisfy:

```
∂²E/∂x² = μ₀ε₀ × ∂²E/∂t²
```

This is a wave equation with speed:

```
c = 1/√(μ₀ε₀) = 2.998 × 10⁸ m/s
```

**Light is an electromagnetic wave!**

### Properties of EM Waves

- E and B perpendicular to each other
- Both perpendicular to propagation direction (transverse)
- E and B in phase
- E/B = c

### Energy and Intensity

```
Intensity: I = P/A = (1/2)ε₀cE₀²

Poynting vector: S⃗ = (1/μ₀)E⃗ × B⃗
```

---

## Day 11-12: Antennas and Phased Arrays

### Dipole Antenna

A half-wave dipole:
- Length = λ/2
- Resonates at design frequency
- Radiates perpendicular to axis

### Antenna Arrays

Multiple antennas in an array:
- Signals combine constructively/destructively
- Creates directional beam pattern
- Beam direction depends on relative phase

### Phased Array Beam Steering

**The key insight:** By controlling the phase of signal at each antenna element, the beam direction changes electronically — no mechanical movement!

```
Phase shift for beam at angle θ:
Δφ = (2π/λ) × d × sin θ

Where d = element spacing
```

### SpaceX Starlink Phased Arrays

**User Terminal ("Dishy"):**
- 1,280 antenna elements
- Flat panel, no moving parts
- Steers beam by electronic phase control
- Tracks satellites across the sky
- Frequency: 10.7-12.7 GHz (Ku-band downlink)

**Satellite Antennas:**
- Multiple phased arrays
- 48 spot beams per satellite
- Dynamic beam allocation
- Handoff as satellites move overhead

---

## Day 13: Lab — RLC Resonance

### Experiment Setup

**Materials:**
- Function generator
- Oscilloscope
- Resistor (100 Ω)
- Capacitor (0.1 µF)
- Inductor (10 mH)

**Procedure:**
1. Build series RLC circuit
2. Calculate theoretical f₀ = 1/(2π√(LC))
3. Sweep frequency, measure voltage across R
4. Plot V_R vs. frequency
5. Identify resonance peak
6. Measure bandwidth, calculate Q

### Analysis Questions

1. How does measured f₀ compare to calculated?
2. What is the measured Q factor?
3. If you add another resistor in series, how does the curve change?

---

## Day 14-15: Assessment and Applications

### Starlink Communication System

**Frequency Bands:**
- User link: 10.7-12.7 GHz (downlink), 14.0-14.5 GHz (uplink)
- Gateway link: 17.8-18.6 GHz, 18.8-19.3 GHz
- Inter-satellite link: 1550 nm laser (optical)

**Latency:**
- LEO orbit: ~550 km altitude
- Round-trip light time: ~4 ms
- Total latency: ~20-40 ms (vs. 600+ ms for GEO)

**Data Rates:**
- User terminal: 50-200 Mbps download
- Per satellite: ~20 Gbps aggregate

### Simulation Exercise

```python
import numpy as np
import matplotlib.pyplot as plt

def phased_array_pattern(num_elements, spacing_lambda, beam_angle_deg):
    """Calculate array factor for linear phased array"""
    theta = np.linspace(-90, 90, 1000) * np.pi/180
    beam_angle = beam_angle_deg * np.pi/180

    # Phase shift for each element
    k = 2 * np.pi  # in units of 1/wavelength
    d = spacing_lambda  # element spacing in wavelengths

    # Array factor
    psi = k * d * (np.sin(theta) - np.sin(beam_angle))
    AF = np.sin(num_elements * psi / 2) / (num_elements * np.sin(psi / 2 + 1e-10))

    return theta * 180/np.pi, np.abs(AF)

# Plot beam patterns for different steering angles
plt.figure(figsize=(10, 6))
for angle in [0, 15, 30, 45]:
    theta, AF = phased_array_pattern(16, 0.5, angle)
    plt.plot(theta, 20*np.log10(AF + 1e-10), label=f'{angle}°')

plt.xlabel('Angle (degrees)')
plt.ylabel('Array Factor (dB)')
plt.title('Phased Array Beam Steering')
plt.legend()
plt.grid(True)
plt.ylim(-40, 5)
```

---

## Unit Summary

| Concept | Key Equation | Application |
|---------|--------------|-------------|
| Impedance | Z = √(R² + (X_L-X_C)²) | AC analysis |
| Resonance | f₀ = 1/(2π√(LC)) | Tuning circuits |
| Q factor | Q = ω₀L/R | Selectivity |
| EM wave speed | c = 1/√(μ₀ε₀) | Light/radio |
| Phased array | Δφ = kd sin θ | Beam steering |

---

## Problem Sets

### Tier 1: Foundation (Must Do)

1. A 100 Ω resistor, 10 mH inductor, and 1 µF capacitor are in series. Calculate (a) resonant frequency, (b) impedance at resonance, (c) Q factor.

2. At 1 kHz, find the reactance of (a) a 10 µF capacitor, (b) a 100 mH inductor.

3. An AC source provides 120 V (rms) at 60 Hz. If current is 5 A (rms) and power factor is 0.8, what is the average power consumed?

### Tier 2: Application (Should Do)

4. A radio receiver uses an LC circuit to tune stations. If C = 100 pF and the desired frequency range is 500 kHz to 1500 kHz, what range of L is needed?

5. A 16-element linear phased array has spacing d = λ/2. Calculate the phase shift per element needed to steer the beam to 30°.

### Tier 3: Challenge (Want to Try?)

6. **Starlink Analysis:** A Starlink satellite at 550 km altitude communicates at 12 GHz. Calculate (a) wavelength, (b) free-space path loss to ground, (c) if transmitted power is 1 W and antenna gain is 30 dB, what is received power density at ground?

7. **φ-Frequency:** If an RLC circuit had L and C values in ratio φ (L/C = φ × 1 H/F), what would be the resonant frequency? Is there any relationship between this and naturally occurring frequencies?

---

## Resources

### Videos
- Veritasium: "How Starlink Works"
- MIT OpenCourseWare: AC Circuits

### References
- Griffiths: "Introduction to Electrodynamics"
- Starlink FCC filings (public)

---

*© 2026 Thomas A. Husmann / iBuilt LTD. All rights reserved.*
*Licensed under CC BY-NC-SA 4.0 for academic and research use.*
