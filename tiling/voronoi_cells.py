"""
voronoi_cells.py — Voronoi Tessellation of the Triple Tiling
=============================================================

Let the tiling build its own tile shape via Voronoi tessellation.
Instead of constructing an arbitrary heptahedron, we let the
tiling geometry define the natural cell at each vertex.

Key questions:
  1. How many faces does each Voronoi cell have?
  2. Do different vertex types produce different cell shapes?
  3. What fraction of volume is at matter (BGS) vertices?
  4. Are the matter and vacuum networks connected?
  5. Does a characteristic shape emerge (7 faces? 12? 14?)

Run:  python3 tiling/voronoi_cells.py
"""

import sys, os, math, json
import numpy as np
from collections import Counter, defaultdict, OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEAN = os.path.join(ROOT, 'CLEAN')
sys.path.insert(0, CLEAN)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.constants import PHI, W, LEAK
from tiling import build_triple_tiling, analyze_vertices
from scipy.spatial import Voronoi, ConvexHull
from scipy.sparse.csgraph import connected_components
from scipy.sparse import lil_matrix


# ═════════════════════════════════════════════════════════════════
# 1. BUILD TILING & VORONOI
# ═════════════════════════════════════════════════════════════════

def build_voronoi_tiling(n_gold=15, n_silver=12, n_bronze=6, radius=8.0):
    """Build the triple tiling and compute its Voronoi tessellation.

    Returns the tiling vertices, their types, and the Voronoi object.
    """
    vertices = build_triple_tiling(n_gold, n_silver, n_bronze, radius)
    vf, total = analyze_vertices(vertices)

    # Extract vertex positions and types
    # vertices is a list of dicts with 'x', 'y', 'type' keys
    positions = []
    types = []
    for v in vertices:
        positions.append([v['x'], v['y']])
        types.append(v['type'])

    positions = np.array(positions)
    types = np.array(types)

    return positions, types, vf, total


def compute_voronoi_cells(positions, types, clip_radius=None):
    """Compute Voronoi tessellation and analyze each cell.

    Returns list of cell dicts with face count, area, perimeter, etc.
    Cells at the boundary (infinite) are excluded.
    """
    vor = Voronoi(positions)

    if clip_radius is None:
        # Use 80% of the max radius to avoid boundary effects
        clip_radius = 0.8 * np.max(np.linalg.norm(positions, axis=1))

    cells = []
    for i, region_idx in enumerate(vor.point_region):
        region = vor.regions[region_idx]

        # Skip cells with infinite vertices (-1)
        if -1 in region or len(region) < 3:
            continue

        # Skip cells near the boundary
        center = positions[i]
        if np.linalg.norm(center) > clip_radius:
            continue

        # Get cell vertices
        cell_verts = vor.vertices[region]

        # Number of edges/faces (in 2D: edges = vertices)
        n_edges = len(region)

        # Cell area (shoelace formula for 2D)
        # Order vertices by angle from centroid
        centroid = np.mean(cell_verts, axis=0)
        angles = np.arctan2(cell_verts[:, 1] - centroid[1],
                            cell_verts[:, 0] - centroid[0])
        order = np.argsort(angles)
        ordered = cell_verts[order]

        area = 0
        n = len(ordered)
        for j in range(n):
            x1, y1 = ordered[j]
            x2, y2 = ordered[(j + 1) % n]
            area += x1 * y2 - x2 * y1
        area = abs(area) / 2

        # Perimeter
        perimeter = 0
        edge_lengths = []
        for j in range(n):
            d = np.linalg.norm(ordered[(j + 1) % n] - ordered[j])
            perimeter += d
            edge_lengths.append(d)

        # Isoperimetric ratio: 4π·area / perimeter² (1 for circle)
        iso_ratio = 4 * math.pi * area / (perimeter**2) if perimeter > 0 else 0

        # Edge length statistics
        edge_arr = np.array(edge_lengths)

        cells.append({
            'index': i,
            'type': types[i],
            'center': center,
            'n_edges': n_edges,
            'area': area,
            'perimeter': perimeter,
            'iso_ratio': iso_ratio,
            'edge_mean': float(np.mean(edge_arr)),
            'edge_std': float(np.std(edge_arr)),
            'edge_min': float(np.min(edge_arr)),
            'edge_max': float(np.max(edge_arr)),
            'vertices': ordered,
            'region_idx': region_idx,
        })

    return cells, vor


