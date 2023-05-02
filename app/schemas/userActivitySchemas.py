from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel



class LikesCreate(BaseModel):
    post_id: UUID

class Likes(LikesCreate):
    id: UUID
    liked_by: UUID
    created_at: datetime

    class Config:
        orm_mode = True

class FollowCreate(BaseModel):
    follower: UUID

class FollowersCreate(BaseModel):
    follower: UUID

class Followers(FollowersCreate):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True

class FollowingCreate(BaseModel):
    following: UUID

class Following(FollowingCreate):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True