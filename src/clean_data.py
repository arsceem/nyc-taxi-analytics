
import pandas as pd
from pathlib import Path

# File locations
input_file = Path("data/raw/yellow_tripdata_2026-08.parquet")
output_file = Path("data/processed/yellow_tripdata_2026-08_clean.parquet")

# Load the original data
df = pd.read_parquet(input_file)

# Record the original row count
original_rows = len(df)

# Calculate trip duration in minutes
df["trip_duration_minutes"] = (
    df["tpep_dropoff_datetime"] - df["tpep_pickup_datetime"]
).dt.total_seconds() / 60

# Identify records with invalid chronological timestamps
valid_duration = df["trip_duration_minutes"] > 0

# Keep trips whose pickup timestamps fall in August 2026
valid_pickup_month = (
    (df["tpep_pickup_datetime"] >= "2026-08-01")
    & (df["tpep_pickup_datetime"] < "2026-09-01")
)

# Report how many records fail each rule
invalid_duration_count = (~valid_duration).sum()
outside_month_count = (~valid_pickup_month).sum()

# Apply both cleaning rules
clean_df = df.loc[valid_duration & valid_pickup_month].copy()

# Ensure the output directory exists
output_file.parent.mkdir(parents=True, exist_ok=True)

# Save the cleaned dataset
clean_df.to_parquet(output_file, index=False)

# Report cleaning results
print("--- CLEANING SUMMARY ---")
print(f"Original rows: {original_rows:,}")
print(f"Rows with nonpositive duration: {invalid_duration_count:,}")
print(f"Rows with pickup outside August 2026: {outside_month_count:,}")
print(f"Cleaned rows: {len(clean_df):,}")
print(f"Rows removed overall: {original_rows - len(clean_df):,}")
print(
    "Zero-duration trips retained: "
    f"{(clean_df['trip_duration_minutes'] == 0).sum()}"
)
print(f"Saved to: {output_file}")

# Apply both rules
clean_df = df.loc[valid_duration & valid_pickup_month].copy()

# Ensure the output directory exists
output_file.parent.mkdir(parents=True, exist_ok=True)

# Save cleaned data
clean_df.to_parquet(output_file, index=False)

# Report results
print("--- CLEANING SUMMARY ---")
print(f"Original rows: {original_rows:,}")
print(f"Cleaned rows: {len(clean_df):,}")
print(f"Rows removed: {original_rows - len(clean_df):,}")
print(f"Saved to: {output_file}")
print(f"Zero-duration trips retained: {(clean_df['trip_duration_minutes'] == 0).sum()}")
