from fastapi import Depends, status, HTTPException, APIRouter, Response
from random import randrange
from app import utils, oauth2
from app.models.like import Like
from app.models.posts import Post
from app.models.reImagined import ReImaginedPost
from app.models.notifications import Notification
from ..schemas import userActivitySchemas
import global_mock

router = APIRouter(
    prefix="/likes",
    tags=['likes']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=userActivitySchemas.Likes)
def create_likes(like: userActivitySchemas.LikesCreate,current_user: int = Depends(oauth2.get_current_user)):
    like = Like(**like.dict())
    like.liked_by = current_user["id"]
    like.save()
    posts_user = dict(Post.objects.filter(id = like.post_id).first())
    Notification(owner_id= posts_user["author_id"], notification_type= 'Like',
    message =f"{current_user['username']} just Liked you'r post {posts_user['title']}", author= current_user['username']).save()
    return dict(like)

@router.post("/re_imagined", status_code=status.HTTP_201_CREATED, response_model=userActivitySchemas.Likes)
def create_re_imagined_likes(likes: userActivitySchemas.LikesCreate,current_user: int = Depends(oauth2.get_current_user)):
    like = Like(**like.dict())
    like.liked_by = current_user["id"]
    like.save()
    re_imagined_user = dict(ReImaginedPost.objects.filter(id = like.post_id).first())
    Notification(owner_id= re_imagined_user["author_id"], notification_type= 'R_Like',
    message =f"{current_user['username']} just Liked you'r re-imagined post {re_imagined_user['title']}", 
    author= current_user['username']).save()
    return dict(like)


@router.get("/re_imagined/{post_id}", response_model=int)
def get_re_imagined_like(post_id: str,current_user: int = Depends(oauth2.get_current_user)):
    likes = Like.objects.filter(post_id= post_id)
    return likes.count()

@router.get("/{post_id}", response_model=int)
def get_post_like(post_id: str,current_user: int = Depends(oauth2.get_current_user)):
    likes = Like.objects.filter(post_id= post_id)
    return likes.count()

@router.delete("/re_imagined/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_re_imagined_like(post_id: str, current_user: int = Depends(oauth2.get_current_user)):
    query = Like.objects.filter(post_id = post_id).filter(liked_by= current_user["id"])
    if query.count() == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                detail=f'no post available.')
    query.delete()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_like(post_id: str, current_user: int = Depends(oauth2.get_current_user)):
    query = Like.objects.filter(post_id = post_id).filter(liked_by= current_user["id"])
    id =query.first()['id']
    if query.count() == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                detail=f'no post available.')
    query.filter(id= id).delete()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/liked/{post_id}", response_model= bool,status_code= status.HTTP_202_ACCEPTED)
def is_liked(post_id: str,current_user: int = Depends(oauth2.get_current_user)):
    like = Like.objects.filter(post_id = post_id).filter(liked_by = current_user["id"])
    if like.count() == 0:
        return False
    return True