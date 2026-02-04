import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import numpy as np

# ------------------------
# Config
# ------------------------
XLSX_FILE = "all_data_M_2024.xlsx"
SHEET_NAME = "All May 2024 data"
PARQUET_OUT = "all_data_M_2024_cleaned.parquet"

# ------------------------
# Read Excel (as STRING to avoid type issues)
# ------------------------
df = pd.read_excel(
    XLSX_FILE,
    sheet_name=SHEET_NAME,
    header=0,
    engine="openpyxl",
    dtype=str
)

# ------------------------
# Clean column names
# ------------------------
df.columns = [str(c).strip() for c in df.columns]
df = df.loc[:, ~df.columns.str.match(r"^Unnamed")]

# ------------------------
# Trim whitespace
# ------------------------
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# ------------------------
# Replace bad values with NULL
# ------------------------
df = df.replace(
    to_replace=[r"^\s*$", r"^\*$", r"^#*$"],
    value=np.nan,
    regex=True
)

df = df.replace(
    {"N/A": np.nan, "NA": np.nan, "na": np.nan}
)

# ------------------------
# Preview
# ------------------------
print("Shape:", df.shape)
print(df.head(3).to_string(index=False))

# ------------------------
# Write Parquet (ALL columns as STRING — safest)
# ------------------------
schema = pa.schema([
    pa.field(col, pa.string()) for col in df.columns
])

table = pa.Table.from_pandas(
    df,
    schema=schema,
    preserve_index=False
)

pq.write_table(
    compression="snappy"
)   PARQUET_OUT,

print("Wrote Parquet:", PARQUET_OUT)
