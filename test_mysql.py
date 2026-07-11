import mysql.connector

print("Program Started")

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Hrithik.11@",
        database="sales_dashboard",
        connection_timeout=5
    )

    print("✅ Connected successfully!")

    conn.close()
    print("✅ Connection closed")

except Exception as e:
    print("❌ Error:")
    print(type(e))
    print(e)