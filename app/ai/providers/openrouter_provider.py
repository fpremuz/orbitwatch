import os
import requests
from app.ai.providers.base import AIProvider

class OpenRouterProvider(AIProvider):
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")

    def generate(self, prompt: str) -> str:
        res = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}"
            },
            json={
                "model": "deepseek/deepseek-v4-flash:free",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
        )

        return res.json()["choices"][0]["message"]["content"]