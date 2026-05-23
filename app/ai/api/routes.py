from fastapi import APIRouter
from app.ai.services.ai_analysis_service import AIAnalysisService
from app.ai.models.telemetry import TelemetryData

router = APIRouter()

@router.post("/analyze")
def analyze_telemetry(data: TelemetryData):
    service = AIAnalysisService()
    result = service.analyze_telemetry(data)

    return {
        "status": "ok",
        "data": result
    }