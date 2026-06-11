from fastapi import APIRouter
from pydantic import BaseModel

from app.chat.services.chat_service import ChatService

router = APIRouter()


class ChatRequest(BaseModel):
    conversation_id: str | None = None
    question: str


@router.post("/chat")
def chat(request: ChatRequest):

    service = ChatService()

    result = service.ask(
        request.question,
        conversation_id=request.conversation_id,
    )

    return {
        "status": "ok",
        **result
    }