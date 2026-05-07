import json
import time
import uuid
import traceback
import app.models

from sqlalchemy.exc import IntegrityError

from app.core.logging import logger
from app.core.database import SessionLocal
from app.core.redis import redis_client
from app.telemetry.services.ingestion_service import TelemetryIngestionService
from app.telemetry.domain.processed_event_model import ProcessedEvent
from app.core.metrics import (
    telemetry_processed_total,
    alerts_generated_total,
    telemetry_failed_total,
    telemetry_dlq_total,
)

STREAM_NAME = "telemetry_stream"
DLQ_STREAM = "telemetry_dlq"

GROUP_NAME = "telemetry_group"
CONSUMER_NAME = "worker-1"

MAX_RETRIES = 3


def process_stream():
    logger.info("🚀 Telemetry worker started...")

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

                        logger.info(f"\n📦 Processing message {message_id}")
                        logger.info(f"🔁 Retry count: {retry_count}")

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
                                logger.warning(f"⚠️ Duplicate event skipped: {event_id}")

                        if events_to_process:

                            result = ingestion_service.ingest_event_batch(
                                events_to_process
                            )

                            logger.info(f"✅ Processed: {result}")

                            telemetry_processed_total.inc(result["processed"])
                            alerts_generated_total.inc(result["alerts_generated"])

                        redis_client.xack(
                            STREAM_NAME,
                            GROUP_NAME,
                            message_id,
                        )

                    except Exception as e:

                        db.rollback()

                        logger.exception(f"\n❌ Processing error")
                        telemetry_failed_total.inc()
                        logger.info(str(e))

                        traceback.print_exc()

                        retry_count += 1

                        if retry_count >= MAX_RETRIES:

                            logger.error(f"💀 Sending message to DLQ")

                            telemetry_dlq_total.inc()

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

                            logger.info(
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

            logger.error(f"\n🔥 Worker error")
            logger.info(str(e))

            traceback.print_exc()

            time.sleep(2)


if __name__ == "__main__":
    process_stream()