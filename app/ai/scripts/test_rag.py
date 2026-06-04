from app.ai.services.rag_service import RagService

rag = RagService()

response = rag.ask(
    "What should operators do when a thermal anomaly is detected?"
)

print(response)