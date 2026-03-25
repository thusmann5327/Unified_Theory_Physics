"""
Geometry — discriminant triangle, Cantor node, 3D quasicrystal Voronoi, bonds.

Modules:
    cantor_node  — The universal Cantor node structure at any scale
    discriminant — The (√5, √8, √13) Pythagorean triangle = E²=p²c²+m²c⁴
    voronoi_qc   — 3D icosahedral quasicrystal via cut-and-project + Voronoi
    qc_bonds     — Bond energies and molecular geometry from QC tiles
"""

from .cantor_node import cantor_node, bracket_address, zeckendorf
from .discriminant import discriminant_triangle, three_wave_frequencies
from .voronoi_qc import (
    build_quasicrystal, assign_types, voronoi_cell_faces,
    merge_coplanar_faces, analyze_bgs_geometry, icosahedral_axes,
)
from .qc_bonds import (
    classify_faces_orbital, bond_energy, predict_bond_energies,
    build_bgs_graph, find_tetrahedral_clusters, correlation_function,
    galaxy_correlation_prediction,
    E_BRACKET, THETA_LEAK, THETA_RC, THETA_BASE,
)
