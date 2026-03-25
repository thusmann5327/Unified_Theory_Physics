"""
universe_db.py — PostgreSQL interface for the Universe Database
===============================================================

Stores quasicrystal vertices, Voronoi cells, neighbors, elements,
molecules, and gamma convergence results.
"""

import os
import time
import numpy as np
import psycopg2
from psycopg2.extras import execute_values, Json


SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'schema.sql')


class UniverseDB:
    def __init__(self, dbname='universe', host='localhost'):
        self.conn = psycopg2.connect(dbname=dbname, host=host)
        self.conn.autocommit = False

    def init_schema(self):
        """Create tables if they don't exist."""
        with open(SCHEMA_PATH) as f:
            sql = f.read()
        with self.conn.cursor() as cur:
            cur.execute(sql)
        self.conn.commit()

    def store_points(self, pts, pts_perp, types, n_half, batch_id=None):
        """Bulk insert vertex data."""
        if batch_id is None:
            batch_id = int(time.time())

        has_perp = pts_perp is not None
        rows = []
        for i in range(len(pts)):
            rows.append((
                float(pts[i, 0]), float(pts[i, 1]), float(pts[i, 2]),
                float(pts_perp[i, 0]) if has_perp else None,
                float(pts_perp[i, 1]) if has_perp else None,
                float(pts_perp[i, 2]) if has_perp else None,
                None,  # bracket
                str(types[i]),
                None,  # depth
                n_half,
                batch_id,
            ))

        with self.conn.cursor() as cur:
            execute_values(
                cur,
                """INSERT INTO vertices
                   (x, y, z, perp_x, perp_y, perp_z, bracket,
                    vertex_type, depth, n_half, batch_id)
                   VALUES %s""",
                rows, page_size=5000,
            )
        self.conn.commit()
        return batch_id

    def store_computation(self, n_half, n_points, n_bgs, bgs_fraction,
                          gamma_bgs, gamma_all, compute_time_s,
                          has_voronoi=False, has_cells=False):
        """Store a computation summary row."""
        with self.conn.cursor() as cur:
            cur.execute(
                """INSERT INTO computations
                   (n_half, n_points, n_bgs, bgs_fraction,
                    gamma_bgs, gamma_all, has_voronoi, has_cells, compute_time_s)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (int(n_half), int(n_points), int(n_bgs), float(bgs_fraction),
                 float(gamma_bgs), float(gamma_all),
                 has_voronoi, has_cells, float(compute_time_s)),
            )
        self.conn.commit()

    def store_gamma(self, n_half, n_bgs, gamma, gamma_err=None,
                    r0=None, fit_range=None, n_fit_bins=None):
        """Store gamma convergence result."""
        with self.conn.cursor() as cur:
            cur.execute(
                """INSERT INTO gamma_convergence
                   (n_half, n_bgs, gamma, gamma_err, r0,
                    fit_range_min, fit_range_max, n_fit_bins)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                   ON CONFLICT (n_half) DO UPDATE SET
                   gamma=EXCLUDED.gamma, n_bgs=EXCLUDED.n_bgs,
                   gamma_err=EXCLUDED.gamma_err""",
                (int(n_half), int(n_bgs), float(gamma),
                 float(gamma_err) if gamma_err is not None else None,
                 float(r0) if r0 is not None else None,
                 float(fit_range[0]) if fit_range else None,
                 float(fit_range[1]) if fit_range else None,
                 int(n_fit_bins) if n_fit_bins is not None else None),
            )
        self.conn.commit()

    def get_bgs_cloud(self, n_half=None, limit=None):
        """Query all BGS positions, optionally for a specific n_half."""
        sql = "SELECT x, y, z FROM vertices WHERE vertex_type = 'BGS'"
        params = []
        if n_half is not None:
            sql += ' AND n_half = %s'
            params.append(n_half)
        if limit:
            sql += ' LIMIT %s'
            params.append(limit)

        with self.conn.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
        return np.array(rows) if rows else np.empty((0, 3))

    def get_all_gamma(self):
        """Get the gamma convergence table."""
        with self.conn.cursor() as cur:
            cur.execute(
                'SELECT n_half, n_bgs, gamma, gamma_err '
                'FROM gamma_convergence ORDER BY n_half')
            return cur.fetchall()

    def get_type_fractions(self, n_half):
        """Get vertex type distribution for a given n_half."""
        with self.conn.cursor() as cur:
            cur.execute(
                """SELECT vertex_type, COUNT(*) as n,
                   COUNT(*)::float / SUM(COUNT(*)) OVER () as frac
                   FROM vertices WHERE n_half = %s
                   GROUP BY vertex_type ORDER BY n DESC""",
                (n_half,),
            )
            return cur.fetchall()

    def stats(self):
        """Print database statistics."""
        with self.conn.cursor() as cur:
            cur.execute('SELECT COUNT(*) FROM vertices')
            n_total = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM vertices WHERE vertex_type='BGS'")
            n_bgs = cur.fetchone()[0]
            cur.execute(
                'SELECT DISTINCT n_half FROM vertices ORDER BY n_half')
            n_halfs = [r[0] for r in cur.fetchall()]
            cur.execute('SELECT COUNT(*) FROM cells')
            n_cells = cur.fetchone()[0]
            cur.execute('SELECT COUNT(*) FROM neighbors')
            n_neighbors = cur.fetchone()[0]
            cur.execute('SELECT COUNT(*) FROM gamma_convergence')
            n_gamma = cur.fetchone()[0]
            cur.execute('SELECT COUNT(*) FROM computations')
            n_comp = cur.fetchone()[0]

        print(f"""
  Universe Database Statistics
  ────────────────────────────
  Total vertices:     {n_total:,}
  BGS vertices:       {n_bgs:,} ({100*n_bgs/max(n_total,1):.1f}%)
  Voronoi cells:      {n_cells:,}
  Neighbor pairs:     {n_neighbors:,}
  N_half computed:    {n_halfs}
  Gamma measurements: {n_gamma}
  Computations:       {n_comp}
""")

    def close(self):
        self.conn.close()
