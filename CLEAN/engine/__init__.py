"""
engine/ — Material property predictions from gate overflow
============================================================

The gate overflow G(Z) = (ratio_obs - ratio_pred) / ratio_pred
is the discrepancy between the Cantor node prediction and
observation. This discrepancy IS the prediction:

    G < 0 → compact cloud → hard material
    G > 0 → extended cloud → soft, metallic

One axiom: φ² = φ + 1. Zero free parameters.
"""

from .gate_overflow import gate_overflow, gate_overflow_all
