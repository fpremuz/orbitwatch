from opentelemetry import trace

from opentelemetry.sdk.resources import Resource

from opentelemetry.sdk.trace import TracerProvider

from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)

from opentelemetry.instrumentation.fastapi import (
    FastAPIInstrumentor,
)

from opentelemetry.instrumentation.sqlalchemy import (
    SQLAlchemyInstrumentor,
)

from opentelemetry.instrumentation.redis import (
    RedisInstrumentor,
)

from opentelemetry.instrumentation.logging import (
    LoggingInstrumentor,
)

from app.core.database import engine


def setup_tracing(app):

    resource = Resource.create({
        "service.name": "orbitwatch",
    })

    provider = TracerProvider(
        resource=resource,
    )

    trace.set_tracer_provider(provider)

    console_exporter = ConsoleSpanExporter()

    span_processor = BatchSpanProcessor(
        console_exporter
    )

    provider.add_span_processor(
        span_processor
    )

    FastAPIInstrumentor.instrument_app(app)

    SQLAlchemyInstrumentor().instrument(
        engine=engine
    )

    RedisInstrumentor().instrument()

    LoggingInstrumentor().instrument(
        set_logging_format=False
    )