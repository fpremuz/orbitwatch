import app.models
from fastapi import FastAPI
from app.satellites.api.routes import router as satellite_router
from app.telemetry.api.routes import router as telemetry_router

app = FastAPI(title="OrbitWatch")

app.include_router(satellite_router)
app.include_router(telemetry_router)