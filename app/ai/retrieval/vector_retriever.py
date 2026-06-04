from sqlalchemy import text

from app.ai.services.embedding_service import EmbeddingService
from app.core.database import SessionLocal


class VectorRetriever:

    def __init__(self):
        self.embedding_service = EmbeddingService()

    def retrieve(
        self,
        query: str,
        limit: int = 3
    ):

        embedding = self.embedding_service.embed(query)

        db = SessionLocal()

        try:

            sql = text("""
                SELECT
                    id,
                    content
                FROM knowledge_chunks
                ORDER BY embedding <=> CAST(:embedding AS vector)
                LIMIT :limit
            """)

            result = db.execute(
                sql,
                {
                    "embedding": str(embedding),
                    "limit": limit
                }
            )

            return result.fetchall()

        finally:
            db.close()