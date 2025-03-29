from sqlmodel import Field, SQLModel
from datetime import datetime


class UserBase(SQLModel):
    username: str = Field(index=True)
    email: str = Field(index=True, unique=True)
    create_at: datetime = datetime.now()
    update_at: datetime = datetime.now()
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    is_verified: bool = Field(default=False)
    is_deleted: bool = Field(default=False)
    is_blocked: bool = Field(default=False)
    is_staff: bool = Field(default=False)
    is_anonymous: bool = Field(default=False)
    is_authenticated: bool = Field(default=False)
    is_okta: bool = Field(default=False)
    is_google: bool = Field(default=False)
    is_facebook: bool = Field(default=False)
    is_twitter: bool = Field(default=False)
    is_linkedin: bool = Field(default=False)
    is_github: bool = Field(default=False)
    is_microsoft: bool = Field(default=False)
    is_apple: bool = Field(default=False)
    is_amezone: bool = Field(default=False)
    is_azure: bool = Field(default=False)
    is_salesforce: bool = Field(default=False)
    is_slack: bool = Field(default=False)
    address: str | None = None
    phone: str | None = None
    age: int | None = None


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    hashed_password: str = Field(default=None)


class UserPublic(User):
    pass
