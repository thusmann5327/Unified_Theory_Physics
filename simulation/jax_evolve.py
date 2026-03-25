"""
jax_evolve.py — JAX/Metal GPU-accelerated emergent evolution
=============================================================

Ports the strain-minimization engine to JAX for Apple M4 GPU.
Handles 240K+ vertices at interactive speed.

No forces coded. The stiffness hierarchy IS the force hierarchy.
Shape emerges from bracket-dependent anisotropic stiffness.

Usage:
    python3 simulation/jax_evolve.py [n_half] [n_steps] [bracket]
    # Default: n_half=6, n_steps=5000, bracket=230 (galaxy)

Requires: jax, jax-metal
"""

import sys
import os
import time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ── JAX setup ────────────────────────────────────────────────────
try:
    import jax
    import jax.numpy as jnp
    from jax import jit, vmap
    JAX_OK = True
    _dev = jax.devices()[0]
    print(f"  JAX {jax.__version__} on {_dev.platform.upper()}")
    if _dev.platform == 'cpu':
        print("  WARNING: Running on CPU. For GPU: pip install jax-metal")
except ImportError:
    JAX_OK = False
    print("  JAX not available — falling back to NumPy")

# ── Framework constants ──────────────────────────────────────────
PHI = (1 + 5**0.5) / 2
W = 0.4671338922
LEAK = 1.0 / PHI**4
R_C = 1.0 - 1.0 / PHI**4

# ── Stiffness table (7 vertex types → 28 unique pairs) ──────────

def _build_stiffness_lookup():
    """Build stiffness as a 7×7 matrix indexed by type ID.

    Type IDs: B=0, BG=1, BGS=2, BS=3, G=4, GS=5, S=6
    """
    TYPE_ORDER = ['B', 'BG', 'BGS', 'BS', 'G', 'GS', 'S']
    TYPE_TO_ID = {t: i for i, t in enumerate(TYPE_ORDER)}

    table = {
        ('BGS', 'BGS'): 1.0,
        ('BGS', 'BS'):  R_C,
        ('BGS', 'GS'):  LEAK,
        ('BG', 'BGS'):  LEAK**2,
        ('BGS', 'G'):   0.0,
        ('BGS', 'S'):   0.0,
        ('B', 'BGS'):   0.0,
        ('BS', 'BS'):   R_C**2,
        ('BS', 'GS'):   R_C * LEAK,
        ('BG', 'BS'):   R_C * LEAK**2,
        ('GS', 'GS'):   LEAK**2,
        ('BG', 'GS'):   LEAK**3,
        ('BG', 'BG'):   LEAK**4,
        ('BS', 'S'):    LEAK**2,
        ('BS', 'G'):    0.0,
        ('B', 'BS'):    LEAK**2,
        ('GS', 'S'):    LEAK**2,
        ('G', 'GS'):    LEAK**2,
        ('B', 'GS'):    0.0,
        ('BG', 'G'):    LEAK**3,
        ('B', 'BG'):    LEAK**3,
        ('BG', 'S'):    0.0,
        ('G', 'G'):     LEAK**3,
        ('S', 'S'):     LEAK**3,
        ('B', 'B'):     LEAK**3,
        ('G', 'S'):     0.0,
        ('B', 'G'):     0.0,
        ('B', 'S'):     0.0,
    }

    mat = np.zeros((7, 7), dtype=np.float32)
    for (t1, t2), v in table.items():
        i, j = TYPE_TO_ID[t1], TYPE_TO_ID[t2]
        mat[i, j] = v
        mat[j, i] = v

    return mat, TYPE_TO_ID, TYPE_ORDER

STIFFNESS_MATRIX, TYPE_TO_ID, TYPE_ORDER = _build_stiffness_lookup()


def types_to_ids(types):
    """Convert type strings to integer IDs."""
    return np.array([TYPE_TO_ID[t] for t in types], dtype=np.int32)


# ── Shape operator (bracket-dependent) ───────────────────────────

