from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

database_url = os.environ["DATABASE_URL"]
engine = create_engine(database_url)

Base = declarative_base()
LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    Base.metadata.create_all(engine)


def get_session():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()
