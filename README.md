# US Job Market & Salary Analytics — AWS ETL (Bronze → Silver → Gold)

## Overview
This project builds an end-to-end ETL pipeline on AWS to process job market and wage data.
Raw files land in S3 (Bronze), are cleaned and standardized into Parquet (Silver), and then curated into an analytics-ready dataset (Gold) for querying in Athena.

## Tech Stack
- AWS S3 (Bronze/Silver/Gold storage)
- AWS Glue (PySpark ETL)
- AWS Athena (SQL queries + validation)
- Python (Excel → cleaned Parquet pre-processing)

## Data Source
Public U.S. wage/occupation dataset (Excel).
*Note: Raw dataset files are not included in this repo to keep it lightweight.*

## Pipeline
1. **Bronze**: Raw Excel uploaded to `s3://.../bronze/`
2. **Silver**: Convert Excel → Parquet and clean values (replace `*`, `#`, blanks → NULL)
3. **Gold**: Select required columns, remove duplicates, export curated output for analytics

## Output Columns (Gold)
- area_title
- prim_state
- naics_title
- i_group
- occ_title
- tot_emp
- emp_prse
- h_mean
- a_mean
- mean_prse
- h_median
- a_median
- annual
- hourly

## How to Run
### Step 1 — Excel to Cleaned Parquet (local or CloudShell)
Run:
`python3 scripts/excel_to_cleaned_parquet.py`

Upload output Parquet to:
`s3://.../silver/`

### Step 2 — Glue Job (Silver → Gold)
Use Glue script in:
`glue/gold_curated_export.py`

Output written to:
`s3://.../gold/`

### Step 3 — Query in Athena
See:
`sql/athena_analysis_queries.sql`

## What I Learned
- Why Parquet is safer than CSV for Spark/Athena
- Handling Excel cleaning issues (symbols, blanks, schema)
- Glue DynamicFrame vs Spark DataFrame and schema consistency
- Building a lakehouse-style structure (Bronze/Silver/Gold)

## Future Enhancements (optional)
- Partition Gold by `prim_state` to reduce Athena scan cost
- Add Glue crawler + table versioning
- QuickSight / Power BI dashboard on Athena output
