import os
from contextlib import contextmanager
from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from src.config import get_settings

engine = create_engine(get_settings().database_url, pool_pre_ping=True)  # type: ignore

Base = declarative_base()


@lru_cache
def create_session() -> scoped_session:
    Session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )
    return Session


def create_tables():
    Base.metadata.create_all(engine)


@contextmanager
def get_session():
    """Provide a transactional scope around a series of operations."""
    session = create_session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
        session = None
