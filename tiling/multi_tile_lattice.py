"""
multi_tile_lattice.py — Monte Carlo Heptahedral Tiling Simulation
=================================================================

Grows heptahedral tilings outward from a seed, layer by layer.
Uses Monte Carlo sampling: for each open face, collects ALL allowed
orientations and picks one uniformly at random.

Three rule sets tested:
  LOOSE  — only 3 forbidden pairs (G↔B, G↔BG, G↔BGS)
  STRICT — forbidden + neutral = 11 pairs blocked, 17 allowed
  PHYSICS — only same-type and Ward-identity junctions

Tracks how forbidden constraints scale across lattice depth and
whether the effective orientation count converges to 13 = F(7).

Run:  python3 tiling/multi_tile_lattice.py
"""

import sys
import os
import math
import numpy as np
from collections import defaultdict, Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEAN = os.path.join(ROOT, 'CLEAN')
sys.path.insert(0, CLEAN)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from core.constants import PHI
from heptahedron import (
    FACE_NAMES, FACE_FORCE,
    ALLOWED_JUNCTIONS, FORBIDDEN_JUNCTIONS,
    get_face_fractions, icosahedral_axes, select_7_normals,
    _icosahedral_rotations,
)


# ═════════════════════════════════════════════════════════════════
# JUNCTION LOGIC — Three Rule Sets
# ═════════════════════════════════════════════════════════════════

def make_junction_checker(mode='loose'):
    """Return a function (a, b) → bool (True if allowed).

    Modes:
      'loose'   — only FORBIDDEN pairs blocked (3 pairs)
      'strict'  — only ALLOWED pairs permitted (17 pairs)
      'physics' — tighter: same-type + direct Ward-identity only
    """
    if mode == 'loose':
        def check(a, b):
            pair, rev = (a, b), (b, a)
            return pair not in FORBIDDEN_JUNCTIONS and rev not in FORBIDDEN_JUNCTIONS
        return check

    elif mode == 'strict':
        def check(a, b):
            pair, rev = (a, b), (b, a)
            return pair in ALLOWED_JUNCTIONS or rev in ALLOWED_JUNCTIONS
        return check

    elif mode == 'physics':
        # Tightest physically motivated rules:
        # Same-type always ok, cross-type only if they share a letter
        # (G↔GS ok because both have G, but S↔BG not ok)
        def shares_letter(a, b):
            sa, sb = set(a), set(b)
            # Special: single letters G,S,B are sets of one char
            # Compound: GS={G,S}, BG={B,G}, BS={B,S}, BGS={B,G,S}
            # We check if the LABELS share a component
            labels_a = set()
            labels_b = set()
            for lbl, s in [('G', a), ('S', a), ('B', a)]:
                if lbl in s:
                    labels_a.add(lbl)
            for lbl, s in [('G', b), ('S', b), ('B', b)]:
                if lbl in s:
                    labels_b.add(lbl)
            return bool(labels_a & labels_b)

        def check(a, b):
            if a == b:
                return True
            return shares_letter(a, b)
        return check

    raise ValueError(f"Unknown mode: {mode}")


# ═════════════════════════════════════════════════════════════════
# PRECOMPUTE ROTATION DATA
# ═════════════════════════════════════════════════════════════════

def precompute_rotation_tables(normals):
    """For each of 60 rotations, compute face signature and anti-face map."""
    rotations = _icosahedral_rotations()
    normal_array = np.array([normals[name] for name in FACE_NAMES])
    tables = []

    for R in rotations:
        rotated = (R @ normal_array.T).T

        # Face signature: which original face type is at each position
        signature = []
        for i in range(7):
            dots = np.abs(normal_array @ rotated[i])
            signature.append(int(np.argmax(dots)))

        # Anti-face map: for each face of central tile, which face of
        # this rotated tile is anti-parallel (the touching face)?
        anti_map = {}
        for i in range(7):
            dots = rotated @ normal_array[i]
            j = int(np.argmin(dots))
            if dots[j] < -0.3:
                anti_map[i] = (j, signature[j])

        tables.append({
            'sig_names': tuple(FACE_NAMES[s] for s in signature),
            'anti_map': anti_map,
        })

    return tables


# ═════════════════════════════════════════════════════════════════
# TILE
# ═════════════════════════════════════════════════════════════════

