import os

from app.ai.providers.openai_provider import OpenAIProvider
from app.ai.providers.ollama_provider import OllamaProvider


class AIAnalysisService:

    def __init__(self):

        provider = os.getenv("AI_PROVIDER", "openrouter")

        if provider == "ollama":
            self.provider = OllamaProvider()
        else:
            self.provider = OpenAIProvider()

    def analyze_telemetry(self, telemetry: dict):

        prompt = f"""
        Analyze this telemetry data and summarize operational concerns:

        {telemetry}
        """

        return self.provider.analyze(prompt)