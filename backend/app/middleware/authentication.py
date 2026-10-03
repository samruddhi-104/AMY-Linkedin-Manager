from fastapi import Request


async def authentication_middleware(
    request: Request,
    call_next,
):
    """
    Authentication placeholder for Phase 1.

    Real user authentication will be implemented later.
    """
    return await call_next(request)