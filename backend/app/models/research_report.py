import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin


class ResearchReport(TimestampMixin, Base):
    __tablename__ = "research_reports"

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

    topic: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        index=True,
    )

    summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    findings: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    recommendations: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    content_opportunities: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )
