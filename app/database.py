"""
This file sets up the connection to our database.
We're using SQLite for now because it needs zero setup (just a file on disk).
Later, switching to PostgreSQL only means changing DATABASE_URL.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# The database will be a single file called library.db in this folder
DATABASE_URL = "sqlite:///./library.db"

# The engine is what actually talks to the database
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # needed only for SQLite
)

# SessionLocal is a factory for creating database "sessions" (conversations with the DB)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is what our model classes (in models/) will inherit from
Base = declarative_base()


def get_db():
    """
    This function gives each request its own database session,
    and makes sure it's closed afterwards. FastAPI will call this
    automatically wherever we use Depends(get_db).
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()