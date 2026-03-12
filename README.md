# 🚀 OrbitWatch

## Overview

**OrbitWatch** is a modular satellite mission control backend designed to simulate the architecture of modern small-satellite ground segment systems.

The project focuses on the telemetry pipeline used by Earth Observation (EO) satellites: ingestion, processing, anomaly detection, and archival.

OrbitWatch is structured as a domain-oriented modular monolith to reflect the backend design used by many NewSpace startups and mission control platforms.

The system is intentionally designed to evolve toward realistic mission control capabilities, including telemetry monitoring, anomaly detection, and geospatial satellite awareness.

---

## 🎯 Project Goals

### Phase 1 – Telemetry Platform (Current Focus)
- Telemetry ingestion (CCSDS-inspired structure)
- Telemetry measurement persistence
- Telemetry processing pipeline
- Parameter extraction
- Limit evaluation (basic anomaly detection)
- Alert generation
- Monitoring endpoints
- Telemetry query API
- Satellite registry

### Phase 2 – Orbital & Geospatial Awareness
- Satellite orbit propagation (SGP4)
- Ground track simulation
- Geospatial satellite visualization support
- Map-ready API endpoints
- Time-series telemetry analytics

### Phase 3 — Advanced Monitoring
- Event-driven telemetry processing
- Alert lifecycle management
- Satellite health state engine
- AI-based anomaly detection
- Mission planning primitives
  
---

## 🏗 Architecture Principles

OrbitWatch follows several architectural principles inspired by real backend systems used in satellite operations.

### Modular Monolith

The system is structured as a modular monolith where domains are separated internally while sharing a single deployable backend.

This approach allows:

- clean domain boundaries
- easier local development
- simpler deployment
- future migration to microservices if needed

### Domain-Oriented Structure

Instead of separating code by technical layers (controllers/services/models), OrbitWatch is organized by business domains.

Example: satellites, telemetry, core

Each domain contains its own API layer, business logic, and persistence code.

### API-First Design

OrbitWatch exposes its functionality through a REST API built with FastAPI, allowing external tools or mission dashboards to integrate easily.

## Telemetry Pipeline Architecture

Telemetry flows through several processing stages before being archived:

```
Satellite / Simulator
        │
        ▼
 Telemetry Ingestion API
        │
        ▼
 Telemetry Processing Layer
        │
        ├── Parameter validation
        ├── Limit evaluation
        ├── Alert generation
        └── Telemetry archival
        │
        ▼
 PostgreSQL
```

This mirrors the telemetry flow used in real mission control systems.

## 🧱 System Architecture

```
Client / Simulator
        │
        ▼
FastAPI API Layer
        │
        ▼
Application Services
        │
        ▼
Repository Layer
        │
        ▼
SQLAlchemy ORM
        │
        ▼
PostgreSQL (Docker)
```

### Responsibilities

#### API Layer
- request validation
- response serialization
- HTTP routing

#### Application Services
- orchestrate domain operations
- enforce business rules
- coordinate telemetry processing

#### Repository Layer
- abstract database operations
- isolate persistence logic

#### ORM
- map Python domain models to relational tables

#### PostgreSQL
- transactional storage
- time-series telemetry archive

## Telemetry Domain

OrbitWatch collects telemetry measurements from satellites.

Telemetry records represent time-series measurements produced by spacecraft subsystems.

Fields:
- satellite_id (UUID foreign key)
- timestamp
- temperature
- velocity
- altitude

A composite index (satellite_id, timestamp) is used to optimize time-range queries. This index optimizes the dominant telemetry query pattern: satellite_id + timestamp time range scans.

Typical query patterns:

- Retrieve telemetry for a satellite within a time range
- Stream recent telemetry values
- Perform aggregations (min, max, average)

## Telemetry Ingestion

Telemetry data is ingested using batch requests.

Instead of sending one measurement per request, the API accepts multiple telemetry measurements in a single request.

Benefits:
- Reduced network overhead
- Lower API load
- More efficient database writes
- Better scalability for high-frequency telemetry streams

- Endpoint:

```
POST /telemetry/batch
```

Example payload:

```
{
  "measurements": [
    {
      "satellite_id": "uuid",
      "temperature": 23.4,
      "velocity": 7600,
      "altitude": 690
    }
  ]
}
```

## 🔍 Telemetry Query API

OrbitWatch exposes a query API for retrieving historical telemetry.

```
GET /telemetry
```

Supported filters:
- satellite_id
- start_time
- end_time
- cursor
- limit
  
Example: /telemetry?satellite_id=<uuid>&limit=100

Cursor-based pagination allows efficient streaming of large telemetry datasets.

## 🚨 Limit Monitoring

OrbitWatch includes a basic limit monitoring engine for telemetry parameters.

Limit rules allow the system to detect anomalous conditions in satellite telemetry.

Example rule:

- temperature > 80°C  → WARNING
- temperature > 95°C  → CRITICAL

When a limit is violated, the telemetry processor generates an alert event.

Alerts can be queried through monitoring APIs and will later support lifecycle management.

## 🧠 Future AI Integration

The telemetry processing pipeline is designed to allow integration of machine learning models for anomaly detection.

Potential extensions include:

Isolation Forest anomaly detection

autoencoder-based telemetry anomaly detection

LSTM-based telemetry forecasting

AI-assisted satellite health classification

The architecture separates ingestion, processing, and analytics layers to enable future AI workloads without major refactoring.

## Project Structure

```
app/
 ├ core
 │   └ database.py
 │
 ├ satellites
 │   ├ api
 │   ├ domain
 │   └ infrastructure
 │
 ├ telemetry
 │   ├ api
 │   ├ domain
 │   ├ services
 │   └ infrastructure
 │
 └ main.py
```

### Layers

#### API

- HTTP endpoints and request/response schemas.

#### Domain

- Business entities and core domain models.

#### Services

- Application logic and orchestration.

#### Infrastructure

- Database repositories and persistence code.

---

## 🧰 Tech Stack

### Backend
- Python 3.12
- FastAPI
- SQLAlchemy 2.0
- PostgreSQL 16
- Alembic
- Docker

### Future Extensions
- PostGIS (geospatial queries)
- React mission dashboard
- Mapbox / Leaflet visualization
- Redis or Kafka event pipeline

---

## ⚙️ Development Setup

### 1️⃣ Start Database

```bash
docker compose up -d
```

2️⃣ Activate Virtual Environment (Windows)

```
venv\Scripts\activate
```

3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

## 🗃 Database Management

Schema evolution is handled using Alembic migrations.

Generate migration:
alembic revision --autogenerate -m "message"

Apply migration:
alembic upgrade head

## 🛰 Example API Call

Once the server is running:

```
uvicorn app.main:app --reload
```

Open Swagger UI:

```
http://127.0.0.1:8000/docs
```

Create a satellite:

POST /satellites

```
{
  "name": "Sentinel-1A",
  "norad_id": "39634"
}
```

If successful, the satellite will be stored in PostgreSQL.

## UUID Primary Keys

OrbitWatch uses UUID primary keys for all core entities.

Reasons:

- Safer in distributed systems

- Avoids sequential ID exposure

- Compatible with future multi-tenant SaaS architecture

- Production-grade identifier strategy

UUIDs are automatically generated using uuid4() at insertion time.

## 📌 Long-Term Vision

OrbitWatch is designed to evolve into a lightweight Earth Observation ground segment platform with:

- Telemetry monitoring

- Anomaly detection

- Geospatial awareness

- Mission planning support

The system is structured to allow integration of a future Flight Dynamics module without architectural refactoring.
