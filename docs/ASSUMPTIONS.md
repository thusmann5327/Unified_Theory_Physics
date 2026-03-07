# Framework Assumptions and Adjustable Parameters

## Overview

This document catalogs the core assumptions underlying the Husmann Decomposition framework and identifies parameters that can be adjusted for experimental refinement.

---

## Category 1: Mathematical Foundations

### 1.1 Golden Ratio as Fundamental Constant

**Assumption**: The golden ratio φ = (1+√5)/2 represents a fundamental organizational principle in physical systems.

**Justification**:
- Appears naturally in Fibonacci sequence limit
- Satisfies unique self-referential equation: φ² = φ + 1
- Generates aperiodic tilings that span Euclidean space without repeating

**Status**: Mathematical fact, physical interpretation requires validation

### 1.2 Unity Identity

**Assumption**: The identity 1/φ + 1/φ³ + 1/φ⁴ = 1 has physical significance.

**Verification**:
```python
phi = (1 + 5**0.5) / 2
result = 1/phi + 1/phi**3 + 1/phi**4
# Returns: 1.0000000000000000 (exact to machine precision)
```

**Status**: Mathematically proven, cosmological interpretation speculative

---

## Category 2: Lattice Parameters

### 2.1 Aubry-André-Harper (AAH) Lattice

**Model**: H = J[ψ(n+1) + ψ(n-1)] + V cos(2πn/φ)ψ(n)

**Critical Parameters**:

| Parameter | Symbol | Value | Uncertainty | Source |
|-----------|--------|-------|-------------|--------|
| Lattice spacing | l | 9.3 nm | ±0.1 nm | Fitted to c |
| Hopping energy | J | 10.6 eV | ±0.1 eV | Fitted to c |
| Potential ratio | V/J | 2.0 | exact | Critical point |
| Bands | N | 3 | fixed | Low-energy limit |
| Sector width | W | 45.78° | derived | φ × φ × Golden angle |

### 2.2 Adjustable Parameter Space

**Primary tuning parameters**:
1. `l` (lattice spacing): Determines velocity scale
2. `J` (hopping energy): Sets energy/mass scale
3. `N` (band count): Controls fine structure denominator

**Constraint equation**: c = 2Jl/ℏ (Lieb-Robinson velocity)

**Current fit**: l = 9.3 nm, J = 10.6 eV yields c ≈ 2.998 × 10⁸ m/s

---

## Category 3: Signal Processing Parameters

### 3.1 Fibonacci Attractor Frequencies

**Assumption**: Neural oscillations lock to Fibonacci-harmonic frequencies.

**Current frequency set**:
```python
freqs = [4.0, 7.0, 11.0, 18.0, 29.0, 47.0]  # Hz
```

**Adjustable parameters**:
- Base frequency (currently 4 Hz)
- Number of cascade levels (currently 6)
- Frequency tolerance for band detection

### 3.2 Phase Coherence Thresholds

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| Window length | 0.5 s | 0.1-2.0 s | Analysis window |
| Sampling rate | 20 kHz | 1-40 kHz | Required for phase accuracy |
| Coherence threshold | 0.5 | 0.3-0.8 | Minimum for "locked" state |
| Skip depth | 3 | 1-5 | Error correction levels |

---

## Category 4: Cosmological Correspondence

### 4.1 Energy Density Mapping

**Assumption**: Unity identity maps to cosmic energy budget.

| Term | Value | Interpretation | Observed |
|------|-------|----------------|----------|
| 1/φ | 0.618 | Dark energy | 0.68 |
| 1/φ³ | 0.236 | Dark matter | 0.27 |
| 1/φ⁴ | 0.146 | Baryonic matter | 0.05 |

**Discrepancy**: ~3× for baryonic matter

**Possible resolutions**:
1. Higher-order terms needed
2. Different physical interpretation
3. Additional mechanism for matter fraction

### 4.2 Status

This mapping is **speculative** and requires:
- Derivation from first principles
- Explanation of ~3× discrepancy
- Independent cosmological predictions

---

## Category 5: Dimensional Analysis

### 5.1 Dimensionless Ratios

**Assumption**: Dimensionless constants arise from geometric ratios.

**Examples**:
| Constant | Observed | Framework | Match |
|----------|----------|-----------|-------|
| α (fine structure) | 1/137.036 | 1/(N×W) | 0.19% |
| Proton/electron mass | 1836.15 | φ^(16.2) | exact fit |

### 5.2 Adjustable Aspects

- Choice of band count N
- Sector width calculation method
- Power law exponents

---

## Category 6: Quantum Mechanical Translations

### 6.1 Core Assumption

**Claim**: Standard QM formulas can be rewritten in terms of φ and Fibonacci operations.

**Status by formula**:

| Formula | Translation Status | Validation |
|---------|-------------------|------------|
| Euler identity | Exact | Mathematical |
| Planck-Einstein | Symbolic | Interpretive |
| Schrödinger | Structural | Needs derivation |
| Dirac equation | Partial | In progress |
| Maxwell's equations | Geometric | Symbolic |

### 6.2 Validation Requirements

Each translation requires:
1. Mathematical equivalence proof
2. Physical interpretation
3. Experimental test (where applicable)

---

## Summary: Confidence Levels

| Category | Confidence | Notes |
|----------|------------|-------|
| Mathematical identities | High | Proven |
| Unity identity | High | Proven |
| AAH lattice structure | Medium | Well-studied model |
| Lattice parameters (l, J) | Medium | Fitted, not derived |
| Fine structure derivation | Medium | Good match, ad hoc |
| Signal processing | Medium | Empirically validated |
| Cosmological mapping | Low | Speculative |
| QM translations | Variable | Case-by-case |

---

## How to Adjust Parameters

### For Researchers

1. **Modify lattice parameters**:
   ```python
   # In phi_pipeline.py or constants.py
   l = 9.3e-9  # meters - adjust for velocity scale
   J = 10.6    # eV - adjust for energy scale
   ```

2. **Change frequency set**:
   ```python
   # Generate custom Fibonacci-harmonic set
   def generate_freqs(base=4.0, levels=6):
       phi = (1 + 5**0.5) / 2
       return [base * phi**(i/2) for i in range(levels)]
   ```

3. **Adjust coherence thresholds**:
   ```python
   # In analysis functions
   window_sec = 0.5      # Analysis window
   coherence_min = 0.5   # Minimum coherence
   skip_depth = 3        # Error correction depth
   ```

---

## Contributing Refinements

If you find improved parameter values or identify new constraints:

1. Document the change and justification
2. Provide validation data/analysis
3. Submit via pull request with evidence

**Contact**: Thomas.a.husmann@gmail.com

---

*© 2026 Thomas A. Husmann / iBuilt LTD. All rights reserved.*
*Licensed under CC BY-NC-SA 4.0 for academic and research use.*
