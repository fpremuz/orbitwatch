from sqlalchemy.orm import Session

from app.chat.domain.models.message import Message
from app.chat.domain.models.conversation import Conversation


class ConversationService:

    def get_history(
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

    def get_recent_messages(
        self,
        db: Session,
        conversation_id,
        limit: int = 10
    ):
        return self.get_history(
            db,
            conversation_id,
            limit,
        )

    def get_all_conversations(
        self,
        db: Session,
    ):
        return (
            db.query(Conversation)
            .order_by(
                Conversation.created_at.desc()
            )
            .all()
        )

    def get_conversation(
        self,
        db: Session,
        conversation_id,
    ):
        return (
            db.query(Conversation)
            .filter(
                Conversation.id == conversation_id
            )
            .first()
        )