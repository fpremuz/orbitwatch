from pathlib import Path

from app.ai.models.knowledge_chunk import KnowledgeChunk
from app.ai.services.embedding_service import EmbeddingService
from app.core.database import SessionLocal


KNOWLEDGE_DIR = Path("knowledge")


def chunk_text(text: str, chunk_size: int = 1000):

    chunks = []

    start = 0

    while start < len(text):
        chunks.append(
            text[start:start + chunk_size]
        )
        start += chunk_size

    return chunks


def main():

    db = SessionLocal()

    embedding_service = EmbeddingService()

    db.query(KnowledgeChunk).delete()

    for file in KNOWLEDGE_DIR.glob("*.md"):

        content = file.read_text(
            encoding="utf-8"
        )

        chunks = chunk_text(content)

        for chunk in chunks:

            embedding = embedding_service.embed(chunk)

            db.add(
                KnowledgeChunk(
                    content=chunk,
                    embedding=embedding
                )
            )

    db.commit()

    db.close()

    print("Knowledge loaded")


if __name__ == "__main__":
    main()