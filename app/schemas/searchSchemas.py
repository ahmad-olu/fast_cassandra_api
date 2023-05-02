from datetime import datetime
from typing import List
from typing import Optional
from pydantic import BaseModel

from app.schemas.enum import PostType
from app.schemas import userSchemas, postSchemas, reImaginedSchemas


class Search(BaseModel):
    id: str
    author: Optional[userSchemas.UserOut] = None
    post: Optional[postSchemas.Post] = None
    re_imagined: Optional[reImaginedSchemas.ReImagined] = None

class SearchCreate(Search):
    pass

class Search(Search):
    #created_at: datetime

    class Config:
        orm_mode = True