# ═════════════════════════════════════════════════════════════════
# 2. CELL STATISTICS BY TYPE
# ═════════════════════════════════════════════════════════════════

def cell_statistics(cells):
    """Compute statistics of Voronoi cells grouped by vertex type."""
    TYPES = ['G', 'S', 'B', 'GS', 'BG', 'BS', 'BGS']
    stats = OrderedDict()

    for vtype in TYPES:
        type_cells = [c for c in cells if c['type'] == vtype]
        if not type_cells:
            stats[vtype] = None
            continue

        n_edges = [c['n_edges'] for c in type_cells]
        areas = [c['area'] for c in type_cells]
        isos = [c['iso_ratio'] for c in type_cells]

        n_arr = np.array(n_edges)
        a_arr = np.array(areas)
        iso_arr = np.array(isos)

        stats[vtype] = {
            'count': len(type_cells),
            'edges_mean': float(np.mean(n_arr)),
            'edges_median': float(np.median(n_arr)),
            'edges_mode': int(Counter(n_edges).most_common(1)[0][0]),
            'edges_min': int(np.min(n_arr)),
            'edges_max': int(np.max(n_arr)),
            'edges_std': float(np.std(n_arr)),
            'edges_histogram': dict(Counter(n_edges)),
            'area_mean': float(np.mean(a_arr)),
            'area_std': float(np.std(a_arr)),
            'area_total': float(np.sum(a_arr)),
            'iso_mean': float(np.mean(iso_arr)),
        }

    return stats


# ═════════════════════════════════════════════════════════════════
# 3. PACKING FRACTIONS (2D area analogue)
# ═════════════════════════════════════════════════════════════════

def packing_fractions(cells):
    """Compute area fractions for matter vs vacuum cells."""
    total_area = sum(c['area'] for c in cells)

    matter_types = {'BGS'}
    conduit_types = {'GS'}
    dark_types = {'BG', 'BS'}
    pure_types = {'G', 'S', 'B'}

    matter_area = sum(c['area'] for c in cells if c['type'] in matter_types)
    conduit_area = sum(c['area'] for c in cells if c['type'] in conduit_types)
    dark_area = sum(c['area'] for c in cells if c['type'] in dark_types)
    pure_area = sum(c['area'] for c in cells if c['type'] in pure_types)

    return {
        'total_area': total_area,
        'matter_BGS': matter_area / total_area,
        'conduit_GS': conduit_area / total_area,
        'dark_BG_BS': dark_area / total_area,
        'pure_G_S_B': pure_area / total_area,
        'matter_plus_conduit': (matter_area + conduit_area) / total_area,
        'comparisons': {
            'BGS vs W⁴': (matter_area / total_area, W**4,
                           abs(matter_area / total_area - W**4) / W**4 * 100),
            'BGS vs LEAK': (matter_area / total_area, LEAK,
                            abs(matter_area / total_area - LEAK) / LEAK * 100),
            'BGS+GS vs LEAK': ((matter_area + conduit_area) / total_area,
                                LEAK,
                                abs((matter_area + conduit_area) / total_area
                                    - LEAK) / LEAK * 100),
        }
    }


# ═════════════════════════════════════════════════════════════════
# 4. DUAL LATTICE CONNECTIVITY
# ═════════════════════════════════════════════════════════════════

def dual_lattice_analysis(cells, vor):
    """Analyze connectivity of matter vs vacuum cell networks.

    Set A (matter): BGS and GS cells
    Set B (vacuum): everything else

    Check if each set forms a connected network.
    """
    n = len(cells)
    cell_idx_map = {c['index']: i for i, c in enumerate(cells)}

    # Build adjacency from Voronoi ridge structure
    adj = lil_matrix((n, n), dtype=int)

    for ridge_points in vor.ridge_points:
        p1, p2 = ridge_points
        if p1 in cell_idx_map and p2 in cell_idx_map:
            i, j = cell_idx_map[p1], cell_idx_map[p2]
            adj[i, j] = 1
            adj[j, i] = 1

    # Set A: matter + conduit
    set_a_indices = [i for i, c in enumerate(cells)
                     if c['type'] in {'BGS', 'GS'}]
    # Set B: vacuum
    set_b_indices = [i for i, c in enumerate(cells)
                     if c['type'] not in {'BGS', 'GS'}]

    # Check connectivity of Set A
    if len(set_a_indices) > 0:
        a_adj = adj[np.ix_(set_a_indices, set_a_indices)]
        n_comp_a, _ = connected_components(a_adj, directed=False)
    else:
        n_comp_a = 0

    if len(set_b_indices) > 0:
        b_adj = adj[np.ix_(set_b_indices, set_b_indices)]
        n_comp_b, _ = connected_components(b_adj, directed=False)
    else:
        n_comp_b = 0

    # Boundary edges: ridges between Set A and Set B
    boundary_edges = 0
    total_edges = 0
    for ridge_points in vor.ridge_points:
        p1, p2 = ridge_points
        if p1 in cell_idx_map and p2 in cell_idx_map:
            i, j = cell_idx_map[p1], cell_idx_map[p2]
            total_edges += 1
            type_i = cells[i]['type']
            type_j = cells[j]['type']
            a_set = {'BGS', 'GS'}
            if (type_i in a_set) != (type_j in a_set):
                boundary_edges += 1

    return {
        'set_a_size': len(set_a_indices),
        'set_b_size': len(set_b_indices),
        'set_a_connected': n_comp_a == 1,
        'set_a_components': n_comp_a,
        'set_b_connected': n_comp_b == 1,
        'set_b_components': n_comp_b,
        'boundary_edges': boundary_edges,
        'total_edges': total_edges,
        'boundary_fraction': boundary_edges / max(1, total_edges),
    }


