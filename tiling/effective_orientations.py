"""
effective_orientations.py — Matching-Constrained Orientation Count
==================================================================

Of the 60 icosahedral orientations of the heptahedral prototile,
how many can actually participate in a valid aperiodic tiling?

Method:
  1. Generate all 60 rotations of the heptahedron
  2. For each face of a central tile, try attaching each of the 60
     orientations as a neighbor — the neighbor's touching face must
     form an ALLOWED junction (not forbidden, not neutral)
  3. The EFFECTIVE orientation count = number of distinct orientations
     that survive all matching constraints

Key question: does the matching rules reduce 60 → 13?

Run:  python3 tiling/effective_orientations.py
"""

import sys
import os
import math
import numpy as np
from collections import OrderedDict, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEAN = os.path.join(ROOT, 'CLEAN')
sys.path.insert(0, CLEAN)

from core.constants import PHI
from tiling import build_triple_tiling, analyze_vertices

# Import from heptahedron.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from heptahedron import (
    FACE_NAMES, FACE_FORCE, FACE_COLORS,
    ALLOWED_JUNCTIONS, FORBIDDEN_JUNCTIONS,
    get_face_fractions, icosahedral_axes, select_7_normals,
    _icosahedral_rotations, _rotation_matrix,
)


def is_allowed(face_a, face_b):
    """Check if face_a ↔ face_b is an allowed junction."""
    pair = (face_a, face_b)
    rev = (face_b, face_a)
    return pair in ALLOWED_JUNCTIONS or rev in ALLOWED_JUNCTIONS


def is_forbidden(face_a, face_b):
    """Check if face_a ↔ face_b is a forbidden junction."""
    pair = (face_a, face_b)
    rev = (face_b, face_a)
    return pair in FORBIDDEN_JUNCTIONS or rev in FORBIDDEN_JUNCTIONS


def build_junction_table():
    """Build full junction lookup: (A,B) → 'ALLOWED'/'FORBIDDEN'/'NEUTRAL'."""
    table = {}
    for a in FACE_NAMES:
        for b in FACE_NAMES:
            if is_forbidden(a, b):
                table[(a, b)] = 'FORBIDDEN'
            elif is_allowed(a, b):
                table[(a, b)] = 'ALLOWED'
            else:
                table[(a, b)] = 'NEUTRAL'
    return table


