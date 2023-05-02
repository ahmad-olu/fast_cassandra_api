from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.schemas import userSchemas
from .. import utils, oauth2
from app.models.users import User


router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model= userSchemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
    user = getUser(user_credentials.username)
    #user = dict(User.objects.filter(email=user_credentials.username).first())
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
            detail=f'Invalid Credentials')
    if not utils.verify(user_credentials.password, user['password']):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
            detail=f'Invalid Credentials')
    access_token = oauth2.create_access_token(data={"user_id": str(user["id"])})
    return {"access_token":access_token , "token_type": "bearer"}

def getUser(email: str):
    user = User.objects.filter(email= email)
    return dict(user.first())