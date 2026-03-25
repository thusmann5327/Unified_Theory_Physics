"""
Geometry — discriminant triangle, Cantor node, 3D quasicrystal Voronoi.

Modules:
    cantor_node  — The universal Cantor node structure at any scale
    discriminant — The (√5, √8, √13) Pythagorean triangle = E²=p²c²+m²c⁴
    voronoi_qc   — 3D icosahedral quasicrystal via cut-and-project + Voronoi
"""

from .cantor_node import cantor_node, bracket_address, zeckendorf
from .discriminant import discriminant_triangle, three_wave_frequencies
from .voronoi_qc import (
    build_quasicrystal, assign_types, voronoi_cell_faces,
    merge_coplanar_faces, analyze_bgs_geometry, icosahedral_axes,
)
