from fastapi import Request


async def rate_limit_middleware(
    request: Request,
    call_next,
):
    """
    Basic placeholder.

    Production rate limiting will be added later.
    """
    return await call_next(request)