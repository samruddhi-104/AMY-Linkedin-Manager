from app.providers.openai.client import OpenAIProvider
from app.providers.search.client import SearchProvider


class OpenAIWebSearchProvider(SearchProvider):

    def __init__(
        self,
        openai_provider: OpenAIProvider,
    ) -> None:
        self.openai = openai_provider

    async def search(
        self,
        query: str,
    ) -> list[dict]:

        result = await self.openai.generate_text(
            instructions=(
                "Search the web for the user's query. "
                "Return a concise research-oriented summary "
                "with the important sources used."
            ),
            input_text=query,
            use_web_search=True,
        )

        return [
            {
                "summary": result["text"],
                "response_id": result["response_id"],
            }
        ]

    async def fetch(
        self,
        url: str,
    ) -> dict:

        result = await self.openai.generate_text(
            instructions=(
                "Analyze the supplied URL and summarize "
                "the useful information available from it."
            ),
            input_text=url,
            use_web_search=True,
        )

        return {
            "url": url,
            "content": result["text"],
            "response_id": result["response_id"],
        }