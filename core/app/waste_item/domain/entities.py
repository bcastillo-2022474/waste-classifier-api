from typing import Optional, Protocol
from uuid import UUID
from datetime import datetime
from uuid import uuid4

from enum import Enum
from pydantic import BaseModel, Field, UrlConstraints


class WasteItemType(str, Enum):
    NON_RECYCLABLE = "non_recyclable" # Residuos que no pueden volver a usarse
    RECYCLABLE = "recyclable"
    ORGANIC = "organic"

class WasteItem(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    image: str
    material: str
    type: WasteItemType
    approximate_weight: float

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    created_by_id: Optional[UUID] = None


    class Config:
        extra = "ignore"
        allow_mutations = False

    def __getitem__(self, item):
        return getattr(self, item)


class WasteItemInfo(BaseModel):
    material: str
    type: WasteItemType
    approximate_weight: float

    class Config:
        extra = "ignore"
        allow_mutations = False

    def __getitem__(self, item):
        return getattr(self, item)

class Image:
    def __init__(self, url: str):
        self.url = url

    def __str__(self):
        return self.url