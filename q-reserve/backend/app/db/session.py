from sqlmodel import SQLModel, create_engine, Session
from .init_db import init_db
from ..core.config import settings

engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,
    pool_recycle=300,
)


def get_session():
    """Get database session."""
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    """Create database tables."""
    SQLModel.metadata.create_all(engine)
    init_db()


def init():
    """Initialize database."""
    create_db_and_tables() 