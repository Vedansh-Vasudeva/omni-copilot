import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Omni-Copilot API"
    host: str = "0.0.0.0"
    port: int = 8000
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    chromadb_dir: str = "./data/chromadb"
    mem0_api_key: str = os.getenv("MEM0_API_KEY", "")

settings = Settings()
