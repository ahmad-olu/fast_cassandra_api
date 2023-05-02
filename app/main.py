from typing import List
from uuid import UUID
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from cassandra.cqlengine.management import sync_table , drop_table
from cassandra.cqlengine.query import BatchQuery
from app.models import (reImagined, users,posts, comment, follows, like, feedback)
from app.routers import (
    auth_route, comment_route, likes_route, notification_route, 
    post_route, reImagined_post_route, search_route, user_route,
    image_upload_route, feedback_route)

from . import ( config, db)

settings = config.get_settings()

app = FastAPI()

session = None

#Todo?? ==> make sure users dont have two models like, followers and following for a single post or user model

#todo?? ===> when user changes profileimage make sure to delete the old one and user it userid for the new image

@app.on_event("startup")
def on_startup():
    global session
    session = db.get_session()
    sync_table(users.User)
    sync_table(users.UserFollow)
    #drop_table(comment.Comment)
    sync_table(posts.Post)
    sync_table(reImagined.ReImaginedPost)
    sync_table(comment.Comment)
    sync_table(follows.Following)
    sync_table(follows.Follower)
    sync_table(like.Like)
    sync_table(feedback.Feedback)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials= True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post_route.router)
app.include_router(user_route.router)
app.include_router(auth_route.router)
app.include_router(comment_route.router)
app.include_router(likes_route.router)
app.include_router(notification_route.router)
app.include_router(reImagined_post_route.router)
app.include_router(search_route.router)
app.include_router(image_upload_route.router)
app.include_router(feedback_route.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/u}")
def u(request: Request):
    return {"data":request.url.path}

@app.get("/u_all")
def u_all():
    # b = BatchQuery()
    # users.User.batch(b).create(email= "a1@gmail.com", username= "al", password='password1234')
    # users.User.batch(b).create(email= "a2@gmail.com", username= "a2", password='password1234')
    # users.User.batch(b).create(email= "a3@gmail.com", username= "a3", password='password1234')
    # users.User.batch(b).create(email= "a4@gmail.com", username= "a4", password='password1234')
    # b.execute()

    # u = users.User.objects.all()

    # b = BatchQuery()
    # posts.Post.batch(b).create(author_id= UUID("e96a0ed0-9faf-11ed-a7a0-dc53608776b5"), author_username = "a1", title = "abacus" , content = "bye bye")
    # posts.Post.batch(b).create(author_id= UUID("e96a0ed0-9faf-11ed-a7a0-dc53608776b5"), author_username = "a1", title = "babylon", content = "bye bye")
    # posts.Post.batch(b).create(author_id= UUID("e96a0ed0-9faf-11ed-a7a0-dc53608776b5"), author_username = "a1", title = "cactus" , content = "bye bye")
    # posts.Post.batch(b).create(author_id= UUID("e96a0ed0-9faf-11ed-a7a0-dc53608776b5"), author_username = "a1", title = "moldova", content = "bye bye")
    # b.execute()

    p = posts.Post.objects.all()

    # "author_id": "598c5742-9f51-11ed-b504-dc53608776b5",
    #         "id": "8712fd9a-9f53-11ed-92b8-dc53608776b5",

    
    # post_id = [x['id'] for x in  posts.Post.objects.filter(author_id= 'e96a0ed0-9faf-11ed-a7a0-dc53608776b5')]
    # posts.Post.objects.filter(author_id= 'e96a0ed0-9faf-11ed-a7a0-dc53608776b5').filter(id__in = post_id).update(author_username = 'alphonzo')
    # p = posts.Post.objects.all()
    return {'status': list(p)}