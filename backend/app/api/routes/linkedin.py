from fastapi import APIRouter

from app.config import get_settings
from app.providers.linkedin.factory import (
    get_linkedin_provider,
)
from app.services.in_memory_store import store


router = APIRouter(
    prefix="/linkedin",
    tags=["LinkedIn"],
)


@router.get("/status")
async def linkedin_status():

    settings = get_settings()

    if settings.mock_mode:

        return {
            "success": True,
            "data": {
                "connected": True,
                "provider": "mock",
                "account": (
                    "CTons Solutions"
                ),
            },
        }

    account = (
        store.get_linkedin_account()
    )

    if account is None:

        return {
            "success": True,
            "data": {
                "connected": False,
                "provider": "linkedin",
            },
        }

    provider = (
        get_linkedin_provider()
    )

    status = await provider.get_status()

    return {
        "success": True,
        "data": status.model_dump(),
    }


@router.get("/account")
async def linkedin_account():

    provider = (
        get_linkedin_provider()
    )

    account = (
        await provider.get_account()
    )

    return {
        "success": True,
        "data": account.model_dump(),
    }

from fastapi import HTTPException

from app.agents.linkedin_agent import (
    LinkedInAgent,
)


@router.post("/publish/{post_id}")
async def publish_post(
    post_id: str,
):

    post = store.get_post(
        post_id
    )

    if post is None:

        raise HTTPException(
            status_code=404,
            detail="Post not found.",
        )

    if post.get("status") != "APPROVED":

        raise HTTPException(
            status_code=400,
            detail=(
                "Post must be approved "
                "before publishing."
            ),
        )

    if post.get(
        "linkedin_post_id"
    ):

        return {
            "success": True,
            "data": {
                "status": (
                    "ALREADY_PUBLISHED"
                ),
                "linkedin_post_id": (
                    post[
                        "linkedin_post_id"
                    ]
                ),
            },
        }

    agent = LinkedInAgent()

    result = await agent.run(
        task_id=f"publish-{post_id}",
        input_data={
            "post_id": post_id,
        },
    )

    return {
        "success": True,
        "data": result,
    }