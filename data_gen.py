import numpy as np
import pandas as pd

np.random.seed(42)

n_points_per_sku = 365  # daily data for one year per SKU
sku_ids = [f"SKU{i:04d}" for i in range(1, 6)]
start_date = pd.Timestamp('2024-01-01')

all_data = []

for sku_id in sku_ids:
    dates = pd.date_range(start=start_date, periods=n_points_per_sku)

    base_price = np.random.uniform(80, 200)
    base_cost = base_price * np.random.uniform(0.5, 0.8)
    base_inventory = np.random.randint(30, 100)
    base_competitor_price = base_price * np.random.uniform(0.9, 1.1)

    prices = base_price * np.random.uniform(0.88, 1.10, n_points_per_sku)
    competitor_prices = base_competitor_price * np.random.uniform(0.90, 1.10, n_points_per_sku)
    inventory = np.maximum(base_inventory - np.cumsum(np.random.poisson(0.1, n_points_per_sku)), 0)

    # Demand parameters (varies per SKU to simulate elasticity differences)
    a = np.random.uniform(20, 60)
    b = np.random.uniform(0.1, 0.3)
    c = np.random.uniform(0.05, 0.2)

    noise = np.random.normal(0, 2, n_points_per_sku)
    units_sold = (a - b * prices + c * (competitor_prices - prices) + noise).round()
    units_sold = np.clip(units_sold, 0, None)

    cost = np.full(n_points_per_sku, base_cost)

    df = pd.DataFrame({
        'SKU': [sku_id] * n_points_per_sku,
        'Date': dates,
        'Units_Sold': units_sold.astype(int),
        'Price': prices.round(2),
        'Cost': cost.round(2),
        'Inventory': inventory,
        'Competitor_Price': competitor_prices.round(2)
    })

    all_data.append(df)

synthetic_data_multi_sku = pd.concat(all_data, ignore_index=True)
synthetic_data_multi_sku.head()
import os

# Define the directory and file path
directory = 'SampleData'
file_path = os.path.join(directory, 'data.csv')

# Create the directory if it doesn't exist
os.makedirs(directory, exist_ok=True)

# Append the data to the file
synthetic_data_multi_sku.to_csv(file_path, mode='a', index=False, header=not os.path.exists(file_path))
