from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.songs.crud import song_crud
from tests.songs.factories import SongCreationFactory


@pytest.mark.asyncio
async def test_crud_create(db: AsyncSession):
    sond_data = SongCreationFactory.build()
    result = await song_crud.create(
        db,
        obj_in=sond_data.model_dump(),
    )
    assert result
    assert result.id


@pytest.mark.asyncio
async def test_crud_get_all_should_be_empty(db: AsyncSession):
    result = await song_crud.get_all(db)
    assert not result


@pytest.mark.asyncio
@patch("app.songs.crud.song_crud.get_all", AsyncMock(return_value="Hola"))
async def test():
    result = await song_crud.get_all(None)
    assert result == "Hola"
