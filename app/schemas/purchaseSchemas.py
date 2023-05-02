from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.schemas.enum import PostType


class PurchaseBase(BaseModel):
    author_id: str
    book_price: int
    post_id: Optional[str] = None
    post_type: PostType
    currency: Optional[str] = None
    discount: Optional[int] = None

class PurchaseCreate(PurchaseBase):
    pass

class Purchase(PurchaseBase):
    id: int
    #created_at: datetime

    class Config:
        orm_mode = True

