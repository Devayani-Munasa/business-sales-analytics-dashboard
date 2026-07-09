import pandas as pd

# ===============================
# Load Dataset
# ===============================
df = pd.read_csv("data/raw/superstore_sales.csv")

print("=" * 50)
print("DATA CLEANING")
print("=" * 50)

# ===============================
# Convert Date Columns
# ===============================
df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)
df["Ship Date"] = pd.to_datetime(df["Ship Date"], dayfirst=True)

print("\n✅ Date columns converted.")

# ===============================
# Check Duplicate Records
# ===============================
duplicates = df.duplicated().sum()
print(f"\nDuplicate Rows: {duplicates}")

# Remove duplicates if any
if duplicates > 0:
    df = df.drop_duplicates()
    print("✅ Duplicate rows removed.")
else:
    print("✅ No duplicate rows found.")

# ===============================
# Standardize Column Names
# ===============================
df.columns = (
    df.columns
      .str.strip()
      .str.lower()
      .str.replace(" ", "_")
      .str.replace("-", "_")
)

print("\n✅ Column names standardized.")

# ===============================
# Create New Features
# ===============================

# Order Year
df["order_year"] = df["order_date"].dt.year

# Order Month
df["order_month"] = df["order_date"].dt.month_name()

# Profit Margin (%)
df["profit_margin"] = (df["profit"] / df["sales"]) * 100

print("✅ New columns created.")

# ===============================
# Dataset Information
# ===============================
print("\nFinal Shape:", df.shape)

print("\nNew Columns:")
print(df.columns.tolist())

# ===============================
# Save Cleaned Dataset
# ===============================
df.to_csv("data/cleaned/cleaned_sales.csv", index=False)

print("\n✅ Cleaned dataset saved successfully!")