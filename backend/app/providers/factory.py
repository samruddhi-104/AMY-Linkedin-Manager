from app.config import get_settings
from app.providers.openai.client import OpenAIProvider
from app.providers.search.client import SearchProvider
from app.providers.search.mock_search import MockSearchProvider
from app.providers.search.openai_search import OpenAIWebSearchProvider


def get_openai_provider() -> OpenAIProvider:
    """
    Return the configured OpenAI provider.
    """
    return OpenAIProvider()


def get_search_provider() -> SearchProvider:
    """
    Return the appropriate search provider.

    MOCK_MODE=true:
        MockSearchProvider

    MOCK_MODE=false:
        OpenAIWebSearchProvider
    """

    settings = get_settings()

    if settings.mock_mode:
        return MockSearchProvider()

    openai_provider = get_openai_provider()

    return OpenAIWebSearchProvider(
        openai_provider=openai_provider
    )