import os
from together import Together

class Embedding:
    def __init__(self, api_key=None, model=None):
        if api_key is None:
            api_key = os.getenv('TOGETHER_API_KEY')
        if model is None:
            model = os.environ.get('TOGETHER_EMBEDDING_MODEL', 'togethercomputer/m2-bert-80M-32k-retrieval')
        self.client = Together(api_key=api_key)
        self.model = model

    def embed(self, texts):
        try:
            embeddings = []
            for text in texts:
                response = self.client.embeddings.create(
                    input=text,
                    model=self.model
                )
                embeddings.append(response.data[0].embedding)
            return embeddings
        except Exception as e:
            print(f"❌ Erro ao gerar embeddings: {e}")
            return []
