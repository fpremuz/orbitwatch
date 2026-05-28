import asyncio

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

from prometheus_client import generate_latest

import app.satellites.domain.models

from app.core.redis import redis_client

from app.ai.api.routes import (
    router as ai_router,
)

from app.telemetry.api.routes import (
    router as telemetry_router,
)

from app.satellites.api.routes import (
    router as satellites_router,
)

from app.alerts.api.routes import (
    router as alerts_router,
)

from app.ws.routes import (
    router as ws_router,
)

from app.ws.pubsub_listener import (
    redis_listener,
)


@asynccontextmanager
async def lifespan(app: FastAPI):

    redis_client.ping()

    listener_task = asyncio.create_task(
        redis_listener()
    )

    print("Websocket Redis listener started")

    yield

    listener_task.cancel()


app = FastAPI(
    title="OrbitWatch",
    lifespan=lifespan,
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

app.include_router(
    telemetry_router
)

app.include_router(
    satellites_router
)

app.include_router(
    alerts_router
)

app.include_router(
    ws_router
)

app.include_router(
    ai_router,
    prefix="/ai",
)


@app.get("/metrics")
def metrics():

    return PlainTextResponse(
        generate_latest().decode("utf-8")
    )