# 🧪 CSV XLS Batch Converter (ordered columns)

A Python script to process and merge experimental signal recordings from Excel files. It converts each `.xlsx` file into a `.csv`, dynamically renames headers using metadata, and merges all `.csv` files into one master dataset with correctly ordered columns.

---

## 🚀 Features

- Reads Excel files with `metadata` and `Processed` sheets
- Maps processed ROI names to meaningful source names using metadata
- Saves cleaned CSVs
- Merges all CSVs into one final CSV:
  - Removes all duplicate `Time (s)` columns (only keeps the first)
  - Sorts headers: `Time (s)` → all `*pre*` columns → all `*post*` columns
- Dynamically generates the output filename based on content (e.g., `absolute_1pre_4post.csv`)

## 🧪 How-to / Steps

Start your environment 
    
    source environment_name/bin/activate
        
    if no environment is created, make one with 

        python -m venv /path-to-environments-folder/environment_name

Go to folder where your projects are stored

    cd path/to/your-repo

Git clone the XLS Batch Converter repo locally

    git clone https://github.com/daviderubio/xls_batch_converter.git

Prepare Your Files

        Place all Excel .xlsx files inside the data/raw/ folder.

        Each file should include at least:

            A sheet called metadata (with headers on the 3rd row)

            A sheet called Processed

Run the Script

        python xlsx_batch_converter_ordered.py
        
        or
        
        python3 xlsx_batch_converter_ordered.py

Check the Output

    Converted and renamed .csv versions of each Excel file will be saved in data/output/

    A merged dataset (e.g. absolute_1pre_4post.csv) will also appear in data/output/

## 📦 requirements.txt

    pandas>=1.0.0
    openpyxl>=3.0.0
    numpy>=1.18.0
    scipy>=1.4.0
    jupyter

This ensures compatibility with reading .xlsx files and DataFrame manipulation.

If you're using a virtual environment, you can install the dependencies with:

    pip install -r requirements.txt

## 🧰 Main Script

    xlsx_batch_converter_ordered.py

## 🧰 Secondary Scripts

    rename_rois.py

Purpose: Processes a single Excel file to rename the "Processed" sheet columns using the metadata and export it as a CSV (i.e. renames headers)

    folder_rename_rois.py 

Purpose: Processes multiple Excel file to rename the "Processed" sheet columns using the metadata and export it as a CSV (i.e. renames headers)

    xlsx_batch_converter.py

Purpose: renames headers, merges multiple CSVs

    xlsx_batch_converter_ordered.py // main script

Purpose: renames headers, merges multiple CSVs and orders columns by pre and post.