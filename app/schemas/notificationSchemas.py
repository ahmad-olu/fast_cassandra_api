from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

from app.schemas.enum import NotificationType


class NotificationBase(BaseModel):
    owner_id: str
    title: str
    post_id: Optional[str] = None
    notification_type: NotificationType

class NotificationCreate(NotificationBase):
    pass

class Notification(NotificationBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True

