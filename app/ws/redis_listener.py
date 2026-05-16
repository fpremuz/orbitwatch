import asyncio
import json

from app.core.redis import redis_client
from app.ws.connection_manager import manager


async def redis_listener():

    pubsub = redis_client.pubsub()

    pubsub.subscribe("telemetry_events")

    while True:

        message = pubsub.get_message(
            ignore_subscribe_messages=True
        )

        if message:

            data = json.loads(
                message["data"]
            )

            await manager.broadcast_json(data)

        await asyncio.sleep(0.01)