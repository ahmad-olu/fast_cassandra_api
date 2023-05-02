from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

from app.schemas.enum import PostType



class FeedBackBase(BaseModel):
    content: str
    image_url: Optional[str] = None

class FeedBackCreate(FeedBackBase):
    pass

class FeedBack(FeedBackBase):
    id: UUID
    author_username: str
    author_email: str
    author_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True

