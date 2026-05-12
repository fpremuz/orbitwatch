import asyncio
import json

from app.core.redis import redis_client
from app.core.websocket_manager import manager


async def redis_event_listener():

    pubsub = redis_client.pubsub()

    pubsub.subscribe(
        "telemetry_events"
    )

    print(
        "Redis websocket listener started"
    )

    while True:

        message = pubsub.get_message(
            ignore_subscribe_messages=True
        )

        if message:

            data = json.loads(
                message["data"]
            )

            print(
                "Received Redis pubsub event:",
                data
            )

            await manager.broadcast(
                data
            )

        await asyncio.sleep(0.1)