from datetime import datetime
from typing import List
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

from app.schemas.enum import PostType


class PostBase(BaseModel):
    title: str
    sub_title: Optional[str] = None
    post_type: str
    content: str
    publish: Optional[bool] = True
    images_url: List[str] = []

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: UUID
    author_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True

