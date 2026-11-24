import duckdb
import pandas as pd
import random
from datetime import datetime, timedelta

print("Connecting to DuckDB (Creating local database file)...")
# This creates a local file named 'legacy_warehouse.db'
con = duckdb.connect('legacy_warehouse.db')

# 1. Generate some Mock "Legacy" Data
print("Generating mock legacy data...")
customers_data = {
    'customer_id': [1, 2, 3, 4, 5],
    'name': ['Alice Smith', 'Bob Jones', 'Charlie Brown', 'Diana Prince', 'Evan Wright'],
    'signup_date': ['2023-01-15', '2023-02-20', '2023-03-10', '2023-04-05', '2023-05-12'],
    'region': ['North', 'South', 'East', 'West', 'North']
}

orders_data = []
for i in range(100): # Let's make 100 mock orders
    orders_data.append({
        'order_id': 1000 + i,
        'customer_id': random.randint(1, 5),
        'order_date': (datetime(2023, 6, 1) + timedelta(days=random.randint(0, 100))).strftime('%Y-%m-%d'),
        'amount': round(random.uniform(10.0, 500.0), 2),
        'status': random.choice(['completed', 'cancelled', 'pending', 'returned'])
    })

df_customers = pd.DataFrame(customers_data)
df_orders = pd.DataFrame(orders_data)

# 2. Load the data into DuckDB (The Bronze Layer)
print("Loading data into DuckDB 'bronze' schema...")
# Create a schema to mimic a modern data stack
con.execute("CREATE SCHEMA IF NOT EXISTS bronze;")

# Register the dataframes and create tables
con.execute("CREATE OR REPLACE TABLE bronze.customers AS SELECT * FROM df_customers;")
con.execute("CREATE OR REPLACE TABLE bronze.orders AS SELECT * FROM df_orders;")

# 3. Let's verify it worked!
print("\n--- Verification ---")
print("Customers in DB:")
print(con.execute("SELECT * FROM bronze.customers LIMIT 3").df())
print("\nTotal Orders in DB:")
print(con.execute("SELECT COUNT(*) as total_orders FROM bronze.orders").df())

print("\nSuccess! Your local DuckDB warehouse 'legacy_warehouse.db' is ready.")
con.close()
