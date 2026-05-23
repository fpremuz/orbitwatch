import requests


class OllamaProvider:
    def __init__(self, model: str = "llama3.2:3b"):
        self.model = model
        self.base_url = "http://host.docker.internal:11434/api/generate"

    def generate(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(self.base_url, json=payload)

        if response.status_code != 200:
            return f"AI error: {response.text}"

        data = response.json()
        return data.get("response", "")