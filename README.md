# Real-Time Crypto Streaming Pipeline

A production-grade data engineering pipeline for ingesting, processing, and storing real-time cryptocurrency market data.  
This system is designed for low-latency analytics and follows modern streaming architecture principles using Apache Kafka, Spark Structured Streaming, and MySQL.

---

## Repository: `crypto-realtime-streaming`

This repository contains the full implementation of the pipeline, including:

- Python producer for Binance API ingestion  
- Kafka integration via Docker Compose  
- Spark Structured Streaming processor  
- MySQL persistence layer  
- Modular architecture for scalability and maintainability  

---

## System Overview

**Data Flow:**

Binance API → Python Producer → Kafka → Spark Streaming → MySQL

**Symbols tracked:** BTC, ETH, SOL, BNB, ADA  
**Aggregation window:** 1-minute tumbling window  
**Storage:** MySQL table `moving_averages`

---

## Quick Start

### 1. Start Kafka and Zookeeper

```bash
docker compose up -d
```

### 2. Start the Producer

```bash
python src/producers/btc_producer.py
```

### 3. Start the Spark Processor

```bash
python src/processors/stream_processor.py
```

### 4. Validate in MySQL

```sql
SELECT * FROM moving_averages ORDER BY start_time DESC;
```

---

## Project Structure

```
crypto-realtime-streaming/
│
├── src/
│   ├── producers/
│   │   ├── __init__.py
│   │   └── btc_producer.py
│   ├── processors/
│   │   ├── __init__.py
│   │   └── stream_processor.py
│
├── docker-compose.yml
├── requirements.txt
├── README.md
└── docs/
    ├── ARCHITECTURE.md
    ├── C4_MODEL.md
    ├── ROADMAP.md
    ├── TROUBLESHOOTING.md
    ├── TESTING.md
    ├── SECURITY.md
    ├── PERFORMANCE.md
    ├── FAQ.md
    ├── OPERATIONS_RUNBOOK.md
    ├── INCIDENT_PLAYBOOK.md
    └── ADR.md
```

---

## Documentation Index

Detailed technical documentation is located in the `/docs` directory and is categorized as follows:

### Architecture and Design
- [System Architecture](docs/ARCHITECTURE.md) – High-level overview of the system flow and components.
- [C4 Model Diagrams](docs/C4_MODEL.md) – Structured visual abstraction of the system architecture.
- [Architectural Decision Records (ADR)](docs/ADR.md) – Historical log of key technical and design decisions.

### Operations and Maintenance
- [Troubleshooting Guide](docs/TROUBLESHOOTING.md) – Solutions for common runtime and connectivity issues.
- [Operations Runbook](docs/OPERATIONS_RUNBOOK.md) – Standard operating procedures for managing the pipeline.
- [Incident Playbook](docs/INCIDENT_PLAYBOOK.md) – Response protocols for critical system failures.

### Quality and Performance
- [Testing Strategy](docs/TESTING.md) – Documentation of unit, integration, and streaming test protocols.
- [Security Guidelines](docs/SECURITY.md) – Security standards and data protection measures.
- [Performance Benchmarks](docs/PERFORMANCE.md) – Analysis of system latency and scaling capabilities.

### Roadmap and FAQ
- [Project Roadmap](docs/ROADMAP.md) – Strategic plan for upcoming features and system enhancements.
- [Frequently Asked Questions (FAQ)](docs/FAQ.md) – Reference for common inquiries regarding the project.

---

## Author

Developed by Willian Phaiffer Cardoso  
Location: Matinhos, Paraná, Brazil