from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class IncidentCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1)
    status: str = Field(default="open", min_length=1, max_length=50)


class IncidentUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, min_length=1)
    status: str | None = Field(default=None, min_length=1, max_length=50)


class IncidentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str
    status: str
    created_at: datetime


class IncidentAlertLinkCreate(BaseModel):
    alert_id: UUID


class IncidentAlertLinkRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    incident_id: UUID
    alert_id: UUID


class IncidentCommentCreate(BaseModel):
    comment: str = Field(min_length=1)


class IncidentCommentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    incident_id: UUID
    user_id: UUID
    comment: str
    created_at: datetime