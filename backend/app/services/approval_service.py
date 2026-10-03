from app.services.in_memory_store import store


class ApprovalService:
    """
    Handles the lifecycle of LinkedIn content approval.

    Lifecycle:

        DRAFT
          ↓
        REVIEW
          ↓
        APPROVED

    Publishing is handled separately by LinkedInAgent.
    """

    def submit_for_review(
        self,
        post_id: str,
    ) -> dict:
        """
        Move a draft post into REVIEW status.
        """

        post = store.get_post(
            post_id
        )

        if post is None:
            raise ValueError(
                "Post not found."
            )

        current_status = post.get(
            "status"
        )

        if current_status not in {
            "DRAFT",
            "REVIEW",
        }:
            raise ValueError(
                "Only draft content can be submitted for review."
            )

        post["status"] = "REVIEW"

        return post

    def approve(
        self,
        post_id: str,
    ) -> dict:
        """
        Approve a post for publishing.
        """

        post = store.get_post(
            post_id
        )

        if post is None:
            raise ValueError(
                "Post not found."
            )

        current_status = post.get(
            "status"
        )

        if current_status not in {
            "DRAFT",
            "REVIEW",
        }:
            raise ValueError(
                "Only draft or review content can be approved."
            )

        post["status"] = "APPROVED"

        return post

    def reject(
        self,
        post_id: str,
        reason: str = "",
    ) -> dict:
        """
        Reject a post and return it to DRAFT.
        """

        post = store.get_post(
            post_id
        )

        if post is None:
            raise ValueError(
                "Post not found."
            )

        post["status"] = "DRAFT"

        post["rejection_reason"] = (
            reason.strip()
            if reason
            else None
        )

        return post


approval_service = ApprovalService()