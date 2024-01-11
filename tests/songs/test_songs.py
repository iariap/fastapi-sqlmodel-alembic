from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.songs.crud import song_crud
from tests.songs.factories import SongCreationFactory


@pytest.mark.asyncio
async def test_crud_create(db: AsyncSession):
    song_data = SongCreationFactory.build()
    result = await song_crud.create(
        db,
        obj_in=song_data.model_dump(),
    )
    assert result
    assert result.id


@pytest.mark.asyncio
async def test_crud_get_all_should_be_empty(db: AsyncSession):
    result = await song_crud.get_all(db)
    assert not result


@pytest.mark.asyncio
async def test_crud_get_all_filtering_deleted(db: AsyncSession):
    songs_data = SongCreationFactory.batch(5)
    last_song = None
    for song_data in songs_data:
        last_song = await song_crud.create(
            db,
            obj_in=song_data.model_dump(),
        )
    songs = await song_crud.get_all(db)
    assert len(songs) == 5

    await song_crud.remove(db, id=last_song.id)

    songs = await song_crud.get_all(db)
    assert len(songs) == 4


@pytest.mark.asyncio
@patch("app.songs.crud.song_crud.get_all", AsyncMock(return_value="Hola"))
async def test():
    result = await song_crud.get_all(None)
    assert result == "Hola"