def compute_shape_modifiers_np(bracket, dr_vectors, sym_axis=None):
    """Compute per-bond stiffness multipliers from bracket + direction.
    NumPy version for setup; JAX version used in loop.
    """
    if bracket is None:
        return np.ones(len(dr_vectors), dtype=np.float32)

    if sym_axis is None:
        sym_axis = np.array([0, 0, 1], dtype=np.float64)
    sym_axis = sym_axis / (np.linalg.norm(sym_axis) + 1e-15)

    b_offset = (bracket - 119) / 50.0
    fw_s = PHI ** (-5.0 * b_offset)
    fw_d = PHI ** (+4.0 * b_offset)
    fw_p = PHI ** (-1.5 * b_offset)
    fw_f = PHI ** (+1.0 * b_offset)

    r = np.sqrt(np.sum(dr_vectors**2, axis=1, keepdims=True)) + 1e-15
    dr_hat = dr_vectors / r
    cos_theta = np.abs(dr_hat @ sym_axis)
    sin_theta = np.sqrt(np.maximum(1 - cos_theta**2, 0) + 1e-15)

    s_frac = cos_theta**2
    d_frac = sin_theta**2
    cross = 2.0 * cos_theta * sin_theta
    p_frac = cross * 0.6
    f_frac = cross * 0.4
    total = s_frac + d_frac + p_frac + f_frac + 1e-15

    raw = (s_frac * fw_s + d_frac * fw_d +
           p_frac * fw_p + f_frac * fw_f) / total

    # Normalize: preserve mean stiffness, only redistribute anisotropy
    mean_mod = np.mean(raw)
    if mean_mod > 1e-10:
        raw /= mean_mod

    return raw.astype(np.float32)


# ── Neighbor graph ───────────────────────────────────────────────

def build_neighbor_pairs(positions, nn_multiplier=1.6):
    """Build neighbor pairs using KDTree. Returns (pairs, threshold)."""
    from scipy.spatial import KDTree
    tree = KDTree(positions)
    nn_dists = tree.query(positions, k=2)[0][:, 1]
    threshold = float(np.mean(nn_dists) * nn_multiplier)
    pairs = tree.query_pairs(threshold, output_type='ndarray')
    return pairs, threshold


def compute_ideal_dists(positions, types, pairs):
    """Compute junction-type ideal distances from initial QC tiling."""
    from collections import defaultdict
    jdists = defaultdict(list)
    for i, j in pairs:
        key = tuple(sorted([types[i], types[j]]))
        d = np.linalg.norm(positions[i] - positions[j])
        jdists[key].append(d)
    ideals = {}
    for key, dists in jdists.items():
        ideals[key] = float(np.mean(dists))
    all_d = [d for ds in jdists.values() for d in ds]
    ideals['_mean'] = float(np.mean(all_d))
    return ideals


# ── JAX evolution kernel ─────────────────────────────────────────

def _make_jax_step(N, M):
    """Create JIT-compiled evolution step function.

    Closure over N (vertices) and M (pairs) for static shapes.
    """

    @jit
    def step_fn(pos, vel, ii, jj, pair_stiffness, pair_ideal, dt, damping):
        """One leapfrog step of strain minimization."""
        dr = pos[jj] - pos[ii]                               # (M, 3)
        r2 = jnp.sum(dr * dr, axis=1)                        # (M,)
        r = jnp.sqrt(r2) + 1e-10                             # (M,)

        delta = r - pair_ideal                                # (M,)
        strain_grad = 2.0 * delta / (pair_ideal**2)           # (M,)
        f_mag = -pair_stiffness * strain_grad / r             # (M,)
        f_vec = f_mag[:, None] * dr                           # (M, 3)

        # Scatter-add forces (JAX segment_sum)
        acc = jnp.zeros((N, 3), dtype=jnp.float32)
        acc = acc.at[ii].add(f_vec)
        acc = acc.at[jj].add(-f_vec)

        vel_new = (vel + acc * dt) * damping
        pos_new = pos + vel_new * dt

        # Strain metric
        total_strain = jnp.sum(pair_stiffness * delta**2 / pair_ideal**2)

        return pos_new, vel_new, total_strain

    return step_fn


