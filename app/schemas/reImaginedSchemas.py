from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

from app.schemas.enum import PostType


class ReImaginedBase(BaseModel):
    post_type: str
    content: str

class ReImaginedCreate(ReImaginedBase):
    post_id: UUID

class ReImaginedUpdate(ReImaginedBase):
    pass

class ReImagined(ReImaginedBase):
    id: UUID
    post_id: UUID
    author_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True

