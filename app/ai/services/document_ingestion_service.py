from pathlib import Path

from app.ai.models.document_embedding import DocumentEmbedding
from app.ai.services.embedding_service import EmbeddingService


class DocumentIngestionService:

    def __init__(self, db):
        self.db = db
        self.embedding_service = EmbeddingService()

    def ingest_directory(self, directory="knowledge"):

        files = Path(directory).glob("*.md")

        for file in files:

            content = file.read_text(encoding="utf-8")

            embedding = self.embedding_service.embed(content)

            document = DocumentEmbedding(
                content=content,
                embedding=embedding
            )

            self.db.add(document)

        self.db.commit()