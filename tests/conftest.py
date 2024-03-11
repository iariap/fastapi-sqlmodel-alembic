import pytest
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.base.db import get_session
from app.main import app

# Async engine for in-memory SQLite database
# db_url = "sqlite+aiosqlite:///:memory:"
# engine = create_async_engine(db_url, echo=True)

__config_path__ = "app/alembic.ini"
__migration_path__ = "app/migrations"

cfg = Config(__config_path__)
cfg.set_main_option("script_location", __migration_path__)


@pytest.fixture(scope="session")
async def sqlite_engine():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    try:
        yield engine
    finally:
        await engine.dispose()


@pytest.fixture(scope="function")
async def db(sqlite_engine):
    """
    Fixture that returns a SQLAlchemy session with a SAVEPOINT, and the rollback to it
    after the test completes.
    """
    connection = await sqlite_engine.connect()
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


@pytest.fixture(scope="function")
def api_client(db) -> TestClient:
    # replace the app dependency to get test database
    app.dependency_overrides[get_session] = lambda: db

    return TestClient(app)
