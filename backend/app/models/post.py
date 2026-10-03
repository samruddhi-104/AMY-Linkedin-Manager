import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin


class Post(TimestampMixin, Base):
    __tablename__ = "posts"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    company_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="DRAFT",
        nullable=False,
        index=True,
    )

    content_type: Mapped[str] = mapped_column(
        String(50),
        default="text",
        nullable=False,
    )

    title: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    hook: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    body: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    cta: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    keywords: Mapped[list | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    hashtags: Mapped[list | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    visual_concept: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    linkedin_post_id: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        unique=True,
    )