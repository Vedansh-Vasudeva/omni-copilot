from mem0 import Memory
import os

class UserMemory:
    def __init__(self):
        # We use the local memory instead of managed if Mem0 is locally run.
        # Mem0 automatically uses LLM keys to extract memories.
        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "dummy_key")
        self.m = Memory()
        
    def add_interaction(self, user_id: str, message: str, role: str = "user"):
        self.m.add(message, user_id=user_id)
        
    def get_context(self, user_id: str, query: str) -> str:
        results = self.m.search(query, filters={"user_id": user_id})
        memories = [res.get("memory", str(res)) for res in results]
        return "\n".join(memories)

user_memory = UserMemory()
