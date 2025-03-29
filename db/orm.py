from sqlmodel import Session, create_engine
from db.models import SQLModel
from typing import Annotated
from config import settings

database_url = settings.DATABASE_URL
debug = settings.DEBUG 

connection_args = {"check_same_thread": False}

engine = create_engine(database_url, echo=debug, connect_args=connection_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


if __name__ == "__main__":
    create_db_and_tables()
    print("Database and tables created successfully.")
