import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class Asset(Base):
    __tablename__ = "assets"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )

    hostname: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True
    )

    ip: Mapped[str] = mapped_column(
        String(45),
        nullable=False,
        unique=True,
        index=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    alerts: Mapped[list["Alert"]] = relationship(
        "Alert",
        back_populates="asset",
        cascade="all, delete-orphan",
    )