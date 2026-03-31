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
SIGMA3 = 0.04854                        # σ₃ spectral width (≈ W⁴ to 1.9%)
TRANSMISSION = 1.0 - W * (1 - W * SIGMA3)  # 0.5435 — gap self-taxes through its own matter
SILVER_MEAN = 1 + 2**0.5                    # δ_S = 2.41421
SILVER_TAX  = LEAK / SILVER_MEAN            # 0.06045 — entanglement tax per transaction

# ── Parker spiral toggle ─────────────────────────────────────────
# When True, sound force follows Parker spiral (inward + tangential).
# When False, sound force is purely radial inward (legacy behavior).
# Set via evolve_jax(parker_spiral=...) or directly.
PARKER_SPIRAL = True

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


def _build_asymmetry_lookup():
    """Build asymmetry as a 7×7 matrix indexed by type ID.

    Same indexing as STIFFNESS_MATRIX: B=0, BG=1, BGS=2, BS=3, G=4, GS=5, S=6.
    Asymmetry values from matching rule tiling preference.
    """
    mat = np.zeros((7, 7), dtype=np.float32)
    BGS_ID = TYPE_TO_ID['BGS']
    BS_ID = TYPE_TO_ID['BS']
    GS_ID = TYPE_TO_ID['GS']
    BG_ID = TYPE_TO_ID['BG']

    # BGS-BGS: strong matter clumping
    mat[BGS_ID, BGS_ID] = 2.0
    # BGS-BS: strong force confinement
    mat[BGS_ID, BS_ID] = mat[BS_ID, BGS_ID] = 1.5
    # BGS-GS: EM moderate
    mat[BGS_ID, GS_ID] = mat[GS_ID, BGS_ID] = 0.5
    # BGS-BG: gravity weak
    mat[BGS_ID, BG_ID] = mat[BG_ID, BGS_ID] = 0.3
    # Double-type bonds with stiffness > LEAK² get 0.2 (handled in vectorized code)
    return mat

ASYMMETRY_MATRIX = _build_asymmetry_lookup()


def _build_gate_lookup():
    """Build strain gate as a 7×7 matrix indexed by type ID.

    Three-gate model: Localized (BGS-BGS)=1.0, Critical (filament)=R_C, Extended=0.
    """
    mat = np.zeros((7, 7), dtype=np.float32)
    BGS_ID = TYPE_TO_ID['BGS']
    BS_ID = TYPE_TO_ID['BS']
    GS_ID = TYPE_TO_ID['GS']
    BG_ID = TYPE_TO_ID['BG']

    # Matter-matter: full force
    mat[BGS_ID, BGS_ID] = 1.0
    # BGS + double-type force carriers: gated at crossover
    for dt in [BS_ID, GS_ID, BG_ID]:
        mat[BGS_ID, dt] = mat[dt, BGS_ID] = R_C
    # BGS + single-type: weak
    for st_name in ['B', 'G', 'S']:
        st = TYPE_TO_ID[st_name]
        mat[BGS_ID, st] = mat[st, BGS_ID] = LEAK
    # Double-type pairs: barely resists (handled via stiffness check in vectorized code)
    return mat

GATE_MATRIX = _build_gate_lookup()


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

def _make_jax_step(N, M, parker_spiral=True):
    """Create JIT-compiled evolution step function.

    Asymmetric strain: extension is penalized more than compression
    for matter bonds (pair_asymmetry > 0). This creates net infall →
    galaxy formation. Vacuum bonds expand via pair_expansion.

    The physics is STILL emergent:
    - Asymmetry comes from matching rules preferring dense tiling
    - Expansion comes from vacuum self-interaction (dark energy)
    - The stiffness hierarchy determines WHICH bonds cluster vs expand
    """

    GOLDEN_ANGLE = 2.0 * 3.141592653589793 / (PHI * PHI)  # 137.508° in radians
    USE_PARKER = parker_spiral  # captured in closure for JIT

    @jit
    def step_fn(pos, vel, ii, jj, pair_stiffness, pair_ideal,
                pair_asymmetry, pair_expansion, dt, damping,
                strain_gate, spin_axis, vortex_strength,
                pair_depth, pair_fill, fill_active,
                gate_drag_strength, orbital_mode,
                type_silver, type_gold,
                photon_rate, sound_rate, speed_ratio):
        """One leapfrog step with gated hierarchical strain + vortex torque.

        strain_gate: (M,) per-pair multiplier [0,1] that gates spring forces.
            1.0 = full spring force (matter bonds, filaments)
            R_C  = gated filament force (entanglement tax)
            0.0 = free expansion (vacuum bonds — dark energy)

        spin_axis: (3,) unit vector — rotation axis (from disc PCA or tidal field)
        vortex_strength: float — angular momentum coupling (0=off)
        pair_depth: (M,) — locality depth of each pair (0=outer, 1=core).
        pair_fill: (M,) — well-fill factor [0,1]. Tracks how settled each bond is.
            0.0 = well empty (full force), 1.0 = well full (force → 0).
            Updated each step from per-pair strain: when a bond's strain drops
            near zero, its well is full and force should vanish.

        The well-fill insight: in lattice QCD, the correlator C(t) decays to
        a constant at the ground state — M_eff → 0. Similarly, when a bond
        reaches its equilibrium distance (strain → 0), the gravity well is
        "full" and the entanglement tax has been fully paid. Continuing to
        apply force would be like measuring a correlator past its plateau —
        you'd be fitting noise, not physics.
        """
        dr = pos[jj] - pos[ii]                               # (M, 3)
        r2 = jnp.sum(dr * dr, axis=1)                        # (M,)
        r = jnp.sqrt(r2) + 1e-10                             # (M,)

        # Dark energy: vacuum ideal distances grow each step
        ideal_now = pair_ideal * (1.0 + pair_expansion)       # (M,)

        delta_raw = r - ideal_now                             # (M,)

        # ── STRAIN HORIZON (night-sky clamp) ──────────────────
        delta = jnp.clip(delta_raw, -ideal_now, ideal_now)

        # Per-pair normalized strain (for well-fill tracking)
        pair_strain = delta**2 / (ideal_now**2 + 1e-10)      # (M,)

        # Asymmetric strain: extension (delta > 0) is stronger
        asym_factor = jnp.where(delta > 0,
                                1.0 + pair_asymmetry,
                                1.0)
        strain_grad = 2.0 * delta * asym_factor / (ideal_now**2)
        f_mag = -pair_stiffness * strain_grad / r             # (M,)

        # ── LOCALITY-DEPENDENT GATE (entanglement tax gradient) ──
        gate_tax = 1.0 - pair_depth * (1.0 - R_C)            # (M,)
        effective_gate = strain_gate * gate_tax

        # ── WELL-FILL DAMPING ─────────────────────────────────
        # When a bond's strain is near zero, its gravity well is full.
        # The fill factor tracks this as an exponential moving average.
        # Force is multiplied by (1 - fill), so full wells → zero force.
        #
        # Fill update: exponential moving average of "how settled is this bond?"
        # settled = 1 when strain/threshold < 1, settled = 0 when strain >> threshold
        # fill accumulates slowly (rate = 1-R_C = LEAK per step)
        # fill drains even slower (only when strain returns, same rate)
        # This way wells take ~1/LEAK ≈ 7 steps to fill, much longer to drain
        fill_threshold = LEAK                                 # strain below this → filling
        strain_ratio = jnp.clip(pair_strain / fill_threshold, 0.0, 1.0)
        settled = 1.0 - strain_ratio                          # 1=settled, 0=strained
        fill_rate = LEAK                                      # slow accumulation
        fill_new = pair_fill + fill_rate * (settled - pair_fill)
        fill_new = jnp.clip(fill_new, 0.0, 1.0)
        # Only accumulate fill after thermal phase (fill_active = 0 during thermal)
        fill_new = fill_new * fill_active

        # Force reduction: full well → no force
        well_factor = 1.0 - fill_new                          # (M,)
        f_mag = f_mag * effective_gate * well_factor

        f_vec = f_mag[:, None] * dr                           # (M, 3)

        # Scatter-add radial forces
        acc = jnp.zeros((N, 3), dtype=jnp.float32)
        acc = acc.at[ii].add(f_vec)
        acc = acc.at[jj].add(-f_vec)

        # ── TWO-POTENTIAL FLOW (photon outward + sound inward) ────
        # Photon (gold): tension bonds near center emit outward radial force
        # Sound (silver): compression bonds near edge apply inward force
        # Speed difference: photon = c (immediate), sound = c/√3 (damped)
        #
        # Each vertex type couples differently:
        #   Gold-rich (G, BG, GS): feel photon force strongly
        #   Silver-rich (S, BS, GS): feel sound force strongly
        #   BGS: feel both equally (full transducer)
        has_flow = (photon_rate > 1e-10) | (sound_rate > 1e-10)

        # Bond strain decomposition (already have delta from spring calc)
        tension = jnp.maximum(delta, 0.0)         # positive = stretched = photon
        compression = jnp.maximum(-delta, 0.0)     # negative = squeezed = sound

        # Radial direction of each bond midpoint relative to COM
        mid = 0.5 * (pos[ii] + pos[jj])            # (M, 3)
        com_flow = jnp.mean(pos, axis=0)            # (3,)
        r_from_com_bond = mid - com_flow[None, :]   # (M, 3)
        r_bond = jnp.sqrt(jnp.sum(r_from_com_bond**2, axis=1)) + 1e-10
        r_hat_bond = r_from_com_bond / r_bond[:, None]  # (M, 3) radial unit

        # PHOTON: tension × depth → outward force (emitted from dense core)
        # Deeper bonds have more gravitational energy to convert to radiation
        photon_mag = photon_rate * tension * pair_depth  # (M,)
        photon_f = photon_mag[:, None] * r_hat_bond      # (M, 3) outward

        # SOUND: compression × (1-depth) → inward force
        # When parker_spiral=True: follows Parker spiral (inward + tangential)
        # When parker_spiral=False: purely radial inward (legacy)
        sound_mag = sound_rate * compression * (1.0 - pair_depth) / speed_ratio

        if USE_PARKER:
            # Tangential direction at each bond midpoint: cross(spin_axis, r_hat)
            t_cross = jnp.cross(spin_axis[None, :], r_from_com_bond)  # (M, 3)
            t_norm = jnp.sqrt(jnp.sum(t_cross**2, axis=1, keepdims=True)) + 1e-10
            t_hat_bond = t_cross / t_norm                              # (M, 3)

            # Parker spiral: tan(ψ) = 1/φ → cos = φ/√(2+φ), sin = 1/√(2+φ)
            spiral_denom = jnp.sqrt(2.0 + PHI)
            spiral_cos = PHI / spiral_denom    # radial fraction  ≈ 0.851
            spiral_sin = 1.0 / spiral_denom    # tangential frac  ≈ 0.526
            spiral_dir = -spiral_cos * r_hat_bond + spiral_sin * t_hat_bond
            sound_f = sound_mag[:, None] * spiral_dir              # (M, 3)
        else:
            sound_f = -sound_mag[:, None] * r_hat_bond             # (M, 3) radial

        # Scatter to vertices weighted by type fraction
        # Photon → gold-sensitive vertices, Sound → silver-sensitive vertices
        photon_acc = jnp.zeros((N, 3), dtype=jnp.float32)
        photon_acc = photon_acc.at[ii].add(photon_f * type_gold[ii, None])
        photon_acc = photon_acc.at[jj].add(photon_f * type_gold[jj, None])

        sound_acc = jnp.zeros((N, 3), dtype=jnp.float32)
        sound_acc = sound_acc.at[ii].add(sound_f * type_silver[ii, None])
        sound_acc = sound_acc.at[jj].add(sound_f * type_silver[jj, None])

        # Normalize by bond count per vertex (prevent accumulation blow-up)
        bond_count = jnp.zeros(N, dtype=jnp.float32)
        bond_count = bond_count.at[ii].add(1.0)
        bond_count = bond_count.at[jj].add(1.0)
        bond_count = jnp.maximum(bond_count, 1.0)  # avoid /0
        flow_acc = (photon_acc + sound_acc) / bond_count[:, None]

        acc = acc + flow_acc * jnp.float32(has_flow)

        # ── VORTEX TORQUE (golden angle rotation) ─────────────
        # Energy flowing through Cantor gates rotates by golden angle
        # per bracket step. Deeper bonds → faster angular velocity.
        # Torque = cross(spin_axis, r_vec) × stiffness × depth × vortex_strength
        #
        # This creates differential rotation:
        #   Inner (high depth): fast rotation → tightly wound
        #   Outer (low depth): slow rotation → loosely wound
        #   Result: logarithmic spiral arms
        if_vortex = vortex_strength > 1e-10

        # Position of each vertex relative to center of mass
        com = jnp.mean(pos, axis=0)                           # (3,)
        r_from_com = pos - com[None, :]                       # (N, 3)

        # Tangential direction: cross(spin_axis, r_from_com)
        # This gives the "whirlpool" direction at each vertex
        tang = jnp.cross(spin_axis[None, :], r_from_com)     # (N, 3)
        tang_norm = jnp.sqrt(jnp.sum(tang * tang, axis=1, keepdims=True)) + 1e-10
        tang_hat = tang / tang_norm                           # (N, 3)

        # Distance from spin axis (cylindrical radius)
        r_cyl = tang_norm[:, 0]                               # (N,)

        # Per-vertex depth (scatter from pair_depth)
        v_depth = jnp.zeros(N, dtype=jnp.float32)
        v_depth = v_depth.at[ii].add(pair_depth * pair_stiffness)
        v_depth = v_depth.at[jj].add(pair_depth * pair_stiffness)
        v_count = jnp.zeros(N, dtype=jnp.float32)
        v_count = v_count.at[ii].add(pair_stiffness)
        v_count = v_count.at[jj].add(pair_stiffness)
        v_depth = v_depth / (v_count + 1e-10)                # (N,) mean depth

        # Angular velocity: deeper → faster (golden angle scaling)
        # ω(depth) = vortex_strength × (1 + depth × φ)
        # The φ factor means core rotates φ× faster than edge
        omega = vortex_strength * (1.0 + v_depth * PHI)       # (N,)

        # Torque acceleration: a_tang = ω² × r_cyl × tang_hat
        # (centripetal → tangential via golden angle offset)
        torque_mag = omega * r_cyl * GOLDEN_ANGLE             # (N,)
        torque_acc = torque_mag[:, None] * tang_hat            # (N, 3)

        # Only apply vortex to gated bonds (matter + filaments, not vacuum)
        # Use vertex-level gate: if vertex has any gated bonds, it feels torque
        v_gated = jnp.zeros(N, dtype=jnp.float32)
        v_gated = v_gated.at[ii].add(effective_gate)
        v_gated = v_gated.at[jj].add(effective_gate)
        torque_mask = jnp.minimum(v_gated / (v_count + 1e-10), 1.0)  # 0-1

        acc = acc + torque_acc * torque_mask[:, None] * jnp.float32(if_vortex)

        # ── GATE-DEPENDENT DRAG (circuit model) ─────────────────
        # Per-vertex depth from bond network: 1=center(deep well), 0=edge(shallow)
        # Deep well = closed gate = silver retained = free rotation
        # Shallow well = open gate = silver escapes = drag (entanglement tax)
        #
        # Gate openness = 1 - depth:
        #   Center (depth~1): gate closed, no tax, free spin
        #   Edge (depth~0): gate open, SILVER_TAX per transaction, drag
        gate_open = 1.0 - v_depth                          # (N,) uses depth from vortex calc
        # Drag: SILVER_TAX × gate_openness × gate_drag_strength
        # gate_drag_strength=0 → uniform damping (backward compatible)
        drag = SILVER_TAX * gate_open * gate_drag_strength

        # ── ORBITAL MODE: separate radial and tangential damping ──
        # When orbital_mode > 0:
        #   - Radial velocity: damped by base damping (settle into orbit)
        #   - Tangential velocity: damped ONLY by gate drag (orbits persist)
        # This allows sustained differential rotation.
        vel_raw = vel + acc * dt

        # Decompose velocity into radial and tangential components
        # relative to the spin axis (using com already computed for vortex)
        r_hat = r_from_com / (jnp.sqrt(jnp.sum(r_from_com**2, axis=1, keepdims=True)) + 1e-10)
        # Project along spin axis to get cylindrical r direction
        along_spin = jnp.sum(r_from_com * spin_axis[None, :], axis=1, keepdims=True) * spin_axis[None, :]
        r_cyl_vec = r_from_com - along_spin                # (N, 3)
        r_cyl_norm = jnp.sqrt(jnp.sum(r_cyl_vec**2, axis=1, keepdims=True)) + 1e-10
        r_cyl_hat = r_cyl_vec / r_cyl_norm                 # (N, 3) radial unit in disc plane

        # Tangential unit: cross(spin_axis, r_cyl_hat)
        tang_unit = jnp.cross(spin_axis[None, :], r_cyl_hat)  # (N, 3)

        # Decompose velocity
        v_radial = jnp.sum(vel_raw * r_cyl_hat, axis=1, keepdims=True) * r_cyl_hat
        v_along  = jnp.sum(vel_raw * spin_axis[None, :], axis=1, keepdims=True) * spin_axis[None, :]
        v_tang   = vel_raw - v_radial - v_along             # tangential component

        # Orbital mode: radial gets base damping, tangential gets only gate drag
        tang_damp = 1.0 - drag                              # (N,) gate drag only
        radial_damp = damping                               # scalar base damping
        along_damp = damping                                # base damping for vertical

        vel_orbital = (v_radial * radial_damp +
                       v_tang * tang_damp[:, None] +
                       v_along * along_damp)

        # Standard mode: uniform per_vertex_damping on everything
        per_vertex_damping = damping * (1.0 - drag)        # (N,)
        vel_standard = vel_raw * per_vertex_damping[:, None]

        # Select based on orbital_mode flag
        vel_new = jnp.where(orbital_mode > 0.5, vel_orbital, vel_standard)
        pos_new = pos + vel_new * dt

        # Strain metric — only count where gate is open
        total_strain = jnp.sum(effective_gate * pair_stiffness * delta**2 / ideal_now**2)

        # Mean fill level (diagnostic — how full are the wells?)
        mean_fill = jnp.mean(fill_new)

        # Mean drag (diagnostic)
        mean_drag = jnp.mean(drag)

        return pos_new, vel_new, total_strain, fill_new, mean_fill, mean_drag

    return step_fn


