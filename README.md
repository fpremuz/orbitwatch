OrbitWatch
Overview

OrbitWatch is a modular Earth Observation satellite mission control backend designed to simulate a professional ground segment system.

The project aims to replicate core components of real-world Mission Control Systems (MCS) used in small satellite and NewSpace companies.

This is not a demo project.
It is architected as a production-oriented backend foundation with future geospatial capabilities.

Project Goals

Phase 1 (MVP):

Telemetry ingestion (CCSDS-like structure)

Raw packet persistence

Parameter extraction

Limit evaluation

Alert lifecycle management

Backend monitoring API

Phase 2 (Planned):

Geospatial satellite position simulation

Ground track visualization support

Map-ready API endpoints

Time-series telemetry endpoints

Basic mission planning module

Architecture Principles

Modular monolith

Domain separation

API-first backend

PostgreSQL persistence

Future PostGIS compatibility

Containerized environment

Industry-aligned telemetry structure (CCSDS-inspired)

Tech Stack

Backend:

Python 3.12

FastAPI

SQLAlchemy 2.0

PostgreSQL 16

Alembic

Docker

Future:

PostGIS

React

Leaflet / Mapbox GL

Current Status

Environment setup in progress:

Dockerized PostgreSQL

Python virtual environment

Dependency installation

Development Setup

Start database:

docker compose up -d


Activate virtual environment:

venv\Scripts\activate


Install dependencies:

pip install -r requirements.txt

Long-Term Vision

OrbitWatch is designed to evolve into a lightweight Earth Observation ground segment platform with telemetry monitoring, anomaly detection, and geospatial awareness capabilities.