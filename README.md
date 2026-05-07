# 🚀 OrbitWatch

## Overview

**OrbitWatch** is a backend platform that simulates the telemetry processing pipeline used in modern satellite mission control systems.

The project focuses on high-throughput telemetry ingestion, asynchronous processing, anomaly detection, alert generation, and operational observability.

OrbitWatch is designed as a domain-oriented modular monolith inspired by backend architectures commonly used in aerospace and NewSpace engineering environments.

---

# ✨ Current Features

## Telemetry Ingestion Pipeline

- Batch telemetry ingestion API
- Redis Streams-based asynchronous processing
- Background telemetry workers
- Idempotent event processing
- Retry handling
- Dead Letter Queue (DLQ)

## Telemetry Processing

- Parameter extraction
- Dynamic parameter registration
- Threshold-based anomaly detection
- Alert generation engine
- Historical telemetry persistence

## Observability

- Structured logging
- Processing metrics
- Alert statistics endpoints
- Operational monitoring endpoints

## Satellite Management

- Satellite registry
- Parameter association
- Telemetry ownership validation

---

# 🏗 Architecture

OrbitWatch follows a modular monolith architecture.

Each domain owns its:
- API layer
- business logic
- persistence models

Current domains:

```
text
satellites/
telemetry/
alerts/
core/
```

The system is intentionally structured to evolve incrementally without premature microservice complexity.

# 📡 Telemetry Processing Flow

```
Client / Simulator
        │
        ▼
 FastAPI Ingestion API
        │
        ▼
 Redis Stream
        │
        ▼
 Telemetry Worker
        │
        ├── Validation
        ├── Idempotency Check
        ├── Parameter Resolution
        ├── Limit Evaluation
        ├── Alert Generation
        └── Persistence
        │
        ▼
 PostgreSQL
```

# 🔁 Reliability Features
## Idempotent Processing

Every telemetry event receives a unique event_id.

Processed events are tracked to prevent duplicate processing during retries or worker restarts.

## Retry Mechanism

Failed messages are automatically retried before being discarded.

This simulates resilient event processing commonly used in distributed backend systems.

## Dead Letter Queue (DLQ)

Messages that exceed retry limits are moved into a DLQ stream for later inspection.

This prevents poison messages from blocking the ingestion pipeline.

## 🚨 Alert Engine

OrbitWatch includes a telemetry limit evaluation engine.

Example:

```
temperature > 80  → WARNING
temperature > 95  → CRITICAL
```

When thresholds are violated:

alerts are generated
alerts are persisted
monitoring APIs expose alert history and statistics

# 📊 Monitoring APIs
## Retrieve Alerts

```
GET /alerts
```

## Alert Statistics

```
GET /alerts/stats
```

Example response:

```
[
  {
    "level": "CRITICAL",
    "count": 6
  }
]
```

# 🛰 Example Telemetry Payload

```
{
  "events": [
    {
      "satellite_id": "3ab5b981-607d-4f19-9f61-e4ecd5792351",
      "timestamp": "2026-01-01T00:00:00Z",
      "parameters": [
        {
          "name": "temperature",
          "value": 500
        }
      ]
    }
  ]
}
```

# 🧱 Tech Stack

## Backend

- Python 3.12+

- FastAPI

- SQLAlchemy 2.0

- PostgreSQL

- Redis Streams

- Alembic

- Docker

# 📂 Project Structure

```
app/
├── alerts/
├── core/
├── satellites/
├── telemetry/
│   ├── api/
│   ├── domain/
│   ├── services/
│   └── workers/
└── main.py
```

# ⚙️ Local Development

## Start Infrastructure

```
docker compose up -d
```

# Activate Virtual Environment (Windows)

```
venv\Scripts\activate
```

# Install Dependencies

```
pip install -r requirements.txt
```

# Run API

```
uvicorn app.main:app --reload
```

# Run Telemetry Worker

```
python -m app.telemetry.workers.telemetry_worker
```

# 🗃 Database Migrations

Generate migration:

```
alembic revision --autogenerate -m "message"
```

Apply migrations:

```
alembic upgrade head
```

# 🔭 Planned Extensions

- React operational dashboard

- Real-time telemetry visualization

- Orbit propagation (SGP4)

- Geospatial satellite tracking

- Time-series analytics

- Advanced anomaly detection

- Prometheus + Grafana integration

# 🎯 Project Goals

OrbitWatch is primarily a backend engineering project focused on:

- asynchronous systems

- telemetry pipelines

- resilient processing

- operational observability

- distributed-system patterns

- aerospace-inspired architectures

The goal is to simulate the kinds of backend systems used in real telemetry and mission operations environments while keeping the codebase understandable and incrementally extensible.
