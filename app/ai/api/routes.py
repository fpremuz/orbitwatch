from fastapi import APIRouter

from app.ai.services.ai_analysis_service import (
    AIAnalysisService,
)


router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.get("/test")
def test_ai_analysis():

    response = AIAnalysisService.analyze_alert(
        satellite_name="Hubble-X",
        alert_message="Temperature exceeded safe threshold",
        telemetry_points=[
            {
                "parameter": "temperature_c",
                "value": 82,
            },
            {
                "parameter": "battery_voltage",
                "value": 21.2,
            },
        ],
    )

    return {
        "analysis": response,
    }