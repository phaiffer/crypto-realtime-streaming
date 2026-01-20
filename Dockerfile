FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y default-jdk procps && \
    apt-get clean;

ENV JAVA_HOME=/usr/lib/jvm/default-java

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

CMD ["python", "--version"]# Use a lightweight Python base image
FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y default-jdk procps && \
    apt-get clean;

ENV JAVA_HOME=/usr/lib/jvm/default-java

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

CMD ["python", "--version"]