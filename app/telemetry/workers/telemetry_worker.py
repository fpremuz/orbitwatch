import json
import time
from redis.exceptions import ResponseError

from app.core.redis import redis_client
from app.core.database import SessionLocal
from app.telemetry.services.ingestion_service import TelemetryIngestionService

STREAM_NAME = "telemetry_stream"
DLQ_STREAM = "telemetry_dlq"

GROUP_NAME = "telemetry_group"
CONSUMER_NAME = "worker-1"

MAX_RETRIES = 3


def create_group():
    try:
        redis_client.xgroup_create(
            STREAM_NAME,
            GROUP_NAME,
            id="0",
            mkstream=True,
        )
    except ResponseError:
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

        for stream, msgs in messages:
            for msg_id, data in msgs:

                db = SessionLocal()
                service = TelemetryIngestionService(db)

                try:
                    events_data = json.loads(data["data"])
                    retry_count = int(data.get("retry_count", 0))

                    service.ingest_event_batch(events_data)

                    redis_client.xack(STREAM_NAME, GROUP_NAME, msg_id)

                except Exception as e:
                    print(f"[ERROR] Processing failed: {e}")

                    retry_count = int(data.get("retry_count", 0))

                    if retry_count >= MAX_RETRIES:
                        # Send to DLQ
                        redis_client.xadd(
                            DLQ_STREAM,
                            {
                                "data": data["data"],
                                "error": str(e),
                            },
                        )
                        print("Received message:", data)

                        redis_client.xack(STREAM_NAME, GROUP_NAME, msg_id)

                    else:
                        # Retry → requeue with incremented retry_count
                        redis_client.xadd(
                            STREAM_NAME,
                            {
                                "data": data["data"],
                                "retry_count": retry_count + 1,
                            },
                        )

                        redis_client.xack(STREAM_NAME, GROUP_NAME, msg_id)

                finally:
                    db.close()