class Tile:
    __slots__ = ['tile_id', 'rot_idx', 'sig_names', 'layer',
                 'neighbors', 'position']

    def __init__(self, tile_id, rot_idx, sig_names, layer, position):
        self.tile_id = tile_id
        self.rot_idx = rot_idx
        self.sig_names = sig_names
        self.layer = layer
        self.neighbors = {}
        self.position = position

    def face_type(self, fp):
        return self.sig_names[fp]

    def open_faces(self):
        return [i for i in range(7) if i not in self.neighbors]


# ═════════════════════════════════════════════════════════════════
# MONTE CARLO TILING GROWTH
# ═════════════════════════════════════════════════════════════════

def mc_grow(rot_tables, normals, is_allowed, rng,
            max_layers=5, max_tiles=150):
    """Grow one tiling with random orientation selection.

    Returns dict with tiles placed, orientations used, junction stats.
    """
    normal_array = np.array([normals[name] for name in FACE_NAMES])
    seed_rot = rng.randint(0, 60)
    seed = Tile(0, seed_rot, rot_tables[seed_rot]['sig_names'], 0, np.zeros(3))
    tiles = {0: seed}
    frontier = [seed]
    next_id = 1

    sigs_used = {rot_tables[seed_rot]['sig_names']}
    rots_used = {seed_rot}
    junction_pairs = Counter()
    forbidden_attempts = 0
    total_attempts = 0
    tiles_per_layer = [1]

    for layer in range(1, max_layers + 1):
        new_frontier = []
        layer_tiles = 0

        for parent in frontier:
            for face_pos in parent.open_faces():
                if next_id >= max_tiles:
                    break

                parent_ft = parent.face_type(face_pos)
                candidates = []

                for r_idx, rtab in enumerate(rot_tables):
                    anti = rtab['anti_map'].get(face_pos)
                    if anti is None:
                        continue
                    touching_ft = FACE_NAMES[anti[1]]
                    total_attempts += 1

                    if is_allowed(parent_ft, touching_ft):
                        candidates.append((r_idx, anti[0], touching_ft))
                    else:
                        forbidden_attempts += 1

                if not candidates:
                    continue

                # Pick uniformly at random
                choice = candidates[rng.randint(0, len(candidates))]
                r_idx, touching_pos, touching_ft = choice
                rtab = rot_tables[r_idx]

                pos = parent.position + normal_array[face_pos] * 2.0
                new_tile = Tile(next_id, r_idx, rtab['sig_names'],
                                layer, pos)
                parent.neighbors[face_pos] = new_tile
                new_tile.neighbors[touching_pos] = parent
                tiles[next_id] = new_tile
                next_id += 1
                layer_tiles += 1
                new_frontier.append(new_tile)

                sigs_used.add(rtab['sig_names'])
                rots_used.add(r_idx)
                junction_pairs[tuple(sorted([parent_ft, touching_ft]))] += 1

            if next_id >= max_tiles:
                break

        tiles_per_layer.append(layer_tiles)
        frontier = new_frontier
        if not frontier:
            break

    return {
        'n_tiles': len(tiles),
        'n_sigs': len(sigs_used),
        'n_rots': len(rots_used),
        'sigs_used': sigs_used,
        'junction_pairs': junction_pairs,
        'forbidden_attempts': forbidden_attempts,
        'total_attempts': total_attempts,
        'tiles_per_layer': tiles_per_layer,
        'tiles': tiles,
    }


