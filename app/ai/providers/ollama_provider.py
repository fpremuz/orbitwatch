import requests

class OllamaProvider:
    def __init__(self, model: str = "llama3.2:3b"):
        self.model = model
        self.base_url = "http://host.docker.internal:11434/api/generate"

    def generate(self, prompt: str) -> str:
        try:
            response = requests.post(self.base_url, json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            })

            response.raise_for_status()
            data = response.json()

            return data.get("response", "")

        except Exception as e:
            return f"Ollama error: {str(e)}"