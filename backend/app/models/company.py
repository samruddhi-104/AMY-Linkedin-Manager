import uuid

from sqlalchemy import String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin


class Company(TimestampMixin, Base):
    __tablename__ = "companies"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    website: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    industry: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    target_audience: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    brand_voice: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    preferred_cta: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    visual_style: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    autonomous_publishing: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
    )
