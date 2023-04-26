from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from .schema import TokenData
from .config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE = settings.access_token_expire_minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'login')

def encode_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE)
    to_encode.update({'exp':expire})

    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return access_token

def verify_token(token:str, credential_exception):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = data.get('user_id')
        if id is None:
            raise 
        token_data = TokenData(id = id)
    except JWTError:
        raise credential_exception
    
    return token_data
    
def get_current_user(token:str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(
        status_code = status.HTTP_403_FORBIDDEN,
        detail="not authenticated",
        headers = {'WWW-Authenticate': 'Bearer'}
    )

    return verify_token(token, credential_exception)