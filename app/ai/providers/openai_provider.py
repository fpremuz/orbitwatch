import os

from openai import OpenAI

from app.ai.providers.base import AIProvider


class OpenAIProvider(AIProvider):

    def __init__(self):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
        )

    def analyze(self, prompt: str) -> str:

        response = self.client.chat.completions.create(
            model="deepseek/deepseek-v4-flash:free",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.choices[0].message.content