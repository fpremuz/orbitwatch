from prometheus_client import Counter


telemetry_processed_total = Counter(
    "telemetry_processed_total",
    "Total telemetry points processed"
)

alerts_generated_total = Counter(
    "alerts_generated_total",
    "Total alerts generated"
)

telemetry_failed_total = Counter(
    "telemetry_failed_total",
    "Total failed telemetry messages"
)

telemetry_dlq_total = Counter(
    "telemetry_dlq_total",
    "Total messages sent to DLQ"
)