from app.chat.domain.models.message import Message


class MessageRepository:

    def create(
        self,
        db,
        conversation_id,
        role,
        content,
    ):

        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )

        db.add(message)
        db.commit()
        db.refresh(message)

        return message