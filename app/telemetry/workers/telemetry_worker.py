import json
import time
import uuid
import traceback
import asyncio

from sqlalchemy.exc import IntegrityError

from app.core.database import SessionLocal
from app.core.logging import logger
from app.core.redis import redis_client
from app.core.websocket_manager import manager

from app.telemetry.domain.processed_event_model import (
    ProcessedEvent,
)

from app.telemetry.services.ingestion_service import (
    TelemetryIngestionService,
)

from app.core.metrics import (
    telemetry_processed_total,
    alerts_generated_total,
    telemetry_failed_total,
    telemetry_dlq_total,
    telemetry_processing_duration_seconds,
)

from app.core.worker_metrics import (
    start_worker_metrics_server,
)


STREAM_NAME = "telemetry_stream"
DLQ_STREAM = "telemetry_dlq"

GROUP_NAME = "telemetry_group"
CONSUMER_NAME = "worker-1"

MAX_RETRIES = 3


def process_stream():

    logger.info(
        "Telemetry worker started",
        extra={
            "worker": CONSUMER_NAME,
            "stream": STREAM_NAME,
            "group": GROUP_NAME,
        }
    )

    start_worker_metrics_server()

    logger.info(
        "Worker metrics server started",
        extra={
            "metrics_port": 8001,
        }
    )

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

                logger.info(
                    "Received message batch from stream",
                    extra={
                        "stream": stream_name,
                        "message_count": len(messages),
                    }
                )

                for message_id, message_data in messages:

                    processing_start = time.perf_counter()

                    with SessionLocal() as db:

                        ingestion_service = (
                            TelemetryIngestionService(db)
                        )

                        retry_count = int(
                            message_data.get(
                                "retry_count",
                                0,
                            )
                        )

                        try:

                            events = json.loads(
                                message_data["data"]
                            )

                            logger.info(
                                "Processing telemetry message",
                                extra={
                                    "message_id": message_id,
                                    "retry_count": retry_count,
                                    "events_in_message": len(events),
                                }
                            )

                            events_to_process = []

                            for event in events:

                                event_id = uuid.UUID(
                                    event["event_id"]
                                )

                                processed = ProcessedEvent(
                                    event_id=event_id
                                )

                                try:

                                    db.add(processed)
                                    db.flush()

                                    events_to_process.append(
                                        event
                                    )

                                except IntegrityError:

                                    db.rollback()

                                    logger.warning(
                                        "Duplicate event skipped",
                                        extra={
                                            "event_id": str(event_id),
                                            "message_id": message_id,
                                        }
                                    )

                            if events_to_process:

                                result = (
                                    ingestion_service
                                    .ingest_event_batch(
                                        events_to_process
                                    )
                                )

                                telemetry_processed_total.inc(
                                    result["processed"]
                                )

                                alerts_generated_total.inc(
                                    result[
                                        "alerts_generated"
                                    ]
                                )

                                processing_duration = (
                                    time.perf_counter()
                                    - processing_start
                                )

                                telemetry_processing_duration_seconds.observe(
                                    processing_duration
                                )

                                logger.info(
                                    "Telemetry batch processed",
                                    extra={
                                        "message_id": message_id,
                                        "processed": (
                                            result[
                                                "processed"
                                            ]
                                        ),
                                        "alerts_generated": (
                                            result[
                                                "alerts_generated"
                                            ]
                                        ),
                                        "duration_seconds": round(
                                            processing_duration,
                                            4,
                                        ),
                                    }
                                )

                                asyncio.run(
                                    manager.broadcast(
                                        {
                                            "type": "telemetry_processed",
                                            "message_id": message_id,
                                            "processed": result["processed"],
                                            "alerts_generated": result["alerts_generated"],
                                        }
                                    )
                                )

                            else:

                                logger.info(
                                    "No new telemetry events to process",
                                    extra={
                                        "message_id": message_id,
                                    }
                                )

                            redis_client.xack(
                                STREAM_NAME,
                                GROUP_NAME,
                                message_id,
                            )

                            logger.info(
                                "Message acknowledged",
                                extra={
                                    "message_id": message_id,
                                }
                            )

                        except Exception as e:

                            if db.is_active:
                                db.rollback()

                            telemetry_failed_total.inc()

                            logger.exception(
                                "Telemetry processing failed",
                                extra={
                                    "message_id": message_id,
                                    "retry_count": retry_count,
                                    "error": str(e),
                                }
                            )

                            traceback.print_exc()

                            retry_count += 1

                            if retry_count >= MAX_RETRIES:

                                telemetry_dlq_total.inc()

                                logger.error(
                                    "Sending message to DLQ",
                                    extra={
                                        "message_id": message_id,
                                        "retry_count": retry_count,
                                    }
                                )

                                redis_client.xadd(
                                    DLQ_STREAM,
                                    {
                                        "data": (
                                            message_data["data"]
                                        ),
                                        "error": str(e),
                                        "original_message_id": (
                                            message_id
                                        ),
                                    }
                                )

                                redis_client.xack(
                                    STREAM_NAME,
                                    GROUP_NAME,
                                    message_id,
                                )

                            else:

                                logger.warning(
                                    "Requeueing telemetry message",
                                    extra={
                                        "message_id": message_id,
                                        "retry_count": retry_count,
                                    }
                                )

                                redis_client.xadd(
                                    STREAM_NAME,
                                    {
                                        "data": (
                                            message_data["data"]
                                        ),
                                        "retry_count": (
                                            str(retry_count)
                                        ),
                                    }
                                )

                                redis_client.xack(
                                    STREAM_NAME,
                                    GROUP_NAME,
                                    message_id,
                                )

        except Exception as e:

            logger.exception(
                "Fatal worker loop failure",
                extra={
                    "worker": CONSUMER_NAME,
                    "error": str(e),
                }
            )

            traceback.print_exc()

            time.sleep(2)


if __name__ == "__main__":
    process_stream()