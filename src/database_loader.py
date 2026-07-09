print("Step 1: Program started")

import pandas as pd
import mysql.connector

print("Step 2: Libraries imported")

from config import HOST, USER, PASSWORD, DATABASE

print("Step 3: Config imported")

connection = mysql.connector.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    database=DATABASE
)

print("✅ Connected to MySQL!")

connection.close()

print("✅ Connection closed.")