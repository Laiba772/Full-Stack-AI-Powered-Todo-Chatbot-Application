"""Database connection and session management."""
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from typing import AsyncGenerator, Optional
import logging
from contextlib import asynccontextmanager

from src.config import settings

logger = logging.getLogger(__name__)

# Global engine variable, initialized later
engine: Optional[AsyncEngine] = None


def get_engine() -> AsyncEngine:
    """Get the asynchronous database engine."""
    if engine is None:
        raise ValueError("Database engine has not been initialized. Call init_db() first.")
    return engine


def set_engine(new_engine: AsyncEngine) -> None:
    """Set the database engine. Useful for testing."""
    global engine
    engine = new_engine


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Get an asynchronous database session."""
    if engine is None:
        raise ValueError("Database engine has not been initialized. Call init_db() first.")
    async with AsyncSession(engine) as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


async def create_db_and_tables(current_engine: AsyncEngine) -> None:
    """Create all tables in the database asynchronously."""
    async with current_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    logger.info("Database tables created successfully")


from urllib.parse import urlparse, urlunparse, parse_qs, urlencode

# ... (existing imports)

def remove_unsupported_params(database_url: str) -> str:
    """Removes unsupported parameters like sslmode from the database URL."""
    parsed_url = urlparse(database_url)
    query_params = parse_qs(parsed_url.query)

    if 'sslmode' in query_params:
        del query_params['sslmode']
    if 'channel_binding' in query_params:
        del query_params['channel_binding']

    new_query = urlencode(query_params, doseq=True)
    new_url = urlunparse(parsed_url._replace(query=new_query))
    return new_url

# ... (rest of the file)


async def init_db() -> None:
    """Initialize the database asynchronously."""
    global engine
    if engine is None:
        processed_database_url = remove_unsupported_params(settings.database_url)
        engine = create_async_engine(
            processed_database_url,
            echo=settings.debug,
        )
    await create_db_and_tables(engine)
    logger.info("Database initialized")

