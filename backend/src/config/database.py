import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

database_url = os.environ["DATABASE_URL"]
engine = create_engine(database_url)

Base = declarative_base()
LocalSession = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, expire_on_commit=False
)


def create_tables():
    Base.metadata.create_all(engine)


session = None


@contextmanager
def get_session():
    """Provide a transactional scope around a series of operations."""
    global session
    if session is None:
        session = LocalSession()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
        session = None
