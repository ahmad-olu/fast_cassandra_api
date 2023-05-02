from fastapi import Depends, status, HTTPException, APIRouter, Response
from random import randrange
from typing import List
from app import utils, oauth2
from app.models.reImagined import ReImaginedPost
from app.models.posts import Post
from app.models.notifications import Notification
from ..schemas import reImaginedSchemas
import global_mock

router = APIRouter(
    prefix="/re_imagined",
    tags=['reImagined']
)

@router.get("/",response_model=List[reImaginedSchemas.ReImagined])
def get_posts(current_user: int = Depends(oauth2.get_current_user)):
    posts = ReImaginedPost.objects.filter(author_id = current_user['id'])
    return list(posts)


@router.get("/all/{post_id}",response_model=List[reImaginedSchemas.ReImagined])
def get_all_posts(post_id: str,current_user: int = Depends(oauth2.get_current_user)):
    post = ReImaginedPost.objects.filter(post_id= post_id)
    return list(post)

@router.get("/{id}", response_model=reImaginedSchemas.ReImagined)
def get_post(id: str,current_user: int = Depends(oauth2.get_current_user)):
    post = ReImaginedPost.objects.filter(id= id)
    if post.count() == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'post {id} not found')
    return dict(post.first())

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=reImaginedSchemas.ReImagined)
def create_posts(posts: reImaginedSchemas.ReImaginedCreate,current_user: int = Depends(oauth2.get_current_user)):
    post = ReImaginedPost(**posts.dict())
    post.author_id = current_user['id']
    post.author_username = current_user['username']
    post.author_profile_image_url = current_user['profile_image_url']
    posts_user = dict(Post.objects.filter(id = post.post_id).first())
    Notification(owner_id= posts_user["author_id"], notification_type= 'ReImagined',
    message =f"{current_user['username']} just re-imagined on you'r post {posts_user['title']}", author= current_user['username']).save()
    post.save()
    return dict(post)

@router.put("/{id}", status_code=status.HTTP_201_CREATED, response_model=reImaginedSchemas.ReImagined)
def update_posts(id:str,post:reImaginedSchemas.ReImaginedCreate,current_user: int = Depends(oauth2.get_current_user)):
    query = ReImaginedPost.objects.filter(id= id).filter(author_id= current_user['id']).filter(post_id= post.post_id)
    if query.count() == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                detail=f'no post available.')
    post = reImaginedSchemas.ReImaginedUpdate(**post.dict())
    print(post)
    post = query.update(**post.dict())
    return Response(status_code=status.HTTP_201_CREATED)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: str, current_user: int = Depends(oauth2.get_current_user)):
    post = ReImaginedPost.objects.filter(author_id= current_user['id']).filter(id= id)
    if post.count() == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                detail=f'no post available.')
    post.delete()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
