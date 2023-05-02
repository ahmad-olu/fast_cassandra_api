import uuid
from fastapi import status, HTTPException
from datetime import datetime
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


from .. import validators


class User(Model):
    __keyspace__ = "geat_dev"
    id = columns.UUID(primary_key= True, default=uuid.uuid1)
    email = columns.Text(index = True, required= True)
    username = columns.Text(index = True, required= True)
    password = columns.Text(required= True)
    fullname = columns.Text()
    website = columns.Text()
    email_verified = columns.Boolean(default=False)
    has_payment_account = columns.Boolean(default=False)
    profile_image_url = columns.Text()
    background_image_url = columns.Text()
    bio = columns.Text()
    created_at = columns.DateTime(default= datetime.now())

    @staticmethod
    def create_user(email,username,fullname, website, bio, profile_image_url, password =None):
        q_email = User.objects.filter(email=email)
        if q_email.count() != 0:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
            detail=f'User already has an account.')
        q_username = User.objects.filter(username= username)
        if q_username.count() != 0:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
            detail=f'User already has an account.')
        valid,msg, email = validators._validate_email(email)
        if not valid:
            raise Exception(f"Invalid email: {msg}")
        obj = User(email=email,username= username, fullname= fullname, website= website,
        bio= bio, profile_image_url= profile_image_url)
        obj.password = password
        obj.save()
        return obj

class UserFollow(Model):
    __keyspace__ = "geat_dev"
    user_id = columns.UUID(primary_key= True)
    id = columns.UUID(primary_key= True, default=uuid.uuid1)
    following = columns.Counter()
    followers = columns.Counter()