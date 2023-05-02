from fastapi import Depends, status, APIRouter
from app import oauth2
from typing import List
from ..schemas import feedbackSchemas
from app.models.feedback import Feedback

router = APIRouter(
    prefix="/feedback",
    tags=['Feedback']
)

@router.get("/",response_model=List[feedbackSchemas.FeedBack])
def get_feedbacks(current_user: int = Depends(oauth2.get_current_user)):
    comment = Feedback.objects.all()
    return list(comment)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=feedbackSchemas.FeedBack)
def create_feedbacks(feedbacks: feedbackSchemas.FeedBackCreate,current_user: int = Depends(oauth2.get_current_user)):
    feedback = Feedback(**feedbacks.dict())
    feedback.author_id = current_user["id"]
    feedback.author_username = current_user['username']
    feedback.author_email = current_user['email']
    feedback.save()
    return dict(feedback)
