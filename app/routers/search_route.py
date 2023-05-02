from fastapi import Depends, status, HTTPException, APIRouter, Response
from random import randrange
from typing import List
from app import utils, oauth2
from app.schemas import searchSchemas
import global_mock

router = APIRouter(
    prefix="/search",
    tags=['Search']
)

@router.get("/",response_model=List[searchSchemas.Search])
def search(query: str,current_user: int = Depends(oauth2.get_current_user)):
    #todo!: search algolia
    #global_mock.my_post
    return {}
