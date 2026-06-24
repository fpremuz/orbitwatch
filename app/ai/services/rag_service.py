from app.ai.agents.graph import graph


class RagService:

    def ask(
        self,
        question: str,
        history: str = "",
    ) -> str:

        result = graph.invoke(
            {
                "question": question,
                "history": history,
                "context": "",
                "answer": "",
            }
        )

        return result["answer"]