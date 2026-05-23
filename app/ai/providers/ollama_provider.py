import requests

from app.ai.providers.base import AIProvider


class OllamaProvider(AIProvider):

    def analyze(self, prompt: str) -> str:

        response = requests.post(
            "http://host.docker.internal:11434/api/generate",
            json={
                "model": "llama3.2:3b",
                "prompt": prompt,
                "stream": False,
            },
            timeout=120,
        )

        data = response.json()

        return data["response"]