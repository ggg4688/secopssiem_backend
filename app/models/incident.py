from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="open")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    alert_links: Mapped[list["IncidentAlert"]] = relationship(
        "IncidentAlert",
        back_populates="incident",
        cascade="all, delete-orphan",
    )
    comments: Mapped[list["IncidentComment"]] = relationship(
        "IncidentComment",
        back_populates="incident",
        cascade="all, delete-orphan",
    )

