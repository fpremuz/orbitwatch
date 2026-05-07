import json
import time
import uuid
import traceback
import app.models

from sqlalchemy.exc import IntegrityError

from app.core.database import SessionLocal
from app.core.redis import redis_client
from app.telemetry.services.ingestion_service import TelemetryIngestionService
from app.telemetry.domain.processed_event_model import ProcessedEvent

STREAM_NAME = "telemetry_stream"
DLQ_STREAM = "telemetry_dlq"

GROUP_NAME = "telemetry_group"
CONSUMER_NAME = "worker-1"

MAX_RETRIES = 3


def process_stream():
    print("🚀 Telemetry worker started...")

    db = SessionLocal()
    ingestion_service = TelemetryIngestionService(db)

    while True:

        try:
            response = redis_client.xreadgroup(
                groupname=GROUP_NAME,
                consumername=CONSUMER_NAME,
                streams={STREAM_NAME: ">"},
                count=10,
                block=5000,
            )

            if not response:
                continue

            for stream_name, messages in response:

                for message_id, message_data in messages:

                    retry_count = int(message_data.get("retry_count", 0))

                    try:

                        events = json.loads(message_data["data"])

                        print(f"\n📦 Processing message {message_id}")
                        print(f"🔁 Retry count: {retry_count}")

                        events_to_process = []

                        for event in events:

                            event_id = uuid.UUID(event["event_id"])

                            processed = ProcessedEvent(event_id=event_id)

                            try:
                                db.add(processed)
                                db.flush()

                                events_to_process.append(event)

                            except IntegrityError:
                                db.rollback()
                                print(f"⚠️ Duplicate event skipped: {event_id}")

                        if events_to_process:

                            result = ingestion_service.ingest_event_batch(
                                events_to_process
                            )

                            print(f"✅ Processed: {result}")

                        redis_client.xack(
                            STREAM_NAME,
                            GROUP_NAME,
                            message_id,
                        )

                    except Exception as e:

                        db.rollback()

                        print(f"\n❌ Processing error")
                        print(str(e))

                        traceback.print_exc()

                        retry_count += 1

                        if retry_count >= MAX_RETRIES:

                            print(f"💀 Sending message to DLQ")

                            redis_client.xadd(
                                DLQ_STREAM,
                                {
                                    "data": message_data["data"],
                                    "error": str(e),
                                    "original_message_id": message_id,
                                }
                            )

                            redis_client.xack(
                                STREAM_NAME,
                                GROUP_NAME,
                                message_id,
                            )

                        else:

                            print(
                                f"🔁 Requeueing message "
                                f"(attempt {retry_count})"
                            )

                            redis_client.xadd(
                                STREAM_NAME,
                                {
                                    "data": message_data["data"],
                                    "retry_count": str(retry_count),
                                }
                            )

                            redis_client.xack(
                                STREAM_NAME,
                                GROUP_NAME,
                                message_id,
                            )

        except Exception as e:

            print(f"\n🔥 Worker error")
            print(str(e))

            traceback.print_exc()

            time.sleep(2)


if __name__ == "__main__":
    process_stream()