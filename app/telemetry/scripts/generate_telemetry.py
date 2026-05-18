import json
import random
import time
from uuid import uuid4
from datetime import datetime, UTC

import redis

redis_client = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True,
)

SATELLITES = [
    {
        "satellite_id": "af6f1df7-da0d-437f-9b01-4836cec81212",
        "norad_id": 25544,
    },
    {
        "satellite_id": "2c50054c-604c-460b-bd52-bedc9941ae78",
        "norad_id": 20580,
    },
    {
        "satellite_id": "3f174425-3b65-4ae1-a7f9-1f73c8c077a6",
        "norad_id": 39634,
    },
]


def generate_event(satellite):

    return {
        "event_id": str(uuid4()),
        "satellite_id": satellite["satellite_id"],
        "norad_id": satellite["norad_id"],
        "timestamp": (
            datetime.now(UTC)
            .replace(microsecond=0)
            .isoformat()
            .replace("+00:00", "Z")
        ),
        "parameters": [
            {
                "name": "temperature_c",
                "value": round(random.uniform(-20, 80), 2),
            },
            {
                "name": "battery_voltage",
                "value": round(random.uniform(2.5, 4.2), 2),
            },
            {
                "name": "altitude_km",
                "value": round(random.uniform(400, 1200), 2),
            },
            {
                "name": "velocity_kmh",
                "value": round(random.uniform(26000, 29000), 2),
            },
        ],
    }


print("Starting telemetry generator...")

while True:

    for satellite in SATELLITES:

        event = generate_event(satellite)

        print(event["timestamp"])

        redis_client.xadd(
            "telemetry_stream",
            {
                "data": json.dumps([event]),
            },
        )

        print(
            f"Published event for satellite {satellite['norad_id']}"
        )

        time.sleep(0.2)

    time.sleep(2)