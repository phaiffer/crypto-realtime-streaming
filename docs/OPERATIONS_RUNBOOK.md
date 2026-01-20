## 1. Purpose of This Document

This Operations Runbook provides standardized procedures for operating, monitoring, and maintaining the Real-Time Crypto Streaming Pipeline.  
It is intended for on-call engineers, data engineers, and operations personnel responsible for ensuring system reliability and continuity.

The runbook follows enterprise operational standards and includes daily, weekly, and monthly procedures, as well as operational checklists.

---

## 2. System Overview

The pipeline consists of:

- **Producer Layer** – Python producer fetching data from Binance API  
- **Kafka Layer** – Message broker for ingestion and buffering  
- **Spark Structured Streaming Layer** – Real-time processing engine  
- **MySQL Layer** – Storage for aggregated results  

Each component must be monitored and maintained to ensure end-to-end data flow.

---

## 3. Daily Operational Tasks

### 3.1 Validate Kafka Health

Commands:

```bash
docker ps
kafka-topics --bootstrap-server localhost:9092 --list
```

Checks:

- Kafka and Zookeeper containers are running  
- Topic `crypto_prices` exists  
- No abnormal restarts in container logs  

---

### 3.2 Validate Spark Streaming Job

Checks:

- Spark job is running without errors  
- Micro-batch processing time is stable  
- No backlog in Kafka (topic lag)  

Optional:

- Review Spark logs for warnings  
- Validate MySQL writes are occurring  

---

### 3.3 Validate Producer Health

Checks:

- Producer script is running  
- No API failures or rate limit errors  
- Messages are being published to Kafka  

---

### 3.4 Validate MySQL Storage

Commands:

```sql
SELECT COUNT(*) FROM moving_averages;
SELECT * FROM moving_averages ORDER BY start_time DESC LIMIT 10;
```

Checks:

- New rows are being inserted  
- No duplicate or corrupted data  
- Timestamps are correct  

---

## 4. Weekly Operational Tasks

### 4.1 Review Logs

Review logs for:

- Producer  
- Kafka  
- Spark  
- MySQL  

Look for:

- Repeated warnings  
- Connection failures  
- Serialization errors  
- Slow micro-batches  

---

### 4.2 Validate Schema Consistency

Ensure:

- Kafka message schema has not changed  
- Spark schema matches expected fields  
- MySQL table schema is intact  

---

### 4.3 Backup MySQL Database

Recommended:

```bash
mysqldump -u root -p crypto_streaming > backup.sql
```

Store backups securely.

---

## 5. Monthly Operational Tasks

### 5.1 Dependency Updates

Update:

- Python packages  
- Kafka Docker images  
- Spark version  
- MySQL version  

Ensure compatibility before upgrading.

---

### 5.2 Performance Review

Evaluate:

- Kafka throughput  
- Spark micro-batch duration  
- MySQL write latency  
- End-to-end latency  

Identify bottlenecks and plan improvements.

---

### 5.3 Capacity Planning

Review:

- Kafka disk usage  
- MySQL table growth  
- CPU and memory usage  

Plan scaling actions if needed.

---

## 6. Operational Procedures

### 6.1 Restarting the Producer

```bash
pkill -f btc_producer.py
python src/producers/btc_producer.py &
```

---

### 6.2 Restarting Kafka

```bash
docker compose restart kafka
```

---

### 6.3 Restarting Spark Processor

```bash
pkill -f stream_processor.py
python src/processors/stream_processor.py &
```

---

### 6.4 Restarting MySQL

```bash
sudo systemctl restart mysql
```

---

## 7. Monitoring Guidelines

### 7.1 Key Metrics

| Component | Metric | Description |
|----------|--------|-------------|
| Producer | API latency | Time to fetch data from Binance |
| Kafka | Topic lag | Messages waiting to be processed |
| Spark | Micro-batch duration | Time to process each batch |
| MySQL | Write latency | Time to insert aggregated rows |

---

### 7.2 Alerting (Future)

Recommended alerts:

- Kafka topic lag > threshold  
- Spark micro-batch duration > threshold  
- MySQL write failures  
- Producer API failure rate > threshold  

---

## 8. Incident Response

For detailed incident procedures, refer to:

```
docs/INCIDENT_PLAYBOOK.md
```

---

## 9. Contacts

Primary Maintainer:

**Willian Phaiffer Cardoso**  
Data Engineer  

---

**End of Document**