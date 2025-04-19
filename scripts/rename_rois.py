# 📦 Imports
import pandas as pd
import os

# 📂 Load the Excel file
file_path = "/Users/davideusebiorubiodelossantos/Desktop/Code/projects/VT1211_odor_responses/data/raw/240911_absolute_1pre.xlsx"

# Extract the base name of the file without extension
base_name = os.path.basename(file_path).replace('.xlsx', '')

# Load the 'metadata' sheet, specifying the header as the 3rd row (index 2)
metadata_df = pd.read_excel(file_path, sheet_name="metadata", header=2)

# Load the 'Processed' sheet
processed_df = pd.read_excel(file_path, sheet_name="Processed")

# Create a mapping from 'name' to 'source name'
name_to_source = dict(zip(metadata_df['name'], metadata_df['source name']))

# Replace column headers in 'processed' (excluding the first column)
new_columns = [processed_df.columns[0]]  # Keep "Time (s)" as-is
for col in processed_df.columns[1:]:
    # Extract the ROI name (e.g., "ROI 1 - 1" from "ROI 1 - 1 Processed")
    roi_name = col.replace(" Processed", "")
    # Map to source name if available
    source_name = name_to_source.get(roi_name, roi_name)
    new_columns.append(source_name)

# Assign new columns
processed_df.columns = new_columns

# Define output folder path
output_folder = "data/output"

# Make sure the folder exists, if not, create it
os.makedirs(output_folder, exist_ok=True)

# Save to CSV with the name derived from the XLS file
output_csv = os.path.join(output_folder, f"{base_name}.csv")
processed_df.to_csv(output_csv, index=False)

print(f"✅ Processed data saved as: {output_csv}")