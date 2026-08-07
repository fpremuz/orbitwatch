from app.ai.providers.ollama_provider import OllamaProvider
from app.ai.retrieval.vector_retriever import VectorRetriever
from app.ai.tools.alert_tools import AlertTools
from app.ai.agents.planner import parse_plan


retriever = VectorRetriever()
llm = OllamaProvider()
tools = AlertTools()


def classify_request(state):

    prompt = f"""
        You are an AI planner.

        Choose ONE decision.

        retrieve
        tool
        both
        direct

        Rules:

        retrieve
        - telemetry
        - satellites
        - mission docs
        - procedures

        tool
        - jokes
        - math
        - date
        - utility tasks

        both
        - telemetry + external reasoning

        direct
        - normal conversation

        Question:

        {state["question"]}

        Decision:
    """

    decision = llm.generate(prompt)

    state["decision"] = parse_plan(decision)

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