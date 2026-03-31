#!/usr/bin/env python3
"""
T52 Galaxy Evolution v2 — Persistent Bonds + Bronze Retyping + σ₄ Shell
========================================================================

Changes from v1:
    1. BRONZE RETYPING: Pure B vertices (14.4%, zero coupling to BGS) are
       retyped to BG or BS based on local gold/silver neighbor balance.
       Bronze is emergent (Δ₃=13 = Δ₁=5 + Δ₂=8) — pure B is unphysical.

    2. PERSISTENT BONDS: Strong bonds (stiffness > LEAK) are tracked across
       evolution segments. Between segments, vertices with structural bonds
       that drifted apart are nudged back into bonding range so the KDTree
       rebuild reconnects them. This prevents wall destruction.

    3. σ₄ SHELL POTENTIAL: BGS vertices receive a gentle radial nudge toward
       the σ₄ outer wall (0.559R) between segments. BGS should accumulate
       there because the 23-faced heptahedral cell IS the outer wall.

The evolution runs in segments (default 5000 steps each). Between segments:
    - Structural bonds are identified and preserved
    - BGS vertices are nudged toward σ₄
    - Velocities carry forward for continuity

Usage:
    PYTHONUNBUFFERED=1 caffeinate -i python3 simulation/t52_standalone_v2.py
    python3 simulation/t52_standalone_v2.py --steps 25000 --segment 5000

© 2026 Thomas A. Husmann / iBuilt LTD. Patent App. 19/560,637.
"""

import argparse
import json
import os
import sys
import time

import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from jax_evolve import (
    evolve_jax, PHI, W, LEAK, R_C, SILVER_TAX,
    STIFFNESS_MATRIX, TYPE_TO_ID, TYPE_ORDER,
    build_neighbor_pairs,
)

# ── Constants ──────────────────────────────────────────────────────
SQRT3 = 1.7320508
SIGMA3 = 0.0728    # core
SIGMA2 = 0.2350    # inner wall
SIGMA_SHELL = 0.3972
SIGMA4 = 0.5594    # outer wall
COS_ALPHA = 0.3672 # decoupling surface


# ═══════════════════════════════════════════════════════════════════
# 1. BRONZE RETYPING
# ═══════════════════════════════════════════════════════════════════

def retype_pure_bronze(positions, types_list, nn_multiplier=1.6):
    """Retype pure B vertices to BG or BS based on local environment.

    Bronze is emergent: Δ₃ = 13 = Δ₁(gold=5) + Δ₂(silver=8).
    Pure B should not exist as a standalone type. Each B vertex is
    retyped based on the gold/silver balance of its neighbors:

        gold_count >= silver_count → BG (gravity conduit)
        silver_count > gold_count  → BS (strong force carrier)

    Returns new types_list with zero pure B vertices.
    """
    types_out = list(types_list)
    b_indices = [i for i, t in enumerate(types_out) if t == 'B']

    if not b_indices:
        print("  No pure B vertices to retype")
        return types_out

    # Build neighbor graph
    pairs, threshold = build_neighbor_pairs(positions, nn_multiplier)

    # Build adjacency: for each vertex, list of neighbor indices
    adj = {i: [] for i in range(len(positions))}
    for i, j in pairs:
        adj[i].append(j)
        adj[j].append(i)

    # Gold and silver containing types
    gold_types = {'G', 'BG', 'GS', 'BGS'}
    silver_types = {'S', 'BS', 'GS', 'BGS'}

    n_to_bg = 0
    n_to_bs = 0

    for idx in b_indices:
        neighbors = adj.get(idx, [])
        gold_count = sum(1 for n in neighbors if types_out[n] in gold_types)
        silver_count = sum(1 for n in neighbors if types_out[n] in silver_types)

        if gold_count >= silver_count:
            types_out[idx] = 'BG'
            n_to_bg += 1
        else:
            types_out[idx] = 'BS'
            n_to_bs += 1

    print(f"  Bronze retyping: {len(b_indices)} pure B → {n_to_bg} BG + {n_to_bs} BS")
    return types_out


# ═══════════════════════════════════════════════════════════════════
# 2. PERSISTENT BOND TRACKING
# ═══════════════════════════════════════════════════════════════════

