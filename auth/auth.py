import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status, Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from db.orm import get_session, Session
from pydantic import BaseModel
from user.utils import verify_password
from user.models import UserLogin, User
from db.models import User as DBUser
from config import settings


SECRET_KEY = settings.SECRET_KEY
ALGOTITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

oauth2_scheme =  OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token : str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None


def get_user(username: str, session: Session):
    try:
        user_obj = session.query(DBUser).filter(DBUser.username == username).first()
        return user_obj
    except Exception as e:
        raise e


def authenticate_user(user: UserLogin, session: Session) -> UserLogin:
    try:
        user_obj = get_user(user.username, session)
        if not user_obj:
            return False
        if not verify_password(user.hashed_password, user_obj.hashed_password):
            return False
        return user
    except Exception as e:
        raise e


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGOTITHM)
    return encode_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           session: Session = Depends(get_session)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid authentication credentials',
                            headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGOTITHM])
        username = payload.get('sub')
        if username is None:
            raise credential_exception
        token_data = TokenData(username=username)
        user = get_user(username=token_data.username, session=session)
        if user is None:
            raise credential_exception
        return user
    except InvalidTokenError:
        raise credential_exception
    finally:
        session.close()


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail='Inactive user')
    return current_user
