from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env")

    # Azure OpenAI
    azure_openai_api_key: str = ""
    azure_openai_endpoint: str = "https://users-direct-oai.openai.azure.com/"
    azure_openai_api_version: str = "2025-04-01-preview"
    azure_openai_deployment: str = "o4-mini"
    azure_openai_embedding_deployment: str = "uniko-poc-embeddings"
    azure_openai_embedding_api_version: str = "2024-12-01-preview"

    # LangSmith
    langchain_tracing_v2: bool = True
    langchain_api_key: str = ""
    langchain_project: str = "nbg-banking-agent"
    langchain_endpoint: str = "https://api.smith.langchain.com"

    # RAG
    chunk_size: int = 1000
    chunk_overlap: int = 200
    retrieval_top_k: int = 5

    # Crawling
    nbg_base_url: str = "https://www.nbg.gr"
    crawl_rate_limit: float = 1.0

    # Paths
    data_dir: str = "data"
    vector_store_path: str = "data/vector_store"


settings = Settings()
