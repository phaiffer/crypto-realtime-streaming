import pytest
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, window, avg
from pyspark.sql.types import StructType, StructField, StringType, FloatType, TimestampType
from datetime import datetime


@pytest.fixture(scope="session")
def spark():
    """
    Creates a local SparkSession for testing.
    """
    return SparkSession.builder \
        .appName("UnitTesting") \
        .master("local[2]") \
        .getOrCreate()


def test_moving_average_calculation(spark):
    """
    Verifies if the Moving Average logic calculates the mean correctly.
    """
    # 1. Define Schema
    schema = StructType([
        StructField("symbol", StringType(), True),
        StructField("price", FloatType(), True),
        StructField("timestamp", TimestampType(), True)
    ])

    # 2. Create Dummy Data
    # We have 3 data points. The average of 100, 200, 300 is 200.
    data = [
        ("BTCUSDT", 100.0, datetime.strptime("2024-01-01 10:00:05", "%Y-%m-%d %H:%M:%S")),
        ("BTCUSDT", 200.0, datetime.strptime("2024-01-01 10:00:10", "%Y-%m-%d %H:%M:%S")),
        ("BTCUSDT", 300.0, datetime.strptime("2024-01-01 10:00:15", "%Y-%m-%d %H:%M:%S")),
    ]

    input_df = spark.createDataFrame(data, schema)

    # 3. Apply the EXACT logic from stream_processor.py
    # Group by 1 minute window and calculate average
    result_df = input_df \
        .groupBy(
        window(col("timestamp"), "1 minute"),
        col("symbol")
    ) \
        .agg(avg("price").alias("average_price"))

    # 4. Collect results to Python list
    results = result_df.collect()

    # 5. Assertions
    assert len(results) == 1  # Should be 1 window
    row = results[0]

    assert row['symbol'] == "BTCUSDT"
    # Average of 100, 200, 300 must be 200
    assert row['average_price'] == 200.0