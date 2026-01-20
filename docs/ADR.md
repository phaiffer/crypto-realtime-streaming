## 1. Purpose of This Document

This document captures key architectural decisions made during the design and implementation of the Real-Time Crypto Streaming Pipeline.  
Architecture Decision Records (ADRs) provide transparency, traceability, and justification for major technical choices.

Each ADR includes:
- Context  
- Decision  
- Alternatives considered  
- Consequences  

This format follows enterprise architecture documentation standards.

---

# ADR-001  
## Use Apache Kafka as the Message Broker

### Status  
Accepted

### Context  
The pipeline requires a reliable, scalable, and fault-tolerant messaging system to buffer real-time cryptocurrency price data between ingestion and processing layers.

### Decision  
Apache Kafka is used as the message broker for the `crypto_prices` topic.

### Alternatives Considered  
- **RabbitMQ** – Not optimized for high-throughput streaming workloads  
- **AWS Kinesis** – Cloud-only, not ideal for local development  
- **Redis Streams** – Less mature for large-scale streaming pipelines  

### Consequences  
- Enables horizontal scaling  
- Provides durability and backpressure handling  
- Requires operational overhead (mitigated by Docker Compose locally)

---

# ADR-002  
## Use Spark Structured Streaming for Real-Time Processing

### Status  
Accepted

### Context  
The system must process streaming data in real time, apply windowing, and compute aggregated metrics.

### Decision  
Spark Structured Streaming is used as the processing engine.

### Alternatives Considered  
- **Flink** – More complex to configure for local development  
- **Kafka Streams** – Limited for multi-symbol windowed aggregations  
- **Python-only processing** – Not scalable or fault-tolerant  

### Consequences  
- Provides fault tolerance and micro-batch processing  
- Integrates natively with Kafka  
- Enables future migration to distributed clusters (EMR, Databricks)

---

# ADR-003  
## Use MySQL as the Storage Layer

### Status  
Accepted

### Context  
The pipeline requires a persistent storage layer for aggregated results that supports SQL queries and integrates easily with Spark.

### Decision  
MySQL is used as the primary storage engine for aggregated moving averages.

### Alternatives Considered  
- **PostgreSQL** – Equivalent option; MySQL chosen for simplicity  
- **MongoDB** – Not ideal for analytical queries  
- **ClickHouse** – Excellent performance but more complex to operate  

### Consequences  
- Easy integration with Spark JDBC  
- Suitable for local development  
- May require migration to a more scalable store in the future

---

# ADR-004  
## Use 1-Minute Tumbling Windows for Aggregation

### Status  
Accepted

### Context  
The system must compute short-term moving averages for cryptocurrency prices.

### Decision  
A 1-minute tumbling window is used for aggregations.

### Alternatives Considered  
- Sliding windows  
- Longer windows (5–15 minutes)  
- Real-time incremental updates  

### Consequences  
- Provides timely insights  
- Reduces computational overhead  
- Easy to query and visualize  

---

# ADR-005  
## Use Docker Compose for Local Infrastructure

### Status  
Accepted

### Context  
Local development requires reproducible infrastructure for Kafka and MySQL.

### Decision  
Docker Compose is used to provision Kafka, Zookeeper, and MySQL.

### Alternatives Considered  
- Manual installation  
- Kubernetes (too heavy for local development)  
- Cloud-managed services (not ideal for offline work)  

### Consequences  
- Simplifies setup  
- Ensures consistent environments  
- Requires Docker installed locally  

---

# ADR-006  
## Use Python for the Producer Component

### Status  
Accepted

### Context  
The ingestion layer must fetch data from the Binance API and publish it to Kafka.

### Decision  
Python is used for the producer implementation.

### Alternatives Considered  
- Node.js – Good for async workloads but less common in data engineering  
- Java – More verbose, slower development cycle  
- Go – Excellent performance but unnecessary complexity  

### Consequences  
- Fast development  
- Easy integration with Kafka via `kafka-python`  
- Simple error handling and retries  

---

# ADR-007  
## Use JSON as the Message Format

### Status  
Accepted

### Context  
Messages must be serialized before being published to Kafka.

### Decision  
JSON is used as the message serialization format.

### Alternatives Considered  
- Avro – Requires Schema Registry  
- Protobuf – More efficient but adds complexity  
- CSV – Not suitable for nested structures  

### Consequences  
- Human-readable  
- Easy to parse in Spark  
- Slightly larger payload size  

---

# ADR-008  
## Use Local Mode for Spark Execution

### Status  
Accepted

### Context  
The project is designed for local development and portfolio demonstration.

### Decision  
Spark runs in local mode (`local[*]`).

### Alternatives Considered  
- Standalone Spark cluster  
- Kubernetes cluster  
- EMR or Databricks  

### Consequences  
- Simplifies development  
- Reduces infrastructure requirements  
- Limits scalability (acceptable for this project)

---

# ADR-009  
## Use a Single Kafka Topic for All Symbols

### Status  
Accepted

### Context  
The pipeline ingests multiple cryptocurrency symbols.

### Decision  
All symbols are published to a single Kafka topic (`crypto_prices`).

### Alternatives Considered  
- One topic per symbol  
- Partitioning by symbol  

### Consequences  
- Simplifies producer logic  
- Spark can group by symbol efficiently  
- Partitioning by symbol may be added later for scaling

---

# ADR-010  
## Use MySQL Timestamp Fields for Window Boundaries

### Status  
Accepted

### Context  
Aggregated results must include window start and end times.

### Decision  
MySQL `DATETIME` fields are used for `start_time` and `end_time`.

### Alternatives Considered  
- Unix timestamps  
- String-based timestamps  

### Consequences  
- Easy to query  
- Compatible with BI tools  
- Requires timezone consistency  

---

**End of Document**