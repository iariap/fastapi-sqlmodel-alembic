import pytest
from alembic.config import Config
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

# Async engine for in-memory SQLite database
# db_url = "sqlite+aiosqlite:///:memory:"
# engine = create_async_engine(db_url, echo=True)

__config_path__ = "app/alembic.ini"
__migration_path__ = "app/migrations"

cfg = Config(__config_path__)
cfg.set_main_option("script_location", __migration_path__)


# https://github.com/igortg/pytest-async-sqlalchemy/blob/master/pytest_async_sqlalchemy.py
@pytest.fixture(scope="function")
async def sqla_engine():
    engine = create_async_engine(
        "postgresql+asyncpg://postgres:postgres@db:5432/fanspark"
    )
    try:
        yield engine
    finally:
        await engine.dispose()


@pytest.fixture(scope="function")
async def db(sqla_engine):
    """
    Fixture that returns a SQLAlchemy session with a SAVEPOINT, and the rollback to it
    after the test completes.
    """
    connection = await sqla_engine.connect()
    trans = await connection.begin()

    Session: AsyncSession = sessionmaker(
        connection, expire_on_commit=False, class_=AsyncSession
    )
    session = Session()

    try:
        yield session
    finally:
        await session.close()
        await trans.rollback()
        await connection.close()
