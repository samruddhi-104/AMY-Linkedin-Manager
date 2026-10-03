class OpenAIProviderError(Exception):
    """Base OpenAI provider error."""


class OpenAIConfigurationError(OpenAIProviderError):
    """Raised when OpenAI configuration is missing or invalid."""


class OpenAIRequestError(OpenAIProviderError):
    """Raised when an OpenAI request fails."""