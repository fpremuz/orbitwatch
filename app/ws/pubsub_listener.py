import asyncio
import json

from app.core.redis import redis_client

from app.ws.connection_manager import (
    manager,
)

CHANNEL_NAME = "telemetry_broadcast"


async def redis_listener():

    pubsub = redis_client.pubsub()

    pubsub.subscribe(
        CHANNEL_NAME
    )

    while True:

        message = pubsub.get_message(
            ignore_subscribe_messages=True
        )

        if message:

            data = json.loads(
                message["data"]
            )

            await manager.broadcast(
                data
            )

        await asyncio.sleep(0.01)