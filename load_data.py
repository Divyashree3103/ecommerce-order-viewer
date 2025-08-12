import pandas as pd
import os

# Path to your current folder
folder_path = os.getcwd()

# Get all CSV files in the folder
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

print("CSV files found:", csv_files)

# Loop through each CSV and show first few rows
for file in csv_files:
    print(f"\n--- Preview of {file} ---")
    df = pd.read_csv(os.path.join(folder_path, file))
    print(df.head())  # First 5 rows
    print("\nColumns:", df.columns.tolist())
