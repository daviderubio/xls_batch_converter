# 📦 Imports
import pandas as pd
import os
import re
from glob import glob

# 📁 Define folders
input_folder = "../data/raw"
output_folder = "../data/output"
os.makedirs(output_folder, exist_ok=True)

# 📌 Helper to extract dynamic output filename
def get_dynamic_name(files):
    # Extract base names without extension
    base_names = [os.path.basename(f).replace(".xlsx", "") for f in files]
    # Remove initial digits and split by underscores
    stripped_parts = [re.sub(r'^\d+_', '', name).split('_') for name in base_names]
    # Get shared elements
    first_words = [parts[0] for parts in stripped_parts]
    second_words = ['_'.join(parts[1:]) for parts in stripped_parts]
    prefix = first_words[0]
    suffix = '_'.join(sorted(set(second_words)))
    return f"{prefix}_{suffix}"

# 📌 Helper to sort columns
def sort_columns(columns):
    time_cols = [col for col in columns if col.strip().lower() == "time (s)"]
    pre_cols = [col for col in columns if re.search(r'\d*pre', col.lower())]
    post_cols = [col for col in columns if re.search(r'\d*post', col.lower())]
    other_cols = [col for col in columns if col not in time_cols + pre_cols + post_cols]
    return time_cols + pre_cols + post_cols + other_cols

# 📥 Step 1: Process Excel files to individual CSVs
csv_files = []
for file_name in os.listdir(input_folder):
    if file_name.endswith(".xlsx"):
        file_path = os.path.join(input_folder, file_name)
        base_name = os.path.basename(file_path).replace(".xlsx", "")

        # Load sheets
        metadata_df = pd.read_excel(file_path, sheet_name="metadata", header=2)
        processed_df = pd.read_excel(file_path, sheet_name="Processed")

        # Replace headers using metadata
        name_to_source = dict(zip(metadata_df['name'], metadata_df['source name']))
        new_columns = [processed_df.columns[0]]
        for col in processed_df.columns[1:]:
            roi_name = col.replace(" Processed", "")
            source_name = name_to_source.get(roi_name, roi_name)
            new_columns.append(source_name)

        processed_df.columns = new_columns

        # Save individual CSV
        output_csv = os.path.join(output_folder, f"{base_name}.csv")
        processed_df.to_csv(output_csv, index=False)
        csv_files.append(output_csv)
        print(f"✅ Saved: {output_csv}")

# 🧩 Step 2: Merge CSVs
merged_df = None
for i, csv_file in enumerate(csv_files):
    df = pd.read_csv(csv_file)
    if i == 0:
        merged_df = df
    else:
        df = df.drop(columns=["Time (s)"], errors="ignore")  # Keep "Time (s)" only from the first file
        merged_df = pd.concat([merged_df, df], axis=1)

# 🧹 Step 3: Reorder columns
merged_df = merged_df[sort_columns(merged_df.columns)]

# 🧾 Step 4: Save merged CSV
merged_name = get_dynamic_name(csv_files)
merged_csv_path = os.path.join(output_folder, f"{merged_name}.csv")
merged_df.to_csv(merged_csv_path, index=False)
print(f"\n📦 Merged file saved as: {merged_csv_path}")