def identify_structural_bonds(pairs, type_ids, pair_fill,
                              stiffness_threshold=None, fill_threshold=0.1):
    """Identify bonds that should persist across rebuilds.

    A structural bond has:
        - Stiffness > LEAK (not a vacuum bond)
        - Fill > fill_threshold (even slightly settled counts)

    For very strong bonds (stiffness > R_C, i.e. BGS-BGS and BGS-BS),
    we keep them regardless of fill — they are always structural.

    Returns set of (i, j) tuples (sorted).
    """
    if stiffness_threshold is None:
        stiffness_threshold = LEAK

    structural = set()
    for k in range(len(pairs)):
        i, j = int(pairs[k, 0]), int(pairs[k, 1])
        ti, tj = type_ids[i], type_ids[j]
        stiff = STIFFNESS_MATRIX[ti, tj]
        # Very strong bonds (BGS-BGS=1.0, BGS-BS=0.854) always persist
        if stiff >= R_C:
            structural.add((min(i, j), max(i, j)))
        # Moderate bonds persist if partially settled
        elif stiff > stiffness_threshold and pair_fill[k] > fill_threshold:
            structural.add((min(i, j), max(i, j)))
    return structural


def enforce_structural_bonds(positions, structural_bonds, threshold,
                             max_nudge_frac=0.05):
    """Nudge vertices with structural bonds back into KDTree bonding range.

    For each structural bond (i, j), if the pair has drifted beyond the
    neighbor threshold, apply a symmetric nudge to bring them within range.
    This ensures the KDTree rebuild will reconnect them.

    max_nudge_frac: maximum displacement as fraction of threshold distance.
    """
    n_nudged = 0
    max_nudge = threshold * max_nudge_frac

    for (i, j) in structural_bonds:
        if i >= len(positions) or j >= len(positions):
            continue
        dr = positions[j] - positions[i]
        dist = np.linalg.norm(dr)
        if dist > threshold * 0.95:  # approaching or beyond threshold
            # Nudge both vertices toward each other
            overshoot = dist - threshold * 0.85  # target 85% of threshold
            if overshoot > 0:
                nudge = min(overshoot * 0.5, max_nudge)
                direction = dr / (dist + 1e-15)
                positions[i] += direction * nudge
                positions[j] -= direction * nudge
                n_nudged += 1

    return n_nudged


# ═══════════════════════════════════════════════════════════════════
# 3. σ₄ SHELL POTENTIAL FOR BGS
# ═══════════════════════════════════════════════════════════════════

def apply_sigma4_potential(positions, types_list, strength=0.01):
    """Apply gentle radial nudge pushing BGS toward the σ₄ shell.

    Physics: BGS cells have 23 faces that merge into 7 coarse faces
    (heptahedron). This outer wall IS σ₄ at 0.559R. BGS should
    accumulate there, not scatter freely.

    Only affects BGS vertices outside the σ₂ inner wall (we don't
    want to disturb the core).

    strength: nudge magnitude as fraction of position error per call.
    """
    bgs_mask = np.array([t == 'BGS' for t in types_list])
    if np.sum(bgs_mask) < 5:
        return 0

    # Use 95th percentile of ALL vertices as R
    com = np.mean(positions, axis=0)
    r_all = np.sqrt(np.sum((positions - com)**2, axis=1))
    R_total = np.percentile(r_all, 95)

    r_sigma4 = R_total * SIGMA4
    r_sigma2 = R_total * SIGMA2

    bgs_indices = np.where(bgs_mask)[0]
    n_nudged = 0

    for idx in bgs_indices:
        r_vec = positions[idx] - com
        r = np.linalg.norm(r_vec)

        if r < r_sigma2 or r < 1e-10:
            continue  # don't disturb core BGS

        # Fractional error from σ₄ target
        error = (r_sigma4 - r) / r_sigma4
        # Gentle nudge proportional to error
        nudge = r_vec / r * error * r * strength
        positions[idx] += nudge
        n_nudged += 1

    return n_nudged


# ═══════════════════════════════════════════════════════════════════
# 4. ANALYSIS HELPERS (inlined from v1)
# ═══════════════════════════════════════════════════════════════════

