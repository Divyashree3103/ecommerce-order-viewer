import pandas as pd
import os

# Get the current working directory
current_dir = os.getcwd()
print(f"Current working directory: {current_dir}")

# Loop through files in the current folder
for file in os.listdir():
    if file.endswith(".xlsx"):
        csv_file = file.replace(".xlsx", ".csv")
        df = pd.read_excel(file)
        df.to_csv(csv_file, index=False)
        print(f"Converted {file} → {os.path.join(current_dir, csv_file)}")

print("All Excel files converted to CSV.")