def monte_carlo_ensemble(rot_tables, normals, is_allowed,
                         n_runs=500, max_layers=5, max_tiles=150,
                         seed=42):
    """Run n_runs Monte Carlo tilings, collect statistics."""
    rng = np.random.RandomState(seed)

    all_sigs = set()
    per_run_sigs = []
    per_run_tiles = []
    per_run_junctions = Counter()
    per_run_forbidden = []
    per_run_junction_types = []

    for run in range(n_runs):
        result = mc_grow(rot_tables, normals, is_allowed, rng,
                         max_layers=max_layers, max_tiles=max_tiles)
        all_sigs |= result['sigs_used']
        per_run_sigs.append(result['n_sigs'])
        per_run_tiles.append(result['n_tiles'])
        per_run_forbidden.append(result['forbidden_attempts'])
        per_run_junction_types.append(len(result['junction_pairs']))
        for pair, count in result['junction_pairs'].items():
            per_run_junctions[pair] += count

    sigs_arr = np.array(per_run_sigs)
    tiles_arr = np.array(per_run_tiles)
    forb_arr = np.array(per_run_forbidden)
    jt_arr = np.array(per_run_junction_types)

    return {
        'n_runs': n_runs,
        'max_tiles': max_tiles,
        'total_unique_sigs': len(all_sigs),
        'sigs_mean': float(np.mean(sigs_arr)),
        'sigs_median': float(np.median(sigs_arr)),
        'sigs_std': float(np.std(sigs_arr)),
        'sigs_min': int(np.min(sigs_arr)),
        'sigs_max': int(np.max(sigs_arr)),
        'sigs_histogram': Counter(per_run_sigs),
        'tiles_mean': float(np.mean(tiles_arr)),
        'forbidden_mean': float(np.mean(forb_arr)),
        'forbidden_rate': float(np.sum(forb_arr)) / max(1, sum(
            r['total_attempts'] for r in [mc_grow(rot_tables, normals,
            is_allowed, np.random.RandomState(0), max_layers=1,
            max_tiles=2)] * 0) or 1),
        'junction_diversity_mean': float(np.mean(jt_arr)),
        'top_junctions': per_run_junctions.most_common(15),
    }


# ═════════════════════════════════════════════════════════════════
# SCALING ANALYSIS
# ═════════════════════════════════════════════════════════════════

def scaling_sweep(rot_tables, normals, is_allowed, mode_name,
                  tile_counts=[20, 50, 100, 200, 300],
                  n_runs=200, max_layers=6):
    """Run ensembles at different tile counts to see convergence."""
    results = []
    for max_t in tile_counts:
        rng = np.random.RandomState(42)
        sigs_list = []
        for _ in range(n_runs):
            r = mc_grow(rot_tables, normals, is_allowed, rng,
                        max_layers=max_layers, max_tiles=max_t)
            sigs_list.append(r['n_sigs'])
        arr = np.array(sigs_list)
        results.append({
            'max_tiles': max_t,
            'mean': float(np.mean(arr)),
            'median': float(np.median(arr)),
            'std': float(np.std(arr)),
            'min': int(np.min(arr)),
            'max': int(np.max(arr)),
        })
    return results


# ═════════════════════════════════════════════════════════════════
# FACE TYPE CENSUS
# ═════════════════════════════════════════════════════════════════

def face_census(tiles, fracs):
    """Count face type distribution in a placed tiling."""
    counts = Counter()
    for tile in tiles.values():
        for fp in range(7):
            counts[tile.face_type(fp)] += 1
    total = sum(counts.values())
    return {name: (counts[name], counts[name] / total,
                   fracs[name]) for name in FACE_NAMES}


# ═════════════════════════════════════════════════════════════════
# MAIN
# ═════════════════════════════════════════════════════════════════

