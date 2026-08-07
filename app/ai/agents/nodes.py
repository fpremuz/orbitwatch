from app.ai.providers.ollama_provider import OllamaProvider
from app.ai.retrieval.vector_retriever import VectorRetriever
from app.ai.tools.registry import ToolRegistry
from app.ai.agents.planner import plan

retriever = VectorRetriever()
llm = OllamaProvider()
tool_registry = ToolRegistry()


def classify_request(state):

    routing = plan(state["question"])

    print("=" * 80)
    print("ROUTER")
    print(routing)
    print("=" * 80)

    state["decision"] = routing["decision"]
    state["selected_tool"] = routing["selected_tool"]

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

    print("=" * 80)
    print("RETRIEVAL")
    print(state["context"])
    print("=" * 80)

    return state


def execute_tool(state):

    print("=" * 80)
    print("EXECUTING TOOL")
    print(state["selected_tool"])
    print("=" * 80)

    state["tool_output"] = tool_registry.execute(
        state["selected_tool"]
    )

    state["context"] = ""

    print("=" * 80)
    print("TOOL OUTPUT")
    print(state["tool_output"])
    print("=" * 80)

    return state


def generate_answer(state):

    print("=" * 80)
    print("GENERATE")
    print("Context:")
    print(state["context"])
    print()
    print("Tool:")
    print(state["tool_output"])
    print("=" * 80)

    prompt = f"""
You are OrbitWatch AI Assistant.

IMPORTANT RULES

If Tool Output is NOT EMPTY:

- You MUST answer ONLY using Tool Output.
- Do NOT ignore Tool Output.
- Do NOT replace Tool Output with your own knowledge.
- You MAY rephrase it to sound natural.
- Do NOT invent extra information.

If Tool Output is EMPTY:

- Use Retrieved Context.

If both Tool Output and Retrieved Context are empty:

- Use your own knowledge.

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