from app.ai.providers.ollama_provider import OllamaProvider

class AIProviderRouter:
    def __init__(self):
        self.local = OllamaProvider()

    def generate(self, prompt: str) -> str:
        return self.local.generate(prompt)