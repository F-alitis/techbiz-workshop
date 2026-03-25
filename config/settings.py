from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env")

    # Azure OpenAI — LLM
    azure_openai_api_key: str
    azure_openai_endpoint: str
    azure_openai_api_version: str
    azure_openai_deployment: str

    # Azure OpenAI — Embeddings
    azure_openai_embedding_deployment: str
    azure_openai_embedding_api_version: str

    # LangSmith
    langchain_tracing_v2: bool
    langchain_api_key: str
    langchain_project: str
    langchain_endpoint: str

    # RAG
    chunk_size: int
    chunk_overlap: int
    retrieval_top_k: int

    # Crawling
    nbg_base_url: str
    nbg_crawl_urls: list[str]
    nbg_scrape_urls: list[str]
    crawl_rate_limit: float
    crawl_max_depth: int
    crawl_timeout: int
    crawl_allowed_domain: str

    # Paths
    data_dir: str
    vector_store_path: str


settings = Settings()
