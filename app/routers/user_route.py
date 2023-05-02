from fastapi import Depends, status, HTTPException, APIRouter, Response, Request
from random import randrange
from typing import List
from app import utils, oauth2
from app.schemas import userSchemas, userActivitySchemas
from app.models.users import User, UserFollow
from app.models.posts import Post
from app.models.comment import Comment
from app.models.reImagined import ReImaginedPost
from app.models.follows import Follower, Following
from app.models.notifications import Notification

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=userSchemas.UserOut)
def create_user(user: userSchemas.UserCreate):
    #hash the password => user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = User.create_user(**user.dict())
    UserFollow(user_id = new_user.id).save()
    return dict(new_user)

@router.put("/", status_code=status.HTTP_201_CREATED, response_model=userSchemas.UserOut)
def update_user(users: userSchemas.UserUpdate, current_user: int = Depends(oauth2.get_current_user)):
    user = User.objects.filter(id= current_user['id']).update(**users.dict())
    post_id = [x['id'] for x in  Post.objects.filter(author_id= current_user['id'])]
    Post.objects.filter(author_id= current_user['id']).filter(id__in = post_id).update(author_username = users.username, author_profile_image_url = users.profile_image_url)
    # comment_id = [x['id'] for x in  Comment.objects.filter(author_id= current_user['id'])]
    # Comment.objects.filter(author_id= current_user['id']).filter(id__in = comment_id).update(author_username = users.username)
    # reImagined_id = [x['id'] for x in  ReImaginedPost.objects.filter(author_id= current_user['id'])]
    # ReImaginedPost.objects.filter(author_id= current_user['id']).filter(id__in = reImagined_id).update(author_username = users.username)
    return Response(content='Updated...')

@router.get("/",response_model=userSchemas.UserOut)
def get_user(current_user: int = Depends(oauth2.get_current_user)):
    user = User.objects.filter(id= current_user['id'])
    if user.count() == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'no Account available with the provided access.')
    return dict(user.first())

@router.get("/username/{name}", response_model= bool,status_code= status.HTTP_202_ACCEPTED)
def available_username(name: str):
    q_username = User.objects.filter(username= name)
    if q_username.count() == 0:
        return False
    return True

@router.patch("/update_username", status_code=status.HTTP_201_CREATED, response_model=userSchemas.UserOut)
def update_username(username: str, current_user: int = Depends(oauth2.get_current_user)):
    q_username = User.objects.filter(username= username)
    if q_username.count() != 0:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
            detail=f'username already has an account.')
    user = User.objects.filter(id= current_user['id']).update(username = username)
    post_id = [x['id'] for x in  Post.objects.filter(author_id= current_user['id'])]
    Post.objects.filter(author_id= current_user['id']).filter(id__in = post_id).update(author_username = user.username)
    # comment_id = [x['id'] for x in  Comment.objects.filter(author_id= current_user['id'])]
    # Comment.objects.filter(author_id= current_user['id']).filter(id__in = comment_id).update(author_username = user.username)
    # reImagined_id = [x['id'] for x in  ReImaginedPost.objects.filter(author_id= current_user['id'])]
    # ReImaginedPost.objects.filter(author_id= current_user['id']).filter(id__in = reImagined_id).update(author_username = user.username)
    return Response(content='Updated...')

@router.patch("/update_email", status_code=status.HTTP_201_CREATED, response_model=userSchemas.UserOut)
def update_email(email: str, current_user: int = Depends(oauth2.get_current_user)):
    q_email = User.objects.filter(email= email)
    if q_email.count() != 0:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
            detail=f'email already has an account.')
    user = User.objects.filter(id= current_user['id']).update(email = email)
    return dict(user)

@router.patch("/update_password", status_code=status.HTTP_201_CREATED, response_model=userSchemas.UserOut)
def update_password(password: str, current_user: int = Depends(oauth2.get_current_user)):
    hashed_password = utils.hash(password)
    user = User.objects.filter(id= current_user['id']).update(password = hashed_password)
    return dict(user)

@router.post("/follow", status_code=status.HTTP_201_CREATED, response_model=userSchemas.UserOut)
def follow_user(following_id: userActivitySchemas.FollowCreate, current_user: int = Depends(oauth2.get_current_user)):
    follow = UserFollow.objects.filter(user_id= current_user['id'])
    if follow.count() == 0:
        return Response(status_code= status.HTTP_404_NOT_FOUND)
    Following(user_id = current_user['id'],following= following_id.follower).save()
    Follower(followers= following_id.follower, user_id= current_user['id']).save()
    follow.update(following = 1,followers = 1)
    Notification(owner_id= following_id.follower, notification_type= 'Follow',author= current_user['username']).save()
    return current_user

@router.delete("/un_follow", status_code=status.HTTP_201_CREATED, response_model=userSchemas.UserOut)
def un_follow_user(un_follow_user_id: userActivitySchemas.FollowCreate, current_user: int = Depends(oauth2.get_current_user)):
    Following(user_id = current_user['id'],following= un_follow_user_id.follower).delete()
    Follower(followers= un_follow_user_id.follower, user_id= current_user['id']).delete()
    UserFollow.objects.filter(user_id= current_user['id']).update(following = -1, followers = -1)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/is_following/{other_user_id}", status_code=status.HTTP_201_CREATED, response_model=bool)
def is_following_user(other_user_id: str, current_user: int = Depends(oauth2.get_current_user)):
    following = Following.objects.filter(user_id = current_user['id']).filter(following= other_user_id)
    if following.count() == 0:
        return False
    return True