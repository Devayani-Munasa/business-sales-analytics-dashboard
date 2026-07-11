import pandas as pd
import pymysql

from config import HOST, USER, PASSWORD, DATABASE

print("🚀 Starting Database Loader...")

# Connect to MySQL
connection = pymysql.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    database=DATABASE,
    port=3306,
    charset="utf8mb4"
)

print("✅ Connected to MySQL!")

cursor = connection.cursor()

# Read cleaned CSV
df = pd.read_csv("data/cleaned/cleaned_sales.csv")

print(f"✅ CSV Loaded ({len(df)} rows)")

print(df.head())