from fastapi import Depends, status, HTTPException, APIRouter, Response
from random import randrange
from app import utils, oauth2
from typing import List
from ..schemas import commentsSchemas
from app.models.posts import Post
from app.models.comment import Comment
from app.models.notifications import Notification
import global_mock

router = APIRouter(
    prefix="/comments",
    tags=['Comments']
)

@router.get("/{post_id}",response_model=List[commentsSchemas.Comment])
def get_comments(post_id: str,current_user: int = Depends(oauth2.get_current_user)):
    comment = Comment.objects.filter(post_id= post_id)
    return list(comment)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=commentsSchemas.Comment)
def create_comments(comments: commentsSchemas.CommentCreate,current_user: int = Depends(oauth2.get_current_user)):
    comment = Comment(**comments.dict())
    comment.author_id = current_user["id"]
    #comment.post_id = comment.post_id
    comment.author_username = current_user['username']
    comment.author_profile_image_url = current_user['profile_image_url']
    posts_user = dict(Post.objects.filter(id = comment.post_id).first())
    Notification(owner_id= posts_user["author_id"], notification_type= 'Comment',
    message =f"{current_user['username']} just commented on you'r post {posts_user['title']}", author= current_user['username']).save()
    comment.save()
    return dict(comment)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comments(id: str, current_user: int = Depends(oauth2.get_current_user)):
    query = Comment.objects.filter(author_id= current_user["id"]).filter(id= id)
    if query.count() == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                detail=f'no comment found.')
    query.delete()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
