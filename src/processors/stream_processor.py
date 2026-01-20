import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, avg
from pyspark.sql.types import StructType, StructField, StringType, FloatType, TimestampType

# --- Configuration ---
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
KAFKA_TOPIC = 'crypto_prices'

# --- MySQL Configuration ---
# 'host.docker.internal' allows Docker to talk to your local machine's MySQL
MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_PORT = "3306"
MYSQL_DB = "crypto_project"
MYSQL_USER = "root"
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'W!ll!@n55361316') # Security best practice

# JDBC Connection URL
JDBC_URL = f"jdbc:mysql://{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

# --- Spark Session Initialization ---
# We include 'mysql-connector-java' to allow Spark to write to the database
spark = SparkSession.builder \
    .appName("CryptoStreamingApp") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,mysql:mysql-connector-java:8.0.33") \
    .getOrCreate()

# Set logging level to WARN to reduce console clutter
spark.sparkContext.setLogLevel("WARN")

# --- Schema Definition ---
# Define the structure of the incoming JSON data from Kafka
schema = StructType([
    StructField("symbol", StringType(), True),
    StructField("price", FloatType(), True),
    StructField("timestamp", TimestampType(), True)
])

# --- 1. Read Stream from Kafka ---
raw_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
    .option("subscribe", KAFKA_TOPIC) \
    .option("startingOffsets", "latest") \
    .load()

# Parse JSON data and extract columns
parsed_df = raw_df.select(
    from_json(col("value").cast("string"), schema).alias("data")
).select("data.*")

# --- 2. Data Processing (Moving Average) ---
# Calculate the average price over a 1-minute window
moving_avg_df = parsed_df \
    .groupBy(
        window(col("timestamp"), "1 minute"),
        col("symbol")
    ) \
    .agg(avg("price").alias("average_price"))

# --- 3. Flatten Structure for MySQL ---
# MySQL requires flat columns, so we extract start/end times from the struct
final_df = moving_avg_df.select(
    col("window.start").alias("start_time"),
    col("window.end").alias("end_time"),
    col("symbol"),
    col("average_price")
)

# --- 4. Write Function (JDBC) ---
# This function is called for every batch of processed data
def write_to_mysql(df, epoch_id):
    try:
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
        print(f"Error writing to MySQL: {e}")

# --- 5. Start Streaming ---
print("Starting streaming to MySQL...")

# outputMode "update" is required when using aggregations like average
query = final_df.writeStream \
    .outputMode("update") \
    .foreachBatch(write_to_mysql) \
    .start()

query.awaitTermination()