import mysql.connector

print("Program Started")

try:
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Hrithik.11@",
        database="sales_dashboard",
        connection_timeout=10
    )

    print("✅ Connected!")

except Exception as e:
    print("❌ Error:")
    print(e)

finally:
    try:
        conn.close()
        print("Connection Closed")
    except:
        pass

print("Program Finished")