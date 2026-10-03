from app.providers.search.client import SearchProvider


class MockSearchProvider(SearchProvider):

    async def search(
        self,
        query: str,
    ) -> list[dict]:

        return [
            {
                "title": "Mock AI Industry Trend",
                "url": "https://example.com/mock-ai-trend",
                "domain": "example.com",
                "snippet": (
                    "Mock research result for development."
                ),
                "published_at": None,
                "source_type": "mock",
                "query": query,
            },
            {
                "title": "Mock Enterprise Automation Trend",
                "url": "https://example.com/mock-automation",
                "domain": "example.com",
                "snippet": (
                    "Mock enterprise automation result."
                ),
                "published_at": None,
                "source_type": "mock",
                "query": query,
            },
        ]

    async def fetch(
        self,
        url: str,
    ) -> dict:

        return {
            "url": url,
            "content": (
                "This is mock content used during development."
            ),
            "source_type": "mock",
        }