def _make_numpy_step():
    """NumPy fallback step function."""

    def step_fn(pos, vel, ii, jj, pair_stiffness, pair_ideal, dt, damping):
        N = len(pos)
        dr = pos[jj] - pos[ii]
        r = np.sqrt(np.sum(dr * dr, axis=1)) + 1e-10
        delta = r - pair_ideal
        strain_grad = 2.0 * delta / (pair_ideal**2)
        f_mag = -pair_stiffness * strain_grad / r
        f_vec = f_mag[:, None] * dr

        acc = np.zeros((N, 3), dtype=np.float64)
        np.add.at(acc, ii, f_vec)
        np.add.at(acc, jj, -f_vec)

        vel_new = (vel + acc * dt) * damping
        pos_new = pos + vel_new * dt
        total_strain = float(np.sum(pair_stiffness * delta**2 / pair_ideal**2))
        return pos_new, vel_new, total_strain

    return step_fn


# ── Main evolution function ──────────────────────────────────────

def evolve_jax(positions, types, n_steps=5000, bracket=None,
               perturbation=0.02, damping=0.9985, nn_multiplier=1.6,
               rebuild_every=200, save_every=None, callback=None):
    """JAX-accelerated emergent strain minimization.

    Parameters
    ----------
    positions : (N, 3) array
    types : list of str
    n_steps : int
    bracket : int or None — shape operator bracket (94–294)
    perturbation : float — initial symmetry breaking
    damping : float — velocity damping per step
    callback : callable(step, total, metrics)

    Returns dict with frames, steps, metrics, params
    """
    N = len(positions)
    pos = positions.astype(np.float64).copy()
    pos -= pos.mean(axis=0)

    # Build neighbor graph
    pairs, threshold = build_neighbor_pairs(pos, nn_multiplier)
    M = len(pairs)
    print(f"  Vertices: {N:,}  Pairs: {M:,}  Threshold: {threshold:.4f}")

    # Compute ideal distances
    ideals = compute_ideal_dists(pos, types, pairs)
    mean_spacing = ideals['_mean']

    # Auto-calibrate
    dt = 0.002 * mean_spacing
    if save_every is None:
        save_every = max(1, n_steps // 200)

    # Pair arrays
    ii = pairs[:, 0]
    jj = pairs[:, 1]

    type_ids = types_to_ids(types)
    pair_stiffness = np.array([STIFFNESS_MATRIX[type_ids[i], type_ids[j]]
                               for i, j in pairs], dtype=np.float32)
    pair_ideal = np.array([ideals.get(tuple(sorted([types[i], types[j]])), mean_spacing)
                           for i, j in pairs], dtype=np.float32)

    # Shape operator
    if bracket is not None:
        from simulation.shape_operator import detect_symmetry_axis, bracket_info
        sym_axis = detect_symmetry_axis(pos, types)
        info = bracket_info(bracket)
        print(f"  Shape: bracket={bracket} ({info['label']}) "
              f"disc/sphere={info['disc_sphere_ratio']:.2f} → {info['expected_shape']}")
        dr_init = pos[jj] - pos[ii]
        shape_mods = compute_shape_modifiers_np(bracket, dr_init, sym_axis)
        pair_stiffness *= shape_mods

    # Perturbation
    rng = np.random.RandomState(42)
    pos += rng.normal(0, perturbation * mean_spacing, pos.shape)

    # Convert to JAX or keep NumPy
    use_jax = JAX_OK
    if use_jax:
        pos_j = jnp.array(pos, dtype=jnp.float32)
        vel_j = jnp.zeros((N, 3), dtype=jnp.float32)
        ii_j = jnp.array(ii, dtype=jnp.int32)
        jj_j = jnp.array(jj, dtype=jnp.int32)
        stiff_j = jnp.array(pair_stiffness, dtype=jnp.float32)
        ideal_j = jnp.array(pair_ideal, dtype=jnp.float32)

        step_fn = _make_jax_step(N, M)

        # Warm-up JIT
        print("  JIT compiling...")
        t0 = time.time()
        pos_j, vel_j, _ = step_fn(pos_j, vel_j, ii_j, jj_j, stiff_j, ideal_j,
                                   jnp.float32(dt), jnp.float32(damping))
        pos_j.block_until_ready()
        print(f"  JIT compiled in {time.time()-t0:.1f}s")
    else:
        vel = np.zeros((N, 3), dtype=np.float64)
        step_fn = _make_numpy_step()

    # Storage
    frames = [np.array(pos_j if use_jax else pos).copy()]
    steps_list = [0]
    strain_list = [0.0]

    t_start = time.time()

    for step in range(1, n_steps + 1):
        # Rebuild neighbors periodically
        if step % rebuild_every == 0:
            current_pos = np.array(pos_j if use_jax else pos)
            pairs, threshold = build_neighbor_pairs(current_pos, nn_multiplier)
            M = len(pairs)
            ii = pairs[:, 0]
            jj = pairs[:, 1]

            pair_stiffness = np.array([STIFFNESS_MATRIX[type_ids[i], type_ids[j]]
                                       for i, j in pairs], dtype=np.float32)
            pair_ideal = np.array([ideals.get(tuple(sorted([types[i], types[j]])),
                                  mean_spacing) for i, j in pairs], dtype=np.float32)

            if bracket is not None:
                sym_axis = detect_symmetry_axis(current_pos, types)
                dr_cur = current_pos[jj] - current_pos[ii]
                shape_mods = compute_shape_modifiers_np(bracket, dr_cur, sym_axis)
                pair_stiffness *= shape_mods

            if use_jax:
                ii_j = jnp.array(ii, dtype=jnp.int32)
                jj_j = jnp.array(jj, dtype=jnp.int32)
                stiff_j = jnp.array(pair_stiffness, dtype=jnp.float32)
                ideal_j = jnp.array(pair_ideal, dtype=jnp.float32)
                step_fn = _make_jax_step(N, M)
                # Re-JIT for new pair count
                pos_j, vel_j, _ = step_fn(pos_j, vel_j, ii_j, jj_j, stiff_j, ideal_j,
                                           jnp.float32(dt), jnp.float32(damping))
                pos_j.block_until_ready()

        # Step
        if use_jax:
            pos_j, vel_j, strain = step_fn(pos_j, vel_j, ii_j, jj_j, stiff_j, ideal_j,
                                            jnp.float32(dt), jnp.float32(damping))
        else:
            pos, vel, strain = step_fn(pos, vel, ii, jj, pair_stiffness, pair_ideal,
                                        dt, damping)

        # Save frame
        if step % save_every == 0:
            if use_jax:
                frame_np = np.array(pos_j)
                strain_val = float(strain)
            else:
                frame_np = pos.copy()
                strain_val = float(strain)

            frames.append(frame_np)
            steps_list.append(step)
            strain_list.append(strain_val)

            if callback:
                callback(step, n_steps, {'total_strain': strain_val})

        # Progress
        if step % max(1, n_steps // 10) == 0:
            elapsed = time.time() - t_start
            s_val = float(strain) if use_jax else float(strain)
            print(f"  Step {step:5d}/{n_steps}: strain={s_val:.4f}  [{elapsed:.1f}s]")

    # Final frame
    if steps_list[-1] != n_steps:
        if use_jax:
            frames.append(np.array(pos_j))
        else:
            frames.append(pos.copy())
        steps_list.append(n_steps)
        strain_list.append(float(strain))

    elapsed = time.time() - t_start
    print(f"\n  Evolution: {n_steps} steps, {N:,} vertices, {elapsed:.1f}s")
    print(f"  Rate: {n_steps * N / elapsed / 1e6:.1f}M vertex-steps/s")
    print(f"  Final strain: {strain_list[-1]:.4f}")

    return {
        'frames': frames,
        'steps': steps_list,
        'strain': strain_list,
        'types': types,
        'type_ids': type_ids.tolist(),
        'params': {
            'N': N,
            'n_steps': n_steps,
            'bracket': bracket,
            'dt': dt,
            'damping': damping,
            'mean_spacing': mean_spacing,
            'jax': use_jax,
            'device': str(_dev) if use_jax else 'cpu',
        },
    }


# ── Galaxy finder (friends-of-friends) ───────────────────────────

def find_galaxies(positions, types, linking_length=None, min_members=5,
                  linking_multiplier=1.8):
    """Friends-of-friends clustering on BGS (matter) vertices.

    Uses a wider linking length (1.8× mean NN) to find galaxy-scale
    overdensities. The QC tiling creates natural density fluctuations;
    FOF finds connected overdense regions.

    Returns list of galaxy dicts with center, size, members, shape info.
    """
    from scipy.spatial import KDTree

    bgs_mask = np.array([t == 'BGS' for t in types])
    bgs_pos = positions[bgs_mask]
    bgs_idx = np.where(bgs_mask)[0]
    N_bgs = len(bgs_pos)

    if N_bgs < min_members:
        return []

    tree = KDTree(bgs_pos)
    nn_dists = tree.query(bgs_pos, k=2)[0][:, 1]
    if linking_length is None:
        linking_length = float(np.mean(nn_dists) * linking_multiplier)

    # Union-Find FOF
    parent = list(range(N_bgs))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    pairs = tree.query_pairs(linking_length, output_type='ndarray')
    for i, j in pairs:
        union(i, j)

    # Collect groups
    from collections import defaultdict
    groups = defaultdict(list)
    for i in range(N_bgs):
        groups[find(i)].append(i)

    galaxies = []
    for root, members in groups.items():
        if len(members) < min_members:
            continue
        member_pos = bgs_pos[members]
        center = member_pos.mean(axis=0)
        spread = np.std(np.linalg.norm(member_pos - center, axis=1))

        # Shape: eigenvalues of inertia tensor → oblate/prolate/spherical
        centered = member_pos - center
        cov = np.cov(centered.T)
        eigvals = np.sort(np.linalg.eigvalsh(cov))[::-1]  # largest first
        # Axis ratios
        if eigvals[0] > 1e-10:
            b_a = np.sqrt(eigvals[1] / eigvals[0])  # intermediate/major
            c_a = np.sqrt(eigvals[2] / eigvals[0])  # minor/major
        else:
            b_a, c_a = 1.0, 1.0

        if c_a < 0.3 and b_a > 0.6:
            shape = 'disc'
        elif c_a < 0.3 and b_a < 0.4:
            shape = 'filament'
        elif c_a > 0.7:
            shape = 'sphere'
        else:
            shape = 'oblate'

        galaxies.append({
            'center': center.tolist(),
            'n_members': len(members),
            'radius': float(spread),
            'member_indices': [int(bgs_idx[m]) for m in members],
            'shape': shape,
            'axis_ratios': [float(b_a), float(c_a)],
            'eigvals': eigvals.tolist(),
        })

    # Sort by size
    galaxies.sort(key=lambda g: g['n_members'], reverse=True)

    print(f"\n  Galaxy finder: {len(galaxies)} structures found")
    print(f"  Linking length: {linking_length:.4f}")
    for i, g in enumerate(galaxies[:10]):
        print(f"    #{i+1}: {g['n_members']:4d} members, "
              f"R={g['radius']:.3f}, shape={g['shape']}, "
              f"b/a={g['axis_ratios'][0]:.2f} c/a={g['axis_ratios'][1]:.2f}")

    return galaxies


def find_structures_multiscale(positions, types, n_scales=4, min_members=3):
    """Multi-scale structure finder using density-based clustering.

    Runs FOF at multiple linking lengths to find structures from
    tight clusters (galaxies) to loose filaments (cosmic web).
    Also computes local density for each BGS vertex.

    Returns dict with galaxies at each scale + density per vertex.
    """
    from scipy.spatial import KDTree

    bgs_mask = np.array([t == 'BGS' for t in types])
    bgs_pos = positions[bgs_mask]
    bgs_idx = np.where(bgs_mask)[0]
    N_bgs = len(bgs_pos)

    if N_bgs < 10:
        return {'scales': [], 'density': [], 'bgs_positions': bgs_pos.tolist()}

    tree = KDTree(bgs_pos)
    nn_dists = tree.query(bgs_pos, k=2)[0][:, 1]
    mean_nn = float(np.mean(nn_dists))

    # Local density: number of BGS neighbors within 3× mean NN
    density_radius = mean_nn * 3.0
    neighbor_counts = tree.query_ball_point(bgs_pos, density_radius)
    local_density = np.array([len(c) - 1 for c in neighbor_counts], dtype=np.float32)

    # Normalize to overdensity: δ = (ρ - ρ_mean) / ρ_mean
    mean_density = np.mean(local_density)
    if mean_density > 0:
        overdensity = (local_density - mean_density) / mean_density
    else:
        overdensity = np.zeros_like(local_density)

    # Multi-scale FOF
    linking_multipliers = [1.2, 1.8, 2.5, 3.5][:n_scales]
    scale_names = ['cluster', 'galaxy', 'group', 'filament'][:n_scales]

    scales = []
    for mult, name in zip(linking_multipliers, scale_names):
        gals = find_galaxies(positions, types, linking_multiplier=mult,
                             min_members=min_members)
        scales.append({
            'name': name,
            'linking_multiplier': mult,
            'linking_length': mean_nn * mult,
            'n_structures': len(gals),
            'structures': gals,
        })

    print(f"\n  Multi-scale structure summary:")
    print(f"  Mean NN distance: {mean_nn:.4f}")
    print(f"  Overdensity range: [{overdensity.min():.2f}, {overdensity.max():.2f}]")
    for sc in scales:
        print(f"    {sc['name']:10s}: {sc['n_structures']:3d} structures "
              f"(link={sc['linking_length']:.4f})")

    return {
        'scales': scales,
        'density': local_density.tolist(),
        'overdensity': overdensity.tolist(),
        'bgs_positions': bgs_pos.tolist(),
        'bgs_indices': bgs_idx.tolist(),
        'mean_nn': mean_nn,
    }


# ── Density field ────────────────────────────────────────────────

def compute_density_field(positions, types, grid_res=32):
    """Compute 3D density field of BGS vertices on a regular grid.

    Returns (density_3d, grid_edges, bgs_positions).
    """
    bgs_mask = np.array([t == 'BGS' for t in types])
    bgs_pos = positions[bgs_mask]

    if len(bgs_pos) < 10:
        return None, None, bgs_pos

    mins = bgs_pos.min(axis=0) - 0.5
    maxs = bgs_pos.max(axis=0) + 0.5

    density, edges = np.histogramdd(
        bgs_pos, bins=grid_res,
        range=[(mins[0], maxs[0]), (mins[1], maxs[1]), (mins[2], maxs[2])]
    )

    # Gaussian smooth
    from scipy.ndimage import gaussian_filter
    density = gaussian_filter(density, sigma=1.0)

    return density, edges, bgs_pos


# ── Two-point correlation ────────────────────────────────────────

def measure_gamma(pos, n_bins=40):
    """Measure two-point correlation exponent γ."""
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
    rho = n_s / max(V_box, 1e-15)
    expected = 4 * np.pi * r_centers**2 * dr * rho * n_s / 2

    xi = np.where(expected > 0, counts / expected - 1, 0)
    valid = (xi > 0.01) & (r_centers > r_centers[3])
    gamma = 0.0
    if valid.sum() > 5:
        coeffs = np.polyfit(np.log10(r_centers[valid]),
                            np.log10(xi[valid]), 1)
        gamma = -coeffs[0]

    return float(gamma), r_centers.tolist(), xi.tolist()


# ── Load from database ───────────────────────────────────────────

def load_vertices(n_half):
    """Load vertices from PostgreSQL."""
    from database.universe_db import UniverseDB
    db = UniverseDB()
    with db.conn.cursor() as cur:
        cur.execute('''
            SELECT x, y, z, vertex_type
            FROM vertices WHERE n_half = %s ORDER BY id
        ''', (n_half,))
        rows = cur.fetchall()
    db.close()
    positions = np.array([(r[0], r[1], r[2]) for r in rows], dtype=np.float64)
    types = [r[3] for r in rows]
    return positions, types


def generate_qc(n_half):
    """Generate quasicrystal directly (no database needed)."""
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), 'CLEAN'))
    from geometry.voronoi_qc import build_quasicrystal, assign_types

    # Allow larger point counts for big N_half
    target_max = max(10000, n_half**6)
    pts_par, pts_perp, R_accept = build_quasicrystal(
        n_half, target_range=(1000, target_max))
    vtypes = assign_types(pts_perp, R_accept)
    return pts_par, list(vtypes)


