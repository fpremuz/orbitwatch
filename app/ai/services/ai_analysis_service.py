from app.ai.providers.router import AIProviderRouter

class AIAnalysisService:
    def __init__(self):
        self.provider = AIProviderRouter()

    def analyze(self, prompt: str) -> dict:
        result = self.provider.generate(prompt)

        return {
            "input": prompt,
            "output": result
        }