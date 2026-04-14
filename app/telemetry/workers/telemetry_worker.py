import json
import time
from redis.exceptions import ResponseError

from app.core.redis import redis_client
from app.core.database import SessionLocal
from app.telemetry.services.ingestion_service import TelemetryIngestionService

STREAM_NAME = "telemetry_stream"
GROUP_NAME = "telemetry_group"
CONSUMER_NAME = "worker-1"


def create_group():
    try:
        redis_client.xgroup_create(
            STREAM_NAME,
            GROUP_NAME,
            id="0",
            mkstream=True,
        )
    except ResponseError:
        # Group already exists
        pass


def run_worker():
    create_group()

    while True:
        messages = redis_client.xreadgroup(
            GROUP_NAME,
            CONSUMER_NAME,
            {STREAM_NAME: ">"},
            count=10,
            block=5000,
        )

        if not messages:
            continue

        db = SessionLocal()
        service = TelemetryIngestionService(db)

        try:
            for stream, msgs in messages:
                for msg_id, data in msgs:

                    events_data = json.loads(data["data"])

                    service.ingest_event_batch(events_data)

                    redis_client.xack(STREAM_NAME, GROUP_NAME, msg_id)

        except Exception as e:
            print(f"Error processing message: {e}")
            db.rollback()

        finally:
            db.close()