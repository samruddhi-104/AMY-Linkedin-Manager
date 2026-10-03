import uuid

from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin


class Keyword(TimestampMixin, Base):
    __tablename__ = "keywords"

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

    keyword: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    keyword_type: Mapped[str] = mapped_column(
        String(100),
        default="secondary",
        nullable=False,
    )

    relevance_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
