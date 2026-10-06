CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS samples (
    id BIGSERIAL PRIMARY KEY,
    sample_no VARCHAR(100) NOT NULL UNIQUE,
    geom geometry(Point,4326) NOT NULL,
    gps_accuracy_m DOUBLE PRECISION,
    magnetometer_nt DOUBLE PRECISION,
    satellite_score DOUBLE PRECISION CHECK (
        satellite_score IS NULL
        OR (
            satellite_score >= 0
            AND satellite_score <= 100
        )
    ),
    photo_url TEXT,
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_samples_geom
    ON samples USING GIST (geom);

CREATE INDEX IF NOT EXISTS idx_samples_created_at
    ON samples (created_at);