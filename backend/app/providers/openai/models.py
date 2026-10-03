from dataclasses import dataclass
from typing import Any


@dataclass
class OpenAITextResult:
    response_id: str
    text: str
    raw: Any


@dataclass
class OpenAIJSONResult:
    response_id: str
    data: dict[str, Any]
    raw: Any