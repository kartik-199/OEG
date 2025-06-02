import numpy as np
import pandas as pd

np.random.seed(42)

n_points = 1000

base_price = 120
base_cost = 80
base_inventory = 50
base_competitor_price = 115

dates = pd.date_range(start='2025-01-01', periods=n_points)

prices = base_price * np.random.uniform(0.88, 1.10, n_points)

competitor_prices = base_competitor_price * np.random.uniform(0.90, 1.10, n_points)

inventory = np.maximum(base_inventory - np.cumsum(np.random.poisson(0.05, n_points)), 0)


a = 40
b = 0.2
c = 0.1

units_sold = (a - b * prices + c * (competitor_prices - prices) + np.random.normal(0, 2, n_points)).round()
units_sold = np.clip(units_sold, 0, None)  # no negative sales

# Cost is fixed (can add some noise if you want)
cost = np.full(n_points, base_cost)

# SKU ID repeated
sku = ['OEM1234'] * n_points

# Create DataFrame
synthetic_data = pd.DataFrame({
    'SKU': sku,
    'Date': dates,
    'Units_Sold': units_sold.astype(int),
    'Price': prices.round(2),
    'Cost': cost,
    'Inventory': inventory,
    'Competitor_Price': competitor_prices.round(2)
})

# Save to CSV
synthetic_data.to_csv('data.csv', mode='a', index=False, header=False)
