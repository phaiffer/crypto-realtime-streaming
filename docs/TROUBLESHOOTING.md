## 1. Purpose of This Document

This document provides a structured troubleshooting guide for diagnosing and resolving issues within the Real-Time Crypto Streaming Pipeline.  
It covers ingestion, Kafka, Spark Structured Streaming, MySQL, and environment-related problems.

The content follows enterprise operational standards and is intended for engineers responsible for maintaining or debugging the system.

---

## 2. Troubleshooting Index

1. Kafka Issues  
2. Spark Streaming Issues  
3. MySQL Issues  
4. Producer Issues  
5. Docker Issues  
6. Environment Issues  
7. Common Error Messages and Resolutions  

---

## 3. Kafka Issues

### 3.1 Kafka is not receiving messages

**Symptoms:**
- No new messages in topic  
- Spark job shows empty micro-batches  
- Producer logs show successful sends but Kafka remains empty  

**Diagnostics:**
```bash
docker ps
```
Ensure Kafka and Zookeeper containers are running.

Check topic existence:
```bash
kafka-topics --bootstrap-server localhost:9092 --list
```

**Resolution:**
- Restart Kafka container  
- Recreate topic if missing  
- Validate `bootstrap_servers` in producer configuration  

---

### 3.2 Spark cannot connect to Kafka

**Symptoms:**
- Spark job fails on startup  
- Error: “Failed to connect to Kafka broker”  

**Diagnostics:**
Check advertised listeners in `docker-compose.yml`:
```
KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092
```

**Resolution:**
- Ensure port 9092 is not blocked  
- Restart Kafka and Spark job  
- Validate network connectivity inside Docker  

---

### 3.3 Kafka topic lag increases continuously

**Symptoms:**
- Spark cannot keep up with ingestion  
- Growing backlog in Kafka  

**Resolution:**
- Increase Spark micro-batch interval  
- Increase Kafka partitions  
- Scale Spark processing (future cluster deployment)  

---

## 4. Spark Structured Streaming Issues

### 4.1 Spark job fails to start

**Common causes:**
- Missing Kafka integration JAR  
- Incorrect Kafka bootstrap server  
- Invalid schema parsing  

**Resolution:**
Ensure Spark is started with Kafka package:
```
org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0
```

---

### 4.2 Spark job runs but produces no output

**Possible causes:**
- Empty Kafka topic  
- Incorrect JSON schema  
- Timestamp not parsed correctly  

**Diagnostics:**
Enable console sink temporarily:
```python
df.writeStream.format("console").start()
```

---

### 4.3 MySQL write failures from Spark

**Symptoms:**
- JDBC write errors  
- Duplicate key issues  
- Connection refused  

**Resolution:**
- Validate JDBC URL  
- Ensure MySQL is running  
- Check table permissions  
- Increase batch size for writes  

---

## 5. MySQL Issues

### 5.1 MySQL connection refused

**Diagnostics:**
```bash
systemctl status mysql
```

**Resolution:**
- Start MySQL service  
- Validate credentials  
- Ensure port 3306 is open  

---

### 5.2 Data not appearing in MySQL

**Possible causes:**
- Spark job not writing  
- Incorrect table name  
- Write mode misconfigured  

**Resolution:**
- Check Spark logs  
- Validate table schema  
- Confirm JDBC driver installation  

---

## 6. Producer Issues

### 6.1 Producer fails to fetch data from Binance API

**Symptoms:**
- HTTP errors  
- Empty responses  
- Rate limit exceeded  

**Resolution:**
- Implement retry logic  
- Add exponential backoff  
- Validate API endpoint availability  

---

### 6.2 Producer cannot publish to Kafka

**Diagnostics:**
- Check Kafka availability  
- Validate topic name  
- Confirm JSON serialization  

**Resolution:**
- Restart producer  
- Restart Kafka  
- Validate network connectivity  

---

## 7. Docker Issues

### 7.1 Containers fail to start

**Diagnostics:**
```bash
docker compose logs
```

**Resolution:**
- Remove orphan containers  
- Rebuild environment  
```bash
docker compose down
docker compose up -d
```

---

### 7.2 Port conflicts

**Symptoms:**
- Kafka or MySQL fails to bind to port  

**Resolution:**
- Identify conflicting processes  
```bash
sudo lsof -i :9092
sudo lsof -i :3306
```
- Stop or reassign ports  

---

## 8. Environment Issues

### 8.1 Python virtual environment issues

**Resolution:**
Recreate environment:
```bash
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

### 8.2 Java version mismatch for Spark

Spark requires Java 8 or 11.

Check version:
```bash
java -version
```

Install correct version if needed.

---

## 9. Common Error Messages and Resolutions

| Error Message | Cause | Resolution |
|---------------|--------|------------|
| “No such topic: crypto_prices” | Topic missing | Recreate topic |
| “Failed to connect to broker” | Kafka offline | Restart Kafka |
| “JDBC connection refused” | MySQL offline | Start MySQL |
| “Schema mismatch” | JSON parsing error | Validate schema |
| “Task not serializable” | Python closure issue | Refactor Spark code |

---

## 10. Escalation Procedure

If an issue cannot be resolved:

1. Collect logs from producer, Kafka, Spark, and MySQL  
2. Document reproduction steps  
3. Escalate to engineering lead or cloud operations team  

---

**End of Document**