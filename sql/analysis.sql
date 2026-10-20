
-- 1. Count the cleaned taxi trips
SELECT COUNT(*) AS total_trips
FROM read_parquet('data/processed/yellow_tripdata_2026-08_clean.parquet');

-- 2. Calculate total and average trip revenue
SELECT
    ROUND(SUM(total_amount), 2) AS total_recorded_amount,
    ROUND(AVG(total_amount), 2) AS average_amount_per_trip,
    ROUND(AVG(trip_distance), 2) AS average_trip_distance
FROM read_parquet('data/processed/yellow_tripdata_2026-08_clean.parquet');

-- 3. Find the busiest pickup hours
SELECT
    EXTRACT(HOUR FROM tpep_pickup_datetime) AS pickup_hour,
    COUNT(*) AS total_trips
FROM read_parquet('data/processed/yellow_tripdata_2026-08_clean.parquet')
GROUP BY pickup_hour
ORDER BY total_trips DESC;

-- Compare overall metrics with a basic valid-trip subset
SELECT
    COUNT(*) AS total_trips,
    ROUND(AVG(total_amount), 2) AS avg_recorded_amount,
    ROUND(AVG(trip_distance), 2) AS avg_distance,
    SUM(CASE WHEN total_amount < 0 THEN 1 ELSE 0 END)
        AS negative_total_amounts,
    SUM(CASE WHEN trip_distance <= 0 THEN 1 ELSE 0 END)
        AS nonpositive_distances
FROM read_parquet(
    'data/processed/yellow_tripdata_2026-08_clean.parquet'
);

-- Compare overall metrics against a stricter analysis subset
WITH trips AS (
    SELECT *
    FROM read_parquet(
        'data/processed/yellow_tripdata_2026-08_clean.parquet'
    )
)
SELECT
    'All retained trips' AS dataset,
    COUNT(*) AS trip_count,
    ROUND(AVG(total_amount), 2) AS avg_total_amount,
    ROUND(AVG(trip_distance), 2) AS avg_distance
FROM trips

UNION ALL

SELECT
    'Positive distance and nonnegative total' AS dataset,
    COUNT(*) AS trip_count,
    ROUND(AVG(total_amount), 2) AS avg_total_amount,
    ROUND(AVG(trip_distance), 2) AS avg_distance
FROM trips
WHERE trip_distance > 0
  AND total_amount >= 0;
