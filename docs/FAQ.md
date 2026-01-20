## 1. General Questions

### 1.1 What is the purpose of this project?
The project implements a real-time data engineering pipeline that ingests cryptocurrency price data from the Binance API, streams it through Kafka, processes it using Spark Structured Streaming, and stores aggregated results in MySQL.

---

### 1.2 Which cryptocurrencies are supported?
The pipeline currently supports:
- BTC  
- ETH  
- SOL  
- BNB  
- ADA  

Additional symbols can be added easily by modifying the producer logic.

---

### 1.3 Why use Kafka instead of sending data directly to Spark?
Kafka provides:
- Durability  
- Buffering  
- Backpressure handling  
- Decoupling between ingestion and processing  
- Horizontal scalability  

These characteristics make it ideal for real-time pipelines.

---

## 2. Producer Questions

### 2.1 How often does the producer fetch data?
The producer polls the Binance API every second.  
This interval can be adjusted in the producer script.

---

### 2.2 What happens if the Binance API is unavailable?
The producer:
- Retries failed requests  
- Logs errors  
- Continues execution without crashing  

---

### 2.3 Can I add more producers?
Yes.  
You can create additional producer scripts under:

```
src/producers/
```

Each producer can publish to the same or different Kafka topics.

---

## 3. Kafka Questions

### 3.1 Where is Kafka running?
Kafka is provisioned via Docker Compose and runs locally on:

```
localhost:9092
```

---

### 3.2 How do I check if Kafka is working?
Run:

```bash
docker ps
```

Then list topics:

```bash
kafka-topics --bootstrap-server localhost:9092 --list
```

---

### 3.3 What is the name of the Kafka topic?
The pipeline uses:

```
crypto_prices
```

---

## 4. Spark Questions

### 4.1 Why use Spark Structured Streaming?
Spark provides:
- Fault tolerance  
- Windowing support  
- Native Kafka integration  
- Distributed processing capabilities  

---

### 4.2 How often does Spark process data?
Spark uses micro-batches (default: 1 second).  
This can be tuned in the processor script.

---

### 4.3 What happens if Spark falls behind?
Kafka stores messages until Spark catches up.  
This prevents data loss.

---

## 5. MySQL Questions

### 5.1 What data is stored in MySQL?
MySQL stores aggregated 1-minute moving averages for each symbol.

---

### 5.2 How do I query the results?
Example:

```sql
SELECT * FROM moving_averages ORDER BY start_time DESC;
```

---

### 5.3 Can I use another database?
Yes.  
Spark supports JDBC connections to:
- PostgreSQL  
- SQL Server  
- Oracle  
- Snowflake  
- BigQuery (via connector)  

---

## 6. Deployment Questions

### 6.1 Can this pipeline run in the cloud?
Yes. Recommended architecture:

- Kafka → AWS MSK  
- Spark → AWS EMR or Databricks  
- MySQL → AWS RDS  
- Storage → S3  

---

### 6.2 Can I containerize the producer and processor?
Yes.  
Dockerfiles can be added for both components.

---

### 6.3 Is Kubernetes supported?
Yes.  
Spark can run on Kubernetes, and Kafka can be deployed using Helm charts.

---

## 7. Performance Questions

### 7.1 How many messages per second can the pipeline handle?
Local development:
- ~100–300 messages/sec

Cloud deployment:
- Thousands of messages/sec (depending on cluster size)

---

### 7.2 How do I scale the pipeline?
- Increase Kafka partitions  
- Deploy Spark on a cluster  
- Use a more scalable database (e.g., ClickHouse, BigQuery)  

---

## 8. Troubleshooting Questions

### 8.1 Why is MySQL not receiving data?
Possible causes:
- Spark JDBC configuration issue  
- MySQL not running  
- Incorrect credentials  

---

### 8.2 Why is Spark not consuming Kafka messages?
Possible causes:
- Incorrect Kafka bootstrap server  
- Topic does not exist  
- Missing Kafka integration JAR  

---

### 8.3 Why is the producer not sending messages?
Possible causes:
- Binance API failure  
- Kafka offline  
- Serialization errors  

---

## 9. Contribution Questions

### 9.1 How do I contribute?
Submit a pull request with:
- Clear description  
- Test coverage  
- Documentation updates  

---

### 9.2 Are coding standards enforced?
Yes.  
Follow PEP 8 for Python and Spark best practices.

---

## 10. Contact

For questions or support, contact:

**Willian Phaiffer Cardoso**  
Maintainer and Data Engineer  

---

**End of Document**
