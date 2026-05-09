from prometheus_client import Counter
from prometheus_client import Histogram


telemetry_processed_total = Counter(
    "telemetry_processed_total",
    "Total telemetry points processed",
)

alerts_generated_total = Counter(
    "alerts_generated_total",
    "Total alerts generated",
)

telemetry_failed_total = Counter(
    "telemetry_failed_total",
    "Total telemetry processing failures",
)

telemetry_dlq_total = Counter(
    "telemetry_dlq_total",
    "Total telemetry messages sent to DLQ",
)

telemetry_processing_duration_seconds = Histogram(
    "telemetry_processing_duration_seconds",
    "Telemetry message processing duration",
)