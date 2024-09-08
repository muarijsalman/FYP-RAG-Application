from typing import List, Dict
from pinecone import Pinecone, PodSpec, ServerlessSpec
from utils import get_pinecone_api_key, get_pinecone_index_name, batch_inputs


class PineconeVectorDB:
    def __init__(self):
        pinecone_api_key = get_pinecone_api_key()
        pinecone_index_name = get_pinecone_index_name()
        
        self.client = Pinecone(api_key=pinecone_api_key)
        self.embed_dim = 512
        if pinecone_index_name not in self.client.list_indexes().names():
            self.client.create_index(
                name=pinecone_index_name,
                dimension=self.embed_dim,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud='aws', 
                    region='us-east-1'
                ) 
            )
        self.index = self.client.Index(pinecone_index_name)
    
    def upsert_vectors(self, vectors: List[Dict]):
        for batch in batch_inputs(vectors):
            self.index.upsert(batch)
    
    def project_id_exists(self, project_id: str):
        matches = self.index.query(
            vector=[0]*self.embed_dim,
            top_k=3,
            filter={
                "fyp-id": project_id
            }
        )
        if len(matches) != 0:
            return True
        return False

    def query_db(self, query_vector: List, top_k: int=10, filters: dict = None):
        kwargs = {
            "vector": query_vector,
            "top_k":top_k,
            "include_metadata": True
        }
        if filters is not None:
            kwargs["filter"] = filters
        matches = self.index.query(**kwargs)["matches"]
        
        return matches
        