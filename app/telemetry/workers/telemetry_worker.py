import json
import time
import uuid
import app.models

from sqlalchemy.exc import IntegrityError

from app.core.database import SessionLocal
from app.core.redis import redis_client
from app.telemetry.services.ingestion_service import TelemetryIngestionService
from app.telemetry.domain.processed_event_model import ProcessedEvent

STREAM_NAME = "telemetry_stream"
GROUP_NAME = "telemetry_group"
CONSUMER_NAME = "worker-1"


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
                block=5000,  # wait 5s
            )

            if not response:
                continue

            for stream_name, messages in response:
                for message_id, message_data in messages:

                    try:
                        events = json.loads(message_data["data"])

                        events_to_process = []

                        for event in events:
                            event_id = uuid.UUID(event["event_id"])

                            processed = ProcessedEvent(event_id=event_id)

                            try:
                                db.add(processed)
                                db.flush()  # 🔥 triggers PK constraint

                                events_to_process.append(event)

                            except IntegrityError:
                                db.rollback()
                                print(f"⚠️ Duplicate event skipped: {event_id}")

                        if events_to_process:
                            result = ingestion_service.ingest_event_batch(events_to_process)
                            print(f"✅ Processed: {result}")

                        # ✅ ACK only after everything succeeds
                        redis_client.xack(STREAM_NAME, GROUP_NAME, message_id)

                    except Exception as e:
                        print(f"❌ Processing error: {e}")
                        # ❗ DO NOT ACK → will retry
                        continue

        except Exception as e:
            print(f"🔥 Worker error: {e}")
            time.sleep(2)


if __name__ == "__main__":
    process_stream()