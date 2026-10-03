import logging

from fastapi import Request
from fastapi.responses import JSONResponse


logger = logging.getLogger(__name__)


class AMYException(Exception):
    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = 400,
        details: dict | None = None,
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or {}

        super().__init__(message)


class AgentError(AMYException):
    pass


class TaskError(AMYException):
    pass


class ProviderError(AMYException):
    pass


class AuthenticationError(AMYException):
    pass


class AuthorizationError(AMYException):
    pass


class ValidationError(AMYException):
    pass


class RateLimitError(AMYException):
    pass


class PublishingError(AMYException):
    pass


class SchedulingError(AMYException):
    pass


class TaskCancelledError(AMYException):
    pass


async def amy_exception_handler(
    request: Request,
    exc: AMYException,
):
    logger.error(
        "AMY exception: %s - %s",
        exc.code,
        exc.message,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
            },
        },
    )


async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
):
    logger.exception(
        "Unhandled exception",
        exc_info=exc,
    )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected server error occurred.",
                "details": {},
            },
        },
    )