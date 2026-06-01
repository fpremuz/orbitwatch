import requests


class EmbeddingService:

    def __init__(self):
        self.base_url = "http://host.docker.internal:11434/api/embeddings"
        self.model = "nomic-embed-text"

    def embed(self, text: str) -> list[float]:

        response = requests.post(
            self.base_url,
            json={
                "model": self.model,
                "prompt": text,
            },
            timeout=60,
        )

        response.raise_for_status()

        data = response.json()

        return data["embedding"]