def classify_shape(eigenvalues):
    e = sorted(eigenvalues, reverse=True)
    r12 = e[1] / (e[0] + 1e-15)
    r13 = e[2] / (e[0] + 1e-15)
    if r13 > 0.7:
        return 'sphere'
    elif r12 > 0.7 and r13 < 0.4:
        return 'oblate' if r13 < 0.3 else 'disc'
    elif r12 < 0.4:
        return 'prolate' if r13 < 0.3 else 'filament'
    return 'triaxial'


def compute_shape(positions, types_list):
    bgs_mask = np.array([t == 'BGS' for t in types_list])
    pts = positions[bgs_mask] if np.sum(bgs_mask) > 5 else positions
    centered = pts - pts.mean(axis=0)
    cov = np.cov(centered.T)
    evals = np.sort(np.linalg.eigvalsh(cov))[::-1]
    return evals, classify_shape(evals)


def compute_m2(positions, types_list):
    bgs_mask = np.array([t == 'BGS' for t in types_list])
    bgs_pos = positions[bgs_mask]
    if len(bgs_pos) < 10:
        return 0.0
    com = np.mean(bgs_pos, axis=0)
    r = bgs_pos - com
    _, _, Vt = np.linalg.svd(r - r.mean(axis=0))
    normal = Vt[2]
    proj = r - np.outer(r @ normal, normal)
    angles = np.arctan2(proj[:, 1], proj[:, 0])
    c2 = np.mean(np.cos(2 * angles))
    s2 = np.mean(np.sin(2 * angles))
    return float(np.sqrt(c2**2 + s2**2))


def analyze_shells(positions, types_list):
    """Measure radial shell structure and compare to Cantor node."""
    com = np.mean(positions, axis=0)
    r = np.sqrt(np.sum((positions - com)**2, axis=1))
    R = np.percentile(r, 95)

    shells = {}
    for t in ['BGS', 'BG', 'GS', 'BS', 'G', 'B', 'S']:
        mask = np.array([tt == t for tt in types_list])
        n = np.sum(mask)
        if n > 0:
            rr = r[mask]
            shells[t] = {
                'n': int(n),
                'r_median': float(np.median(rr)),
                'r_frac': float(np.median(rr) / R) if R > 0 else 0,
            }

    return shells, float(R)


def render(pos, types_list, name, outdir):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    color_map = {
        'BGS': '#FFD700', 'BG': '#FF8C00', 'GS': '#4169E1',
        'BS': '#6A5ACD', 'G': '#FFA500', 'B': '#CD853F', 'S': '#1E90FF',
    }
    type_sizes = {
        'BGS': 8, 'BG': 2, 'GS': 4, 'BS': 3, 'G': 1.5, 'B': 1, 'S': 6,
    }
    colors = [color_map.get(t, '#FFFFFF') for t in types_list]
    sizes = [type_sizes.get(t, 2) for t in types_list]

    centered = pos - pos.mean(axis=0)
    cov = np.cov(centered.T)
    eigvals, eigvecs = np.linalg.eigh(cov)
    order = np.argsort(eigvals)[::-1]
    axes = eigvecs[:, order].T

    com = pos.mean(axis=0)
    rel = pos - com
    x = rel @ axes[0]
    y = rel @ axes[1]
    lim = np.percentile(np.abs(np.concatenate([x, y])), 95) * 1.3

    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    ax.scatter(x, y, c=colors, s=sizes, alpha=0.6)
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_title(name, fontsize=12, color='white')
    ax.set_aspect('equal')
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')
    ax.tick_params(colors='gray')
    path = os.path.join(outdir, f"{name}.png")
    fig.savefig(path, dpi=150, facecolor='black', bbox_inches='tight')
    plt.close(fig)
    return path


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.floating, np.integer)):
            return float(obj)
        return super().default(obj)


# ═══════════════════════════════════════════════════════════════════
# 5. DATA LOADING
# ═══════════════════════════════════════════════════════════════════

