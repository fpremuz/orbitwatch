import asyncio

from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
)

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

    print("WebSocket client connected")

    try:

        while True:

            await asyncio.sleep(30)
            
            await websocket.send_json(
                {
                    "type": "ping",
                }
            )

    except WebSocketDisconnect:

        print("WebSocket disconnected")

        manager.disconnect(
            websocket
        )

    except Exception as e:

        print(
            "WebSocket error:",
            str(e)
        )

        manager.disconnect(
            websocket
        )