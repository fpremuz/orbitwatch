from app.ai.retrieval.vector_retriever import VectorRetriever
from app.ai.providers.ollama_provider import OllamaProvider


class RagService:

    def __init__(self):
        self.retriever = VectorRetriever()
        self.llm = OllamaProvider()

    def ask(
        self,
        question: str,
        history: str = "",
    ) -> str:

        retrieval_query = f"""
        Previous Conversation:

        {history}

        Current question:

        {question}
        """
        
        chunks = self.retriever.retrieve(
            retrieval_query,
            limit=3
        )

        context = "\n\n".join(
            chunk.content
            for chunk in chunks
        )

        prompt = f"""
        You are OrbitWatch AI Assistant.

        Use conversation history to understand references
        such as "it", "they", "second cause", or "that issue".

        Use retrieved context as the source of factual information.

        If the answer is not in the context,
        say you don't know.

        CHAT HISTORY:

        {history}

        CONTEXT:

        {context}

        QUESTION:

        {question}

        ANSWER:
        """

        return self.llm.generate(prompt)