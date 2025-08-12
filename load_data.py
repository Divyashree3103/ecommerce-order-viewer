import pandas as pd

# Load data
orders = pd.read_csv("orders.csv")
order_items = pd.read_csv("order_items.csv")
products = pd.read_csv("products.csv")
users = pd.read_csv("users.csv")
distribution_centers = pd.read_csv("distribution_centers.csv")
inventory_items = pd.read_csv("inventory_items.csv")

# Check data
print(orders.head())

