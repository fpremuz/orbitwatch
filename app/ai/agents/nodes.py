from app.ai.retrieval.vector_retriever import VectorRetriever
from app.ai.providers.ollama_provider import OllamaProvider

retriever = VectorRetriever()
llm = OllamaProvider()


RAG_KEYWORDS = [
    "telemetry",
    "satellite",
    "orbit",
    "battery",
    "temperature",
    "voltage",
    "altitude",
    "velocity",
    "communication",
    "antenna",
    "payload",
    "alert",
    "anomaly",
    "ground station",
    "mission",
]


def decide_route(state):
    """
    Decide whether the question should use
    Retrieval-Augmented Generation (RAG)
    or a direct LLM response.

    Returns:
        "retrieve" or "direct"
    """

    question = state["question"].lower()

    for keyword in RAG_KEYWORDS:
        if keyword in question:
            return "retrieve"

    return "direct"


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

        Use ONLY the retrieved context.

        If the answer cannot be found,
        say you don't know.

        CHAT HISTORY

        {state["history"]}

        CONTEXT

        {state["context"]}

        QUESTION

        {state["question"]}

        ANSWER
        """

    state["answer"] = llm.generate(prompt)

    return state


def direct_answer(state):

    prompt = f"""
        You are OrbitWatch AI Assistant.

        Answer the user's question.

        If the question is unrelated to OrbitWatch
        or telemetry, answer normally.

        CHAT HISTORY

        {state["history"]}

        QUESTION

        {state["question"]}

        ANSWER
        """

    state["answer"] = llm.generate(prompt)

    return state