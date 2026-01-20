import mysql.connector
from mysql.connector import Error
import sys

# --- Configuration for Local Access ---
# Configuration dictionary for database connection.
# When accessing from the host machine (outside Docker), 'localhost' is used.
DB_CONFIG = {
    'user': 'root',
    'password': 'rootpassword',  # Ensure this matches docker-compose.yml
    'host': 'localhost',  # External access via exposed port 3306
    'port': '3306',
    'database': 'crypto_project'
}


def validate_data():
    """
    Connects to the MySQL database running in Docker via localhost and
    retrieves the latest aggregated data records.

    This function validates connectivity and data persistence.
    """
    print(f"[INFO] Attempting connection to MySQL at {DB_CONFIG['host']}:{DB_CONFIG['port']}...")

    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)

        if conn.is_connected():
            print("[SUCCESS] Database connection established.")

            cursor = conn.cursor()

            # 1. Validate table existence and retrieve row count
            cursor.execute("SELECT COUNT(*) FROM moving_averages")
            result = cursor.fetchone()
            count = result[0] if result else 0

            print(f"[INFO] Total record count in 'moving_averages': {count}")

            if count > 0:
                # 2. Retrieve and display the latest 5 entries
                print("\n[INFO] Retrieving latest 5 entries:")
                print(f"{'Symbol':<10} | {'Price':<15} | {'Window End'}")
                print("-" * 50)

                query = """
                        SELECT symbol, average_price, end_time
                        FROM moving_averages
                        ORDER BY end_time DESC LIMIT 5 \
                        """
                cursor.execute(query)
                rows = cursor.fetchall()

                for row in rows:
                    symbol = row[0]
                    # Ensure price is handled as a float for formatting
                    price = float(row[1])
                    end_time = row[2]
                    print(f"{symbol:<10} | {price:<15.4f} | {end_time}")
            else:
                print("[WARN] The 'moving_averages' table exists but contains no data.")
                print("[HINT] Ensure the Spark processor is running and generating data.")

    except Error as e:
        print(f"[ERROR] Database connection failed: {e}")
        print("[HINT] Verify that the Docker container is running using 'docker ps'.")
        print("[HINT] Ensure no local MySQL service is occupying port 3306.")

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            print("[INFO] Connection closed.")


if __name__ == "__main__":
    validate_data()