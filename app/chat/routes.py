from fastapi import APIRouter

from app.core.database import SessionLocal

from app.chat.services.conversation_service import (
    ConversationService,
)

router = APIRouter()

service = ConversationService()


@router.get("/conversations")
def get_conversations():

    db = SessionLocal()

    try:

        conversations = (
            service.get_all_conversations(db)
        )

        return [
            {
                "id": str(c.id),
                "title": c.title,
                "created_at": c.created_at,
            }
            for c in conversations
        ]

    finally:
        db.close()


@router.get("/conversations/{conversation_id}")
def get_conversation(
    conversation_id: str,
):

    db = SessionLocal()

    try:

        messages = (
            service.get_history(
                db,
                conversation_id,
                limit=100,
            )
        )

        return {
            "id": conversation_id,
            "messages": [
                {
                    "role": m.role,
                    "content": m.content,
                    "created_at": m.created_at,
                }
                for m in messages
            ]
        }

    finally:
        db.close()