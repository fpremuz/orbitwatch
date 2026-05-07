from fastapi import FastAPI
from app.satellites.api.routes import router as satellite_router
from app.telemetry.api.routes import router as telemetry_router
from app.alerts.api.routes import router as alerts_router
from app.metrics.api.routes import router as metrics_router

app = FastAPI(title="OrbitWatch")

app.include_router(satellite_router)
app.include_router(telemetry_router)
app.include_router(alerts_router)
app.include_router(metrics_router)