from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID

from app.database import Base


class IncidentAlert(Base):
    __tablename__ = "incident_alerts"

    incident_id: Mapped[int] = mapped_column(
        ForeignKey("incidents.id", ondelete="CASCADE"),
        primary_key=True,
    )

    alert_id: Mapped[UUID] = mapped_column(
        ForeignKey("alerts.id", ondelete="CASCADE"),
        primary_key=True,
    )

    incident: Mapped["Incident"] = relationship(
        "Incident",
        back_populates="alert_links",
    )

    alert: Mapped["Alert"] = relationship(
        "Alert",
        back_populates="incident_links",
    )