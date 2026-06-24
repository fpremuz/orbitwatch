# 🚀 OrbitWatch

## Overview

**OrbitWatch** is a full-stack aerospace-inspired telemetry platform that simulates the telemetry processing and operational monitoring systems used in modern satellite mission control environments.

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

## AI Integration

- AI-powered telemetry insight generation
  
- OpenRouter-based LLM integration
  
- Provider abstraction layer for future model expansion
  
- Operational analysis endpoint
  
- AI service isolation from core telemetry pipeline

## Operational Dashboard

- React + TypeScript frontend
  
- Real-time telemetry visualization
  
- Live websocket telemetry streaming
  
- Satellite selection dashboard
  
- Historical telemetry charts
  
- Alert monitoring interface

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
ai/
core/
```

The system is intentionally structured to evolve incrementally without premature microservice complexity.

The platform also includes a separate frontend operational dashboard that communicates with the backend through REST APIs and websocket telemetry streams.

# 📡 Telemetry Processing Flow

```
React Dashboard
        │
        ├── REST API Requests
        └── WebSocket Telemetry Stream
                    │
                    ▼
          FastAPI Backend
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

## 🤖 AI Operational Insights

OrbitWatch includes an AI integration layer capable of generating operational telemetry insights using large language models.

The AI subsystem is intentionally isolated from the core telemetry pipeline to preserve processing reliability and avoid coupling mission-critical ingestion flows to external inference providers.

Current capabilities:

- Telemetry analysis endpoint
- Provider abstraction architecture
- OpenRouter integration
- Free-model support for local development and experimentation
- Persistent AI conversations
- Conversation management APIs
- LangGraph workflow orchestration

The architecture is designed to support future extensions such as:

- anomaly explanation
- alert summarization
- mission-status reporting
- operational recommendations
- AI-assisted observability workflows

## 💬 Conversational AI

OrbitWatch now includes a persistent AI assistant interface.

Capabilities:

- Multi-turn conversations

- Persistent chat history

- Conversation restoration

- Conversation titles

- React chat interface

- OpenAI integration

- Database-backed conversation storage

The architecture is designed to evolve toward Retrieval-Augmented Generation (RAG) and agent-based workflows.

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
    "severity": "CRITICAL",
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

- OpenRouter API

- LLM Integration Layer

- LangGraph

## Frontend

- React

- TypeScript

- Vite

- Recharts

- WebSockets

# 📂 Project Structure

```
app/
├── ai/
│   ├── api/
│   ├── providers/
│   └── services/
├── alerts/
├── core/
├── satellites/
├── telemetry/
│   ├── api/
│   ├── domain/
│   ├── services/
│   └── workers/
├── main.py
│
frontend/
├── src/
│   ├── components/
│   ├── services/
│   ├── hooks/
│   └── pages/
```

## 🔐 Environment Variables

OrbitWatch requires a `.env` file for local development.

Example:

```
env
DATABASE_URL=postgresql+psycopg2://orbit:orbit_pass@db:5432/orbitwatch
REDIS_HOST=redis
REDIS_PORT=6379

OPENROUTER_API_KEY=your_api_key_here
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

# Run Frontend

```
cd frontend
npm install
npm run dev
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

### Near-Term Roadmap

- Retrieval-Augmented Generation (RAG)
  
- Document ingestion
  
- Semantic search with pgvector
  
- LangGraph-powered AI workflows
  
- AI-assisted anomaly analysis
  
- Natural-language telemetry summaries
  
- Token and cost observability
  
- Streaming AI responses

# 🔭 Planned Extensions

- React operational dashboard

- Real-time telemetry visualization

- Orbit propagation (SGP4)

- Geospatial satellite tracking

- Time-series analytics

- Advanced anomaly detection

- Prometheus + Grafana integration

- Advanced mission control UI

- Multi-satellite operational views

- Real-time orbital visualization

- Interactive telemetry analytics

# 🎯 Project Goals

OrbitWatch is primarily a backend engineering project focused on:

- asynchronous systems

- telemetry pipelines

- resilient processing

- operational observability

- distributed-system patterns

- aerospace-inspired architectures

The goal is to simulate the kinds of backend systems used in real telemetry and mission operations environments while keeping the codebase understandable and incrementally extensible.
