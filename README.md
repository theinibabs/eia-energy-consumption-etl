# Automated ETL Pipeline for Energy Consumption Data

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](#)
[![pandas](https://img.shields.io/badge/pandas-Data%20Manipulation-150458?logo=pandas&logoColor=white)](#)
[![Data: US EIA](https://img.shields.io/badge/Data-US%20EIA%20MER-blue)](#)

## Overview
This repository contains an automated data extraction, cleaning, and transformation (ETL) script built to process multi-sheet primary energy consumption reports from the U.S. Energy Information Administration (EIA) Monthly Energy Review (Table 1.3).

Official EIA spreadsheets contain non-tabular metadata, split two-row headers, embedded units, and missing values marked as text (e.g., "Not Available")[cite: 46, 47]. While initial data validation and exploratory cleaning were performed manually in Excel, this Python pipeline completely automates the workflow to ensure future monthly and annual releases can be cleaned and standardized instantly for downstream reporting and analytics.

---

## Project Structure
- data/raw/Table_1.3_Primary_Energy_Consumption_by_Source.xlsx
- data/processed/Table_1.3_Primary_Energy_Consumption_by_Source_Excel_Cleaned.xlsx
- data/processed/Table_1.3_Primary_Energy_Consumption_by_Source_Python_Cleaned.xlsx
- scripts/eia_data_cleaning.py
- .gitignore
- README.md

---

## What the Pipeline Does

1. Multi-Sheet Ingestion & Metadata Stripping:
   - Programmatically ingests both the 'Monthly Data' and 'Annual Data' tabs from the source workbook.
   - Skips the first 10 rows of top-level administrative metadata, update notes, and publication headers.

2. Programmatic Header Reconstruction:
   - Dynamically pairs metric descriptions from row 10 with their respective measurement units from row 11 (e.g., combining "Coal Consumption" and "(Quadrillion Btu)" into "Coal Consumption (Quadrillion Btu)").
   - Standardizes time identifiers across datasets ("Month" for monthly observations and "Year" for annual observations).
   - Drops auxiliary unit rows and resets the DataFrame index.

3. Logical Masking & Missing Data Handling:
   - In earlier historical periods, commercial solar and wind installations had not begun contribution reporting, recorded by the EIA as "Not Available".
   - Uses boolean masks to isolate specific historical windows:
     - Monthly: Replaces "Not Available" with 0.0 for Solar and Wind (1973–1983).
     - Annual: Replaces "Not Available" with 0.0 for Geothermal, Solar, and Wind (1949–1983).

4. Type Enforcement & Datetime Standardization:
   - Converts arbitrary string month representations ('%b %Y') into standardized datetime objects (YYYY-MM-01).
   - Converts integer years into proper datetime stamps.
   - Applies vectorized numeric conversion across all energy metric series to enforce float types and eliminate mixed-type column issues.

5. Automated Export:
   - Outputs the cleaned data into a dual-sheet workbook (*_Python_Cleaned.xlsx) with file permission handling.

---

## Getting Started

### Prerequisites
- Python 3.8+
- Required packages:
  pip install pandas openpyxl

### Running the Script
Run the pipeline directly from your terminal:
python scripts/eia_data_cleaning.py

When prompted, provide the path to the raw EIA file:
Enter file path: data/raw/Table_1.3_Primary_Energy_Consumption_by_Source.xlsx

The script will print summary validation statistics (min/max ranges per column) and write the processed dataset to data/processed/.