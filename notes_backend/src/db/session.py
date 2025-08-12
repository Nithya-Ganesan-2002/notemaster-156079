from functools import lru_cache
from typing import Generator

from sqlmodel import Session, SQLModel, create_engine

from src.core.config import get_settings


# PUBLIC_INTERFACE
@lru_cache(maxsize=1)
def get_engine():
    """Create and cache a SQLAlchemy engine using application settings."""
    settings = get_settings()
    uri = settings.sqlalchemy_uri()
    # Enable pre-ping to gracefully handle stale connections
    engine = create_engine(
        uri,
        echo=False,
        pool_pre_ping=True,
        pool_recycle=280,  # recycle before typical 300s idle timeout in some envs
    )
    return engine


# PUBLIC_INTERFACE
def get_session() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a SQLModel Session."""
    engine = get_engine()
    with Session(engine) as session:
        yield session


# PUBLIC_INTERFACE
def init_db() -> None:
    """Create database tables if they do not exist."""
    # Import models inside the function to avoid circular imports
    from src.models.note import Note  # noqa: F401  # Ensure model is registered

    engine = get_engine()
    SQLModel.metadata.create_all(engine)
