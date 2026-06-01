from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text

from pgvector.sqlalchemy import Vector

from app.core.database import Base


class KnowledgeChunk(Base):
    __tablename__ = "knowledge_chunks"

    id = Column(Integer, primary_key=True)

    content = Column(
        Text,
        nullable=False,
    )

    embedding = Column(
        Vector(384),
        nullable=False,
    )