"""
render_server.py — Flask server for 3D quasicrystal visualization
=================================================================

Serves vertex data from the PostgreSQL universe database to a
Three.js frontend. Runs emergent strain-minimization evolution
in background threads and streams frames for animation.

Usage:
    python3 visualization/render_server.py
    # Open http://localhost:8080
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify, send_from_directory, request
from database.universe_db import UniverseDB
from simulation.emergent_evolve import (
    evolve_emergent, load_vertices, measure_gamma,
    LEAK, R_C, STIFFNESS,
)
from simulation.shape_operator import bracket_info, BRACKET_LABELS
try:
    from simulation.jax_evolve import (
        evolve_jax, find_structures_multiscale,
        measure_gamma as jax_measure_gamma,
        load_vertices as jax_load_vertices,
    )
    JAX_AVAILABLE = True
except ImportError:
    JAX_AVAILABLE = False
import numpy as np
import threading

app = Flask(__name__, static_folder='static')
db = UniverseDB()

# Evolution state (shared across requests)
evolution_state = {
    'running': False,
    'progress': 0,
    'result': None,
    'error': None,
}


@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


@app.route('/api/vertices/<int:n_half>')
def get_vertices(n_half):
    """Return all vertices for a given N_half, with optional type filter."""
    type_filter = request.args.get('type', None)
    limit = int(request.args.get('limit', 100000))

    with db.conn.cursor() as cur:
        if type_filter:
            cur.execute('''
                SELECT x, y, z, vertex_type
                FROM vertices WHERE n_half = %s AND vertex_type = %s
                LIMIT %s
            ''', (n_half, type_filter, limit))
        else:
            cur.execute('''
                SELECT x, y, z, vertex_type
                FROM vertices WHERE n_half = %s
                LIMIT %s
            ''', (n_half, limit))
        rows = cur.fetchall()

    vertices = []
    for x, y, z, vtype in rows:
        vertices.append({
            'x': float(x), 'y': float(y), 'z': float(z),
            'type': vtype
        })
    return jsonify(vertices)


@app.route('/api/bgs/<int:n_half>')
def get_bgs(n_half):
    """Return only BGS (matter) vertices."""
    with db.conn.cursor() as cur:
        cur.execute('''
            SELECT x, y, z FROM vertices
            WHERE n_half = %s AND vertex_type = 'BGS'
        ''', (n_half,))
        rows = cur.fetchall()
    return jsonify([{'x': float(r[0]), 'y': float(r[1]), 'z': float(r[2])}
                    for r in rows])


@app.route('/api/stats')
def get_stats():
    """Return database summary statistics."""
    with db.conn.cursor() as cur:
        cur.execute('''
            SELECT n_half, vertex_type, COUNT(*)
            FROM vertices
            GROUP BY n_half, vertex_type
            ORDER BY n_half, vertex_type
        ''')
        type_counts = {}
        for n_half, vtype, count in cur.fetchall():
            key = str(n_half)
            if key not in type_counts:
                type_counts[key] = {}
            type_counts[key][vtype] = count

        cur.execute('SELECT DISTINCT n_half FROM vertices ORDER BY n_half')
        available = [r[0] for r in cur.fetchall()]

        cur.execute('SELECT COUNT(*) FROM vertices')
        total = cur.fetchone()[0]

    return jsonify({
        'total_vertices': total,
        'available_n_half': available,
        'type_counts': type_counts,
    })


@app.route('/api/gamma')
def get_gamma():
    """Return gamma convergence data."""
    with db.conn.cursor() as cur:
        cur.execute('''
            SELECT n_half, n_bgs, gamma, gamma_err
            FROM gamma_convergence
            ORDER BY n_half
        ''')
        rows = cur.fetchall()
    return jsonify([{
        'n_half': r[0], 'n_bgs': r[1],
        'gamma': float(r[2]) if r[2] else None,
        'gamma_err': float(r[3]) if r[3] else None,
    } for r in rows])


@app.route('/api/evolve', methods=['POST'])
def start_evolution():
    """Start emergent strain evolution in a background thread.

    POST JSON: {
        n_half: 3,       // lattice size (3-6 recommended)
        n_steps: 3000,   // evolution steps
        perturbation: 0.02,  // initial symmetry breaking
        damping: 0.9985,     // expansion cooling
    }

    Returns immediately. Poll /api/evolve/status for progress.
    Fetch frames from /api/evolve/frames when done.
    """
    if evolution_state['running']:
        return jsonify({'error': 'Evolution already running'}), 409

    data = request.get_json() or {}
    n_half = data.get('n_half', 3)
    n_steps = data.get('n_steps', 3000)
    perturbation = data.get('perturbation', 0.02)
    damping = data.get('damping', 0.9985)
    bracket = data.get('bracket', None)  # shape operator bracket (94–294)

    evolution_state['running'] = True
    evolution_state['progress'] = 0
    evolution_state['result'] = None
    evolution_state['error'] = None

    def progress_cb(step, total, metrics):
        evolution_state['progress'] = step / total

    use_jax = data.get('use_jax', JAX_AVAILABLE)

    def run():
        try:
            positions, types = load_vertices(n_half)
            n_verts = len(positions)

            if use_jax and JAX_AVAILABLE:
                # JAX/Metal GPU evolution
                result = evolve_jax(
                    positions, types,
                    n_steps=n_steps,
                    perturbation=perturbation,
                    damping=damping,
                    bracket=bracket,
                    callback=progress_cb,
                )
                frames_out = [frame.tolist() for frame in result['frames']]
                bgs_mask = np.array([t == 'BGS' for t in types])
                final_bgs = result['frames'][-1][bgs_mask]
                gamma, _, _ = jax_measure_gamma(final_bgs)

                # Find galaxy structures in final frame
                structures = find_structures_multiscale(
                    result['frames'][-1], types)

                evolution_state['result'] = {
                    'frames': frames_out,
                    'steps': result['steps'],
                    'metrics': [{'total_strain': s} for s in result['strain']],
                    'final_gamma': gamma,
                    'n_vertices': n_verts,
                    'types': types,
                    'params': result['params'],
                    'ideals': {},
                    'structures': structures,
                }
            else:
                # NumPy CPU evolution
                result = evolve_emergent(
                    positions, types,
                    n_steps=n_steps,
                    perturbation=perturbation,
                    damping=damping,
                    callback=progress_cb,
                    bracket=bracket,
                )
                frames_out = [frame.tolist() for frame in result['frames']]
                bgs_mask = np.array([t == 'BGS' for t in types])
                final_bgs = result['frames'][-1][bgs_mask]
                gamma, _, _ = measure_gamma(final_bgs)

                evolution_state['result'] = {
                    'frames': frames_out,
                    'steps': result['steps'],
                    'metrics': result['metrics'],
                    'final_gamma': gamma,
                    'n_vertices': n_verts,
                    'types': types,
                    'params': result['params'],
                    'ideals': result['ideals'],
                }
        except Exception as e:
            evolution_state['error'] = str(e)
            import traceback
            traceback.print_exc()
        finally:
            evolution_state['running'] = False
            evolution_state['progress'] = 1.0

    thread = threading.Thread(target=run, daemon=True)
    thread.start()

    return jsonify({
        'status': 'started',
        'n_half': n_half,
        'n_steps': n_steps,
    })


@app.route('/api/evolve/status')
def evolution_status():
    """Poll evolution progress."""
    resp = {
        'running': evolution_state['running'],
        'progress': evolution_state['progress'],
        'error': evolution_state['error'],
        'has_result': evolution_state['result'] is not None,
    }
    if evolution_state['result']:
        resp['n_frames'] = len(evolution_state['result']['frames'])
        resp['n_vertices'] = evolution_state['result'].get('n_vertices')
        resp['final_gamma'] = evolution_state['result'].get('final_gamma')
    return jsonify(resp)


@app.route('/api/evolve/frames')
def evolution_frames():
    """Return computed evolution frames.

    Query params:
      start: first frame index (default 0)
      count: max frames to return (default all)
      stride: take every Nth frame (default 1)
    """
    if not evolution_state['result']:
        return jsonify({'error': 'No evolution result available'}), 404

    result = evolution_state['result']
    total = len(result['frames'])
    start = int(request.args.get('start', 0))
    stride = int(request.args.get('stride', 1))
    count = int(request.args.get('count', total))

    end = min(start + count * stride, total)
    frames = result['frames'][start:end:stride]
    steps = result['steps'][start:end:stride]
    metrics = result['metrics'][start:end:stride]

    return jsonify({
        'frames': frames,
        'steps': steps,
        'metrics': metrics,
        'types': result['types'],
        'params': result['params'],
        'final_gamma': result.get('final_gamma'),
        'total_frames': total,
    })


@app.route('/api/stiffness')
def get_stiffness():
    """Return the stiffness hierarchy table."""
    table = {f'{k[0]}-{k[1]}': v for k, v in STIFFNESS.items() if v > 0}
    return jsonify({
        'stiffness': table,
        'constants': {
            'LEAK': LEAK,
            'R_C': R_C,
            'LEAK_squared': LEAK**2,
            'LEAK_cubed': LEAK**3,
        }
    })


@app.route('/api/evolve/galaxies')
def evolution_galaxies():
    """Return galaxy structures from the most recent evolution."""
    if not evolution_state['result']:
        return jsonify({'error': 'No evolution result available'}), 404

    result = evolution_state['result']
    structures = result.get('structures')

    if not structures:
        return jsonify({'error': 'No structure data (run with JAX)'}), 404

    # Return galaxy-scale structures with overdensity data
    galaxy_scale = None
    for sc in structures.get('scales', []):
        if sc['name'] == 'galaxy':
            galaxy_scale = sc
            break

    cluster_scale = None
    for sc in structures.get('scales', []):
        if sc['name'] == 'cluster':
            cluster_scale = sc
            break

    resp = {
        'overdensity': structures.get('overdensity', []),
        'bgs_positions': structures.get('bgs_positions', []),
        'mean_nn': structures.get('mean_nn', 0),
        'galaxy_structures': [],
        'cluster_structures': [],
    }

    if galaxy_scale:
        for g in galaxy_scale['structures'][:50]:
            resp['galaxy_structures'].append({
                'center': g['center'],
                'n_members': g['n_members'],
                'radius': g['radius'],
                'shape': g['shape'],
                'axis_ratios': g['axis_ratios'],
            })

    if cluster_scale:
        for g in cluster_scale['structures'][:200]:
            resp['cluster_structures'].append({
                'center': g['center'],
                'n_members': g['n_members'],
                'radius': g['radius'],
                'shape': g['shape'],
                'axis_ratios': g['axis_ratios'],
            })

    return jsonify(resp)


@app.route('/api/bracket/<int:bz>')
def get_bracket_info(bz):
    """Return bracket-dependent shape operator info."""
    info = bracket_info(bz)
    # Convert face weights to serializable
    info['face_weights'] = {k: float(v) for k, v in info['face_weights'].items()}
    info['disc_sphere_ratio'] = float(info['disc_sphere_ratio'])
    return jsonify(info)


@app.route('/api/brackets')
def get_bracket_labels():
    """Return all bracket labels."""
    return jsonify({str(k): v for k, v in BRACKET_LABELS.items()})


if __name__ == '__main__':
    print("\n  Quasicrystal Universe Renderer")
    print("  ══════════════════════════════")
    print("  Emergent physics from matching rule strain")
    print("  http://localhost:8080\n")
    app.run(port=8080, debug=True)
