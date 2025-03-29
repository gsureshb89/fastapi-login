
from datetime import timedelta
from typing import Annotated
from fastapi import FastAPI, Depends, Form
from db.orm import get_session, create_db_and_tables, Session
from user.models import User, UserLogin, UserPublic
from user.utils import get_password_hash
from auth.auth import authenticate_user, create_access_token, get_current_active_user,\
    Token, ACCESS_TOKEN_EXPIRE_MINUTES
from db.models import User as DBUser
from config import settings


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/register/user")
def register_user(user: User = Form(...), session: Session = Depends(get_session)) -> UserPublic:
    try:
        hashed_password = get_password_hash(user.hashed_password)
        user_obj = DBUser(**user.dict())
        user_obj.hashed_password = hashed_password
        session.add(user_obj)
        session.commit()
        session.refresh(user_obj)
        return user_obj
    except Exception as e:
        raise e
    finally:
        session.close()


@app.post("/basic/auth")
def basic_login(user: UserLogin, session: Session = Depends(get_session)):
    try:
        user = authenticate_user(user, session)
        if not user:
            return {"Status_code": 400, "detail":"Incorrect password"}
        return {'message': 'Login successful'}
    except Exception as e:
        raise e
    finally:
        session.close()


@app.post("/token")
async def login_for_access_token(form_data: Annotated[UserLogin, Depends()],
                                 session: Session = Depends(get_session)):
    try:
        user = authenticate_user(form_data, session)
        if not user:
            return {'status_code': 400, 'detail': "Incorrect username or password"}
        access_token_expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expire)
        return Token(access_token=access_token, token_type="bearer")
    except Exception as e:
        raise e
    finally:
        session.close()


@app.get("/current/user")
async def read_users_me(session: Annotated[User, Depends(get_current_active_user)]) -> UserPublic:
    return session


@app.get("/")
def root(session: Annotated[User, Depends(get_current_active_user)]):
    return {"settings": settings.dict()}
