import asyncio

from fastapi import APIRouter
from fastapi import WebSocket
from fastapi import WebSocketDisconnect

from app.core.websocket_manager import manager


router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(
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