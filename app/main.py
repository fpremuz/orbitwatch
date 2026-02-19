from fastapi import FastAPI
from app.satellites.api.routes import router as satellite_router

app = FastAPI(title="OrbitWatch")

app.include_router(satellite_router)