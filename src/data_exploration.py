import pandas as pd

# Load dataset
df = pd.read_csv("data/raw/superstore_sales.csv")

print("=" * 50)
print("SALES DATASET OVERVIEW")
print("=" * 50)

# First 5 rows
print("\nFirst 5 Rows:")
print(df.head())

# Dataset shape
print("\nDataset Shape:")
print(df.shape)

# Column names
print("\nColumns:")
print(df.columns.tolist())

# Data types
print("\nData Types:")
print(df.dtypes)

# Missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Basic statistics
print("\nBasic Statistics:")
print(df.describe())