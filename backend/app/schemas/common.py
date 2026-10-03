from typing import Any


class SuccessResponse:
    pass


def success_response(data: Any) -> dict:
    return {
        "success": True,
        "data": data,
    }


def error_response(
    code: str,
    message: str,
    details: dict | None = None,
) -> dict:
    return {
        "success": False,
        "error": {
            "code": code,
            "message": message,
            "details": details or {},
        },
    }