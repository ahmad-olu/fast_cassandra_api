from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

from app.schemas.enum import PostType



class CommentBase(BaseModel):
    content: str
    post_type: str

class CommentCreate(CommentBase):
    post_id: Optional[UUID] = None

class Comment(CommentBase):
    id: UUID
    post_id: UUID
    author_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True

