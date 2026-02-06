"""Alembic environment configuration."""
import os
import sys
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from logging.config import fileConfig
from alembic import context
from sqlmodel import SQLModel
# from sqlalchemy import create_engine, pool

# Add backend to sys.path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, backend_path)

from src.config import settings
from src.models.task import Task
from src.models.user import User
from src.models.conversation import Conversation
from src.models.message import Message
from src.models.tool_invocation import ToolInvocation

# Alembic Config object
config = context.config

# Configure logging
fileConfig(config.config_file_name)

# Metadata for autogenerate
target_metadata = SQLModel.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=settings.database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(conn):
    context.configure(connection=conn, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

import re
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode

# ... (existing imports)

def remove_unsupported_params(database_url: str) -> str:
    """Removes unsupported parameters like sslmode and channel_binding from the database URL."""
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


async def run_migrations_online():
    """Run migrations in 'online' mode."""
    print(f"Alembic DATABASE_URL: {settings.database_url}")

    processed_database_url = remove_unsupported_params(settings.database_url)

    connectable = create_async_engine(
        processed_database_url,
        # poolclass=pool.NullPool, # Not needed for async_engine
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
