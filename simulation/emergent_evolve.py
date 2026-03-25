"""
emergent_evolve.py — Emergent physics from matching rule strain
================================================================

No forces are coded. No gravity. No dark energy. No EM.
Only matching rule strain on a quasicrystal lattice.

Each vertex moves to minimize strain with its neighbors.
The stiffness hierarchy comes from the framework constants:

    BGS-BGS:  1.000     (baseline)        → "gravity + bonding"
    BGS-BS:   R_C       = 0.854           → "strong force"
    BS-BS:    R_C²      = 0.729           → "nuclear binding"
    BGS-GS:   LEAK     = 0.146           → "electromagnetic"
    BG-BG:    LEAK×R_C  = 0.125           → "weak force"
    BGS-BG:   LEAK²    = 0.021           → "gravity (long range)"
    G-G:      LEAK³    = 0.003           → "dark energy"

The forces of nature are stiffness levels of a quasicrystal.
The universe is a relaxing tiling.

Usage:
    python3 simulation/emergent_evolve.py [n_half] [n_steps]
"""

import numpy as np
from scipy.spatial import KDTree
import time
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ── Framework constants (from φ²=φ+1) ──────────────────────────
PHI = (1 + 5**0.5) / 2
W = 0.4671338922
LEAK = 1.0 / PHI**4          # 0.14590  — gate transmission
R_C = 1.0 - 1.0 / PHI**4     # 0.85410  — crossover parameter


# ── Stiffness hierarchy ────────────────────────────────────────
# Each junction type has a stiffness derived from framework constants.
# Symmetric: stiffness(A-B) = stiffness(B-A).
# Computed from the number of shared metallic means.

def _build_stiffness_table():
    """Build the junction stiffness lookup.

    The stiffness hierarchy maps to the four forces of nature:

      BS faces  → strong force    → stiffest  (R_C = 0.854)
      GS faces  → electromagnetic → medium    (LEAK = 0.146)
      BG faces  → gravity         → very weak (LEAK² = 0.021)
      vacuum    → dark energy     → tiny      (LEAK³ = 0.003)

    Each junction type's stiffness is determined by the PHYSICAL
    ROLE of the shared metallic means, not just the overlap count.

    BS = Bronze+Silver = inner confinement = strong force
    GS = Gold+Silver   = gate transmission = EM
    BG = Bronze+Gold   = outer conduit     = gravity
    """
    # Direct specification from framework physics
    table = {
        # Matter-matter: baseline
        ('BGS', 'BGS'): 1.0,

        # Matter-double: depends on which face mediates
        ('BGS', 'BS'):  R_C,           # strong force face
        ('BGS', 'GS'):  LEAK,          # EM gate face
        ('BG', 'BGS'):  LEAK**2,       # gravity conduit face

        # Matter-single: gate transmission
        ('BGS', 'G'):   0.0,           # vacuum — no direct force
        ('BGS', 'S'):   0.0,           # vacuum
        ('B', 'BGS'):   0.0,           # vacuum

        # Double-double: product of their roles
        ('BS', 'BS'):   R_C**2,        # strong-strong
        ('BS', 'GS'):   R_C * LEAK,    # strong-EM
        ('BG', 'BS'):   R_C * LEAK**2, # strong-gravity
        ('GS', 'GS'):   LEAK**2,       # EM-EM
        ('BG', 'GS'):   LEAK**3,       # EM-gravity
        ('BG', 'BG'):   LEAK**4,       # gravity-gravity

        # Double-single: weaker
        ('BS', 'S'):    LEAK**2,
        ('BS', 'G'):    0.0,
        ('B', 'BS'):    LEAK**2,
        ('GS', 'S'):    LEAK**2,
        ('G', 'GS'):    LEAK**2,
        ('B', 'GS'):    0.0,
        ('BG', 'G'):    LEAK**3,
        ('B', 'BG'):    LEAK**3,
        ('BG', 'S'):    0.0,

        # Single-single: vacuum self-interaction (dark energy)
        ('G', 'G'):     LEAK**3,
        ('S', 'S'):     LEAK**3,
        ('B', 'B'):     LEAK**3,
        ('G', 'S'):     0.0,
        ('B', 'G'):     0.0,
        ('B', 'S'):     0.0,
    }

    # Ensure symmetric keys
    normalized = {}
    for key, val in table.items():
        nkey = tuple(sorted(key))
        normalized[nkey] = val

    return normalized


STIFFNESS = _build_stiffness_table()


