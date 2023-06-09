import os

import openai
import weaviate
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Weaviate
from llama_index import StorageContext, VectorStoreIndex
from llama_index.vector_stores import WeaviateVectorStore

import ingest


class DocumentStore:
    def __init__(self):
        self.index_name = "TalkToNist"
        openai.api_key = 'Free the models'
        openai.api_base = os.environ.get('REMOTE_API_URL')
        self.client = weaviate.Client(url=os.environ.get('WEAVIATE_API_URL'),
                                      additional_headers={
                                          'X-OpenAI-Api-Key': openai.api_key
                                      })
        self.embeddings = OpenAIEmbeddings(openai_api_key="foobar",
                                           openai_api_base=os.environ.get('REMOTE_API_URL'),
                                           model="text-embedding-ada-002")
        self.vectordb = Weaviate(self.client, self.index_name, "content", embedding=self.embeddings)
        self.weaviate_store = WeaviateVectorStore(weaviate_client=self.client)
        self.ingestor = ingest.Ingest(self.index_name, self.client, self.embeddings)

    def query(self, query_text):
        storage_context = StorageContext.from_defaults(vector_store=self.weaviate_store)
        index = VectorStoreIndex.from_vector_store(self.weaviate_store, storage_context=storage_context)
        query_engine = index.as_query_engine()
        return query_engine.query(query_text)

    def load_pdf(self, path):
        ingest.load_data(self.ingestor, path)