def compute_effective_orientations(normals):
    """Core computation: which orientations survive matching constraints.

    For each of the 60 rotations applied to a neighbor tile:
      - For each of the 7 faces of the central tile:
        - Find which face of the rotated neighbor is anti-parallel
          (i.e., the touching face)
        - Check if the junction is allowed

    An orientation is "valid at face i" if it can attach there.
    An orientation is "globally valid" if it can attach at ANY face.
    The effective count = number of globally valid orientations.
    """
    rotations = _icosahedral_rotations()
    normal_array = np.array([normals[name] for name in FACE_NAMES])

    # For each rotation, compute the face-type permutation
    # rotation_perms[r] = [type_at_pos_0, type_at_pos_1, ..., type_at_pos_6]
    rotation_perms = []
    for R in rotations:
        rotated = (R @ normal_array.T).T
        perm = []
        for i in range(7):
            dots = np.abs(normal_array @ rotated[i])
            best = np.argmax(dots)
            perm.append(best)  # face index, not name
        rotation_perms.append(tuple(perm))

    junction_table = build_junction_table()

    # ── Per-face analysis ──
    # For each face i of the central tile (type = FACE_NAMES[i]):
    #   The touching face of a neighbor is the one whose rotated normal
    #   is ANTI-PARALLEL to normal_i.
    #
    #   For rotation R applied to the neighbor:
    #     rotated_normals[j] = R @ normal_j
    #     We need: rotated_normals[j] ≈ -normal_i
    #     i.e., (R @ normal_j) · normal_i ≈ -1
    #     i.e., normal_j · (R^T @ normal_i) ≈ -1

    face_valid_orientations = {}  # face_name → set of rotation indices
    face_valid_details = {}       # face_name → list of (rot_idx, touching_face_type)

    for i, face_name in enumerate(FACE_NAMES):
        valid_rots = set()
        details = []

        for r_idx, R in enumerate(rotations):
            # Find which face of the rotated neighbor touches face i
            # Rotated normal j = R @ normal_j
            # We want R @ normal_j ≈ -normal_i
            rotated = (R @ normal_array.T).T
            dots = rotated @ normal_array[i]  # dot of each rotated normal with face i
            # Most anti-parallel = most negative dot
            touching_j = np.argmin(dots)
            anti_parallel_score = dots[touching_j]

            if anti_parallel_score > -0.3:
                # No face is sufficiently anti-parallel — skip
                continue

            touching_type = FACE_NAMES[touching_j]
            status = junction_table[(face_name, touching_type)]

            if status == 'ALLOWED':
                valid_rots.add(r_idx)
                details.append((r_idx, touching_type, anti_parallel_score))

        face_valid_orientations[face_name] = valid_rots
        face_valid_details[face_name] = details

    # ── Global analysis ──
    # An orientation is globally valid if it can attach at ANY face
    all_valid = set()
    for face_name in FACE_NAMES:
        all_valid |= face_valid_orientations[face_name]

    # An orientation is FULLY compatible if it can attach at ALL faces
    # (stronger constraint)
    fully_compatible = set(range(len(rotations)))
    for face_name in FACE_NAMES:
        fully_compatible &= face_valid_orientations[face_name]

    # ── Distinct face-type signatures ──
    # Two orientations are "equivalent" if they produce the same
    # set of face types at the same positions
    distinct_signatures = set()
    sig_to_rots = defaultdict(list)
    for r_idx in all_valid:
        perm = rotation_perms[r_idx]
        sig = tuple(FACE_NAMES[p] for p in perm)
        distinct_signatures.add(sig)
        sig_to_rots[sig].append(r_idx)

    # ── Constrained distinct orientations ──
    # Among valid orientations, how many produce DISTINCT face configurations?
    # (Two rotations that map to the same face permutation are the same tile)
    effective_count = len(distinct_signatures)

    # ── Tiling propagation analysis ──
    # Start with central tile. For each face, which face types can appear
    # as the touching face of a valid neighbor? This constrains the next
    # layer.
    propagation = {}
    for face_name in FACE_NAMES:
        touching_types = set()
        for _, touching_type, _ in face_valid_details[face_name]:
            touching_types.add(touching_type)
        propagation[face_name] = touching_types

    # ── Iterative constraint propagation ──
    # A valid tiling orientation must be able to:
    #   (a) attach to the central tile at some face
    #   (b) itself have valid neighbors at ALL its own faces
    # This is a fixed-point iteration.

    # Start: all orientations that can attach somewhere
    surviving = set(all_valid)
    for iteration in range(20):
        new_surviving = set()
        for r_idx in surviving:
            perm = rotation_perms[r_idx]
            # For this orientation, check: can each of its 7 faces
            # find at least one other surviving orientation as neighbor?
            can_fill_all = True
            for face_pos in range(7):
                my_face_type = FACE_NAMES[perm[face_pos]]
                # Need a surviving neighbor whose touching face is allowed
                found = False
                for r2_idx in surviving:
                    if r2_idx == r_idx:
                        continue
                    R2 = rotations[r2_idx]
                    rotated2 = (R2 @ normal_array.T).T
                    # Which face of r2 touches my face_pos?
                    dots = rotated2 @ normal_array[face_pos]
                    touching_j = np.argmin(dots)
                    if dots[touching_j] > -0.3:
                        continue
                    touching_type = FACE_NAMES[touching_j]
                    if junction_table[(my_face_type, touching_type)] == 'ALLOWED':
                        found = True
                        break
                if not found:
                    can_fill_all = False
                    break
            if can_fill_all:
                new_surviving.add(r_idx)

        if new_surviving == surviving:
            break
        surviving = new_surviving

    # Final distinct signatures after constraint propagation
    final_signatures = set()
    for r_idx in surviving:
        perm = rotation_perms[r_idx]
        sig = tuple(FACE_NAMES[p] for p in perm)
        final_signatures.add(sig)

    return {
        'total_rotations': len(rotations),
        'per_face': {name: len(face_valid_orientations[name]) for name in FACE_NAMES},
        'per_face_details': face_valid_details,
        'any_face_valid': len(all_valid),
        'all_faces_valid': len(fully_compatible),
        'distinct_signatures_any': len(distinct_signatures),
        'propagation': propagation,
        'constraint_iterations': iteration + 1,
        'surviving_after_propagation': len(surviving),
        'effective_distinct': len(final_signatures),
        'final_signatures': final_signatures,
    }


