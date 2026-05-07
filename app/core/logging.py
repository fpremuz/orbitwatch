import logging
import sys
from contextvars import ContextVar

from pythonjsonlogger import jsonlogger


correlation_id_var: ContextVar[str] = ContextVar(
    "correlation_id",
    default="-",
)

trace_id_var: ContextVar[str] = ContextVar(
    "trace_id",
    default="-",
)


class ContextFilter(logging.Filter):

    def filter(self, record):

        record.correlation_id = correlation_id_var.get()
        record.trace_id = trace_id_var.get()
        record.service = "orbitwatch"

        return True


logger = logging.getLogger("orbitwatch")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)

formatter = jsonlogger.JsonFormatter(
    "%(asctime)s %(levelname)s %(name)s %(message)s "
    "%(service)s %(correlation_id)s %(trace_id)s"
)

handler.setFormatter(formatter)

logger.addHandler(handler)
logger.addFilter(ContextFilter())

logger.propagate = False