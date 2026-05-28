import asyncio
import json

from app.core.redis import redis_client
from app.ws.connection_manager import manager

CHANNELS = [
    "telemetry_events",
    "health_updates",
]

async def redis_listener():

    pubsub = redis_client.pubsub()

    pubsub.subscribe(*CHANNELS)

    print(
        "Redis websocket listener started"
    )

    while True:

        try:

            message = pubsub.get_message(
                ignore_subscribe_messages=True
            )

            if message:

                data = json.loads(
                    message["data"]
                )

                print(
                    "Broadcasting websocket event:",
                    data.get("type")
                )

                await manager.broadcast(
                    data
                )

        except Exception as e:

            print(
                "Redis listener error:",
                str(e)
            )

        await asyncio.sleep(0.01)