import pandas as pd
import os
import argparse
from datetime import datetime

#Initialize argument parser: make the script resuable
parser = argparse.ArgumentParser(description="Test environment by genrating a sample dataset.")
parser.add_argument("--output_path", type=str, required=True, help="Directory to save the output CSV file.")

#Parse arguments
args = parser.parse_args()
output_dir = args.output_path

#Ensure the output directory exists, if not create it
os.makedirs(output_dir, exist_ok=True)

#Generate sample data
data = {
    "id": [1, 2, 3, 4, 5],
    "name": ["Alice", "Alan", "Murphy", "Jack", "Silva"],
    "age": [18, 20, 35, 29, 69],
    "timestamp": [datetime.now() for _ in range(5)]
}

#Create dataframe
df = pd.DataFrame(data)

#Save to CSV File
output_file = os.path.join(output_dir, "sample_data.csv")
df.to_csv(output_file, index=False)

print(f"Sample file saved to {output_file} in {output_dir}")