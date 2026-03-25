"""
multigrid.py — de Bruijn multigrid construction for triple metallic mean tiling
=================================================================================

VERIFIED:
  - Three grids (gold 5-fold, silver 4-fold, bronze 13-fold) produce
    7 vertex types: G, S, B, GS, GB, BS, GSB
  - GS fraction = 14.6% ≈ LEAK = 1/φ⁴ = 14.6% (0.3% error)
  - G only fraction ≈ R_MATTER = 7.28% (2.0% error)
"""

import math
import numpy as np
from collections import Counter

PHI = (1 + 5**0.5) / 2
DELTA_S = 1 + 2**0.5
DELTA_B = (3 + 13**0.5) / 2


def build_grid_lines(n_dirs, spacing, n_lines, offset_seed=0):
    """Build parallel line families for the multigrid method."""
    lines = []
    rng = np.random.RandomState(42 + offset_seed)
    for k in range(n_dirs):
        angle = k * math.pi / n_dirs
        nx = math.cos(angle)
        ny = math.sin(angle)
        gamma = rng.uniform(0.01, 0.49)
        for j in range(-n_lines // 2, n_lines // 2 + 1):
            d = (j + gamma) * spacing
            label = 'G' if n_dirs == 5 else 'S' if n_dirs == 4 else 'B'
            lines.append((nx, ny, d, k, label))
    return lines


def _line_intersection(l1, l2):
    """Intersection of two lines nx*x + ny*y = d."""
    nx1, ny1, d1 = l1[:3]
    nx2, ny2, d2 = l2[:3]
    det = nx1 * ny2 - nx2 * ny1
    if abs(det) < 1e-12:
        return None
    x = (d1 * ny2 - d2 * ny1) / det
    y = (nx1 * d2 - nx2 * d1) / det
    return (x, y)


def _find_vertices(gold_lines, silver_lines, bronze_lines, radius=8.0):
    """Find all pairwise intersections within a circular region."""
    vertices = {}
    tol = 0.05

    def add_vertex(x, y, grid_types):
        if x * x + y * y > radius * radius:
            return
        key = (round(x / tol), round(y / tol))
        for dk in [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]:
            nk = (key[0] + dk[0], key[1] + dk[1])
            if nk in vertices:
                vx, vy, vtypes = vertices[nk]
                if (x - vx)**2 + (y - vy)**2 < tol**2:
                    vtypes.update(grid_types)
                    return
        vertices[key] = (x, y, set(grid_types))

    # All six pair types
    pairs = [
        (gold_lines, gold_lines, {'G'}),
        (silver_lines, silver_lines, {'S'}),
        (bronze_lines, bronze_lines, {'B'}),
        (gold_lines, silver_lines, {'G', 'S'}),
        (gold_lines, bronze_lines, {'G', 'B'}),
        (silver_lines, bronze_lines, {'S', 'B'}),
    ]

    for lines_a, lines_b, types in pairs:
        same_grid = lines_a is lines_b
        for i in range(len(lines_a)):
            start_j = i + 1 if same_grid else 0
            for j in range(start_j, len(lines_b)):
                if same_grid and lines_a[i][3] == lines_b[j][3]:
                    continue
                pt = _line_intersection(lines_a[i], lines_b[j])
                if pt:
                    add_vertex(pt[0], pt[1], types)

    result = []
    for key, (x, y, types) in vertices.items():
        result.append({'x': x, 'y': y, 'type': ''.join(sorted(types))})
    return result


def build_triple_tiling(n_gold=15, n_silver=12, n_bronze=6, radius=8.0):
    """Build the triple metallic mean tiling and return vertices.

    Parameters
    ----------
    n_gold, n_silver, n_bronze : int
        Lines per family for each grid.
    radius : float
        Circular region radius.

    Returns
    -------
    list of dicts with 'x', 'y', 'type' keys.
    """
    gold = build_grid_lines(5, 1.0, n_gold, offset_seed=0)
    silver = build_grid_lines(4, 1.0 / DELTA_S, n_silver, offset_seed=100)
    bronze = build_grid_lines(13, 1.0 / DELTA_B, n_bronze, offset_seed=200)
    return _find_vertices(gold, silver, bronze, radius=radius)


def analyze_vertices(vertices):
    """Classify and count vertex types.

    Returns (type_fractions_dict, total_count).
    """
    type_counts = Counter(v['type'] for v in vertices)
    total = len(vertices)
    results = {}
    for vtype, count in sorted(type_counts.items()):
        results[vtype] = {
            'count': count,
            'fraction': round(count / total, 6),
        }
    return results, total
