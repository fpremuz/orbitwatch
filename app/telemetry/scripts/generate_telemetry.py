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


def generate_temperature():
    # 20% chance of dangerous value
    if random.random() < 0.2:
        return round(random.uniform(85, 120), 2)

    return round(random.uniform(10, 60), 2)


def generate_battery_voltage():
    # 15% chance of low battery
    if random.random() < 0.15:
        return round(random.uniform(1.5, 2.4), 2)

    return round(random.uniform(3.2, 4.2), 2)


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
                "value": generate_temperature(),
            },
            {
                "name": "battery_voltage",
                "value": generate_battery_voltage(),
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

    batch = []

    for satellite in SATELLITES:
        batch.append(generate_event(satellite))

    redis_client.xadd(
        "telemetry_stream",
        {
            "data": json.dumps(batch),
        },
    )

    print(f"Published batch with {len(batch)} events")

    time.sleep(2)