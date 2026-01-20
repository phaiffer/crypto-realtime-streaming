## 1. Purpose of This Document

This document defines the security guidelines and best practices for the Real-Time Crypto Streaming Pipeline.  
It outlines controls, policies, and recommendations to ensure the confidentiality, integrity, and availability of the system and its data.

The guidelines follow enterprise security standards aligned with OWASP, NIST, and cloud security best practices.

---

## 2. Security Objectives

The security strategy for this project focuses on:

1. **Protecting sensitive configuration data**  
2. **Ensuring secure communication between components**  
3. **Preventing unauthorized access to infrastructure**  
4. **Maintaining data integrity across the pipeline**  
5. **Ensuring safe handling of external API interactions**  

---

## 3. Secrets and Credential Management

### 3.1 Never store credentials in source code

Prohibited items in the repository:

- MySQL passwords  
- Kafka credentials (future cloud deployment)  
- API keys  
- Access tokens  

### 3.2 Use environment variables

Recommended approach:

```
export MYSQL_USER=...
export MYSQL_PASSWORD=...
export KAFKA_BOOTSTRAP=localhost:9092
```

### 3.3 Use `.env` files (local only)

- `.env` must be included in `.gitignore`  
- Never commit `.env` to GitHub  

---

## 4. Network and Communication Security

### 4.1 Kafka

For local development, plaintext communication is acceptable.  
For production environments:

- Enable TLS encryption  
- Enable SASL authentication  
- Restrict network access to Kafka brokers  
- Use AWS MSK or Confluent Cloud for managed security  

### 4.2 Spark Structured Streaming

- Use secure Kafka connections (SASL_SSL) in production  
- Restrict Spark driver and executor network access  

### 4.3 MySQL

- Enforce strong passwords  
- Restrict access to localhost or private subnets  
- Enable SSL for remote connections  
- Use least-privilege database accounts  

---

## 5. Data Security

### 5.1 Data in Transit

| Component | Local Dev | Production |
|----------|------------|------------|
| Producer → Kafka | Plaintext | TLS |
| Kafka → Spark | Plaintext | TLS |
| Spark → MySQL | Plaintext | TLS |

### 5.2 Data at Rest

- Kafka logs should be stored on encrypted disks in production  
- MySQL storage should use disk encryption (LUKS, EBS encryption, etc.)  
- Backups must be encrypted  

---

## 6. API Security

### 6.1 Binance API

Although Binance API does not require authentication for price endpoints:

- Implement rate limiting  
- Implement retry logic with exponential backoff  
- Validate all responses before processing  

### 6.2 Input Validation

All external data must be validated:

- JSON schema validation  
- Type casting  
- Null checks  
- Timestamp validation  

---

## 7. Application Security

### 7.1 Python Producer

- Sanitize all external inputs  
- Handle API failures gracefully  
- Log errors without exposing sensitive data  

### 7.2 Spark Processor

- Validate schema before processing  
- Handle malformed messages  
- Avoid arbitrary code execution in UDFs  

---

## 8. Infrastructure Security

### 8.1 Docker Security

- Use official images (Confluent, MySQL, Spark)  
- Avoid running containers as root  
- Restrict exposed ports  
- Keep images updated  

### 8.2 Host Security

- Keep Ubuntu packages updated  
- Restrict SSH access  
- Use firewall rules (UFW)  
- Disable unused services  

---

## 9. Logging and Monitoring

### 9.1 Logging Guidelines

Logs must not contain:

- Passwords  
- API keys  
- Personal data  

Logs should include:

- Error messages  
- Processing failures  
- Kafka offsets  
- MySQL write failures  

### 9.2 Monitoring (Future)

- Integrate Grafana dashboards  
- Add alerting for pipeline failures  
- Monitor Kafka lag  
- Monitor Spark micro-batch latency  

---

## 10. Compliance Considerations

Depending on deployment environment, the system may need to comply with:

- GDPR (if storing user data — currently not applicable)  
- SOC 2 (for enterprise environments)  
- Internal security audits  

---

## 11. Future Security Enhancements

- Implement HashiCorp Vault or AWS Secrets Manager  
- Add Kafka Schema Registry with compatibility checks  
- Add IAM-based access control for cloud deployments  
- Add network segmentation and VPC isolation  
- Implement TLS mutual authentication  

---

## 12. Security Contacts

For security-related issues, contact the project maintainer:

**Willian Phaiffer Cardoso**  
Maintainer and Data Engineer  

---

**End of Document**