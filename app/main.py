from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import WebSocket

from prometheus_client import generate_latest

from app.core.websocket_manager import manager

from app.satellites.api.routes import (
    router as satellite_router
)

from app.telemetry.api.routes import (
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

app.include_router(
    satellite_router
)

app.include_router(
    telemetry_router
)

app.include_router(
    alerts_router
)


@app.get("/metrics")
def metrics():

    return PlainTextResponse(
        generate_latest().decode("utf-8")
    )


@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
):

    await manager.connect(websocket)

    try:

        while True:
            await websocket.receive_text()

    except Exception:

        manager.disconnect(websocket)