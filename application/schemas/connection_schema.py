from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from uuid import UUID


class ConnectionBase(BaseModel):
    provider_id: UUID
    config: Dict[str, Any]


class ConnectionCreate(ConnectionBase):
    pass


class ConnectionUpdate(BaseModel):
    config: Optional[Dict[str, Any]] = None
    status: Optional[str] = None


class ConnectionResponse(BaseModel):
    id: UUID
    user_id: UUID
    provider_id: UUID
    config: Dict[str, Any]
    status: str

    class Config:
        from_attributes = True