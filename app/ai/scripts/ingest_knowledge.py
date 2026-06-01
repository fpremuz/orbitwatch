from app.ai.services.document_ingestion_service import (
    DocumentIngestionService
)

from app.core.database import SessionLocal


db = SessionLocal()

service = DocumentIngestionService(db)

service.ingest_directory()

print("Knowledge ingested")