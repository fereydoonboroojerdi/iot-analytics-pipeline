CREATE TABLE sensor_readings (
    reading_time TIMESTAMP,
    device_id VARCHAR(255),
    factory_id VARCHAR(255),
    metrics SUPER,  -- JSON payload
    anomaly_score FLOAT
) DISTKEY(factory_id) SORTKEY(reading_time);

-- Materialized view for dashboards
CREATE MATERIALIZED VIEW hourly_metrics AS
SELECT 
    DATE_TRUNC('hour', reading_time) AS hour,
    factory_id,
    AVG(metrics.temperature::FLOAT) AS avg_temp,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY metrics.vibration::FLOAT) AS p95_vibration
FROM sensor_readings
GROUP BY 1, 2;