def main():
    print()
    print("  ╔═══════════════════════════════════════════════════════════════╗")
    print("  ║  EFFECTIVE ORIENTATIONS: Matching-Constrained Tiling Count   ║")
    print("  ║  Question: do matching rules reduce 60 → 13?                ║")
    print("  ╚═══════════════════════════════════════════════════════════════╝")

    # ── Build tiling ──
    print("\n  Building tiling and icosahedral axes...")
    fracs, total = get_face_fractions()
    axes = icosahedral_axes()
    normals = select_7_normals(axes)

    # ── Compute ──
    print("  Computing effective orientations under matching constraints...")
    result = compute_effective_orientations(normals)

    # ── Report ──
    print(f"\n{'='*70}")
    print("  STEP 1: PER-FACE VALID NEIGHBOR COUNT")
    print(f"{'='*70}")
    print(f"\n  For each face of the central tile, how many of the 60")
    print(f"  rotated neighbors can attach with an ALLOWED junction?\n")
    print(f"  {'Face':<6} {'Type':<20} {'Valid neighbors':>16} {'Allowed touching types'}")
    print(f"  {'─'*6} {'─'*20} {'─'*16} {'─'*30}")

    propagation = result['propagation']
    for name in FACE_NAMES:
        n_valid = result['per_face'][name]
        touching = ', '.join(sorted(propagation[name]))
        print(f"  {name:<6} {FACE_FORCE[name]:<20} {n_valid:>16} {touching}")

    total_valid_per_face = sum(result['per_face'].values())
    print(f"\n  Total valid (face,orientation) pairs: {total_valid_per_face}")

    # ── Junction constraint summary ──
    print(f"\n{'='*70}")
    print("  STEP 2: GLOBAL ORIENTATION FILTERING")
    print(f"{'='*70}")
    print(f"\n  Total rotations:                       {result['total_rotations']}")
    print(f"  Valid at ANY face (can attach somewhere): {result['any_face_valid']}")
    print(f"  Valid at ALL faces (can fill any slot):   {result['all_faces_valid']}")
    print(f"  Distinct face-type signatures (any):     {result['distinct_signatures_any']}")

    # ── Constraint propagation ──
    print(f"\n{'='*70}")
    print("  STEP 3: CONSTRAINT PROPAGATION (fixed-point iteration)")
    print(f"{'='*70}")
    print(f"\n  An orientation survives only if every one of its 7 faces")
    print(f"  can find a valid neighbor among the surviving set.")
    print(f"\n  Iterations to convergence:               {result['constraint_iterations']}")
    print(f"  Surviving orientations:                  {result['surviving_after_propagation']}")
    print(f"  Effective distinct tile types:            {result['effective_distinct']}")

    effective = result['effective_distinct']

    # ── The 13 test ──
    print(f"\n{'='*70}")
    print("  RESULT")
    print(f"{'='*70}")
    if effective == 13:
        print(f"\n  ★ EFFECTIVE ORIENTATIONS = 13 = F(7) ★")
        print(f"    The matching rules reduce 60 → 13.")
        print(f"    60/13 = {60/13:.3f} ≈ φ³ = {PHI**3:.3f} ({abs(60/13 - PHI**3)/PHI**3*100:.1f}%)")
        print(f"    13 = bronze discriminant = Aufbau multiplier")
    else:
        print(f"\n  Effective orientations = {effective}")
        print(f"  (NOT 13 — the matching rules give a different reduction)")

    # ── φ relationships ──
    print(f"\n  Ratio analysis:")
    print(f"    60 / {effective} = {60/effective:.4f}")
    print(f"    φ³ = {PHI**3:.4f}")
    print(f"    60/φ³ = {60/PHI**3:.4f}")
    print(f"    φ⁴ = {PHI**4:.4f}")
    print(f"    60/φ⁴ = {60/PHI**4:.4f}")

    # Check nearby Fibonacci
    fibs = [1, 2, 3, 5, 8, 13, 21, 34, 55]
    for f in fibs:
        if abs(effective - f) <= 3:
            print(f"    Nearest Fibonacci: F = {f} (off by {effective - f})")

    print(f"\n    60/13 = {60/13:.4f}")
    print(f"    φ³   = {PHI**3:.4f}  (error: {abs(60/13 - PHI**3)/PHI**3*100:.1f}%)")
    print(f"    60/φ³ = {60/PHI**3:.4f} ≈ 13 + {60/PHI**3 - 13:.2f}")

    # ── Signature details ──
    if result['final_signatures']:
        print(f"\n{'='*70}")
        print("  SURVIVING TILE SIGNATURES")
        print(f"{'='*70}")
        sigs = sorted(result['final_signatures'])
        for idx, sig in enumerate(sigs):
            face_list = ', '.join(sig)
            print(f"    {idx+1:>3}. [{face_list}]")

    # ── Save ──
    outdir = os.path.join(ROOT, 'results', 'heptahedron')
    os.makedirs(outdir, exist_ok=True)
    outpath = os.path.join(outdir, 'effective_orientations.txt')

    with open(outpath, 'w') as f:
        f.write("EFFECTIVE ORIENTATIONS: Matching-Constrained Tiling Count\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Total icosahedral rotations:    {result['total_rotations']}\n")
        f.write(f"Valid at any face:              {result['any_face_valid']}\n")
        f.write(f"Valid at all faces:             {result['all_faces_valid']}\n")
        f.write(f"Distinct signatures (any):      {result['distinct_signatures_any']}\n")
        f.write(f"Constraint propagation iters:   {result['constraint_iterations']}\n")
        f.write(f"Surviving after propagation:    {result['surviving_after_propagation']}\n")
        f.write(f"EFFECTIVE DISTINCT:             {result['effective_distinct']}\n\n")

        f.write("Per-face valid neighbor counts:\n")
        for name in FACE_NAMES:
            touching = ', '.join(sorted(propagation[name]))
            f.write(f"  {name:<6} {result['per_face'][name]:>3} valid  "
                    f"touching: {touching}\n")

        f.write(f"\nRatio analysis:\n")
        f.write(f"  60 / {effective} = {60/effective:.4f}\n")
        f.write(f"  φ³ = {PHI**3:.4f}\n")
        f.write(f"  60/φ³ = {60/PHI**3:.4f}\n")
        f.write(f"  60/13 = {60/13:.4f} ≈ φ³ = {PHI**3:.4f} "
                f"({abs(60/13 - PHI**3)/PHI**3*100:.1f}%)\n")

        if result['final_signatures']:
            f.write(f"\nSurviving tile signatures ({len(result['final_signatures'])}):\n")
            for idx, sig in enumerate(sorted(result['final_signatures'])):
                f.write(f"  {idx+1:>3}. [{', '.join(sig)}]\n")

    print(f"\n  Results saved to: {outpath}")
    print()


if __name__ == '__main__':
    main()
