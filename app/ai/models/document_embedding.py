from sqlalchemy import Column, Integer, Text

from pgvector.sqlalchemy import Vector

from app.core.base import Base


class DocumentEmbedding(Base):
    __tablename__ = "document_embeddings"

    id = Column(Integer, primary_key=True)

    content = Column(Text, nullable=False)

    embedding = Column(Vector(384))