def get_stiffness(type1, type2):
    """Look up junction stiffness for two vertex types."""
    key = tuple(sorted([type1, type2]))
    return STIFFNESS.get(key, 0.0)


# ── Ideal geometry from initial tiling ──────────────────────────

def compute_ideals(positions, types, neighbor_pairs):
    """Compute ideal distances for each junction type from the initial tiling.

    The initial QC positions define the 'matching rules' — the
    geometry that minimizes strain. These are the target distances
    that drive the evolution.

    Returns dict mapping junction_key → ideal_distance.
    """
    from collections import defaultdict

    jdists = defaultdict(list)

    for i, j in neighbor_pairs:
        key = tuple(sorted([types[i], types[j]]))
        d = np.linalg.norm(positions[i] - positions[j])
        jdists[key].append(d)

    ideals = {}
    for key, dists in jdists.items():
        ideals[key] = float(np.mean(dists))

    # Also store the global mean spacing
    all_dists = []
    for dists in jdists.values():
        all_dists.extend(dists)
    ideals['_mean_spacing'] = float(np.mean(all_dists))

    return ideals


# ── Neighbor graph builder ──────────────────────────────────────

def build_neighbor_graph(positions, nn_multiplier=1.6):
    """Build neighbor adjacency from KDTree with adaptive threshold.

    Uses 1.6× mean nearest-neighbor distance as the neighbor cutoff.
    Returns list of (i, j) pairs and the threshold used.
    """
    tree = KDTree(positions)
    nn_dists = tree.query(positions, k=2)[0][:, 1]
    threshold = float(np.mean(nn_dists) * nn_multiplier)

    pairs = tree.query_pairs(threshold, output_type='ndarray')
    return pairs, threshold


# ── The evolution engine ────────────────────────────────────────

