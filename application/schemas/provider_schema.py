import uuid
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, model_validator


class ProviderStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class FieldBase(BaseModel):
    name: str
    key: str
    type: str
    isRequired: bool = False
    min: int = -1
    max: int = -1

class UseCaseFieldBase(BaseModel):
    name: str
    key: str
    type: str
    isRequired: bool = False
    depends_on: Optional[str] = None
    min: int = -1
    max: int = -1

class FieldCreate(FieldBase):
    pass

class FieldResponse(FieldBase):
    id: uuid.UUID

    class Config:
        from_attributes = True

class UseCaseFieldCreate(UseCaseFieldBase):
    pass

class UseCaseFieldResponse(UseCaseFieldBase):
    id: uuid.UUID

    class Config:
        from_attributes = True

class ProviderBase(BaseModel):
    title: str
    value: str
    type: List[str]
    img_url: Optional[str] = None
    status: ProviderStatus = ProviderStatus.INACTIVE

    @model_validator(mode="after")
    def set_img_url(self):
        if not self.img_url:
            self.img_url = f"https://raw.githubusercontent.com/devicons/devicon/master/icons/{self.value.lower()}/{self.value.lower()}-original.svg"
        return self

class ProviderCreate(ProviderBase):
    fields: List[FieldCreate]
    use_case_fields: List[UseCaseFieldCreate]

class ProviderListItem(BaseModel):
    id: uuid.UUID
    value: str
    title: str
    type: List[str]
    img_url: Optional[str]
    status: ProviderStatus

    class Config:
        from_attributes = True
