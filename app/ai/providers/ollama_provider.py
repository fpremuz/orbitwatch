import requests

from app.ai.providers.base import AIProvider


class OllamaProvider(AIProvider):

    def analyze(self, prompt: str) -> str:

        response = requests.post(
            "http://ollama:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False,
            },
            timeout=60,
        )

        data = response.json()

        return data["response"]