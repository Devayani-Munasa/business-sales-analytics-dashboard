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
    charset="utf8mb4",
    autocommit=False
)

print("✅ Connected to MySQL!")

cursor = connection.cursor()

# Read cleaned CSV
df = pd.read_csv(
    "data/cleaned/cleaned_sales.csv",
    parse_dates=["order_date", "ship_date"]
)

print(f"✅ CSV Loaded ({len(df)} rows)")

insert_query = """
INSERT INTO sales (
    row_id,
    order_id,
    order_date,
    ship_date,
    ship_mode,
    customer_id,
    customer_name,
    segment,
    country,
    city,
    state,
    postal_code,
    region,
    product_id,
    category,
    sub_category,
    product_name,
    sales,
    quantity,
    discount,
    profit,
    order_year,
    order_month,
    profit_margin
)
VALUES (
    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
)
"""

print("📥 Inserting rows...")

count = 0

for _, row in df.iterrows():

    cursor.execute(
        insert_query,
        (
            int(row["row_id"]),
            row["order_id"],
            row["order_date"].date(),
            row["ship_date"].date(),
            row["ship_mode"],
            row["customer_id"],
            row["customer_name"],
            row["segment"],
            row["country"],
            row["city"],
            row["state"],
            int(row["postal_code"]),
            row["region"],
            row["product_id"],
            row["category"],
            row["sub_category"],
            row["product_name"],
            float(row["sales"]),
            int(row["quantity"]),
            float(row["discount"]),
            float(row["profit"]),
            int(row["order_year"]),
            row["order_month"],
            float(row["profit_margin"])
        )
    )

    count += 1

    if count % 1000 == 0:
        print(f"Inserted {count} rows...")

connection.commit()

print(f"\n🎉 Successfully inserted {count} rows!")

cursor.close()
connection.close()

print("✅ Database loading completed!")