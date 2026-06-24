from app.ai.retrieval.vector_retriever import VectorRetriever
from app.ai.providers.ollama_provider import OllamaProvider

retriever = VectorRetriever()
llm = OllamaProvider()


def retrieve_context(state):

    retrieval_query = f"""
Previous Conversation:

{state["history"]}

Current Question:

{state["question"]}
"""

    chunks = retriever.retrieve(
        retrieval_query,
        limit=3,
    )

    context = "\n\n".join(
        chunk.content
        for chunk in chunks
    )

    state["context"] = context

    return state


def generate_answer(state):

    prompt = f"""
        You are OrbitWatch AI Assistant.

        Use retrieved context only.

        If the answer is not present,
        say you don't know.

        CHAT HISTORY:

        {state["history"]}

        CONTEXT:

        {state["context"]}

        QUESTION:

        {state["question"]}

        ANSWER:
        """

    state["answer"] = llm.generate(prompt)

    return state