"""
particles/ — Standard Model predictions from the Cantor spectrum
================================================================

Three Cantor modes (leak, crossover, baseline) map to three
fermion generations. Mass ratios, mixing angles, and electroweak
boson masses all emerge from (φ, W, N, δ₇).

One axiom: φ² = φ + 1. Zero free parameters.
"""

from .generations import koide_formula, top_charm_ratio
from .electroweak import electroweak_predictions, weinberg_angle
