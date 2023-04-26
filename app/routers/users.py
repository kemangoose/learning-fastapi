from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from ..schema import UserIn
from ..utils import hash_password, verify_password
from .. import models, oauth2, schema

router = APIRouter(tags = ['Users'], prefix = '/users')

@router.post('/register', status_code = status.HTTP_201_CREATED)
async def create_user(user: UserIn, db:Session = Depends(get_db)):
    user_exists = db.query(models.User).filter(models.User.email == user.email).first()

    if user_exists is not None:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = f'{user.email} already exists')
    hashed_password = hash_password(user.password)
    user.password = hashed_password
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()

    return {'message':'user created successfully'}

@router.post('/login', status_code = status.HTTP_200_OK, response_model = schema.Token)
async def login(user:UserIn, db:Session = Depends(get_db)):
    user_in = db.query(models.User).filter(models.User.email == user.email).first()
    
    if user_in is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'user is not found')
    
    if not verify_password(user.password, user_in.password):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail= 'not authenticated')

    access_token = oauth2.encode_token(data={'user_id': user_in.id}) 

    return {'access_token':access_token, 'token_type':'bearer'}