def evolve_emergent(positions, types, n_steps=5000, dt=None,
                    perturbation=0.02, damping=0.9985,
                    nn_multiplier=1.6, rebuild_every=100,
                    save_every=None, callback=None,
                    bracket=None):
    """Minimize total matching rule strain.

    No forces are coded. The gradient of strain energy with respect
    to each vertex position IS the force. Whatever physics emerges
    (gravity, EM, dark energy) is a consequence of the stiffness
    hierarchy, not of coded force laws.

    Parameters
    ----------
    positions : (N, 3) array — initial vertex positions from QC
    types : list of str — vertex type labels (BGS, BG, BS, GS, G, S, B)
    n_steps : int — number of relaxation steps
    dt : float — timestep (auto-calibrated if None)
    perturbation : float — initial perturbation amplitude (fraction of spacing)
    damping : float — velocity damping per step (expansion cooling)
    nn_multiplier : float — neighbor cutoff = this × mean NN distance
    rebuild_every : int — rebuild neighbor graph every N steps
    save_every : int — save frame every N steps (default: n_steps/200)
    callback : callable — called with (step, n_steps, metrics_dict)
    bracket : int or None — bracket level (94–294) for shape operator.
        If None, isotropic stiffness (no shape weighting).

    Returns
    -------
    dict with 'frames', 'steps', 'metrics', 'params', 'ideals'
    """
    N = len(positions)
    pos = positions.astype(np.float64).copy()
    pos -= pos.mean(axis=0)  # center

    # Build initial neighbor graph
    pairs_arr, threshold = build_neighbor_graph(pos, nn_multiplier)
    vtypes = list(types)

    # Compute ideal distances from the INITIAL tiling
    ideals = compute_ideals(pos, vtypes, pairs_arr)
    mean_spacing = ideals['_mean_spacing']

    # Auto-calibrate
    if dt is None:
        dt = 0.002 * mean_spacing
    if save_every is None:
        save_every = max(1, n_steps // 200)

    # Shape operator (bracket-dependent anisotropic stiffness)
    use_shape = bracket is not None
    if use_shape:
        from simulation.shape_operator import (
            bracket_stiffness_modifiers, detect_symmetry_axis, bracket_info
        )
        sym_axis = detect_symmetry_axis(pos, vtypes)
        shape_info = bracket_info(bracket)
        print(f"  Shape operator: bracket={bracket} ({shape_info['label']})")
        print(f"  disc/sphere ratio: {shape_info['disc_sphere_ratio']:.2f} → {shape_info['expected_shape']}")

    # Precompute stiffness for each pair
    pair_stiffness = np.zeros(len(pairs_arr), dtype=np.float64)
    pair_ideal_dist = np.zeros(len(pairs_arr), dtype=np.float64)
    for pi, (i, j) in enumerate(pairs_arr):
        key = tuple(sorted([vtypes[i], vtypes[j]]))
        pair_stiffness[pi] = get_stiffness(vtypes[i], vtypes[j])
        pair_ideal_dist[pi] = ideals.get(key, mean_spacing)

    # Apply bracket-dependent shape modifiers to stiffness
    if use_shape and len(pairs_arr) > 0:
        dr_init = pos[pairs_arr[:, 1]] - pos[pairs_arr[:, 0]]
        shape_mods = bracket_stiffness_modifiers(bracket, dr_init, sym_axis)
        pair_stiffness *= shape_mods

    # Small perturbation to break perfect QC symmetry
    rng = np.random.RandomState(42)
    pos += rng.normal(0, perturbation * mean_spacing, pos.shape)

    # Initial velocity = zero (or tiny thermal noise)
    vel = np.zeros((N, 3), dtype=np.float64)

    # Storage
    frames = [pos.copy()]
    steps_list = [0]
    metrics_list = [_compute_metrics(pos, vtypes, pairs_arr, pair_stiffness,
                                     pair_ideal_dist, mean_spacing)]

    t_start = time.time()

    for step in range(1, n_steps + 1):
        # Optionally rebuild neighbor graph (topology can change)
        if step % rebuild_every == 0 and step > 0:
            pairs_arr, threshold = build_neighbor_graph(pos, nn_multiplier)
            # Recompute stiffness/ideals for new pairs
            pair_stiffness = np.zeros(len(pairs_arr), dtype=np.float64)
            pair_ideal_dist = np.zeros(len(pairs_arr), dtype=np.float64)
            for pi, (i, j) in enumerate(pairs_arr):
                key = tuple(sorted([vtypes[i], vtypes[j]]))
                pair_stiffness[pi] = get_stiffness(vtypes[i], vtypes[j])
                pair_ideal_dist[pi] = ideals.get(key, mean_spacing)
            # Re-apply shape modifiers with updated positions
            if use_shape and len(pairs_arr) > 0:
                sym_axis = detect_symmetry_axis(pos, vtypes)
                dr_current = pos[pairs_arr[:, 1]] - pos[pairs_arr[:, 0]]
                shape_mods = bracket_stiffness_modifiers(bracket, dr_current, sym_axis)
                pair_stiffness *= shape_mods

        # ── Vectorized strain gradient computation ──────────────
        acc = np.zeros((N, 3), dtype=np.float64)

        if len(pairs_arr) > 0:
            ii = pairs_arr[:, 0]
            jj = pairs_arr[:, 1]

            dr = pos[jj] - pos[ii]                           # (M, 3)
            r2 = np.sum(dr * dr, axis=1)                     # (M,)
            r = np.sqrt(r2) + 1e-15                          # (M,)

            # Strain gradient: d/dr [(r - r_ideal)² / r_ideal²]
            #                = 2(r - r_ideal) / r_ideal²
            # Force = -stiffness × strain_gradient × direction
            delta = r - pair_ideal_dist                       # (M,)
            strain_grad = 2.0 * delta / (pair_ideal_dist**2)  # (M,)

            # Force magnitude (positive = push apart if too close)
            f_mag = -pair_stiffness * strain_grad / r         # (M,)

            # Vector force on each particle
            f_vec = f_mag[:, None] * dr                       # (M, 3)

            # Accumulate: i gets pulled toward j, j pushed from i
            np.add.at(acc, ii, f_vec)
            np.add.at(acc, jj, -f_vec)

        # Leapfrog integration
        vel += acc * dt
        vel *= damping
        pos += vel * dt

        # Save frame
        if step % save_every == 0:
            frames.append(pos.copy())
            steps_list.append(step)
            m = _compute_metrics(pos, vtypes, pairs_arr, pair_stiffness,
                                 pair_ideal_dist, mean_spacing)
            metrics_list.append(m)
            if callback:
                callback(step, n_steps, m)

        # Console progress
        if step % max(1, n_steps // 10) == 0:
            elapsed = time.time() - t_start
            m = _compute_metrics(pos, vtypes, pairs_arr, pair_stiffness,
                                 pair_ideal_dist, mean_spacing)
            print(f"  Step {step:5d}/{n_steps}: "
                  f"strain={m['total_strain']:.4f}  "
                  f"clustering={m['clustering']:.3f}  "
                  f"void_frac={m['void_fraction']:.3f}  "
                  f"max_cluster={m['max_cluster_frac']:.3f}  "
                  f"[{elapsed:.1f}s]")

    # Final frame
    if steps_list[-1] != n_steps:
        frames.append(pos.copy())
        steps_list.append(n_steps)
        metrics_list.append(_compute_metrics(pos, vtypes, pairs_arr,
                            pair_stiffness, pair_ideal_dist, mean_spacing))

    elapsed = time.time() - t_start
    final = metrics_list[-1]
    print(f"\n  Evolution complete: {n_steps} steps, {N} vertices, {elapsed:.1f}s")
    print(f"  Final strain:     {final['total_strain']:.4f}")
    print(f"  Final clustering: {final['clustering']:.3f}")
    print(f"  Final void frac:  {final['void_fraction']:.3f}")
    print(f"  Largest cluster:  {final['max_cluster_frac']*100:.1f}%")

    return {
        'frames': frames,
        'steps': steps_list,
        'metrics': metrics_list,
        'ideals': {str(k): v for k, v in ideals.items()},
        'params': {
            'N': N,
            'n_steps': n_steps,
            'dt': dt,
            'perturbation': perturbation,
            'damping': damping,
            'mean_spacing': mean_spacing,
            'n_pairs_initial': int(len(pairs_arr)),
            'stiffness_table': {str(k): v for k, v in STIFFNESS.items()
                                if v > 0},
            'bracket': bracket,
        },
    }


# ── Metrics ─────────────────────────────────────────────────────

def _compute_metrics(pos, vtypes, pairs, stiffness, ideal_dists, mean_spacing):
    """Compute physics metrics from current positions."""
    N = len(pos)

    # Total strain energy
    total_strain = 0.0
    if len(pairs) > 0:
        dr = pos[pairs[:, 1]] - pos[pairs[:, 0]]
        r = np.sqrt(np.sum(dr * dr, axis=1)) + 1e-15
        delta = r - ideal_dists
        strain_per_pair = stiffness * delta**2 / ideal_dists**2
        total_strain = float(np.sum(strain_per_pair))

    # BGS-only analysis (the "matter" distribution)
    bgs_mask = np.array([t == 'BGS' for t in vtypes])
    bgs_pos = pos[bgs_mask]
    n_bgs = len(bgs_pos)

    clustering = 0.0
    void_fraction = 0.0
    filament_frac = 0.0
    max_cluster_frac = 0.0
    mean_nn = mean_spacing
    bgs_strain = 0.0

    if n_bgs > 2:
        tree = KDTree(bgs_pos)
        nn_d = tree.query(bgs_pos, k=min(2, n_bgs))[0][:, -1]
        mean_nn = float(np.mean(nn_d))

        # Neighbor counts within 2× original mean spacing
        counts = tree.query_ball_point(bgs_pos, 2.0 * mean_spacing)
        n_nbrs = np.array([len(c) - 1 for c in counts])

        mean_nbrs = max(np.mean(n_nbrs), 0.01)
        clustering = float(np.std(n_nbrs) / mean_nbrs)
        void_fraction = float(np.mean(n_nbrs == 0))
        filament_frac = float(np.mean(n_nbrs == 2))

        # Largest connected BGS cluster
        max_cluster_frac = _largest_cluster_frac(tree, bgs_pos,
                                                  1.8 * mean_spacing)

    # BGS-BGS strain only
    if len(pairs) > 0:
        bgs_pair_mask = np.array([vtypes[pairs[p, 0]] == 'BGS' and
                                   vtypes[pairs[p, 1]] == 'BGS'
                                   for p in range(len(pairs))])
        if bgs_pair_mask.any():
            bgs_strain = float(np.sum(
                stiffness[bgs_pair_mask] *
                (np.sqrt(np.sum((pos[pairs[bgs_pair_mask, 1]] -
                                 pos[pairs[bgs_pair_mask, 0]])**2, axis=1)) -
                 ideal_dists[bgs_pair_mask])**2 /
                ideal_dists[bgs_pair_mask]**2))

    return {
        'total_strain': total_strain,
        'bgs_strain': bgs_strain,
        'clustering': clustering,
        'void_fraction': void_fraction,
        'filament_fraction': filament_frac,
        'max_cluster_frac': max_cluster_frac,
        'mean_nn_dist': mean_nn,
        'n_bgs': n_bgs,
    }


def _largest_cluster_frac(tree, pos, threshold):
    """Largest connected component fraction."""
    N = len(pos)
    if N < 2:
        return 1.0
    visited = np.zeros(N, dtype=bool)
    max_size = 0
    for start in range(N):
        if visited[start]:
            continue
        stack = [start]
        size = 0
        while stack:
            node = stack.pop()
            if visited[node]:
                continue
            visited[node] = True
            size += 1
            for nb in tree.query_ball_point(pos[node], threshold):
                if not visited[nb]:
                    stack.append(nb)
        max_size = max(max_size, size)
    return max_size / N


# ── Correlation measurement ─────────────────────────────────────

def measure_gamma(pos, n_bins=40):
    """Measure two-point correlation exponent γ of a point set."""
    from scipy.spatial.distance import pdist

    N = len(pos)
    if N < 10:
        return 0.0, [], []

    sample = pos[:min(N, 3000)]
    dists = pdist(sample)
    r_max = np.percentile(dists, 60)
    r_bins = np.linspace(0.05, r_max, n_bins + 1)
    r_centers = 0.5 * (r_bins[:-1] + r_bins[1:])
    dr = r_bins[1] - r_bins[0]

    counts = np.histogram(dists, bins=r_bins)[0]
    V_box = (2 * np.max(np.abs(sample)))**3
    n_s = len(sample)
    rho = n_s / V_box
    expected = 4 * np.pi * r_centers**2 * dr * rho * n_s / 2

    xi = np.where(expected > 0, counts / expected - 1, 0)

    valid = (xi > 0.01) & (r_centers > r_centers[3])
    gamma = 0.0
    if valid.sum() > 5:
        coeffs = np.polyfit(np.log10(r_centers[valid]),
                            np.log10(xi[valid]), 1)
        gamma = -coeffs[0]

    return float(gamma), r_centers.tolist(), xi.tolist()


# ── Load from database ──────────────────────────────────────────

def load_vertices(n_half):
    """Load all vertices and types for a given N_half from the database."""
    from database.universe_db import UniverseDB

    db = UniverseDB()
    with db.conn.cursor() as cur:
        cur.execute('''
            SELECT x, y, z, vertex_type
            FROM vertices WHERE n_half = %s
            ORDER BY id
        ''', (n_half,))
        rows = cur.fetchall()
    db.close()

    positions = np.array([(r[0], r[1], r[2]) for r in rows], dtype=np.float64)
    types = [r[3] for r in rows]
    return positions, types


# ── Command-line runner ─────────────────────────────────────────

if __name__ == '__main__':
    n_half = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    n_steps = int(sys.argv[2]) if len(sys.argv) > 2 else 3000

    print(f"\n  Emergent Physics — Matching Rule Strain Minimization")
    print(f"  ════════════════════════════════════════════════════")
    print(f"  N_half={n_half}, {n_steps} steps")
    print(f"  No coded forces. Only stiffness hierarchy:")
    print(f"    BGS-BGS: 1.000  |  BGS-BS: {R_C:.3f}  |  BGS-GS: {LEAK:.3f}")
    print(f"    BGS-BG: {LEAK**2:.4f}  |  G-G: {LEAK**3:.5f}")
    print()

    positions, types = load_vertices(n_half)
    print(f"  Loaded {len(positions)} vertices ({sum(1 for t in types if t=='BGS')} BGS)")
    print()

    result = evolve_emergent(positions, types, n_steps=n_steps)

    # Measure correlation on BGS vertices
    bgs_mask = np.array([t == 'BGS' for t in types])
    final_bgs = result['frames'][-1][bgs_mask]
    gamma, _, _ = measure_gamma(final_bgs)
    print(f"\n  BGS correlation exponent γ = {gamma:.3f}")
    print(f"  Framework prediction: γ = 1/σ₄ = 1.788")

    # Save
    import json
    out = {
        'n_half': n_half,
        'n_steps': n_steps,
        'n_vertices': len(positions),
        'n_bgs': int(bgs_mask.sum()),
        'final_gamma': gamma,
        'stiffness_table': {str(k): v for k, v in STIFFNESS.items() if v > 0},
        'final_metrics': result['metrics'][-1],
        'n_frames': len(result['frames']),
    }

    os.makedirs('results/simulation', exist_ok=True)
    outpath = f'results/simulation/emergent_{n_half}.json'
    with open(outpath, 'w') as f:
        json.dump(out, f, indent=2, default=str)
    print(f"  Saved to {outpath}\n")
