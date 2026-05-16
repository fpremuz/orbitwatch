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

            await websocket.receive_text()

    except WebSocketDisconnect:

        manager.disconnect(
            websocket
        )