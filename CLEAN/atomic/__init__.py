"""
Atomic physics — predict vdW/cov ratios for all elements from first principles.

Modules:
    elements        — Element database (radii, symbols, electronegativity)
    aufbau          — Electron configurations with anomalous filling
    periodic_table  — Full Z=3-99 unified Pythagorean predictor
"""

from .aufbau import aufbau
from .periodic_table import predict_ratio, run_periodic_table
