from fastapi import APIRouter
from pydantic import BaseModel

from app.ai.services.rag_service import RagService

router = APIRouter()


class ChatRequest(BaseModel):
    question: str


@router.post("/chat")
def chat(request: ChatRequest):

    rag = RagService()

    answer = rag.ask(
        request.question
    )

    return {
        "status": "ok",
        "answer": answer,
    }