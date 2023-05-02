from fastapi import Depends, status, HTTPException, APIRouter, Response
from random import randrange
from typing import List
from app import utils, oauth2
from app.models.notifications import Notification
from ..schemas import notificationSchemas
import global_mock

router = APIRouter(
    prefix="/notifications",
    tags=['Notification']
)

@router.get("/",response_model=List[notificationSchemas.Notification])
def get_notifications(current_user: int = Depends(oauth2.get_current_user)):
    notifications = Notification.objects.filter(owner_id= current_user.id)
    return list(notifications)
