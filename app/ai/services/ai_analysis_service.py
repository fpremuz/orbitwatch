from app.ai.providers.router import AIProviderRouter

class AIAnalysisService:
    def __init__(self):
        self.provider = AIProviderRouter()

    def analyze(self, prompt: str) -> dict:
        raw = self.provider.generate(prompt)

        return {
            "summary": raw,
            "severity": "low",
            "recommendation": "No action required"
        }