import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Set DATABASE_URL (e.g. postgresql+psycopg://user:pass@host:5432/dbname) to use
# PostgreSQL. Falls back to the local SQLite file only if it's not set.
DB_PATH = Path(__file__).parent / "tariff.db"
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DB_PATH}")

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
