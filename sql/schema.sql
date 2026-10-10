
CREATE TABLE IF NOT EXISTS dim_route (
    route_id TEXT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS dim_stop (
    stop_id TEXT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS dim_trip (
    trip_id TEXT PRIMARY KEY,
    route_id TEXT REFERENCES dim_route(route_id)
);

CREATE TABLE IF NOT EXISTS fact_prediction_observation (
    prediction_id TEXT NOT NULL,
    ingested_at TIMESTAMPTZ NOT NULL,
    trip_id TEXT REFERENCES dim_trip(trip_id),
    stop_id TEXT REFERENCES dim_stop(stop_id),
    schedule_id TEXT,
    predicted_arrival TIMESTAMPTZ,
    scheduled_arrival TIMESTAMPTZ,
    predicted_departure TIMESTAMPTZ,
    scheduled_departure TIMESTAMPTZ,
    arrival_delay_seconds INTEGER,
    prediction_status TEXT,
    stop_sequence INTEGER,
    PRIMARY KEY (prediction_id, ingested_at)
);

CREATE INDEX IF NOT EXISTS idx_prediction_trip
    ON fact_prediction_observation (trip_id);

CREATE INDEX IF NOT EXISTS idx_prediction_stop
    ON fact_prediction_observation (stop_id);

CREATE INDEX IF NOT EXISTS idx_prediction_ingested_at
    ON fact_prediction_observation (ingested_at);
