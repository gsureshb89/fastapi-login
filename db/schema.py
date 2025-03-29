from typing import Annotated
from fastapi import Depends
from sqlmodel import Field, SQLModel, create_engine, Session, select

# class Hero(SQLModel, table=True):
#     id: Annotated[int, Field(primary_key=True)]
#     name: str
#     secret_name: str
#     age: int

class User(SQLModel, table=True):
    id: Annotated[int, Field(primary_key=True)]
    username: str
    email: str
    full_name: str
    disabled: bool
    hashed_password: str


sqlite_url = "sqlite:///database.db"

connection_args = {"check_same_thread": False}

engine = create_engine(sqlite_url, echo=True, connect_args=connection_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

