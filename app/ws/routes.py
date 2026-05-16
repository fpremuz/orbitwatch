import asyncio

from fastapi import APIRouter
from fastapi import WebSocket
from fastapi import WebSocketDisconnect

from app.ws.connection_manager import (
    manager,
)

router = APIRouter()


@router.websocket("/ws/telemetry")
async def telemetry_websocket(
    websocket: WebSocket,
):

    await manager.connect(
        websocket
    )

    try:

        while True:

            await asyncio.sleep(60)

    except WebSocketDisconnect:

        manager.disconnect(
            websocket
        )