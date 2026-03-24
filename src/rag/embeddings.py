from langchain_openai import AzureOpenAIEmbeddings

from config.settings import settings


def get_embeddings():
    return AzureOpenAIEmbeddings(
        azure_deployment=settings.azure_openai_embedding_deployment,
        azure_endpoint=settings.azure_openai_endpoint,
        api_key=settings.azure_openai_api_key,
        api_version=settings.azure_openai_embedding_api_version,
    )
