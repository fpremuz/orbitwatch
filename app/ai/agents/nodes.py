from app.ai.providers.ollama_provider import OllamaProvider
from app.ai.retrieval.vector_retriever import VectorRetriever
from app.ai.tools.alert_tools import AlertTools


retriever = VectorRetriever()
llm = OllamaProvider()
tools = AlertTools()


def classify_request(state):
    """
    Placeholder node.

    Routing is performed by graph.py through route_question().
    """
    return state


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

    state["context"] = "\n\n".join(
        chunk.content
        for chunk in chunks
    )

    state["tool_output"] = ""

    return state


def execute_tool(state):

    alerts = tools.get_recent_alerts()

    state["tool_output"] = str(alerts)

    state["context"] = ""

    return state


def generate_answer(state):

    prompt = f"""
You are OrbitWatch AI Assistant.

Answer using:

1. Tool output if available.
2. Retrieved context.
3. Your own knowledge only if neither contains the answer.

Conversation History:

{state["history"]}

Retrieved Context:

{state["context"]}

Tool Output:

{state["tool_output"]}

Question:

{state["question"]}

Answer:
"""

    state["answer"] = llm.generate(prompt)

    return state