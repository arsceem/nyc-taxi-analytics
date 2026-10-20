-- NYC Taxi Analytics: BigQuery Analysis
-- Dataset: August 2026 NYC yellow taxi trip records
-- Table: nyc-taxi-analytics-512206.nyc_taxi.yellow_trips

-- Query 1: Count all rows in the uploaded raw table
SELECT
  COUNT(*) AS total_trips
FROM
  `nyc-taxi-analytics-512206.nyc_taxi.yellow_trips`;

-- Query 2: Identify the busiest pickup hours in August 2026
SELECT
  EXTRACT(HOUR FROM tpep_pickup_datetime) AS pickup_hour,
  COUNT(*) AS total_trips
FROM
  `nyc-taxi-analytics-512206.nyc_taxi.yellow_trips`
WHERE
  tpep_pickup_datetime >= '2026-08-01'
  AND tpep_pickup_datetime < '2026-09-01'
GROUP BY
  pickup_hour
ORDER BY
  total_trips DESC;

-- Query 3: Analyze recorded amounts, distances, and potential data-quality issues
SELECT
  COUNT(*) AS total_trips,
  ROUND(AVG(trip_distance), 2) AS avg_distance_miles,
  ROUND(AVG(total_amount), 2) AS avg_total_amount,
  COUNTIF(total_amount < 0) AS negative_amount_trips,
  COUNTIF(trip_distance <= 0) AS nonpositive_distance_trips
FROM
  `nyc-taxi-analytics-512206.nyc_taxi.yellow_trips`
WHERE
  tpep_pickup_datetime >= '2026-08-01'
  AND tpep_pickup_datetime < '2026-09-01';