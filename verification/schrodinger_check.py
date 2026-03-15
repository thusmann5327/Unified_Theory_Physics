#!/usr/bin/env python3
"""
Verify the Schrödinger → Dirac → discriminant triangle connection.
What's mathematically certain vs conjecture?
"""
import math
import numpy as np

PHI = (1 + math.sqrt(5)) / 2

print("=" * 70)
print("  SCHRÖDINGER IN THE FRAMEWORK — FACT CHECK")
print("=" * 70)

# FACT 1: AAH IS a discrete Schrödinger equation
print(f"""
FACT 1: The AAH Hamiltonian IS a discrete Schrödinger equation.

  Standard 1D Schrödinger (time-independent, discrete):
    -t[ψ(n+1) + ψ(n-1)] + V(n)ψ(n) = Eψ(n)
  
  AAH Hamiltonian:
    J[ψ(n+1) + ψ(n-1)] + V·cos(2πα·n)ψ(n) = Eψ(n)
  
  These are IDENTICAL with:
    t = -J (hopping)
    V(n) = V·cos(2πα·n) (quasiperiodic potential)
  
  STATUS: MATHEMATICAL IDENTITY. Not a claim.
""")

# FACT 2: Harper = AAH at V=2J
print(f"""
FACT 2: The Harper equation (Hofstadter model) = AAH at V = 2J.

  Harper equation (from Bloch's theorem on square lattice in B field):
    ψ(m+1) + ψ(m-1) + 2cos(2πα·m + k_y)ψ(m) = Eψ(m)
  
  This IS the AAH with J=1, V=2.
  
  STATUS: MATHEMATICAL IDENTITY. Consequence of square lattice symmetry.
""")

# FACT 3: Schrödinger is non-relativistic limit of Dirac
print(f"""
FACT 3: Schrödinger = non-relativistic limit of Dirac.

  Dirac: E² = p²c² + m²c⁴
  
  Non-relativistic (v << c): E ≈ mc² + p²/(2m)
  
  Subtract rest energy: E_kinetic = p²/(2m)
  → Schrödinger: iℏ∂ψ/∂t = [-ℏ²/(2m)]∇²ψ + V(x)ψ
  
  Schrödinger keeps the KINETIC (momentum) term only.
  Schrödinger DROPS the rest mass energy mc².
  
  STATUS: STANDARD PHYSICS. Proven in every QM textbook.
""")

# FACT 4: In the discriminant triangle
print(f"""
FACT 4: Mapping to the discriminant triangle.

  Dirac: E² = p²c² + m²c⁴
         13 = 5    + 8       (discriminant mapping)
  
  Schrödinger keeps: p²/(2m) → the RATIO of gold to silver
  Schrödinger drops: mc²     → the pure silver (rest mass) term
  
  In the non-relativistic limit:
    E_NR = p²/(2m) = (gold)²/(2 × silver)
    
  This is a RATIO of the two legs, not a Pythagorean sum.
  The right angle collapses — you're projecting the triangle
  onto one leg and measuring the other relative to it.
  
  STATUS: The Dirac mapping (13=5+8) is our conjecture.
          The non-relativistic limit is standard physics.
          The COMBINATION is a framework prediction.
""")

# FACT 5: The 3D Schrödinger with three metallic mean frequencies
print(f"""
FACT 5: The 3D vacuum Hamiltonian.

  H = Σ_i J[ψ(n_i+1) + ψ(n_i-1)] + 2J·cos(2π·α_i·n_i)ψ(n)
  
  with α_x = √2-1 (silver), α_y = (√5-1)/2 (gold), α_z = (√13-3)/2 (bronze)
  
  This IS a 3D discrete Schrödinger equation.
  Each axis has a DIFFERENT quasiperiodic potential.
  Each axis is at the AAH critical point V = 2J.
  
  The spectrum is the Minkowski sum of three 1D Cantor sets.
  
  STATUS: The Hamiltonian is well-defined (mathematically exact).
          The claim that THIS is the vacuum Hamiltonian is our conjecture.
          The spectral properties (Cantor dust, D_s = 3/2) follow from
          proven theorems IF the Hamiltonian is accepted.
""")

