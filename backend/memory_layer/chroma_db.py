import chromadb
from typing import List

class SemanticMemory:
    def __init__(self, persist_directory="./data/chromadb"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(name="omni_semantic_memory")
        
    def add_memory(self, memory_id: str, document: str, metadata: dict = None):
        self.collection.upsert(
            documents=[document],
            metadatas=[metadata or {}],
            ids=[memory_id]
        )
        
    def query_memories(self, query: str, n_results: int = 3) -> List[str]:
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        if results['documents'] and len(results['documents']) > 0:
            return results['documents'][0]
        return []

semantic_memory = SemanticMemory()
