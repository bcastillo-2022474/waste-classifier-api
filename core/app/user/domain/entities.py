from typing import Optional
from uuid import UUID
from datetime import datetime
from uuid import uuid4
from pydantic import BaseModel, Field


class User(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    first_name: str = Field("", title="First name")
    last_name: str = Field("", title="Last name")
    email: str = Field("", title="Email")
    is_active: bool = Field(True, title="Active status")
    date_joined: datetime = Field(default_factory=datetime.now)

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    created_by_id: Optional[UUID] = None


    class Config:
        extra = "ignore"
        allow_mutations = False

    def __getitem__(self, item):
        return getattr(self, item)