# ── Command-line runner ──────────────────────────────────────────

if __name__ == '__main__':
    n_half = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    n_steps = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
    bracket = int(sys.argv[3]) if len(sys.argv) > 3 else 230

    print(f"\n  JAX Emergent Galaxy Formation")
    print(f"  ═════════════════════════════")
    print(f"  N_half={n_half}, {n_steps} steps, bracket={bracket}")
    print(f"  No coded forces. Shape emerges from anisotropic stiffness.\n")

    # Try database first, fall back to generation
    try:
        positions, types = load_vertices(n_half)
        print(f"  Loaded {len(positions):,} vertices from database")
    except Exception:
        print(f"  Generating QC with N_half={n_half}...")
        positions, types = generate_qc(n_half)
        print(f"  Generated {len(positions):,} vertices")

    n_bgs = sum(1 for t in types if t == 'BGS')
    print(f"  BGS (matter): {n_bgs:,} ({100*n_bgs/len(positions):.1f}%)\n")

    # Evolve
    result = evolve_jax(positions, types, n_steps=n_steps, bracket=bracket)

    # Find structures in final frame (multi-scale)
    final_pos = result['frames'][-1]
    structures = find_structures_multiscale(final_pos, types)

    # Measure correlation
    bgs_mask = np.array([t == 'BGS' for t in types])
    final_bgs = final_pos[bgs_mask]
    gamma, r_centers, xi = measure_gamma(final_bgs)
    print(f"\n  BGS correlation γ = {gamma:.3f}")
    print(f"  Framework prediction: γ = 1/σ₄ = 1.788")

    # Overdensity statistics
    od = np.array(structures['overdensity'])
    n_over = np.sum(od > 0.5)
    n_void = np.sum(od < -0.5)
    print(f"\n  Overdense regions (δ > 0.5): {n_over} vertices ({100*n_over/len(od):.1f}%)")
    print(f"  Void regions (δ < -0.5):     {n_void} vertices ({100*n_void/len(od):.1f}%)")

    # Summary per scale
    for sc in structures['scales']:
        n_s = sc['n_structures']
        shapes = {}
        for g in sc['structures']:
            shapes[g['shape']] = shapes.get(g['shape'], 0) + 1
        print(f"\n  {sc['name'].upper()}: {n_s} structures")
        for shape, count in sorted(shapes.items()):
            print(f"    {shape}: {count}")

    # Save results
    import json
    os.makedirs('results/simulation', exist_ok=True)
    outpath = f'results/simulation/galaxy_{n_half}_bz{bracket}.json'

    # Prepare galaxy data for JSON (limit member indices for size)
    galaxy_scale = None
    for sc in structures['scales']:
        if sc['name'] == 'galaxy':
            galaxy_scale = sc
            break
    if galaxy_scale is None and structures['scales']:
        galaxy_scale = structures['scales'][0]

    galaxies_out = []
    if galaxy_scale:
        for g in galaxy_scale['structures'][:100]:
            galaxies_out.append({
                'center': g['center'],
                'n_members': g['n_members'],
                'radius': g['radius'],
                'shape': g['shape'],
                'axis_ratios': g['axis_ratios'],
            })

    out = {
        'n_half': n_half,
        'n_steps': n_steps,
        'bracket': bracket,
        'n_vertices': len(positions),
        'n_bgs': n_bgs,
        'gamma': gamma,
        'n_galaxies': len(galaxies_out),
        'galaxies': galaxies_out,
        'overdensity_stats': {
            'mean': float(np.mean(od)),
            'std': float(np.std(od)),
            'max': float(np.max(od)),
            'min': float(np.min(od)),
            'n_overdense': int(n_over),
            'n_void': int(n_void),
        },
        'scales_summary': [{
            'name': sc['name'],
            'n_structures': sc['n_structures'],
            'linking_length': sc['linking_length'],
        } for sc in structures['scales']],
        'params': result['params'],
        'final_strain': result['strain'][-1],
    }
    with open(outpath, 'w') as f:
        json.dump(out, f, indent=2, default=str)
    print(f"\n  Saved to {outpath}")
