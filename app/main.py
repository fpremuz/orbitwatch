from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from prometheus_client import generate_latest

from app.core.middleware import CorrelationMiddleware

from app.satellites.api.routes import router as satellite_router
from app.telemetry.api.routes import router as telemetry_router
from app.alerts.api.routes import router as alerts_router


app = FastAPI(title="OrbitWatch")

app.add_middleware(CorrelationMiddleware)

app.include_router(satellite_router)
app.include_router(telemetry_router)
app.include_router(alerts_router)


@app.get("/metrics")
def metrics():
    return PlainTextResponse(
        generate_latest().decode("utf-8")
    )