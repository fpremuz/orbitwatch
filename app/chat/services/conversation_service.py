from sqlalchemy.orm import Session

from app.chat.domain.models.message import Message


class ConversationService:

    def get_recent_messages(
        self,
        db: Session,
        conversation_id,
        limit: int = 10
    ):
        return (
            db.query(Message)
            .filter(
                Message.conversation_id == conversation_id
            )
            .order_by(Message.created_at.asc())
            .limit(limit)
            .all()
        )