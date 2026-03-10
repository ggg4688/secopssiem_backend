from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AssetCreate(BaseModel):
    hostname: str = Field(min_length=1, max_length=255)
    ip: str = Field(min_length=1, max_length=45)


class AssetUpdate(BaseModel):
    hostname: str | None = Field(default=None, min_length=1, max_length=255)
    ip: str | None = Field(default=None, min_length=1, max_length=45)


class AssetRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    hostname: str
    ip: str
    created_at: datetime


class AlertCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1)
    severity: str = Field(min_length=1, max_length=30)
    asset_id: UUID


class AlertUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, min_length=1)
    severity: str | None = Field(default=None, min_length=1, max_length=30)
    asset_id: UUID | None = None


class AlertRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str
    severity: str
    asset_id: UUID
    created_at: datetime