
import duckdb
from pathlib import Path

# Read the SQL file
sql_file = Path("sql/analysis.sql")
sql_text = sql_file.read_text()

# Connect to DuckDB
con = duckdb.connect()

# Run each SQL statement separately
statements = [
    statement.strip()
    for statement in sql_text.split(";")
    if statement.strip()
]

for number, statement in enumerate(statements, start=1):
    print(f"\n--- QUERY {number} RESULTS ---")
    result = con.execute(statement)
    print(result.df().to_string(index=False))

con.close()