# ═════════════════════════════════════════════════════════════════
# 5. EDGE-COUNT ANALYSIS
# ═════════════════════════════════════════════════════════════════

def edge_count_physics(stats):
    """Analyze the edge counts for physical significance."""
    results = {}
    TYPES = ['G', 'S', 'B', 'GS', 'BG', 'BS', 'BGS']

    for vtype in TYPES:
        s = stats.get(vtype)
        if s is None:
            continue
        mode = s['edges_mode']
        mean = s['edges_mean']

        # Check Fibonacci
        fibs = [3, 5, 8, 13, 21]
        nearest_fib = min(fibs, key=lambda f: abs(mode - f))

        # Check metallic mean discriminants
        discriminants = {5: 'gold', 8: 'silver', 13: 'bronze'}

        results[vtype] = {
            'mode': mode,
            'mean': mean,
            'nearest_fibonacci': nearest_fib,
            'is_fibonacci': mode in fibs,
            'is_discriminant': mode in discriminants,
            'discriminant_name': discriminants.get(mode, None),
        }

    return results


# ═════════════════════════════════════════════════════════════════
# MAIN
# ═════════════════════════════════════════════════════════════════

def main():
    print()
    print("  ╔═══════════════════════════════════════════════════════════════╗")
    print("  ║  VORONOI TESSELLATION OF THE TRIPLE TILING                  ║")
    print("  ║  Let the tiling build its own tile shape.                   ║")
    print("  ╚═══════════════════════════════════════════════════════════════╝")

    # ── Build tiling ──
    print("\n  Building triple tiling...")
    positions, types, vf, total = build_voronoi_tiling()
    print(f"  {total} vertices, 7 types")
    print(f"  Position range: [{positions.min():.1f}, {positions.max():.1f}]")

    # ── Voronoi tessellation ──
    print(f"\n  Computing Voronoi tessellation...")
    cells, vor = compute_voronoi_cells(positions, types)
    print(f"  {len(cells)} interior cells (boundary cells excluded)")

    # ── Cell statistics by type ──
    print(f"\n{'='*70}")
    print("  VORONOI CELL STATISTICS BY VERTEX TYPE")
    print(f"{'='*70}")

    stats = cell_statistics(cells)

    print(f"\n  {'Type':<6} {'Count':>6} {'Edges':>6} {'Mode':>5} "
          f"{'Min':>4} {'Max':>4} {'Area μ':>8} {'Iso':>6}")
    print(f"  {'─'*6} {'─'*6} {'─'*6} {'─'*5} {'─'*4} {'─'*4} "
          f"{'─'*8} {'─'*6}")

    for vtype in ['G', 'S', 'B', 'GS', 'BG', 'BS', 'BGS']:
        s = stats.get(vtype)
        if s is None:
            print(f"  {vtype:<6} {'(none)':>6}")
            continue
        print(f"  {vtype:<6} {s['count']:>6} {s['edges_mean']:>6.1f} "
              f"{s['edges_mode']:>5} {s['edges_min']:>4} {s['edges_max']:>4} "
              f"{s['area_mean']:>8.4f} {s['iso_mean']:>6.3f}")

    # ── Edge count histograms ──
    print(f"\n{'='*70}")
    print("  EDGE COUNT DISTRIBUTIONS")
    print(f"{'='*70}")

    for vtype in ['G', 'S', 'B', 'GS', 'BG', 'BS', 'BGS']:
        s = stats.get(vtype)
        if s is None:
            continue
        hist = s['edges_histogram']
        total_count = s['count']
        print(f"\n  {vtype} ({total_count} cells):")
        for k in sorted(hist.keys()):
            pct = hist[k] / total_count * 100
            bar = '█' * int(pct * 0.5)
            print(f"    {k:>3} edges: {hist[k]:>4} ({pct:>5.1f}%) {bar}")

    # ── Global edge count ──
    all_edges = [c['n_edges'] for c in cells]
    global_hist = Counter(all_edges)
    global_mode = global_hist.most_common(1)[0][0]
    global_mean = np.mean(all_edges)

    print(f"\n{'='*70}")
    print("  GLOBAL EDGE COUNT")
    print(f"{'='*70}")
    print(f"\n  Mean: {global_mean:.2f}")
    print(f"  Mode: {global_mode}")
    print(f"  Distribution:")
    for k in sorted(global_hist.keys()):
        pct = global_hist[k] / len(cells) * 100
        bar = '█' * int(pct * 0.5)
        print(f"    {k:>3} edges: {global_hist[k]:>5} ({pct:>5.1f}%) {bar}")

    # ── Edge count physics ──
    print(f"\n{'='*70}")
    print("  EDGE COUNT PHYSICS CONNECTIONS")
    print(f"{'='*70}")

    physics = edge_count_physics(stats)
    for vtype, p in physics.items():
        fib_mark = ' ← FIBONACCI' if p['is_fibonacci'] else ''
        disc_mark = (f' ← {p["discriminant_name"]} DISCRIMINANT'
                     if p['is_discriminant'] else '')
        print(f"\n  {vtype}: mode = {p['mode']}, mean = {p['mean']:.2f}"
              f"{fib_mark}{disc_mark}")
        print(f"    Nearest Fibonacci: {p['nearest_fibonacci']}")

    # The key question
    bgs_stats = stats.get('BGS')
    if bgs_stats:
        bgs_mode = bgs_stats['edges_mode']
        print(f"\n  ★ BGS (matter) cells: mode = {bgs_mode} edges")
        if bgs_mode == 7:
            print(f"    The heptahedron emerges NATURALLY from the tiling!")
        elif bgs_mode == 13:
            print(f"    13 = F(7) = bronze discriminant!")
        else:
            print(f"    The universe tells us its own shape: {bgs_mode}-gon")

    # ── Packing fractions ──
    print(f"\n{'='*70}")
    print("  PACKING FRACTIONS (area analogue)")
    print(f"{'='*70}")

    packing = packing_fractions(cells)
    print(f"\n  Total area: {packing['total_area']:.2f}")
    print(f"\n  {'Subset':<25} {'Fraction':>10} {'Compare':>15} {'Error':>8}")
    print(f"  {'─'*25} {'─'*10} {'─'*15} {'─'*8}")
    print(f"  {'Matter (BGS)':<25} {packing['matter_BGS']:>10.4f}")
    print(f"  {'Conduit (GS)':<25} {packing['conduit_GS']:>10.4f}")
    print(f"  {'Dark (BG+BS)':<25} {packing['dark_BG_BS']:>10.4f}")
    print(f"  {'Pure (G+S+B)':<25} {packing['pure_G_S_B']:>10.4f}")
    print(f"  {'Matter+Conduit':<25} {packing['matter_plus_conduit']:>10.4f}")

    print(f"\n  Comparisons:")
    for name, (val, target, err) in packing['comparisons'].items():
        print(f"    {name}: {val:.4f} vs {target:.4f} ({err:.1f}%)")

    # ── Dual lattice ──
    print(f"\n{'='*70}")
    print("  DUAL LATTICE CONNECTIVITY")
    print(f"{'='*70}")

    dual = dual_lattice_analysis(cells, vor)
    print(f"\n  Set A (matter+conduit, BGS+GS): {dual['set_a_size']} cells")
    print(f"    Connected: {'YES' if dual['set_a_connected'] else 'NO'} "
          f"({dual['set_a_components']} components)")
    print(f"\n  Set B (vacuum, G+S+B+BG+BS):    {dual['set_b_size']} cells")
    print(f"    Connected: {'YES' if dual['set_b_connected'] else 'NO'} "
          f"({dual['set_b_components']} components)")
    print(f"\n  Boundary edges: {dual['boundary_edges']} / "
          f"{dual['total_edges']} ({dual['boundary_fraction']*100:.1f}%)")

    both_connected = dual['set_a_connected'] and dual['set_b_connected']
    if both_connected:
        print(f"\n  ★ BOTH networks percolate — true dual lattice!")
        print(f"    Matter and vacuum interpenetrate (tiling, not superposition)")

    # ── Save ──
    outdir = os.path.join(ROOT, 'results', 'voronoi')
    os.makedirs(outdir, exist_ok=True)

    results = {
        'n_vertices': total,
        'n_cells': len(cells),
        'global_edge_mean': global_mean,
        'global_edge_mode': global_mode,
        'cell_stats': {vtype: (stats[vtype] if stats[vtype]
                               else None) for vtype in stats},
        'packing': {k: v for k, v in packing.items()
                    if k != 'comparisons'},
        'packing_comparisons': {
            name: {'value': float(val), 'target': float(target),
                   'error_pct': float(err)}
            for name, (val, target, err) in packing['comparisons'].items()
        },
        'dual_lattice': dual,
        'edge_physics': physics,
    }

    # Remove non-serializable items from cell_stats
    for vtype in results['cell_stats']:
        s = results['cell_stats'][vtype]
        if s and 'edges_histogram' in s:
            s['edges_histogram'] = {str(k): v
                                     for k, v in s['edges_histogram'].items()}

    with open(os.path.join(outdir, 'voronoi_results.json'), 'w') as f:
        json.dump(results, f, indent=2, default=str)

    # Text report
    with open(os.path.join(outdir, 'voronoi_report.txt'), 'w') as f:
        f.write("VORONOI TESSELLATION OF THE TRIPLE TILING\n")
        f.write("=" * 50 + "\n\n")

        f.write(f"Vertices: {total}, Interior cells: {len(cells)}\n")
        f.write(f"Global edge count: mean={global_mean:.2f}, "
                f"mode={global_mode}\n\n")

        f.write("Cell statistics by vertex type:\n")
        for vtype in ['G', 'S', 'B', 'GS', 'BG', 'BS', 'BGS']:
            s = stats.get(vtype)
            if s is None:
                continue
            f.write(f"  {vtype:<6} count={s['count']:>4}, "
                    f"edges: mode={s['edges_mode']}, "
                    f"mean={s['edges_mean']:.1f}, "
                    f"area={s['area_mean']:.4f}\n")

        f.write(f"\nPacking fractions:\n")
        f.write(f"  Matter (BGS):     {packing['matter_BGS']:.4f}\n")
        f.write(f"  Conduit (GS):     {packing['conduit_GS']:.4f}\n")
        f.write(f"  Dark (BG+BS):     {packing['dark_BG_BS']:.4f}\n")
        f.write(f"  Pure (G+S+B):     {packing['pure_G_S_B']:.4f}\n")

        f.write(f"\nDual lattice:\n")
        f.write(f"  Matter network: "
                f"{'connected' if dual['set_a_connected'] else 'fragmented'} "
                f"({dual['set_a_components']} comp)\n")
        f.write(f"  Vacuum network: "
                f"{'connected' if dual['set_b_connected'] else 'fragmented'} "
                f"({dual['set_b_components']} comp)\n")
        f.write(f"  Boundary: {dual['boundary_fraction']*100:.1f}% of edges\n")

        if bgs_stats:
            f.write(f"\nBGS (matter) Voronoi cell: mode = "
                    f"{bgs_stats['edges_mode']} edges\n")

    print(f"\n  Results saved to: {outdir}/")

    # ── Final verdict ──
    print(f"\n{'='*70}")
    print("  VERDICT")
    print(f"{'='*70}")
    if bgs_stats:
        m = bgs_stats['edges_mode']
        print(f"\n  The tiling builds its own tile shape:")
        print(f"  BGS (matter) cells have {m} edges (2D analogue of faces)")
        if m == 7:
            print(f"  → HEPTAHEDRON confirmed by Voronoi!")
        elif m == 5:
            print(f"  → PENTAGON: golden ratio geometry!")
        elif m == 6:
            print(f"  → HEXAGON: close-packed!")

    print(f"\n  Overall: most cells have {global_mode} edges "
          f"(mean {global_mean:.1f})")

    fibs = [3, 5, 8, 13]
    if global_mode in fibs:
        print(f"  → {global_mode} is FIBONACCI!")

    print()


if __name__ == '__main__':
    main()
