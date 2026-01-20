## 1. Purpose of This Document

This Incident Response Playbook provides standardized procedures for identifying, diagnosing, and resolving incidents affecting the Real-Time Crypto Streaming Pipeline.  
It is intended for on-call engineers, data engineers, and operations personnel responsible for restoring service availability and minimizing downtime.

This document follows enterprise incident management practices, including severity classification, escalation paths, and structured response workflows.

---

## 2. Incident Severity Levels

| Severity | Description | Example |
|----------|-------------|---------|
| SEV-1 | Full pipeline outage | Kafka down, Spark not running |
| SEV-2 | Major degradation | High Kafka lag, MySQL write failures |
| SEV-3 | Minor degradation | Intermittent producer failures |
| SEV-4 | Low-impact issues | Non-critical warnings, log noise |

---

## 3. Incident Response Workflow

1. **Detect** – Identify the issue via monitoring, logs, or alerts  
2. **Diagnose** – Determine root cause and affected components  
3. **Mitigate** – Apply temporary or permanent fixes  
4. **Recover** – Restore full functionality  
5. **Document** – Record incident details and lessons learned  

---

## 4. Common Incident Scenarios and Playbooks

---

## 4.1 Scenario: Kafka is Down (SEV‑1)

### Symptoms
- Producer cannot publish messages  
- Spark job fails to read from Kafka  
- Kafka CLI commands fail  

### Diagnostics
```bash
docker ps
docker compose logs kafka
```

### Immediate Actions
1. Restart Kafka:
   ```bash
   docker compose restart kafka
   ```
2. Validate topic existence:
   ```bash
   kafka-topics --bootstrap-server localhost:9092 --list
   ```
3. Restart producer and Spark processor.

### Root Cause Examples
- Container crash  
- Port conflict  
- Corrupted Kafka logs  

### Long-Term Actions
- Increase Kafka disk space  
- Add monitoring for broker health  
- Migrate to AWS MSK (future)  

---

## 4.2 Scenario: Spark Streaming Job Failure (SEV‑1 or SEV‑2)

### Symptoms
- Spark job stops processing  
- Micro-batch duration spikes  
- Errors in Spark logs  

### Diagnostics
Check logs:
```bash
grep -i error stream_processor.log
```

### Immediate Actions
1. Restart Spark processor:
   ```bash
   pkill -f stream_processor.py
   python src/processors/stream_processor.py &
   ```
2. Validate Kafka connectivity.  
3. Validate MySQL connectivity.

### Root Cause Examples
- Schema mismatch  
- Kafka connection failure  
- MySQL JDBC write failure  

### Long-Term Actions
- Add schema validation  
- Add retry logic for JDBC writes  
- Implement checkpointing  

---

## 4.3 Scenario: MySQL Not Writing Data (SEV‑2)

### Symptoms
- No new rows in `moving_averages`  
- JDBC write errors  
- MySQL connection refused  

### Diagnostics
```bash
sudo systemctl status mysql
```

### Immediate Actions
1. Restart MySQL:
   ```bash
   sudo systemctl restart mysql
   ```
2. Validate credentials.  
3. Validate table schema.

### Root Cause Examples
- MySQL service crash  
- Disk full  
- Incorrect JDBC configuration  

### Long-Term Actions
- Add MySQL monitoring  
- Add connection pooling  
- Optimize table indexes  

---

## 4.4 Scenario: Producer Not Sending Messages (SEV‑2 or SEV‑3)

### Symptoms
- Kafka topic receives no new messages  
- Producer logs show API failures  
- Binance API rate limits  

### Diagnostics
Check producer logs:
```bash
grep -i error btc_producer.log
```

### Immediate Actions
1. Restart producer:
   ```bash
   pkill -f btc_producer.py
   python src/producers/btc_producer.py &
   ```
2. Validate Binance API availability.  
3. Validate Kafka connectivity.

### Root Cause Examples
- API outage  
- Network issues  
- Serialization errors  

### Long-Term Actions
- Add retry with exponential backoff  
- Add API fallback endpoints  
- Add circuit breaker pattern  

---

## 4.5 Scenario: Kafka Topic Lag Increasing (SEV‑2)

### Symptoms
- Spark cannot keep up with ingestion  
- Growing backlog in Kafka  
- Delayed MySQL writes  

### Diagnostics
Check lag:
```bash
kafka-consumer-groups --bootstrap-server localhost:9092 --describe --group spark-group
```

### Immediate Actions
1. Increase Spark micro-batch interval.  
2. Restart Spark processor.  
3. Reduce producer frequency temporarily.

### Root Cause Examples
- Insufficient Spark processing capacity  
- Large message volume  
- Slow MySQL writes  

### Long-Term Actions
- Increase Kafka partitions  
- Deploy Spark on a cluster  
- Optimize MySQL writes  

---

## 5. Communication and Escalation

### 5.1 Escalation Path

1. On-call engineer  
2. Senior data engineer  
3. Engineering lead  
4. Cloud operations team (future)  

### 5.2 Communication Guidelines

- Provide clear incident summary  
- Include timestamps and logs  
- Document actions taken  
- Avoid speculation  

---

## 6. Post‑Incident Review (PIR)

After resolving an incident:

1. Document root cause  
2. Document timeline of events  
3. Identify what worked and what failed  
4. Propose preventive measures  
5. Update runbooks if needed  

---

## 7. Incident Documentation Template

```
Incident ID:
Severity:
Date/Time:
Reported By:

Summary:
Impact:
Root Cause:
Resolution:
Preventive Actions:
Logs and Evidence:
```

---

**End of Document**