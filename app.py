import pandas as pd
from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route("/")
def index():
    # Load your CSV
    folder_path = os.getcwd()
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    
    if not csv_files:
        return "No CSV files found in this folder."

    df = pd.read_csv(os.path.join(folder_path, csv_files[0]))  # Use the first CSV
    return render_template("orders.html", tables=[df.to_html(classes="table table-striped", index=False)], titles=df.columns.values)

if __name__ == "__main__":
    app.run(debug=True)
