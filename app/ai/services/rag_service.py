from app.ai.retrieval.vector_retriever import VectorRetriever
from app.ai.providers.ollama_provider import OllamaProvider


class RagService:

    def __init__(self):
        self.retriever = VectorRetriever()
        self.llm = OllamaProvider()

    def ask(self, question: str) -> str:

        chunks = self.retriever.retrieve(
            question,
            limit=3
        )

        context = "\n\n".join(
            chunk.content
            for chunk in chunks
        )

        prompt = f"""
You are OrbitWatch AI Assistant.

Use ONLY the provided context.

If the answer is not in the context,
say you don't know.

CONTEXT:

{context}

QUESTION:

{question}

ANSWER:
"""

        return self.llm.generate(prompt)