def main():
    print()
    print("  ╔═══════════════════════════════════════════════════════════════╗")
    print("  ║  MONTE CARLO HEPTAHEDRAL LATTICE                            ║")
    print("  ║  Three rule sets × scaling analysis × forbidden tracking    ║")
    print("  ╚═══════════════════════════════════════════════════════════════╝")

    # ── Setup ──
    print("\n  Building tiling and rotation tables...")
    fracs, total = get_face_fractions()
    axes = icosahedral_axes()
    normals = select_7_normals(axes)
    rot_tables = precompute_rotation_tables(normals)
    print(f"  60 rotations, {total} tiling vertices, 7 face types")

    # ── Count allowed pairs per mode ──
    modes = {
        'loose': make_junction_checker('loose'),
        'strict': make_junction_checker('strict'),
        'physics': make_junction_checker('physics'),
    }

    print(f"\n{'='*70}")
    print("  JUNCTION RULE SETS")
    print(f"{'='*70}")

    for mode_name, checker in modes.items():
        n_allowed = 0
        n_blocked = 0
        for a in FACE_NAMES:
            for b in FACE_NAMES:
                if checker(a, b):
                    n_allowed += 1
                else:
                    n_blocked += 1
        # Unique pairs (a,b) with a <= b
        pairs_allowed = set()
        pairs_blocked = set()
        for i, a in enumerate(FACE_NAMES):
            for j, b in enumerate(FACE_NAMES):
                if i <= j:
                    pair = (a, b)
                    if checker(a, b):
                        pairs_allowed.add(pair)
                    else:
                        pairs_blocked.add(pair)
        print(f"\n  {mode_name.upper()}: {len(pairs_allowed)} allowed, "
              f"{len(pairs_blocked)} blocked (of 28 unique pairs)")
        if pairs_blocked:
            blocked_str = ', '.join(f"{a}↔{b}" for a, b in
                                     sorted(pairs_blocked))
            print(f"    Blocked: {blocked_str}")

    # ── Per-face valid neighbor count per mode ──
    print(f"\n{'='*70}")
    print("  PER-FACE VALID NEIGHBORS (of 60 rotations)")
    print(f"{'='*70}")

    header = f"  {'Face':<6}"
    for mode_name in modes:
        header += f" {mode_name:>8}"
    print(f"\n{header}")
    print(f"  {'─'*6}" + " ────────" * len(modes))

    for i, face_name in enumerate(FACE_NAMES):
        line = f"  {face_name:<6}"
        for mode_name, checker in modes.items():
            valid = 0
            for rtab in rot_tables:
                anti = rtab['anti_map'].get(i)
                if anti is None:
                    continue
                touching_ft = FACE_NAMES[anti[1]]
                if checker(face_name, touching_ft):
                    valid += 1
            line += f" {valid:>8}"
        print(line)

    # ── Monte Carlo ensembles ──
    N_RUNS = 500

    for mode_name, checker in modes.items():
        print(f"\n{'='*70}")
        print(f"  MONTE CARLO: {mode_name.upper()} RULES ({N_RUNS} runs)")
        print(f"{'='*70}")

        # Scaling sweep
        tile_counts = [20, 50, 100, 150, 200, 300]
        scaling = scaling_sweep(rot_tables, normals, checker, mode_name,
                                tile_counts=tile_counts, n_runs=N_RUNS)

        print(f"\n  Scaling: orientations vs tiling size")
        print(f"  {'Tiles':>6} {'Mean':>7} {'Median':>7} {'Std':>6} "
              f"{'Min':>5} {'Max':>5}")
        print(f"  {'─'*6} {'─'*7} {'─'*7} {'─'*6} {'─'*5} {'─'*5}")
        for s in scaling:
            print(f"  {s['max_tiles']:>6} {s['mean']:>7.1f} "
                  f"{s['median']:>7.0f} {s['std']:>6.1f} "
                  f"{s['min']:>5} {s['max']:>5}")

        # Detailed histogram at 100 tiles
        print(f"\n  Histogram at 100 tiles:")
        rng = np.random.RandomState(42)
        sigs_100 = []
        for _ in range(N_RUNS):
            r = mc_grow(rot_tables, normals, checker, rng,
                        max_layers=5, max_tiles=100)
            sigs_100.append(r['n_sigs'])
        hist = Counter(sigs_100)
        for k in sorted(hist.keys()):
            pct = hist[k] / N_RUNS * 100
            bar = '█' * int(pct * 0.5)
            print(f"    {k:>3}: {hist[k]:>4} ({pct:>5.1f}%) {bar}")

        median_100 = int(np.median(sigs_100))
        mean_100 = np.mean(sigs_100)

        # Check Fibonacci/φ connections
        fibs = [1, 2, 3, 5, 8, 13, 21, 34, 55]
        nearest_fib = min(fibs, key=lambda f: abs(median_100 - f))
        print(f"\n  Median at 100 tiles: {median_100}")
        print(f"  Mean at 100 tiles:   {mean_100:.1f}")
        print(f"  Nearest Fibonacci:   {nearest_fib} "
              f"(off by {median_100 - nearest_fib:+d})")
        print(f"  60/{median_100} = {60/max(1,median_100):.3f}   "
              f"(φ³ = {PHI**3:.3f})")

        # One detailed run for junction analysis
        rng2 = np.random.RandomState(123)
        detail = mc_grow(rot_tables, normals, checker, rng2,
                         max_layers=6, max_tiles=200)

        print(f"\n  Sample tiling (200 tiles max):")
        print(f"    Tiles placed: {detail['n_tiles']}")
        print(f"    Orientations: {detail['n_sigs']}")
        print(f"    Forbidden blocked: {detail['forbidden_attempts']} "
              f"/ {detail['total_attempts']} attempts "
              f"({detail['forbidden_attempts']/max(1,detail['total_attempts'])*100:.1f}%)")

        # Junction census
        print(f"    Junction types ({len(detail['junction_pairs'])}):")
        for pair, count in detail['junction_pairs'].most_common(10):
            print(f"      {pair[0]}↔{pair[1]}: {count}")

        # Face census
        census = face_census(detail['tiles'], fracs)
        print(f"\n    Face type distribution:")
        print(f"    {'Face':<6} {'Count':>5} {'Frac':>7} {'Target':>7} "
              f"{'Δ':>7}")
        print(f"    {'─'*6} {'─'*5} {'─'*7} {'─'*7} {'─'*7}")
        for name in FACE_NAMES:
            cnt, frac, target = census[name]
            delta = (frac - target) / target * 100 if target > 0 else 0
            print(f"    {name:<6} {cnt:>5} {frac:>7.4f} {target:>7.4f} "
                  f"{delta:>+6.1f}%")

    # ═══════════════════════════════════════════════════════════════
    # SUMMARY
    # ═══════════════════════════════════════════════════════════════
    print(f"\n{'='*70}")
    print("  SUMMARY: EFFECTIVE ORIENTATIONS")
    print(f"{'='*70}")

    print(f"\n  {'Mode':<10} {'@20':>5} {'@50':>5} {'@100':>5} "
          f"{'@200':>5} {'@300':>5} {'→∞':>5}")
    print(f"  {'─'*10} {'─'*5} {'─'*5} {'─'*5} {'─'*5} {'─'*5} {'─'*5}")

    summary_data = {}
    for mode_name, checker in modes.items():
        scaling = scaling_sweep(rot_tables, normals, checker, mode_name,
                                tile_counts=[20, 50, 100, 200, 300],
                                n_runs=300)
        medians = [int(s['median']) for s in scaling]
        line = f"  {mode_name:<10}"
        for m in medians:
            line += f" {m:>5}"
        # Extrapolate: if growing, report max; if stable, report median
        line += f" {medians[-1]:>5}"
        print(line)
        summary_data[mode_name] = medians

    print(f"\n  Key Fibonacci/φ numbers:")
    print(f"    F(5) = 5,  F(6) = 8,  F(7) = 13,  F(8) = 21,  F(9) = 34")
    print(f"    φ³ = {PHI**3:.3f},  60/φ³ = {60/PHI**3:.2f}")
    print(f"    60/13 = {60/13:.3f} ≈ φ³ = {PHI**3:.3f} "
          f"({abs(60/13 - PHI**3)/PHI**3*100:.1f}%)")

    # ── Save ──
    outdir = os.path.join(ROOT, 'results', 'heptahedron')
    os.makedirs(outdir, exist_ok=True)
    outpath = os.path.join(outdir, 'effective_orientations.txt')

    with open(outpath, 'w') as f:
        f.write("EFFECTIVE ORIENTATIONS: Monte Carlo Heptahedral Tiling\n")
        f.write("=" * 60 + "\n\n")
        f.write("Three junction rule sets tested:\n")
        f.write("  LOOSE  — 3 forbidden pairs only\n")
        f.write("  STRICT — 17 allowed pairs only (neutral=forbidden)\n")
        f.write("  PHYSICS — same-type + shared-letter pairs only\n\n")

        f.write(f"Monte Carlo: {N_RUNS} runs per configuration\n\n")

        f.write("SCALING (median orientations at tile count):\n")
        f.write(f"{'Mode':<10} {'@20':>5} {'@50':>5} {'@100':>5} "
                f"{'@200':>5} {'@300':>5}\n")
        f.write(f"{'─'*10} {'─'*5} {'─'*5} {'─'*5} {'─'*5} {'─'*5}\n")
        for mode_name, medians in summary_data.items():
            line = f"{mode_name:<10}"
            for m in medians:
                line += f" {m:>5}"
            f.write(line + "\n")

        f.write(f"\nφ CONNECTIONS:\n")
        f.write(f"  60/13 = {60/13:.4f}\n")
        f.write(f"  φ³   = {PHI**3:.4f}  (error: "
                f"{abs(60/13 - PHI**3)/PHI**3*100:.1f}%)\n")
        f.write(f"  60/φ³ = {60/PHI**3:.4f}\n")
        f.write(f"  F(7) = 13 = bronze discriminant\n")

    print(f"\n  Results saved to: {outpath}")
    print()


if __name__ == '__main__':
    main()
