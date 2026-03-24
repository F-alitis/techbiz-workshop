from openai import AzureOpenAI

from config.settings import settings

_client = None


def get_client() -> AzureOpenAI:
    global _client
    if _client is None:
        _client = AzureOpenAI(
            api_version=settings.azure_openai_api_version,
            azure_endpoint=settings.azure_openai_endpoint,
            api_key=settings.azure_openai_api_key,
        )
    return _client


def ask_llm(prompt: str, model: str | None = None) -> str:
    """Send a prompt to Azure OpenAI Responses API and return the text."""
    client = get_client()
    response = client.responses.create(
        model=model or settings.azure_openai_deployment,
        input=prompt,
    )
    return response.output_text
