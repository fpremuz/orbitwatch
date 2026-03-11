# 🚀 OrbitWatch

## Overview

**OrbitWatch** is a modular Earth Observation (EO) satellite mission control backend designed to simulate a professional-grade ground segment system.

This project is architected to mirror real-world Mission Control Systems (MCS) used in NewSpace and small satellite companies.

It is not a tutorial project — it is built with production-oriented architectural decisions.

---

## 🎯 Project Goals

### Phase 1 – MVP
- Telemetry ingestion (CCSDS-inspired structure)
- Raw packet persistence
- Parameter extraction
- Limit evaluation (anomaly detection)
- Alert lifecycle management
- Monitoring API

### Phase 2 – Planned
- Geospatial satellite position simulation
- Ground track support
- Map-ready API endpoints
- Time-series telemetry endpoints
- Basic mission planning module

---

## 🏗 Architecture Principles

- Modular Monolith
- Domain-driven structure
- API-first backend
- PostgreSQL persistence
- Future PostGIS compatibility
- Containerized infrastructure
- CCSDS-inspired telemetry framing

## 🧱 System Architecture

Client → FastAPI API Layer → Repository Layer → SQLAlchemy ORM → PostgreSQL (Docker)

- API Layer handles HTTP requests
- Repository Layer abstracts database access
- ORM maps Python objects to relational schema
- PostgreSQL provides transactional persistence

## Telemetry Domain

OrbitWatch collects telemetry measurements from satellites.

Telemetry records represent time-series measurements associated with a satellite.

Fields:
- satellite_id (UUID foreign key)
- timestamp
- temperature
- velocity
- altitude

A composite index (satellite_id, timestamp) is used to optimize time-range queries.

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
- PostGIS
- React
- Leaflet / Mapbox GL

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

## 📌 Long-Term Vision

OrbitWatch is designed to evolve into a lightweight Earth Observation ground segment platform with:

- Telemetry monitoring

- Anomaly detection

- Geospatial awareness

- Mission planning support

The system is structured to allow integration of a future Flight Dynamics module without architectural refactoring.

## API Schema Validation

OrbitWatch uses Pydantic v2 for request and response validation.

Response models use:

```
model_config = ConfigDict(from_attributes=True)
```

This allows safe serialization of SQLAlchemy ORM objects into JSON responses while preventing internal database fields from being exposed.

## UUID Primary Keys

OrbitWatch uses UUID primary keys for all core entities.

Reasons:

- Safer in distributed systems

- Avoids sequential ID exposure

- Compatible with future multi-tenant SaaS architecture

- Production-grade identifier strategy

UUIDs are automatically generated using uuid4() at insertion time.
