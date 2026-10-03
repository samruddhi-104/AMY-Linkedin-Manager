import uuid

from sqlalchemy import Boolean, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin


class LinkedInAccount(TimestampMixin, Base):
    __tablename__ = "linkedin_accounts"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    company_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )

    provider_account_id: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        index=True,
    )

    display_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    access_token_encrypted: Mapped[str | None] = mapped_column(
        String(4000),
        nullable=True,
    )

    refresh_token_encrypted: Mapped[str | None] = mapped_column(
        String(4000),
        nullable=True,
    )

    is_connected: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    metadata_json: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )