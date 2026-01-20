## 1. Purpose of This Document

This document defines the testing strategy for the Real-Time Crypto Streaming Pipeline.  
It outlines the testing scope, methodologies, tools, and responsibilities required to ensure system reliability, correctness, and performance.

The testing approach follows enterprise engineering standards and is designed to support continuous integration, maintainability, and operational stability.

---

## 2. Testing Scope

Testing covers the following components:

1. **Producer Layer**  
2. **Kafka Integration**  
3. **Spark Structured Streaming Processor**  
4. **MySQL Persistence Layer**  
5. **End-to-End Pipeline Behavior**  
6. **Performance and Load Testing**  

---

## 3. Testing Types

### 3.1 Unit Tests

Unit tests validate individual functions and modules in isolation.

#### Producer Unit Tests
| Area | Description |
|------|-------------|
| API Client | Validate HTTP requests, response parsing, and error handling. |
| JSON Serialization | Ensure correct formatting and schema compliance. |
| Kafka Publisher | Mock Kafka producer to validate message publishing logic. |

#### Processor Unit Tests
| Area | Description |
|------|-------------|
| Schema Enforcement | Validate Spark schema parsing and type casting. |
| JSON Parsing | Ensure malformed messages are handled gracefully. |
| Window Aggregation | Validate 1-minute tumbling window logic. |

---

### 3.2 Integration Tests

Integration tests validate interactions between components.

#### Kafka → Spark Integration
- Validate Spark can consume messages from Kafka.  
- Ensure offsets are processed correctly.  
- Confirm schema compatibility.

#### Spark → MySQL Integration
- Validate JDBC connectivity.  
- Ensure aggregated results are written correctly.  
- Confirm idempotency and write consistency.

---

### 3.3 End-to-End Tests

End-to-end tests validate the entire pipeline:

1. Producer publishes messages to Kafka  
2. Spark consumes and processes messages  
3. MySQL receives aggregated results  

Success criteria:
- No data loss  
- Correct window aggregation  
- Correct symbol grouping  
- Timely data availability  

---

### 3.4 Performance and Load Testing

Performance testing ensures the system can handle expected and peak loads.

#### Metrics to Measure
- Kafka throughput (messages/sec)  
- Spark micro-batch processing time  
- MySQL write latency  
- End-to-end latency  

#### Load Scenarios
| Scenario | Description |
|----------|-------------|
| Baseline Load | 1 message/sec per symbol |
| Stress Load | 50–100 messages/sec |
| Spike Load | Sudden burst of 500+ messages |

---

### 3.5 Fault Tolerance Testing

Test system behavior under failure conditions:

| Failure | Expected Behavior |
|---------|-------------------|
| Kafka outage | Producer retries; Spark waits for recovery |
| MySQL outage | Spark retries JDBC writes |
| API failure | Producer retries with exponential backoff |
| Malformed messages | Spark filters or logs errors |

---

## 4. Test Environment

### 4.1 Local Development Environment
- Ubuntu  
- PyCharm  
- Python virtual environment (`.venv`)  
- Docker Compose for Kafka  
- Local MySQL instance  

### 4.2 Test Data

Synthetic test data should mimic Binance API responses:

```json
{
  "symbol": "BTCUSDT",
  "price": "42000.55",
  "timestamp": 1700000000.123
}
```

---

## 5. Tools and Frameworks

| Component | Tool |
|----------|------|
| Unit Testing | pytest |
| Mocking | unittest.mock |
| Spark Testing | pyspark local mode |
| Kafka Testing | kafka-python mock or TestContainers |
| Load Testing | Locust or custom Python scripts |
| Database Testing | mysql-connector-python |

---

## 6. Test Execution Strategy

### 6.1 Pre-Commit Tests
- Unit tests  
- Linting  
- Static analysis  

### 6.2 CI Pipeline Tests (Future)
- Unit + integration tests  
- Build validation  
- Docker image validation  

### 6.3 Manual Tests
- End-to-end pipeline validation  
- MySQL data inspection  

---

## 7. Test Coverage Goals

| Layer | Coverage Target |
|-------|-----------------|
| Producer | 80% |
| Processor | 70% |
| Utilities | 90% |
| End-to-End | Functional validation |

---

## 8. Known Testing Limitations

- Spark Structured Streaming is difficult to fully unit test due to micro-batch execution.  
- Kafka integration tests require containerized environments.  
- MySQL write tests may require cleanup scripts.  

---

## 9. Future Improvements

- Add TestContainers for Kafka and MySQL  
- Add CI/CD pipeline with automated testing  
- Add synthetic load generator for stress testing  
- Add schema validation using JSON Schema or Avro  

---

**End of Document**