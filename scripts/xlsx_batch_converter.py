# 📦 Imports
import pandas as pd
import os
import re
from collections import defaultdict

# Define folders
input_folder = "../data/raw"
output_folder = "../data/output"
os.makedirs(output_folder, exist_ok=True)

# Track all generated CSV files
generated_csv_files = []

# 📁 Step 1: Convert Excel files to processed CSVs
for file_name in os.listdir(input_folder):
    if file_name.endswith('.xlsx'):
        file_path = os.path.join(input_folder, file_name)
        base_name = os.path.basename(file_path).replace('.xlsx', '')

        # Read Excel sheets
        metadata_df = pd.read_excel(file_path, sheet_name="metadata", header=2)
        processed_df = pd.read_excel(file_path, sheet_name="Processed")

        # Map headers
        name_to_source = dict(zip(metadata_df['name'], metadata_df['source name']))
        new_columns = [processed_df.columns[0]]  # Preserve "Time (s)"
        for col in processed_df.columns[1:]:
            roi_name = col.replace(" Processed", "")
            source_name = name_to_source.get(roi_name, roi_name)
            new_columns.append(source_name)
        processed_df.columns = new_columns

        # Save processed CSV
        output_csv = os.path.join(output_folder, f"{base_name}.csv")
        processed_df.to_csv(output_csv, index=False)
        generated_csv_files.append(output_csv)
        print(f"✅ Processed data saved as: {output_csv}")

# 📁 Step 2: Merge CSVs into one (keeping one "Time (s)" column)
merged_df = None
filenames = []

for i, csv_file in enumerate(generated_csv_files):
    df = pd.read_csv(csv_file)

    if i == 0:
        merged_df = df  # Keep "Time (s)" column in first file
    else:
        # Drop "Time (s)" from subsequent files
        df = df.drop(columns=["Time (s)"], errors='ignore')
        merged_df = pd.concat([merged_df, df], axis=1)

    filenames.append(os.path.basename(csv_file).replace('.csv', ''))

# 📄 Step 3: Dynamically generate output filename
base_parts = [re.sub(r'^\d+_', '', name) for name in filenames]

grouped = defaultdict(set)
for part in base_parts:
    split_parts = part.split('_', 1)
    if len(split_parts) == 2:
        prefix, suffix = split_parts
        grouped[prefix].add(suffix)

dynamic_names = []
for prefix, suffixes in grouped.items():
    combined_suffix = '_'.join(sorted(suffixes))
    dynamic_name = f"{prefix}_{combined_suffix}"
    dynamic_names.append(dynamic_name)

merged_file_name = dynamic_names[0] + ".csv"
merged_file_path = os.path.join(output_folder, merged_file_name)

# 💾 Save merged CSV
merged_df.to_csv(merged_file_path, index=False)
print(f"\n📎 Merged file saved as: {merged_file_path}")
