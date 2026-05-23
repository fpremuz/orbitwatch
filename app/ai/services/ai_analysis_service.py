from app.ai.providers.ollama_provider import OllamaProvider


class AIAnalysisService:
    def __init__(self):
        self.provider = OllamaProvider()

    def analyze(self, prompt: str) -> str:
        return self.provider.generate(prompt)