def load_initial_state(input_path=None):
    """Load initial vertex positions and types (same as v1)."""
    if input_path and os.path.exists(input_path):
        if input_path.endswith('.npz'):
            data = np.load(input_path, allow_pickle=True)
            print(f"  Loaded from {input_path}")
            return data['positions'], list(data['types'])
        elif input_path.endswith('.json'):
            with open(input_path) as f:
                g = json.load(f)
            print(f"  Loaded from {input_path}")
            return np.array(g['positions']), g['types']

    repo_root = os.path.dirname(SCRIPT_DIR)
    g1733_path = os.path.join(repo_root, 'results/universe/clusters/g1733.json')
    if os.path.exists(g1733_path):
        with open(g1733_path) as f:
            g = json.load(f)
        print(f"  Loaded from {g1733_path}")
        return np.array(g['positions']), g['types']

    for search_dir in [
        os.path.join(repo_root, 'results/candidates/T52_heavy_damp'),
        os.path.join(repo_root, 'results/t52_reproduce'),
    ]:
        for fname in ['T52_step20000.npz', 'T52_step05000.npz']:
            path = os.path.join(search_dir, fname)
            if os.path.exists(path):
                data = np.load(path, allow_pickle=True)
                print(f"  Loaded from {path}")
                return data['positions'], list(data['types'])

    raise FileNotFoundError("No initial state found.")


# ═══════════════════════════════════════════════════════════════════
# 6. SEGMENTED EVOLUTION
# ═══════════════════════════════════════════════════════════════════

