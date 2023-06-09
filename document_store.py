from llama_index.vector_stores import WeaviateVectorStore
import os
import weaviate


class DocumentStore:
    def __init__(self):
        self.client = weaviate.Client(os.environ.get('WEAVIATE_API_URL'))
        self.weaviate_store = WeaviateVectorStore(weaviate_client=self.client)

    def query(self, query_text):
        return self.weaviate_store.query(query_text)
