from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from config import DATABASE_URL

# Kept as an alias — migrations/env.py and other external readers import this
# name specifically.
SQLALCHEMY_DATABASE_URL = DATABASE_URL

if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    # SQLite requires this flag when the same connection is used across threads
    # (which happens because FastAPI runs sync endpoints in a thread pool)
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """FastAPI dependency: yields a session and closes it when the request ends."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