def evolve_v2(positions, types_list, total_steps=25000, segment_steps=5000,
              sigma4_strength=0.01, bond_fill_threshold=0.3,
              save_every=5000, no_render=False, outdir='results/t52_v2'):
    """Run T52 evolution with v2 enhancements.

    1. Retype pure B → BG/BS (once, before evolution)
    2. Evolve in segments of segment_steps
    3. Between segments: preserve structural bonds, nudge BGS toward σ₄
    4. Pass velocities forward for continuity

    Returns (frames, metrics, types_v2).
    """
    os.makedirs(outdir, exist_ok=True)

    # ── Step 1: Retype bronze ──────────────────────────────────────
    print("\n  STEP 1: Bronze retyping")
    types_v2 = retype_pure_bronze(positions, types_list)

    from collections import Counter
    counts = Counter(types_v2)
    for t in ['BGS', 'BG', 'GS', 'BS', 'G', 'B', 'S']:
        c = counts.get(t, 0)
        if c > 0:
            print(f"    {t:>3}: {c:>5} ({100*c/len(types_v2):5.1f}%)")

    type_ids = np.array([TYPE_TO_ID[t] for t in types_v2], dtype=np.int32)

    # ── Step 2: Segmented evolution ────────────────────────────────
    n_segments = max(1, (total_steps + segment_steps - 1) // segment_steps)
    pos = positions.copy()
    vel = None
    structural_bonds = set()
    threshold = None  # will be set after first segment

    all_frames = []
    all_metrics = []
    steps_done = 0

    print(f"\n  STEP 2: Segmented evolution ({n_segments} segments × {segment_steps} steps)")
    t_total = time.time()

    for seg_i in range(n_segments):
        n_this = min(segment_steps, total_steps - steps_done)
        seg_label = f"Segment {seg_i+1}/{n_segments}"

        print(f"\n  {'─'*50}")
        print(f"  {seg_label}: steps {steps_done+1}–{steps_done+n_this}")

        # Run evolution segment
        t0 = time.time()
        result = evolve_jax(
            pos.copy(),
            np.array(types_v2),
            n_steps=n_this,
            vortex_strength=0.002,
            well_fill=True,
            damping=0.9997,
            perturbation=0.001 if seg_i == 0 else 0.0,
            resume=True,
            save_every=save_every if save_every <= n_this else n_this,
            gate_drag=1.0,
            orbital_mode=True,
            photon_rate=1.618,
            sound_rate=1.0,
            speed_ratio=SQRT3,
            parker_spiral=False,
            initial_velocities=vel,
        )
        seg_time = time.time() - t0
        print(f"  {seg_label}: completed in {seg_time:.0f}s")

        # Extract state
        pos = result['frames'][-1].copy()
        vel = result['final_vel'].copy()
        pairs = result['pairs']
        pair_fill = result['pair_fill']

        # Update threshold from the pairs
        if len(pairs) > 0:
            dr = pos[pairs[:, 1]] - pos[pairs[:, 0]]
            dists = np.sqrt(np.sum(dr**2, axis=1))
            threshold = float(np.max(dists)) * 1.05

        # ── Between-segment processing ─────────────────────────────
        # 2z. Clamp extreme outliers to prevent pair explosion
        # Vacuum bonds expand vertices far from core. If we pass these
        # expanded positions to the next evolve_jax call, KDTree computes
        # mean_NN from ALL vertices (including far outliers) → huge threshold
        # → millions of pairs → OOM. Clamp outliers to 3× the 95th percentile.
        com = np.mean(pos, axis=0)
        r_from_com = np.sqrt(np.sum((pos - com)**2, axis=1))
        r95 = np.percentile(r_from_com, 95)
        outlier_mask = r_from_com > 3.0 * r95
        if np.any(outlier_mask):
            n_out = np.sum(outlier_mask)
            for idx in np.where(outlier_mask)[0]:
                direction = (pos[idx] - com) / (r_from_com[idx] + 1e-15)
                pos[idx] = com + direction * 3.0 * r95
                vel[idx] *= 0.1  # damp outlier velocity
            print(f"  Outlier clamping: {n_out} vertices pulled back to 3×R95={3*r95:.1f}")

        # 2a. Identify and preserve structural bonds
        new_structural = identify_structural_bonds(
            pairs, type_ids, pair_fill,
            fill_threshold=bond_fill_threshold)
        n_new = len(new_structural - structural_bonds)
        structural_bonds |= new_structural
        print(f"  Structural bonds: {len(structural_bonds)} total (+{n_new} new)")

        # 2b. Enforce structural bond proximity
        if threshold and structural_bonds:
            n_nudged = enforce_structural_bonds(pos, structural_bonds, threshold)
            if n_nudged > 0:
                print(f"  Bond enforcement: {n_nudged} pairs nudged back into range")

        # 2c. Apply σ₄ shell potential to BGS
        n_shell_nudged = apply_sigma4_potential(pos, types_v2, strength=sigma4_strength)
        if n_shell_nudged > 0:
            print(f"  σ₄ potential: {n_shell_nudged} BGS vertices nudged toward shell")

        # ── Collect frames and metrics ─────────────────────────────
        seg_steps = result['steps']  # [0, save_every, 2*save_every, ..., n_this]
        for fi, frame in enumerate(result['frames']):
            seg_step = seg_steps[fi]
            if seg_step == 0 and seg_i > 0:
                continue  # skip duplicate initial frame on segment restart
            step = steps_done + seg_step
            if step == 0:
                continue  # skip initial state (already saved)
            all_frames.append((step, frame))

            evals, shape = compute_shape(frame, types_v2)
            es = sorted(evals, reverse=True)
            ca = es[2] / (es[0] + 1e-15)
            m2 = compute_m2(frame, types_v2)
            metrics = {'step': step, 'ca': float(ca), 'm2': float(m2), 'shape': shape}
            all_metrics.append(metrics)
            print(f"    [{step:>6}] c/a={ca:.3f}  m2={m2:.3f}  {shape}")

            # Save checkpoint
            fname = f"T52v2_step{step:05d}"
            np.savez(os.path.join(outdir, f"{fname}.npz"),
                     positions=frame, types=types_v2, step=step)
            if not no_render:
                render(frame, types_v2, fname, outdir)

        steps_done += n_this

    elapsed_total = time.time() - t_total

    # ── Shell analysis on final state ──────────────────────────────
    print(f"\n  {'─'*50}")
    print(f"  SHELL ANALYSIS (final state)")
    shells, R_total = analyze_shells(pos, types_v2)
    print(f"  R_total (95th pctile): {R_total:.2f}")
    print(f"  {'Type':>3}  {'n':>5}  {'r_med':>8}  {'r/R':>6}  {'Cantor':>8}")
    cantor_targets = {'BGS': SIGMA4, 'BG': SIGMA2, 'GS': SIGMA2,
                      'BS': None, 'G': SIGMA_SHELL, 'S': SIGMA3}
    for t in ['S', 'BS', 'GS', 'BG', 'G', 'BGS']:
        if t in shells:
            s = shells[t]
            target = cantor_targets.get(t)
            target_str = f"σ={target:.3f}" if target else "—"
            print(f"  {t:>3}  {s['n']:>5}  {s['r_median']:>8.2f}  "
                  f"{s['r_frac']:>6.3f}  {target_str:>8}")

    return all_frames, all_metrics, types_v2, elapsed_total


# ═══════════════════════════════════════════════════════════════════
# 7. MAIN
# ═══════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description='T52 Galaxy Evolution v2 — Persistent Bonds + Bronze Retyping',
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--steps', type=int, default=25000,
                        help='Total evolution steps (default: 25000)')
    parser.add_argument('--segment', type=int, default=5000,
                        help='Steps per segment (default: 5000)')
    parser.add_argument('--save-every', type=int, default=5000,
                        help='Save checkpoint every N steps (default: 5000)')
    parser.add_argument('--outdir', type=str, default='results/t52_v2',
                        help='Output directory')
    parser.add_argument('--input', type=str, default=None,
                        help='Path to initial positions (JSON or NPZ)')
    parser.add_argument('--no-render', action='store_true',
                        help='Skip image rendering')
    parser.add_argument('--sigma4-strength', type=float, default=0.01,
                        help='σ₄ shell potential strength (default: 0.01)')
    parser.add_argument('--bond-threshold', type=float, default=0.3,
                        help='Fill threshold for structural bonds (default: 0.3)')
    args = parser.parse_args()

    # ── Load ───────────────────────────────────────────────────────
    print("Loading initial state...")
    positions, types_list = load_initial_state(args.input)
    print(f"  {len(positions)} vertices")

    from collections import Counter
    counts_before = Counter(types_list)
    print(f"\n  Type distribution (before retyping):")
    for t in ['BGS', 'BG', 'GS', 'BS', 'G', 'B', 'S']:
        c = counts_before.get(t, 0)
        if c > 0:
            print(f"    {t:>3}: {c:>5} ({100*c/len(types_list):5.1f}%)")

    # ── Initial metrics ────────────────────────────────────────────
    evals0, shape0 = compute_shape(positions, types_list)
    es0 = sorted(evals0, reverse=True)
    ca0 = es0[2] / (es0[0] + 1e-15)
    m2_0 = compute_m2(positions, types_list)
    print(f"\n  Initial: c/a={ca0:.3f}  m2={m2_0:.3f}  {shape0}")

    # ── Run v2 evolution ───────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"  T52 v2 — PERSISTENT BONDS + BRONZE RETYPING + σ₄ SHELL")
    print(f"  Steps: {args.steps}  Segments: {args.steps // args.segment}")
    print(f"  σ₄ strength: {args.sigma4_strength}")
    print(f"  Bond persistence fill threshold: {args.bond_threshold}")
    print(f"{'='*60}")

    frames, metrics, types_v2, elapsed = evolve_v2(
        positions, types_list,
        total_steps=args.steps,
        segment_steps=args.segment,
        sigma4_strength=args.sigma4_strength,
        bond_fill_threshold=args.bond_threshold,
        save_every=args.save_every,
        no_render=args.no_render,
        outdir=args.outdir,
    )

    # ── Final summary ──────────────────────────────────────────────
    if metrics:
        final = metrics[-1]
        print(f"\n{'='*60}")
        print(f"  T52 v2 RESULTS")
        print(f"{'='*60}")
        print(f"  Initial:  c/a={ca0:.3f}  m2={m2_0:.3f}  {shape0}")
        print(f"  Final:    c/a={final['ca']:.3f}  m2={final['m2']:.3f}  {final['shape']}")
        print(f"  Time:     {elapsed:.0f}s")
        print(f"{'='*60}")

    # Save summary
    summary = {
        'recipe': 'T52_v2',
        'changes': [
            'Bronze retyping (pure B → BG/BS)',
            'Persistent structural bonds across rebuilds',
            'σ₄ shell potential for BGS accumulation',
        ],
        'n_vertices': len(positions),
        'n_steps': args.steps,
        'segment_steps': args.segment,
        'elapsed_seconds': round(elapsed, 1),
        'initial': {'ca': float(ca0), 'm2': float(m2_0), 'shape': shape0},
        'final': dict(final) if metrics else {},
        'type_distribution_v2': dict(Counter(types_v2)),
        'frames': metrics,
    }
    results_path = os.path.join(args.outdir, 'results.json')
    with open(results_path, 'w') as f:
        json.dump(summary, f, indent=2, cls=NpEncoder)
    print(f"  Results: {results_path}")
    print(f"  Images:  {args.outdir}/")


if __name__ == '__main__':
    main()
