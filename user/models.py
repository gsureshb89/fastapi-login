from pydantic import BaseModel


class BaseUser(BaseModel):
    username: str
    email: str
    is_active: bool = True

class User(BaseUser):
    hashed_password: str = None

class UserPublic(BaseUser):
    pass

class UserLogin(BaseModel):
    username: str
    hashed_password: str