def _make_numpy_step():
    """NumPy fallback step function with gated hierarchical strain + vortex."""

    GOLDEN_ANGLE = 2.0 * np.pi / (PHI * PHI)

    def step_fn(pos, vel, ii, jj, pair_stiffness, pair_ideal,
                pair_asymmetry, pair_expansion, dt, damping,
                strain_gate, spin_axis=None, vortex_strength=0.0,
                pair_depth=None, pair_fill=None, fill_active=1.0,
                gate_drag_strength=0.0, orbital_mode=0.0,
                type_silver=None, type_gold=None,
                photon_rate=0.0, sound_rate=0.0, speed_ratio=1.732):
        N = len(pos)
        M = len(ii)
        dr = pos[jj] - pos[ii]
        r = np.sqrt(np.sum(dr * dr, axis=1)) + 1e-10

        ideal_now = pair_ideal * (1.0 + pair_expansion)
        delta_raw = r - ideal_now
        delta = np.clip(delta_raw, -ideal_now, ideal_now)

        # Per-pair normalized strain (for well-fill tracking)
        pair_strain = delta**2 / (ideal_now**2 + 1e-10)

        asym_factor = np.where(delta > 0, 1.0 + pair_asymmetry, 1.0)
        strain_grad = 2.0 * delta * asym_factor / (ideal_now**2)

        # Locality-dependent gate
        if pair_depth is not None:
            gate_tax = 1.0 - pair_depth * (1.0 - R_C)
            effective_gate = strain_gate * gate_tax
        else:
            effective_gate = strain_gate

        # Well-fill damping
        if pair_fill is not None:
            fill_threshold = LEAK
            strain_ratio = np.clip(pair_strain / fill_threshold, 0.0, 1.0)
            settled = 1.0 - strain_ratio
            fill_rate = LEAK
            fill_new = pair_fill + fill_rate * (settled - pair_fill)
            fill_new = np.clip(fill_new, 0.0, 1.0)
            fill_new = fill_new * fill_active  # only accumulate after thermal
            well_factor = 1.0 - fill_new
        else:
            fill_new = np.zeros(M, dtype=np.float32)
            well_factor = 1.0

        f_mag = -pair_stiffness * strain_grad / r * effective_gate * well_factor
        f_vec = f_mag[:, None] * dr

        acc = np.zeros((N, 3), dtype=np.float64)
        np.add.at(acc, ii, f_vec)
        np.add.at(acc, jj, -f_vec)

        # Two-potential flow (NumPy fallback)
        if photon_rate > 1e-10 or sound_rate > 1e-10:
            tension = np.maximum(delta, 0.0)
            compression = np.maximum(-delta, 0.0)
            mid = 0.5 * (pos[ii] + pos[jj])
            com_f = np.mean(pos, axis=0)
            r_from_com_bond = mid - com_f
            r_bond = np.sqrt(np.sum(r_from_com_bond**2, axis=1)) + 1e-10
            r_hat_bond = r_from_com_bond / r_bond[:, None]

            photon_mag = photon_rate * tension * pair_depth
            photon_f = photon_mag[:, None] * r_hat_bond
            sound_mag = sound_rate * compression * (1.0 - pair_depth) / speed_ratio

            # Parker spiral or radial inward
            if PARKER_SPIRAL and spin_axis is not None:
                t_cross = np.cross(spin_axis, r_from_com_bond)
                t_norm = np.sqrt(np.sum(t_cross**2, axis=1, keepdims=True)) + 1e-10
                t_hat_bond = t_cross / t_norm
                spiral_denom = np.sqrt(2.0 + PHI)
                spiral_cos = PHI / spiral_denom
                spiral_sin = 1.0 / spiral_denom
                spiral_dir = -spiral_cos * r_hat_bond + spiral_sin * t_hat_bond
                sound_f = sound_mag[:, None] * spiral_dir
            else:
                sound_f = -sound_mag[:, None] * r_hat_bond  # radial inward

            flow_acc = np.zeros_like(acc)
            if type_gold is not None:
                np.add.at(flow_acc, ii, photon_f * type_gold[ii, None])
                np.add.at(flow_acc, jj, photon_f * type_gold[jj, None])
            if type_silver is not None:
                np.add.at(flow_acc, ii, sound_f * type_silver[ii, None])
                np.add.at(flow_acc, jj, sound_f * type_silver[jj, None])
            # Normalize by bond count per vertex
            bond_count = np.zeros(N, dtype=np.float32)
            np.add.at(bond_count, ii, 1.0)
            np.add.at(bond_count, jj, 1.0)
            bond_count = np.maximum(bond_count, 1.0)
            acc += flow_acc / bond_count[:, None]

        # Vortex torque
        if vortex_strength > 1e-10 and spin_axis is not None and pair_depth is not None:
            com = np.mean(pos, axis=0)
            r_from_com = pos - com
            tang = np.cross(spin_axis, r_from_com)
            tang_norm = np.sqrt(np.sum(tang * tang, axis=1, keepdims=True)) + 1e-10
            tang_hat = tang / tang_norm
            r_cyl = tang_norm[:, 0]

            v_depth = np.zeros(N)
            v_count = np.zeros(N)
            np.add.at(v_depth, ii, pair_depth * pair_stiffness)
            np.add.at(v_depth, jj, pair_depth * pair_stiffness)
            np.add.at(v_count, ii, pair_stiffness)
            np.add.at(v_count, jj, pair_stiffness)
            v_depth /= (v_count + 1e-10)

            omega = vortex_strength * (1.0 + v_depth * PHI)
            torque_mag = omega * r_cyl * GOLDEN_ANGLE
            torque_acc = torque_mag[:, None] * tang_hat

            v_gated = np.zeros(N)
            np.add.at(v_gated, ii, effective_gate)
            np.add.at(v_gated, jj, effective_gate)
            torque_mask = np.minimum(v_gated / (v_count + 1e-10), 1.0)
            acc += torque_acc * torque_mask[:, None]

        # Gate-dependent drag (circuit model)
        if gate_drag_strength > 0 and pair_depth is not None:
            # Per-vertex depth: 1=center(deep), 0=edge(shallow)
            v_depth_d = np.zeros(N)
            v_count_d = np.zeros(N)
            np.add.at(v_depth_d, ii, pair_depth * pair_stiffness)
            np.add.at(v_depth_d, jj, pair_depth * pair_stiffness)
            np.add.at(v_count_d, ii, pair_stiffness)
            np.add.at(v_count_d, jj, pair_stiffness)
            v_depth_d /= (v_count_d + 1e-10)
            gate_open = 1.0 - v_depth_d
            drag = SILVER_TAX * gate_open * gate_drag_strength

            if orbital_mode > 0.5 and spin_axis is not None:
                # Orbital mode: radial damped, tangential only gate drag
                vel_raw = vel + acc * dt
                com = np.mean(pos, axis=0)
                r_from_com = pos - com
                along_spin = np.outer(r_from_com @ spin_axis, spin_axis)
                r_cyl_vec = r_from_com - along_spin
                r_cyl_norm = np.sqrt(np.sum(r_cyl_vec**2, axis=1, keepdims=True)) + 1e-10
                r_cyl_hat = r_cyl_vec / r_cyl_norm

                v_radial = np.sum(vel_raw * r_cyl_hat, axis=1, keepdims=True) * r_cyl_hat
                v_along = np.sum(vel_raw * spin_axis[None, :], axis=1, keepdims=True) * spin_axis[None, :]
                v_tang = vel_raw - v_radial - v_along

                tang_damp = 1.0 - drag
                vel_new = (v_radial * damping +
                           v_tang * tang_damp[:, None] +
                           v_along * damping)
            else:
                per_vertex_damping = damping * (1.0 - drag)
                vel_new = (vel + acc * dt) * per_vertex_damping[:, None]
        else:
            vel_new = (vel + acc * dt) * damping
        pos_new = pos + vel_new * dt

        total_strain = float(np.sum(effective_gate * pair_stiffness * delta**2 / ideal_now**2))
        mean_fill = float(np.mean(fill_new))
        mean_drag = float(np.mean(drag)) if gate_drag_strength > 0 else 0.0
        return pos_new, vel_new, total_strain, fill_new, mean_fill, mean_drag

    return step_fn


