## 1. Purpose of This Document

This document outlines the performance characteristics, tuning strategies, and optimization guidelines for the Real-Time Crypto Streaming Pipeline.  
It provides recommendations for improving throughput, reducing latency, and ensuring scalability across ingestion, streaming, and storage layers.

The content follows enterprise engineering standards and is intended for performance engineers, data engineers, and system architects.

---

## 2. Performance Objectives

The system is designed to achieve:

- **Low-latency ingestion** from Binance API  
- **High-throughput message handling** in Kafka  
- **Efficient micro-batch processing** in Spark  
- **Reliable and fast writes** to MySQL  
- **Scalability** across all pipeline components  

---

## 3. Performance Characteristics by Component

### 3.1 Python Producer

Key performance factors:

- API request frequency  
- JSON serialization overhead  
- Kafka publish latency  

Optimization recommendations:

- Use persistent HTTP sessions (`requests.Session`)  
- Batch API calls when possible (future enhancement)  
- Use asynchronous I/O for higher throughput  
- Enable Kafka message compression (`snappy` or `lz4`)  

---

### 3.2 Kafka

Kafka is the backbone of the pipeline and must be tuned for throughput and durability.

Key performance factors:

- Number of partitions  
- Replication factor  
- Message size  
- Compression type  

Recommended configurations (development):

| Setting | Value |
|--------|--------|
| Partitions | 3 |
| Replication Factor | 1 |
| Compression | lz4 |
| Retention | 24 hours |

Recommended configurations (production):

| Setting | Value |
|--------|--------|
| Partitions | 6–12 |
| Replication Factor | 3 |
| Compression | snappy |
| Acks | all |

---

### 3.3 Spark Structured Streaming

Spark performance depends on:

- Micro-batch interval  
- Kafka read parallelism  
- Window aggregation complexity  
- JDBC write throughput  

Optimization recommendations:

#### Micro-Batch Interval
- Default: 1 second  
- Increase to 2–5 seconds for higher throughput  

#### Kafka Parallelism
Increase partitions to increase Spark parallelism.

#### Caching
Cache intermediate DataFrames when reused.

#### Serialization
Use Kryo serialization for faster processing:

```python
spark.conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
```

#### Shuffle Optimization
Enable Tungsten and whole-stage code generation (enabled by default).

---

### 3.4 MySQL

MySQL performance depends on:

- Write batch size  
- Indexing strategy  
- Table schema  
- Storage engine  

Optimization recommendations:

- Use `InnoDB` storage engine  
- Add index on `(symbol, start_time)`  
- Use batch inserts via Spark JDBC:

```python
.option("batchsize", "5000")
```

- Increase MySQL buffer pool size  
- Avoid unnecessary indexes  

---

## 4. End-to-End Latency Targets

| Stage | Target Latency |
|--------|----------------|
| Producer → Kafka | < 50 ms |
| Kafka → Spark | < 200 ms |
| Spark Processing | < 1 second per micro-batch |
| Spark → MySQL | < 300 ms |
| End-to-End | < 2 seconds |

---

## 5. Load Testing Strategy

### 5.1 Load Scenarios

| Scenario | Description |
|----------|-------------|
| Baseline | 1 msg/sec per symbol |
| Stress | 50–100 msg/sec |
| Spike | 500+ msg/sec |

### 5.2 Metrics to Monitor

- Kafka topic lag  
- Spark micro-batch duration  
- MySQL write throughput  
- CPU and memory usage  
- Network throughput  

### 5.3 Tools

- Locust (API load testing)  
- Custom Python scripts  
- Kafka performance tools (`kafka-producer-perf-test.sh`)  
- Spark UI  
- MySQL Performance Schema  

---

## 6. Bottleneck Analysis

### 6.1 Producer Bottlenecks

Symptoms:
- Slow API calls  
- High CPU usage  
- Kafka publish delays  

Mitigation:
- Use async I/O  
- Reduce logging  
- Enable compression  

---

### 6.2 Kafka Bottlenecks

Symptoms:
- Increasing topic lag  
- High disk I/O  
- Slow consumer throughput  

Mitigation:
- Increase partitions  
- Use SSD storage  
- Tune broker settings  

---

### 6.3 Spark Bottlenecks

Symptoms:
- Long micro-batch durations  
- High shuffle time  
- Slow JDBC writes  

Mitigation:
- Increase executor memory (future cluster deployment)  
- Optimize window operations  
- Increase JDBC batch size  

---

### 6.4 MySQL Bottlenecks

Symptoms:
- Slow inserts  
- Table locks  
- High CPU usage  

Mitigation:
- Add indexes  
- Increase buffer pool  
- Use connection pooling  

---

## 7. Scaling Strategies

### 7.1 Horizontal Scaling

- Increase Kafka partitions  
- Deploy Spark on a cluster (EMR, Databricks, Kubernetes)  
- Use MySQL read replicas (future)  

### 7.2 Vertical Scaling

- Increase CPU/RAM for Kafka broker  
- Increase Spark driver/executor memory  
- Increase MySQL instance size  

---

## 8. Future Performance Enhancements

- Migrate to AWS MSK for managed Kafka  
- Use Spark Structured Streaming with continuous processing mode  
- Replace MySQL with a columnar store (ClickHouse, BigQuery, Snowflake)  
- Introduce Apache Iceberg or Delta Lake for analytical workloads  
- Add autoscaling policies for cloud deployments  

---

**End of Document**