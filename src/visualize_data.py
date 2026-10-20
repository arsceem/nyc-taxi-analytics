
import duckdb
import matplotlib.pyplot as plt
from pathlib import Path

# Load hourly trip counts from the cleaned Parquet file
con = duckdb.connect()

query = """
SELECT
    EXTRACT(HOUR FROM tpep_pickup_datetime) AS pickup_hour,
    COUNT(*) AS total_trips
FROM read_parquet(
    'data/processed/yellow_tripdata_2026-08_clean.parquet'
)
GROUP BY pickup_hour
ORDER BY pickup_hour;
"""

df = con.execute(query).df()
con.close()

# Create the chart
plt.figure(figsize=(12, 6))
plt.bar(df["pickup_hour"], df["total_trips"])

plt.title("NYC Yellow Taxi Trips by Pickup Hour")
plt.xlabel("Pickup Hour (24-hour clock)")
plt.ylabel("Number of Trips")
plt.xticks(range(24))
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

# Save the chart for your portfolio
output_path = Path("docs/trips_by_hour.png")
plt.savefig(output_path, dpi=150)
plt.show()

print(f"Chart saved to {output_path}")

# Analyze average distance and recorded amount by pickup hour
con = duckdb.connect()

hourly_query = """
SELECT
    EXTRACT(HOUR FROM tpep_pickup_datetime) AS pickup_hour,
    ROUND(AVG(trip_distance), 2) AS avg_distance,
    ROUND(AVG(total_amount), 2) AS avg_amount
FROM read_parquet(
    'data/processed/yellow_tripdata_2026-08_clean.parquet'
)
GROUP BY pickup_hour
ORDER BY pickup_hour;
"""

hourly_df = con.execute(hourly_query).df()
con.close()

# Chart average trip distance by hour
plt.figure(figsize=(12, 6))
plt.plot(
    hourly_df["pickup_hour"],
    hourly_df["avg_distance"],
    marker="o"
)

plt.title("Average NYC Taxi Trip Distance by Pickup Hour")
plt.xlabel("Pickup Hour (24-hour clock)")
plt.ylabel("Average Distance (miles)")
plt.xticks(range(24))
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig("docs/avg_distance_by_hour.png", dpi=150)
plt.show()

# Chart average recorded amount by hour
plt.figure(figsize=(12, 6))
plt.plot(
    hourly_df["pickup_hour"],
    hourly_df["avg_amount"],
    marker="o"
)

plt.title("Average Recorded Taxi Amount by Pickup Hour")
plt.xlabel("Pickup Hour (24-hour clock)")
plt.ylabel("Average Recorded Amount ($)")
plt.xticks(range(24))
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig("docs/avg_amount_by_hour.png", dpi=150)
plt.show()

print("Saved docs/avg_distance_by_hour.png")
print("Saved docs/avg_amount_by_hour.png")
