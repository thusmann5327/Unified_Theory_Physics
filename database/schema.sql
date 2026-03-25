-- Universe Database Schema
-- Stores all computed quasicrystal vertices, Voronoi cells, and derived quantities.

CREATE TABLE IF NOT EXISTS vertices (
    id BIGSERIAL PRIMARY KEY,
    x DOUBLE PRECISION NOT NULL,
    y DOUBLE PRECISION NOT NULL,
    z DOUBLE PRECISION NOT NULL,
    perp_x DOUBLE PRECISION,
    perp_y DOUBLE PRECISION,
    perp_z DOUBLE PRECISION,
    bracket INTEGER,
    vertex_type VARCHAR(3) NOT NULL,
    depth DOUBLE PRECISION,
    n_half INTEGER NOT NULL,
    batch_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_vert_type ON vertices(vertex_type);
CREATE INDEX IF NOT EXISTS idx_vert_bracket ON vertices(bracket);
CREATE INDEX IF NOT EXISTS idx_vert_nhalf ON vertices(n_half);
CREATE INDEX IF NOT EXISTS idx_vert_batch ON vertices(batch_id);
CREATE INDEX IF NOT EXISTS idx_vert_xyz ON vertices(x, y, z);

CREATE TABLE IF NOT EXISTS cells (
    vertex_id BIGINT PRIMARY KEY REFERENCES vertices(id),
    n_faces INTEGER,
    volume DOUBLE PRECISION,
    face_areas DOUBLE PRECISION[],
    n_coarse_faces INTEGER,
    sub_face_counts INTEGER[],
    orbital_groups JSONB,
    is_interior BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS neighbors (
    id BIGSERIAL PRIMARY KEY,
    vertex_id_1 BIGINT REFERENCES vertices(id),
    vertex_id_2 BIGINT REFERENCES vertices(id),
    shared_face_area DOUBLE PRECISION,
    junction_type VARCHAR(10),
    distance DOUBLE PRECISION,
    bond_energy DOUBLE PRECISION,
    bond_type VARCHAR(20)
);

CREATE INDEX IF NOT EXISTS idx_neigh_v1 ON neighbors(vertex_id_1);
CREATE INDEX IF NOT EXISTS idx_neigh_v2 ON neighbors(vertex_id_2);

CREATE TABLE IF NOT EXISTS elements (
    vertex_id BIGINT PRIMARY KEY REFERENCES vertices(id),
    Z INTEGER,
    symbol VARCHAR(3),
    period INTEGER,
    block VARCHAR(2),
    n_s INTEGER, n_p INTEGER, n_d INTEGER, n_f INTEGER,
    radius_ratio_pred DOUBLE PRECISION,
    radius_ratio_obs DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS molecules (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100),
    formula VARCHAR(50),
    vertex_ids BIGINT[],
    geometry_type VARCHAR(20),
    bond_angles DOUBLE PRECISION[],
    bond_lengths DOUBLE PRECISION[],
    total_energy DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS computations (
    id SERIAL PRIMARY KEY,
    n_half INTEGER NOT NULL,
    n_points INTEGER,
    n_bgs INTEGER,
    bgs_fraction DOUBLE PRECISION,
    gamma_bgs DOUBLE PRECISION,
    gamma_all DOUBLE PRECISION,
    has_voronoi BOOLEAN DEFAULT FALSE,
    has_cells BOOLEAN DEFAULT FALSE,
    compute_time_s DOUBLE PRECISION,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS gamma_convergence (
    n_half INTEGER PRIMARY KEY,
    n_bgs INTEGER,
    gamma DOUBLE PRECISION,
    gamma_err DOUBLE PRECISION,
    r0 DOUBLE PRECISION,
    fit_range_min DOUBLE PRECISION,
    fit_range_max DOUBLE PRECISION,
    n_fit_bins INTEGER
);
