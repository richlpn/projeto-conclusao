from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from src.config import get_settings

engine = create_engine(str(get_settings().database_url), pool_pre_ping=True)  # type: ignore

Base = declarative_base()


@lru_cache
def create_session():
    SessionLocal = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )

    return SessionLocal


def create_tables():
    Base.metadata.create_all(engine)
