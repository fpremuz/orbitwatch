import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

from prometheus_client import generate_latest

from app.core.redis import redis_client
from app.api.routes.telemetry import (
    router as telemetry_router,
)

from app.api.routes.satellites import (
    router as satellites_router,
)

from app.ws.routes import (
    router as websocket_router
)

from app.ws.websocket_event_listener import (
    redis_event_listener,
)

from app.satellites.api.routes import (
    router as satellite_router
)

from app.api.routes.telemetry import (
    router as telemetry_router
)

from app.alerts.api.routes import (
    router as alerts_router
)

app = FastAPI(
    title="OrbitWatch"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(satellite_router)

app.include_router(telemetry_router)

app.include_router(alerts_router)

app.include_router(websocket_router)

app.include_router(satellites_router)


@app.get("/metrics")
def metrics():

    return PlainTextResponse(
        generate_latest().decode("utf-8")
    )


@app.on_event("startup")
async def startup_event():

    redis_client.ping()

    asyncio.create_task(
        redis_event_listener()
    )