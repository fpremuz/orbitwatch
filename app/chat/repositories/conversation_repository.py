from app.chat.domain.models.conversation import Conversation


class ConversationRepository:

    def create(self, db):

        conversation = Conversation()

        db.add(conversation)
        db.commit()
        db.refresh(conversation)

        return conversation