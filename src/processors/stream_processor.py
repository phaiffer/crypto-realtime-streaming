import os
import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, avg
from pyspark.sql.types import StructType, StructField, StringType, FloatType, TimestampType

# --- Configuration ---
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
KAFKA_TOPIC = 'crypto_prices'

# --- MySQL Configuration ---
MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_PORT = os.getenv('MYSQL_PORT', "3306")
MYSQL_DB = os.getenv('MYSQL_DB', "crypto_project")
MYSQL_USER = os.getenv('MYSQL_USER', "root")

# Security: Get password from environment. If it doesn't exist, stop the program.
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
if not MYSQL_PASSWORD:
    print("CRITICAL ERROR: Environment variable MYSQL_PASSWORD is not set.")
    sys.exit(1)

# JDBC Connection URL
JDBC_URL = f"jdbc:mysql://{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?useSSL=false&allowPublicKeyRetrieval=true"

# --- Spark Session Initialization ---
spark = SparkSession.builder \
    .appName("CryptoStreamingApp") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,mysql:mysql-connector-java:8.0.33") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# --- Schema Definition ---
schema = StructType([
    StructField("symbol", StringType(), True),
    StructField("price", FloatType(), True),
    StructField("timestamp", TimestampType(), True)
])

# --- 1. Read Stream from Kafka ---
# Added failOnDataLoss=false to prevent errors if Kafka restarts
raw_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
    .option("subscribe", KAFKA_TOPIC) \
    .option("startingOffsets", "latest") \
    .option("failOnDataLoss", "false") \
    .load()

parsed_df = raw_df.select(
    from_json(col("value").cast("string"), schema).alias("data")
).select("data.*")

# --- 2. Data Processing (Moving Average) ---
moving_avg_df = parsed_df \
    .groupBy(
        window(col("timestamp"), "1 minute"),
        col("symbol")
    ) \
    .agg(avg("price").alias("average_price"))

# --- 3. Flatten Structure for MySQL ---
final_df = moving_avg_df.select(
    col("window.start").alias("start_time"),
    col("window.end").alias("end_time"),
    col("symbol"),
    col("average_price")
)

# --- 4. Write Function (JDBC) ---
def write_to_mysql(df, epoch_id):
    try:
        # Check if DataFrame is not empty before attempting to write
        if df.count() > 0:
            df.write \
                .format("jdbc") \
                .option("url", JDBC_URL) \
                .option("driver", "com.mysql.cj.jdbc.Driver") \
                .option("dbtable", "moving_averages") \
                .option("user", MYSQL_USER) \
                .option("password", MYSQL_PASSWORD) \
                .mode("append") \
                .save()
            print(f"Batch {epoch_id} written to MySQL successfully.")
    except Exception as e:
        print(f"Error writing to MySQL (Batch {epoch_id}): {e}")

# --- 5. Start Streaming ---
print("Starting streaming to MySQL...")
print(f"JDBC Configuration: Host={MYSQL_HOST}, DB={MYSQL_DB}, User={MYSQL_USER}")

query = final_df.writeStream \
    .outputMode("update") \
    .foreachBatch(write_to_mysql) \
    .start()

query.awaitTermination()