# ── Main evolution function ──────────────────────────────────────

def evolve_jax(positions, types, n_steps=5000, bracket=None,
               perturbation=0.02, damping=0.9985, nn_multiplier=1.6,
               rebuild_every=200, save_every=None, callback=None,
               disc_exponent=0.0, sym_axis=None, thermal_frac=0.2,
               vortex_strength=0.0, well_fill=False, resume=False,
               initial_velocities=None, gate_drag=0.0, orbital_mode=False,
               photon_rate=0.0, sound_rate=0.0, speed_ratio=1.7320508,
               parker_spiral=None):
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
    disc_exponent : float — shape anisotropy exponent (0=off, 4.0=galaxy disc)
        Applies sin²θ stiffness modulation: bonds in equatorial plane are
        stiffer by factor (1 + (disc_exponent-1) * sin²θ), favoring disc
        formation. Only active when > 0.1.
    sym_axis : (3,) array or None — symmetry axis for disc/vortex.
        If None, auto-detected from BGS PCA (shortest axis = rotation axis).
    thermal_frac : float — fraction of total steps to run at full temperature
        (damping=1.0) before cooling. Allows correlations to develop before
        structure freezes. Default 0.2 = first 20% of steps are undamped.
    vortex_strength : float — angular momentum coupling (0=off, 0.001-0.01 typical).
        Activates the spiral vortex: energy flowing through Cantor gates rotates
        by the golden angle (137.508°) per bracket step. Deeper bonds rotate
        faster → differential rotation → logarithmic spiral arms. The
        entanglement tax gradient (locality-dependent R_C gating) slows energy
        transfer at depth, so silver/gold channels don't dominate — energy
        takes the path of least resistance, spreading azimuthally into arms.

    Returns dict with frames, steps, metrics, params
    """
    # Set Parker spiral mode (global for NumPy path, passed to JIT closure)
    global PARKER_SPIRAL
    if parker_spiral is not None:
        PARKER_SPIRAL = parker_spiral
    use_parker = PARKER_SPIRAL  # local copy for JIT closure

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

    def build_pair_arrays(pairs_arr, pos_current):
        """Build stiffness, ideal, asymmetry, expansion arrays for pairs.

        Fully vectorized — no Python loops over pairs. Uses precomputed
        7×7 lookup matrices (STIFFNESS_MATRIX, ASYMMETRY_MATRIX, GATE_MATRIX)
        indexed by type_ids for O(M) array operations.
        """
        ii_l, jj_l = pairs_arr[:, 0], pairs_arr[:, 1]
        M_l = len(pairs_arr)

        # Type IDs for each end of every pair
        ti = type_ids[ii_l]  # (M,)
        tj = type_ids[jj_l]  # (M,)

        # ── STIFFNESS: vectorized matrix lookup ──────────────────
        stiff = STIFFNESS_MATRIX[ti, tj].copy()

        # ── IDEAL DISTANCES: vectorized via ideal matrix ─────────
        # Build 7×7 ideal distance matrix from the ideals dict
        ideal_mat = np.full((7, 7), mean_spacing, dtype=np.float32)
        for key, d in ideals.items():
            if key == '_mean':
                continue
            t1, t2 = key
            i1, i2 = TYPE_TO_ID.get(t1, -1), TYPE_TO_ID.get(t2, -1)
            if i1 >= 0 and i2 >= 0:
                ideal_mat[i1, i2] = d
                ideal_mat[i2, i1] = d
        ideal = ideal_mat[ti, tj]

        # ── ASYMMETRIC STRAIN: vectorized matrix lookup ──────────
        # Physical basis: QC tiling acceptance window preferentially
        # keeps vertices close to center of perp-space.
        # Extension violates matching rules more than compression.
        asym = ASYMMETRY_MATRIX[ti, tj].copy()
        # Double-type bonds not involving BGS with stiffness > LEAK²: slight clustering
        no_asym_yet = (asym == 0) & (stiff > LEAK**2)
        asym[no_asym_yet] = 0.2

        # ── DARK ENERGY EXPANSION: vectorized ────────────────────
        expansion_rate = LEAK**3 * 0.5  # per step, cumulative (capped at 2x)
        expn = np.zeros(M_l, dtype=np.float32)
        if well_fill:
            # Tax model: expansion reduced by stiffness × TRANSMISSION
            vacuum_mask = stiff < 1e-6
            expn[vacuum_mask] = expansion_rate
            matter_mask = ~vacuum_mask
            tax_factor = np.minimum(stiff[matter_mask], 1.0) * TRANSMISSION
            expn[matter_mask] = expansion_rate * (1.0 - tax_factor)
        else:
            # v4 baseline: discrete type-based expansion
            SINGLE_TYPES = {TYPE_TO_ID['G'], TYPE_TO_ID['S'], TYPE_TO_ID['B']}
            BGS_ID = TYPE_TO_ID['BGS']
            ti_single = np.isin(ti, list(SINGLE_TYPES))
            tj_single = np.isin(tj, list(SINGLE_TYPES))
            ti_bgs = (ti == BGS_ID)
            tj_bgs = (tj == BGS_ID)
            # vacuum-vacuum: full expansion
            vac_vac = ti_single & tj_single
            expn[vac_vac] = expansion_rate
            # mixed (one single-type): slower
            mixed = (ti_single ^ tj_single) & ~ti_bgs & ~tj_bgs
            expn[mixed] = expansion_rate * 0.3
            # matter (BGS involved): zero
            matter = ti_bgs | tj_bgs
            expn[matter] = 0.0
            # double-type (neither single nor BGS): barely
            double = ~vac_vac & ~mixed & ~matter
            expn[double] = expansion_rate * 0.1

        # ── HIERARCHICAL STRAIN GATE: vectorized matrix lookup ───
        # Three-gate model: Localized=1.0, Critical=R_C, Extended=0.0
        gate = GATE_MATRIX[ti, tj].copy()
        # Double-type pairs (no BGS) with stiffness > LEAK²: barely resists
        double_gate = (gate == 0) & (stiff > LEAK**2)
        gate[double_gate] = LEAK**2

        # ── DISC EXPONENT (sin²θ shape anisotropy) ──────────────
        # At galaxy scale (bracket ~256), equatorial bonds stiffer
        # → matter collapses into disc plane, producing c/a < 0.3
        if disc_exponent > 0.1 and M_l > 0:
            from simulation.shape_operator import detect_symmetry_axis
            disc_axis = sym_axis if sym_axis is not None else \
                detect_symmetry_axis(pos_current, types)
            if disc_axis is None:
                disc_axis = np.array([0, 0, 1], dtype=np.float64)
            disc_axis = disc_axis / (np.linalg.norm(disc_axis) + 1e-15)
            dr_disc = pos_current[jj_l] - pos_current[ii_l]
            r_disc = np.sqrt(np.sum(dr_disc**2, axis=1, keepdims=True)) + 1e-15
            dr_hat = dr_disc / r_disc
            cos_th = np.abs(dr_hat @ disc_axis)
            sin_th2 = 1.0 - cos_th**2 + 1e-15
            shape_mod = 1.0 + (disc_exponent - 1.0) * sin_th2
            shape_mod /= np.mean(shape_mod)  # preserve mean stiffness
            stiff *= shape_mod.astype(np.float32)

        # Shape operator (bracket-dependent anisotropy)
        if bracket is not None:
            from simulation.shape_operator import detect_symmetry_axis, bracket_info
            shape_axis = sym_axis if sym_axis is not None else \
                detect_symmetry_axis(pos_current, types)
            dr_v = pos_current[jj_l] - pos_current[ii_l]
            shape_mods = compute_shape_modifiers_np(bracket, dr_v, shape_axis)
            stiff *= shape_mods

        # ── CANTOR ACOUSTIC MODULATION ──────────────────────────────
        # The Cantor node is the reverberation pattern of the AAH wave
        # equation at the photonic sound barrier (V=2J).
        # Gold (φ) carries momentum, Silver (δ_S) carries mass.
        # Where both constructively interfere → superconducting node →
        # matter accumulates. Where out of phase → gap → void.
        # Bronze (observable) = Pythagorean combination (5+8=13).
        bgs_mask_l = np.array([t == 'BGS' for t in types])
        bgs_pos_l = pos_current[bgs_mask_l]
        depth = np.zeros(M_l, dtype=np.float32)

        if len(bgs_pos_l) > 2:
            bgs_com = np.mean(bgs_pos_l, axis=0)
            bgs_radii = np.sqrt(np.sum((bgs_pos_l - bgs_com)**2, axis=1))
            r_max = np.max(bgs_radii) + 1e-10

            # Midpoint of each pair → radial fraction
            mid = 0.5 * (pos_current[ii_l] + pos_current[jj_l])
            r_mid = np.sqrt(np.sum((mid - bgs_com)**2, axis=1))
            r_frac = r_mid / r_max  # 0=center, 1=edge

            # AAH radial potential: gold and silver cosines
            # n = radial site index (233 sites across the radius)
            n_radial = r_frac * 233.0
            gold_wave  = np.cos(2.0 * np.pi / PHI * n_radial)
            silver_wave = np.cos(2.0 * np.pi / SILVER_MEAN * n_radial)

            # Conductivity = where both channels are in phase
            # Product: +1 when both peak, -1 when anti-phase
            # Map to stiffness multiplier: 1 + amplitude × coupling
            coupling = gold_wave * silver_wave  # [-1, +1]
            # Scale: at nodes (coupling > 0), bonds stiffen → matter accumulates
            # In gaps (coupling < 0), bonds loosen → voids form
            cantor_mod = 1.0 + 0.5 * coupling  # [0.5, 1.5]
            # Normalize to preserve mean stiffness
            cantor_mod /= np.mean(cantor_mod)
            # Cantor acoustic modulation: superconducting nodes attract matter
            stiff *= cantor_mod.astype(np.float32)

            # Depth: 1 at center, 0 at edge, clipped
            depth = np.clip(1.0 - r_frac, 0.0, 1.0).astype(np.float32)

        return stiff, ideal, asym, expn, gate, depth

    pair_stiffness, pair_ideal, pair_asymmetry, pair_expansion, strain_gate, pair_depth = \
        build_pair_arrays(pairs, pos)

    if bracket is not None:
        from simulation.shape_operator import bracket_info
        info = bracket_info(bracket)
        print(f"  Shape: bracket={bracket} ({info['label']}) "
              f"disc/sphere={info['disc_sphere_ratio']:.2f} → {info['expected_shape']}")
    n_gated = int(np.sum(strain_gate > 0))
    n_free = len(strain_gate) - n_gated
    print(f"  Asymmetry: BGS-BGS=2.0, BGS-BS=1.5, BGS-GS=0.5, vacuum=0.0")
    print(f"  Strain gate: {n_gated} active bonds, {n_free} free-expansion (vacuum)")
    print(f"  Expansion: vacuum={LEAK**3*0.5:.5f}/step → "
          f"~{LEAK**3*0.5*n_steps*100:.0f}% growth over {n_steps} steps")
    if vortex_strength > 0:
        print(f"  Vortex: strength={vortex_strength:.4f}, golden angle torque active")

    # Perturbation — φ-structured seeds preserve lattice symmetry
    # Random seeds break the quasicrystalline tiling; phi_silver uses
    # gold (φ) on radial axis, silver (δ_S) on angular axis, bronze on polar.
    from simulation.phi_seeds import apply_phi_perturbation
    pos = apply_phi_perturbation(pos, perturbation * mean_spacing,
                                 mode='phi_silver', phase=0.0)
    print(f"  Seed: phi_silver perturbation (φ×δ_S tiling)")
    if gate_drag > 0:
        print(f"  Gate drag: strength={gate_drag:.3f} (SILVER_TAX={SILVER_TAX:.4f} × gate_openness)")

    # Determine spin axis for vortex
    if sym_axis is not None:
        spin_ax = np.array(sym_axis, dtype=np.float32)
    else:
        from simulation.shape_operator import detect_symmetry_axis
        spin_ax = detect_symmetry_axis(pos, types)
        if spin_ax is None:
            spin_ax = np.array([0, 0, 1], dtype=np.float32)
    spin_ax = spin_ax / (np.linalg.norm(spin_ax) + 1e-15)
    spin_ax = spin_ax.astype(np.float32)

    # Track settled/active bond counts for metrics
    n_settled = 0
    n_active = 0

    # ── Type fraction arrays for two-potential coupling ───────────
    # Silver fraction: how strongly vertex couples to sound/inward flow
    # Gold fraction: how strongly vertex couples to photon/outward flow
    SILVER_FRAC_MAP = {'S': 1.0, 'GS': 0.5, 'BS': 0.5, 'BGS': 0.333,
                       'B': 0.0, 'G': 0.0, 'BG': 0.0}
    GOLD_FRAC_MAP   = {'G': 1.0, 'GS': 0.5, 'BG': 0.5, 'BGS': 0.333,
                       'S': 0.0, 'B': 0.0, 'BS': 0.0}
    type_silver = np.array([SILVER_FRAC_MAP.get(t, 0.0) for t in types],
                           dtype=np.float32)
    type_gold = np.array([GOLD_FRAC_MAP.get(t, 0.0) for t in types],
                         dtype=np.float32)
    has_flow = photon_rate > 0 or sound_rate > 0
    if has_flow:
        print(f"  Two-potential flow: photon_rate={photon_rate:.4f}, "
              f"sound_rate={sound_rate:.4f}, speed_ratio={speed_ratio:.3f}")
        print(f"    Silver vertices: {np.sum(type_silver > 0)} "
              f"(mean frac={np.mean(type_silver):.3f})")
        print(f"    Gold vertices: {np.sum(type_gold > 0)} "
              f"(mean frac={np.mean(type_gold):.3f})")

    # Convert to JAX or keep NumPy
    use_jax = JAX_OK
    if use_jax:
        pos_j = jnp.array(pos, dtype=jnp.float32)
        if initial_velocities is not None:
            vel_j = jnp.array(initial_velocities, dtype=jnp.float32)
            print(f"  Initial velocities: max={np.max(np.abs(initial_velocities)):.4f}")
        else:
            vel_j = jnp.zeros((N, 3), dtype=jnp.float32)
        ii_j = jnp.array(ii, dtype=jnp.int32)
        jj_j = jnp.array(jj, dtype=jnp.int32)
        stiff_j = jnp.array(pair_stiffness, dtype=jnp.float32)
        ideal_j = jnp.array(pair_ideal, dtype=jnp.float32)
        asym_j = jnp.array(pair_asymmetry, dtype=jnp.float32)

        step_fn = _make_jax_step(N, M, parker_spiral=use_parker)
        gate_j = jnp.array(strain_gate, dtype=jnp.float32)
        spin_j = jnp.array(spin_ax, dtype=jnp.float32)
        depth_j = jnp.array(pair_depth, dtype=jnp.float32)
        fill_j = jnp.zeros(M, dtype=jnp.float32)  # wells start empty
        tsilver_j = jnp.array(type_silver, dtype=jnp.float32)
        tgold_j = jnp.array(type_gold, dtype=jnp.float32)

        # Warm-up JIT (expansion grows each step)
        print("  JIT compiling...")
        t0 = time.time()
        expn_j = jnp.array(pair_expansion, dtype=jnp.float32)
        pos_j, vel_j, _, fill_j, _, _ = step_fn(pos_j, vel_j, ii_j, jj_j, stiff_j, ideal_j,
                                   asym_j, expn_j, jnp.float32(dt), jnp.float32(damping),
                                   gate_j, spin_j, jnp.float32(vortex_strength),
                                   depth_j, fill_j, jnp.float32(0.0),
                                   jnp.float32(gate_drag), jnp.float32(1.0 if orbital_mode else 0.0),
                                   tsilver_j, tgold_j,
                                   jnp.float32(photon_rate), jnp.float32(sound_rate),
                                   jnp.float32(speed_ratio))
        pos_j.block_until_ready()
        print(f"  JIT compiled in {time.time()-t0:.1f}s")
    else:
        if initial_velocities is not None:
            vel = initial_velocities.astype(np.float64)
            print(f"  Initial velocities: max={np.max(np.abs(initial_velocities)):.4f}")
        else:
            vel = np.zeros((N, 3), dtype=np.float64)
        pair_fill = np.zeros(len(pairs), dtype=np.float32)  # wells start empty
        step_fn = _make_numpy_step()

    # Storage
    frames = [np.array(pos_j if use_jax else pos).copy()]
    steps_list = [0]
    strain_list = [0.0]
    fill_list = [0.0]  # track well-fill level
    base_depth_map = {'_arr': pair_depth.copy()}  # base depth for settlement check

    t_start = time.time()

    cumulative_expansion = np.zeros(len(pairs), dtype=np.float32)
    # Cap expansion at 2× mean spacing to prevent strain explosion
    max_expansion = np.full_like(pair_expansion, 2.0 * mean_spacing)

    # Resume mode: skip thermal phase, zero expansion (positions already encode it)
    if resume:
        pair_expansion = np.zeros_like(pair_expansion)
        print(f"  RESUME MODE: no thermal phase, no expansion (positions already expanded)")

    # Scale rebuild frequency with step count (keep ~25 rebuilds total)
    rebuild_every = max(200, n_steps // 25)

    # Thermal schedule: hot phase → cosine cooldown → final damping
    # Cap at 4000 hot + 4000 cool to prevent numerical issues on long runs
    if resume:
        thermal_steps = 0
        cool_steps = 0
    else:
        thermal_steps = min(int(n_steps * thermal_frac), 4000)
        cool_steps = min(int(n_steps * thermal_frac), 4000)
    print(f"  Thermal: {thermal_steps} hot steps (damping=1.0), "
          f"{cool_steps} cooldown, then damping={damping}")
    print(f"  Rebuild every {rebuild_every} steps")

    for step in range(1, n_steps + 1):
        # Thermal ramp: undamped → cosine cooldown → target damping
        if step <= thermal_steps:
            damp_now = 1.0  # full temperature — let correlations develop
        elif step <= thermal_steps + cool_steps:
            # Cosine ramp from 1.0 to target damping
            t = (step - thermal_steps) / cool_steps
            damp_now = damping + (1.0 - damping) * 0.5 * (1.0 + np.cos(np.pi * t))
        else:
            damp_now = damping

        # Accumulate expansion each step (capped)
        cumulative_expansion += pair_expansion
        np.minimum(cumulative_expansion, max_expansion, out=cumulative_expansion)

        # Rebuild neighbors periodically
        if step % rebuild_every == 0:
            old_ii = np.array(ii)
            old_jj = np.array(jj)
            current_pos = np.array(pos_j if use_jax else pos)
            pairs, threshold = build_neighbor_pairs(current_pos, nn_multiplier)
            M = len(pairs)
            ii = pairs[:, 0]
            jj = pairs[:, 1]

            pair_stiffness, pair_ideal, pair_asymmetry, pair_expansion, strain_gate, pair_depth = \
                build_pair_arrays(pairs, current_pos)
            # Resume mode: zero expansion (positions already encode prior expansion)
            if resume:
                pair_expansion = np.zeros_like(pair_expansion)
            # Reset cumulative expansion for new pairs (capped at 2× mean spacing)
            max_expansion = np.full_like(pair_expansion, 2.0 * mean_spacing)
            cumulative_expansion = np.minimum(pair_expansion * step, max_expansion)

            # ── Bracket promotion: settled bonds donate tax upward ──
            if well_fill and step > (thermal_steps + cool_steps):
                # Compute current strain for old pairs
                dx_old = current_pos[old_ii] - current_pos[old_jj]
                dist_old = np.linalg.norm(dx_old, axis=1)
                old_ideal = np.array(ideal_j if use_jax else pair_ideal)[:len(old_ii)]
                # Use BASE depth for settlement (not promoted depth)
                old_base = base_depth_map.get('_arr', np.zeros(len(old_ii)))[:len(old_ii)]
                pair_strain_old = (dist_old - old_ideal)**2 / (old_ideal**2 + 1e-10)

                # Settled = strain below base depth (well is full at its natural level)
                settled_mask = pair_strain_old < old_base
                # Only active (gated) bonds can settle — vacuum bonds don't carry tax
                old_gate = np.array(gate_j if use_jax else strain_gate)[:len(old_ii)]
                settled_mask = settled_mask & (old_gate > 0.5)
                n_settled = int(np.sum(settled_mask))
                n_active = int(np.sum(old_gate > 0.5))

                if n_settled > 0 and n_active > n_settled:
                    # Donated tax = settled bonds' BASE depth × SILVER_TAX
                    # Silver fraction (LEAK/δ_S = 0.0604) is the per-transaction
                    # entanglement tax — physically grounded in ionization bridge
                    donated = float(np.sum(old_base[settled_mask]) * SILVER_TAX)
                    # 5:8:13 Pythagorean decomposition of bronze interference:
                    #   Silver portion (8/13) = mass → promotes upward to unsettled bonds
                    #   Gold portion (5/13)   = momentum → improves bonding of settled bonds
                    donated_silver = donated * (8.0 / 13.0)  # mass: promotes up
                    donated_gold   = donated * (5.0 / 13.0)  # momentum: bonding improvement
                    n_unsettled = n_active - n_settled
                    promotion = donated_silver / n_unsettled
                    # Cap: promoted depth cannot exceed PHI × base depth
                    active_new = strain_gate > 0.5
                    base_new = pair_depth.copy()  # base from build_pair_arrays
                    pair_depth[active_new] += promotion
                    max_depth = base_new * PHI
                    pair_depth = np.minimum(pair_depth, max_depth)
                    # Gold portion: settled bonds get bonding stiffness boost
                    n_settled_f = max(n_settled, 1)
                    gold_boost = donated_gold / n_settled_f
                    # Apply to settled bonds in current pair arrays via index mapping
                    settled_idx = np.where(settled_mask[:len(strain_gate)])[0]
                    if len(settled_idx) > 0:
                        pair_depth[settled_idx] += gold_boost
                        pair_depth[settled_idx] = np.minimum(
                            pair_depth[settled_idx], base_new[settled_idx] * PHI)
                    actual_promo = float(np.mean(pair_depth[active_new] - base_new[active_new]))
                    print(f"    Bracket promotion: {n_settled}/{n_active} settled, "
                          f"+{actual_promo:.6f} mean depth (5:8:13 split, "
                          f"gold={gold_boost:.6f} bond boost, capped at {PHI:.3f}x)")

            # Store base depth for next promotion check
            base_depth_map['_arr'] = pair_depth.copy()

            # ── IONIZATION HEATING (stellar feedback) ──────────────
            # Stars are ionization pumps: UV → ionization → gate opens →
            # entanglement tax returns energy through the channel.
            # Dense BGS regions = "stars" → local velocity kicks prevent
            # full equilibration, maintaining disc/spiral structure.
            #
            # Kick magnitude ∝ SILVER_TAX × local_density × mean_spacing
            # This is the entanglement tax return — energy coming back.
            if well_fill and step > (thermal_steps + cool_steps):
                bgs_idx = np.array([k for k, t in enumerate(types) if t == 'BGS'])
                if len(bgs_idx) > 5:
                    from scipy.spatial import KDTree
                    bgs_tree = KDTree(current_pos[bgs_idx])
                    # Count BGS neighbors within 2× mean spacing
                    n_nbrs = bgs_tree.query_ball_point(current_pos[bgs_idx],
                                                       2.0 * mean_spacing)
                    densities = np.array([len(nb) for nb in n_nbrs])
                    # Only heat where density > median (= "star forming" regions)
                    med_dens = max(np.median(densities), 1)
                    hot_mask = densities > med_dens
                    n_hot = int(np.sum(hot_mask))
                    if n_hot > 0:
                        hot_global_idx = bgs_idx[hot_mask]
                        # Kick magnitude: SILVER_TAX × mean_spacing × density_excess
                        kick_scale = SILVER_TAX * mean_spacing * 0.1
                        density_factor = (densities[hot_mask] - med_dens) / med_dens
                        kick_mag = kick_scale * np.clip(density_factor, 0, 2.0)
                        # Random direction kicks (isotropic heating)
                        rng = np.random.default_rng(step)
                        kick_dirs = rng.standard_normal((n_hot, 3))
                        kick_dirs /= (np.linalg.norm(kick_dirs, axis=1, keepdims=True) + 1e-10)
                        kicks = kick_dirs * kick_mag[:, None]
                        # Apply to velocities
                        if use_jax:
                            vel_np = np.array(vel_j)
                            vel_np[hot_global_idx] += kicks.astype(np.float32)
                            vel_j = jnp.array(vel_np, dtype=jnp.float32)
                        else:
                            vel[hot_global_idx] += kicks
                        if step % (rebuild_every * 5) == 0:
                            print(f"    Ionization heating: {n_hot}/{len(bgs_idx)} BGS vertices, "
                                  f"mean kick={float(np.mean(kick_mag)):.6f}")

            if use_jax:
                ii_j = jnp.array(ii, dtype=jnp.int32)
                jj_j = jnp.array(jj, dtype=jnp.int32)
                stiff_j = jnp.array(pair_stiffness, dtype=jnp.float32)
                ideal_j = jnp.array(pair_ideal, dtype=jnp.float32)
                asym_j = jnp.array(pair_asymmetry, dtype=jnp.float32)
                gate_j = jnp.array(strain_gate, dtype=jnp.float32)
                depth_j = jnp.array(pair_depth, dtype=jnp.float32)
                fill_j = jnp.zeros(M, dtype=jnp.float32)
                step_fn = _make_jax_step(N, M, parker_spiral=use_parker)
                expn_j = jnp.array(cumulative_expansion, dtype=jnp.float32)
                pos_j, vel_j, _, fill_j, _, _ = step_fn(pos_j, vel_j, ii_j, jj_j, stiff_j, ideal_j,
                                           asym_j, expn_j, jnp.float32(dt), jnp.float32(damp_now),
                                           gate_j, spin_j, jnp.float32(vortex_strength),
                                           depth_j, fill_j, jnp.float32(fill_on),
                                           jnp.float32(gate_drag), jnp.float32(1.0 if orbital_mode else 0.0),
                                           tsilver_j, tgold_j,
                                           jnp.float32(photon_rate), jnp.float32(sound_rate),
                                           jnp.float32(speed_ratio))
                pos_j.block_until_ready()
            else:
                pair_fill = np.zeros(M, dtype=np.float32)

        # Update expansion for JAX
        if use_jax:
            expn_j = jnp.array(cumulative_expansion, dtype=jnp.float32)

        # Well-fill only activates after thermal phase (and only if enabled)
        fill_on = 1.0 if (well_fill and step > (thermal_steps + cool_steps)) else 0.0

        # Step (using thermal-ramped damping)
        if use_jax:
            pos_j, vel_j, strain, fill_j, mean_fill, mean_drag = step_fn(
                pos_j, vel_j, ii_j, jj_j, stiff_j, ideal_j,
                asym_j, expn_j, jnp.float32(dt), jnp.float32(damp_now),
                gate_j, spin_j, jnp.float32(vortex_strength),
                depth_j, fill_j, jnp.float32(fill_on),
                jnp.float32(gate_drag), jnp.float32(1.0 if orbital_mode else 0.0),
                tsilver_j, tgold_j,
                jnp.float32(photon_rate), jnp.float32(sound_rate),
                jnp.float32(speed_ratio))
        else:
            pos, vel, strain, pair_fill, mean_fill, mean_drag = step_fn(
                pos, vel, ii, jj, pair_stiffness, pair_ideal,
                pair_asymmetry, cumulative_expansion, dt, damp_now,
                strain_gate, spin_ax, vortex_strength, pair_depth, pair_fill, fill_on,
                gate_drag, 1.0 if orbital_mode else 0.0,
                type_silver, type_gold, photon_rate, sound_rate, speed_ratio)

        # Save frame
        if step % save_every == 0:
            if use_jax:
                frame_np = np.array(pos_j)
                strain_val = float(strain)
                fill_val = float(mean_fill)
            else:
                frame_np = pos.copy()
                strain_val = float(strain)
                fill_val = float(mean_fill)

            frames.append(frame_np)
            steps_list.append(step)
            strain_list.append(strain_val)
            fill_list.append(fill_val)

            if callback:
                callback(step, n_steps, {'total_strain': strain_val,
                                         'mean_fill': fill_val})

        # Progress
        if step % max(1, n_steps // 10) == 0:
            elapsed = time.time() - t_start
            s_val = float(strain) if use_jax else float(strain)
            f_val = float(mean_fill)
            d_val = float(mean_drag) if gate_drag > 0 else 0
            drag_str = f"  drag={d_val:.4f}" if gate_drag > 0 else ""
            print(f"  Step {step:5d}/{n_steps}: strain={s_val:.4f}  fill={f_val:.3f}{drag_str}  [{elapsed:.1f}s]")

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

    # Extract final bond state and velocities (numpy arrays, not JAX)
    final_vel = np.array(vel_j) if use_jax else vel.copy()
    final_pair_fill = np.array(fill_j) if use_jax else pair_fill.copy()

    return {
        'frames': frames,
        'steps': steps_list,
        'strain': strain_list,
        'fill': fill_list,
        'types': types,
        'type_ids': type_ids.tolist(),
        # ── Bond state (the entanglement graph) ──────────────────
        'final_vel': final_vel,                          # (N, 3) float32 — final velocities
        'pairs': pairs,                              # (M, 2) int — neighbor topology
        'pair_depth': pair_depth.copy(),              # (M,) float32 — Cantor bracket depth
        'pair_fill': final_pair_fill,                 # (M,) float32 — well-fill settlement
        'strain_gate': strain_gate.copy(),            # (M,) float32 — 0/1 gating
        'n_settled': n_settled,
        'n_active': n_active,
        'params': {
            'N': N,
            'n_steps': n_steps,
            'bracket': bracket,
            'dt': dt,
            'damping': damping,
            'mean_spacing': mean_spacing,
            'disc_exponent': disc_exponent,
            'thermal_frac': thermal_frac,
            'vortex_strength': vortex_strength,
            'jax': use_jax,
            'device': str(_dev) if use_jax else 'cpu',
        },
    }


def compute_metrics_from_bonds(positions, types_list, pairs, pair_depth,
                                pair_fill, strain_gate, n_settled=0, n_active=0):
    """Compute galaxy metrics from existing bond state (no KDTree rebuild).

    Uses the pairs array as the neighbor graph instead of building a new
    KDTree. For gamma, subsamples BGS positions (safe at any scale).
    """
    from scipy.spatial.distance import pdist

    type_arr = np.array(types_list)
    bgs_mask = (type_arr == 'BGS')
    bgs_pos = positions[bgs_mask]
    n_bgs = len(bgs_pos)
    N = len(positions)

    if n_bgs < 5:
        return {'composite_score': 0, 'n_bgs': n_bgs, 'error': 'too few BGS'}

    # ── Gamma: two-point correlation (subsampled, safe at 100K+) ──
    sample = bgs_pos[:min(n_bgs, 3000)]
    dists = pdist(sample)
    r_max = np.percentile(dists, 60)
    n_bins = 40
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

    # ── Shape: PCA eigenvalues ────────────────────────────────────
    centered = bgs_pos - bgs_pos.mean(axis=0)
    cov = np.cov(centered.T) if n_bgs > 3 else np.eye(3)
    eigvals = np.sort(np.linalg.eigvalsh(cov))
    ca_ratio = np.sqrt(eigvals[0] / (eigvals[2] + 1e-15))
    ba_ratio = np.sqrt(eigvals[1] / (eigvals[2] + 1e-15))

    # ── Neighbor counts from pairs (O(M), no KDTree) ─────────────
    nbr_counts = np.zeros(N, dtype=np.int32)
    np.add.at(nbr_counts, pairs[:, 0], 1)
    np.add.at(nbr_counts, pairs[:, 1], 1)
    bgs_nbrs = nbr_counts[bgs_mask]

    void_frac = float(np.mean(bgs_nbrs == 0))
    contrast = float(bgs_nbrs.max()) / max(float(np.mean(bgs_nbrs)), 0.01)
    fil_frac = float(np.mean(bgs_nbrs == 2))

    # ── m2 Fourier mode (spiral arm signal) ───────────────────────
    com = np.mean(bgs_pos, axis=0)
    r_vec = bgs_pos - com
    _, _, Vt = np.linalg.svd(r_vec - r_vec.mean(axis=0))
    normal = Vt[2]
    proj = r_vec - np.outer(r_vec @ normal, normal)
    angles = np.arctan2(proj[:, 1], proj[:, 0])
    c2 = np.mean(np.cos(2 * angles))
    s2 = np.mean(np.sin(2 * angles))
    m2 = float(np.sqrt(c2**2 + s2**2))

    # ── Composite score ───────────────────────────────────────────
    gamma_target = 1.77
    gamma_dev = abs(gamma - gamma_target) / gamma_target
    gamma_score = max(0, min(20, 20 * (1 - gamma_dev)))

    ca_target = 1.0 / PHI**0.5  # 1/√φ ≈ 0.786
    ca_dev = abs(ca_ratio - ca_target) / ca_target
    shape_score = max(0, min(20, 20 * (1 - ca_dev)))

    contrast_target = max(2.0, min(4.0, 1.0 + np.log2(max(n_bgs, 5))))
    contrast_score = max(0, min(15, 15 * min(contrast / contrast_target, 1.0)))

    void_score = max(0, min(15, 15 * min(void_frac / 0.08, 1.0) if void_frac <= 0.20
                     else 15 * (1 - (void_frac - 0.20) / 0.80)))
    fil_score = max(0, min(15, 15 * min(fil_frac / 0.05, 1.0)))

    dists_from_center = np.linalg.norm(centered, axis=1)
    extent = float(np.percentile(dists_from_center, 90))
    R_MATTER_FRAC = 0.0728
    R_OUTER_FRAC = 0.5594
    core_frac = float(np.mean(dists_from_center < extent * R_MATTER_FRAC / R_OUTER_FRAC))
    core_score = max(0, min(15, 15 * min(core_frac / 0.10, 1.0)))

    composite = gamma_score + shape_score + contrast_score + void_score + fil_score + core_score

    return {
        'composite_score': float(composite),
        'gamma': float(gamma),
        'ca_ratio': float(ca_ratio),
        'ba_ratio': float(ba_ratio),
        'contrast': float(contrast),
        'void_frac': float(void_frac),
        'filament_frac': float(fil_frac),
        'core_frac': float(core_frac),
        'm2': float(m2),
        'n_bgs': n_bgs,
        'n_settled': n_settled,
        'n_active': n_active,
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
