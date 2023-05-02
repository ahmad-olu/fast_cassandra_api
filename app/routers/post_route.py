from typing import List
from fastapi import Request, Response, status, HTTPException, APIRouter, Depends
from random import randrange
from app import utils, oauth2
from ..schemas import postSchemas
from app.models.posts import Post
from app.models.follows import Follower

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/",response_model=List[postSchemas.Post])
def get_posts(current_user: int = Depends(oauth2.get_current_user)):
    posts = Post.objects.filter(author_id= current_user['id'])
    return list(posts)

@router.get("/user_feed",response_model=List[postSchemas.Post])
#def get_user_feed(limit: int , start_from: int, current_user: int = Depends(oauth2.get_current_user)):
def get_user_feed(current_user: int = Depends(oauth2.get_current_user)):
    user_list = [x['followers'] for x in Follower.objects.filter(user_id= current_user['id'])]
    posts = Post.objects.filter(author_id__in=user_list)
    return list(posts)

# @router.get("/all",response_model=List[postSchemas.Post])
# def get_all_posts(current_user: int = Depends(oauth2.get_current_user)):
#     #todo!: get the list of post 
#     #global_mock.my_post
#     return global_mock.my_post

@router.get("/{id}", response_model=postSchemas.Post)
def get_post(id: str,current_user: int = Depends(oauth2.get_current_user)):
    post = Post.objects.filter(id= id)
    if post.count() == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'post {id} not found')
    return dict(post.first())

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=postSchemas.Post)
def create_posts(new_post: postSchemas.PostCreate,request: Request,current_user: int = Depends(oauth2.get_current_user)):
    post = Post(**new_post.dict())
    post.author_id = current_user['id']
    post.url_path = f'{request.url.path}/{post.id}'
    post.author_username = current_user['username']
    post.author_profile_image_url = current_user['profile_image_url']
    post.save()
    return dict(post)

@router.put("/{id}", status_code=status.HTTP_201_CREATED, response_model=postSchemas.Post)
def update_posts(id:str, u_post:postSchemas.PostCreate,current_user: int = Depends(oauth2.get_current_user)):
    q_post = Post.objects.filter(id= id).filter(author_id = current_user['id'])
    if q_post.count() == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                detail=f'no post available.')
    q_post.update(**u_post.dict())
    return Response(status_code=status.HTTP_201_CREATED)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: str, current_user: int = Depends(oauth2.get_current_user)):
    q_post = Post.objects.filter(author_id= current_user['id']).filter(id= id)
    if q_post.count() == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                detail=f'no post available.')
    q_post.delete()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
