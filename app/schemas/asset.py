from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AssetCreate(BaseModel):
    hostname: str
    ip: str


class AssetRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    hostname: str
    ip: str
    created_at: datetime