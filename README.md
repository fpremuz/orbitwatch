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

## 📌 Long-Term Vision

OrbitWatch is designed to evolve into a lightweight Earth Observation ground segment platform with:

- Telemetry monitoring

- Anomaly detection

- Geospatial awareness

- Mission planning support

The system is structured to allow integration of a future Flight Dynamics module without architectural refactoring.
