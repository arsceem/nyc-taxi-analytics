
import pandas as pd

# Location of our downloaded taxi dataset
file_path = "data/raw/yellow_tripdata_2026-08.parquet"

# Load the dataset
df = pd.read_parquet(file_path)

# 1. Dataset size
print("\n--- DATASET SIZE ---")
print(f"Rows: {df.shape[0]:,}")
print(f"Columns: {df.shape[1]}")

# 2. Column names and data types
print("\n--- COLUMN TYPES ---")
print(df.dtypes)

# 3. Missing values
print("\n--- MISSING VALUES ---")
print(df.isnull().sum().sort_values(ascending=False))

# 4. Basic statistics
print("\n--- NUMERIC SUMMARY ---")
print(df.describe())

# 5. First five records
print("\n--- FIRST FIVE RECORDS ---")
print(df.head())

# 6. Investigate data quality
print("\n--- DATA QUALITY CHECKS ---")

# Expected reporting period: August 2026
start_date = pd.Timestamp("2026-08-01")
end_date = pd.Timestamp("2026-09-01")

outside_month = (
    (df["tpep_pickup_datetime"] < start_date)
    | (df["tpep_pickup_datetime"] >= end_date)
)

invalid_duration = (
    df["tpep_dropoff_datetime"] <= df["tpep_pickup_datetime"]
)

negative_fares = df["fare_amount"] < 0
negative_totals = df["total_amount"] < 0
nonpositive_distance = df["trip_distance"] <= 0

print("Pickups outside August:", outside_month.sum())
print("Dropoff at or before pickup:", invalid_duration.sum())
print("Negative fares:", negative_fares.sum())
print("Negative total amounts:", negative_totals.sum())
print("Zero or negative distances:", nonpositive_distance.sum())

# Display examples of records with suspicious pickup dates
print("\n--- EXAMPLES OF PICKUPS OUTSIDE AUGUST ---")
print(
    df.loc[
        outside_month,
        [
            "tpep_pickup_datetime",
            "tpep_dropoff_datetime",
            "trip_distance",
            "fare_amount",
            "total_amount",
        ],
    ].head(10)
)

# 7. Calculate trip duration in minutes
df["trip_duration_minutes"] = (
    df["tpep_dropoff_datetime"] - df["tpep_pickup_datetime"]
).dt.total_seconds() / 60

print("\n--- TRIP DURATION CHECK ---")

print("Negative durations:",
      (df["trip_duration_minutes"] < 0).sum())

print("Zero-minute durations:",
      (df["trip_duration_minutes"] == 0).sum())

print("\nExamples of negative-duration trips:")
print(
    df.loc[
        df["trip_duration_minutes"] < 0,
        [
            "tpep_pickup_datetime",
            "tpep_dropoff_datetime",
            "trip_duration_minutes",
            "trip_distance",
            "fare_amount",
        ],
    ].head(10)
)
