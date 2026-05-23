from fastapi import APIRouter
from pydantic import BaseModel

from app.ai.services.ai_analysis_service import AIAnalysisService

router = APIRouter()

class AIRequest(BaseModel):
    prompt: str


@router.post("/test")
def test_ai(request: AIRequest):
    service = AIAnalysisService()

    result = service.analyze(request.prompt)

    return {
        "result": result
    }