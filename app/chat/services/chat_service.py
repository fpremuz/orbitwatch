from app.core.database import SessionLocal

from app.chat.domain.models.conversation import Conversation
from app.chat.domain.models.message import Message

from app.ai.services.rag_service import RagService


class ChatService:

    def __init__(self):
        self.rag = RagService()

    def ask(
        self,
        question: str,
        conversation_id: str | None = None,
    ):

        db = SessionLocal()

        try:

            if conversation_id:

                conversation = db.get(
                    Conversation,
                    conversation_id
                )

                if conversation is None:
                    raise ValueError(
                        "Conversation not found"
                    )

            else:

                conversation = Conversation()

                db.add(conversation)
                db.flush()

            user_message = Message(
                conversation_id=conversation.id,
                role="user",
                content=question,
            )

            db.add(user_message)

            answer = self.rag.ask(question)

            ai_message = Message(
                conversation_id=conversation.id,
                role="assistant",
                content=answer,
            )

            db.add(ai_message)

            db.commit()

            return {
                "conversation_id": str(conversation.id),
                "answer": answer,
            }

        finally:
            db.close()