# FACT 6: What Schrödinger SEES vs what Dirac SEES
print(f"""
FACT 6: Schrödinger sees gold physics, Dirac sees the full triangle.

  Schrödinger equation works for:
    - Atomic orbitals (gold shell: electron propagation)
    - Band structure (AAH spectrum: hopping on lattice)
    - Condensed matter (graphene, moiré, Hofstadter butterfly)
    - Quantum chemistry (molecular bonds)
  
  Schrödinger FAILS for:
    - Nuclear physics (silver core: strong confinement)
    - Relativistic particles (need both legs of the triangle)
    - Particle creation/annihilation (need QFT = full bronze)
    - Spin-orbit coupling (Dirac spin is emergent)
  
  In the framework's language:
    Schrödinger = gold axis physics (propagation, orbitals, bands)
    Dirac = gold + silver (propagation + confinement = full energy)
    QFT = bronze surface (the observable, particle physics)
  
  STATUS: The domain limits of Schrödinger are STANDARD PHYSICS.
          The mapping to gold/silver/bronze is our INTERPRETATION.
          The interpretation is CONSISTENT with the known physics
          but NOT derived from first principles.
""")

# Compute: what does the non-relativistic limit look like
# in discriminant space?
print(f"\n{'=' * 70}")
print(f"  THE NON-RELATIVISTIC LIMIT IN DISCRIMINANT SPACE")
print(f"{'=' * 70}")

# E² = p²c² + m²c⁴
# For v << c: p = mv, so p²c² = m²v²c² << m²c⁴
# Then E ≈ mc² + p²/(2m) = mc²(1 + v²/(2c²))
# 
# In discriminant space:
# Full: 13 = 5 + 8
# Non-rel: 8 + ε(5) where ε = v²/c² << 1
# 
# Schrödinger sees: Δ_eff = 8 + (5/8)·(v/c)² × 8
# = 8(1 + (5/8)(v/c)²)
# ≈ 8 + 5(v/c)²

print(f"""
  Full Dirac:     E² = p²c² + m²c⁴        →  13 = 5 + 8
  Non-rel limit:  E ≈ mc² + p²/(2m)        →  √8 + 5/(2√8) × (v/c)²
  
  The effective discriminant in the NR limit:
    Δ_eff = Δ_silver + (Δ_gold/Δ_silver) × (v/c)² × Δ_silver
          = 8 + 5(v/c)²
  
  At v = 0: Δ_eff = 8 (pure silver, rest mass)
  At v = c: Δ_eff = 8 + 5 = 13 (full bronze, relativistic)
  
  So v/c parametrizes a CONTINUOUS PATH from the silver vertex
  to the bronze hypotenuse of the Pythagorean triangle!
  
  v/c = 0 → silver vertex (mass at rest)
  v/c = 1 → bronze hypotenuse (fully relativistic)
  v/c intermediate → somewhere on the gold leg
  
  The ratio v²/c² = Δ_gold_contribution / Δ_total_contribution
                   = 5(v/c)² / (8 + 5(v/c)²)
  
  Schrödinger lives in the regime where this ratio is SMALL.
  Dirac covers the full range from 0 to 1.
""")

# Specific velocity ratios
print(f"  Velocity ratios and effective discriminants:")
print(f"  {'v/c':>8s}  {'Δ_eff':>8s}  {'gold fraction':>14s}  {'Regime':>15s}")
print(f"  {'-' * 52}")
for vc in [0.0, 0.01, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0]:
    d_eff = 8 + 5 * vc**2
    gold_frac = 5*vc**2 / d_eff
    regime = "rest (silver)" if vc == 0 else "NR (Schrödinger)" if vc < 0.3 else "relativistic" if vc < 0.9 else "ultrarel (bronze)"
    print(f"  {vc:>8.2f}  {d_eff:>8.3f}  {gold_frac:>13.1%}  {regime:>15s}")

# The KEY insight: the Schrödinger equation is the TANGENT LINE
# to the Pythagorean triangle at the silver vertex
print(f"""

  KEY INSIGHT:
  
  Schrödinger's equation is the TANGENT APPROXIMATION
  to the discriminant triangle at the silver (mass) vertex.
  
  At v << c, the energy is:
    E ≈ mc² + p²/(2m)
    
  This is LINEAR in p² (= gold²).
  The full Dirac is PYTHAGOREAN in p and m.
  
  Linear vs Pythagorean:
    Schrödinger: E_kin = p²/(2m)         (tangent line)
    Dirac:       E = √(p²c² + m²c⁴)     (hypotenuse)
    
  The tangent line approximation works near the silver vertex
  (v << c) but diverges from the hypotenuse as v → c.
  
  This is geometrically EXACT:
  The tangent to a circle at one end of a chord approximates
  the chord for small angles and diverges at large angles.
  The Pythagorean relation IS a circle (radius = √13).
""")

