import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.songs.crud import band_crud, song_crud
from tests.songs.factories import BandCreationFactory, SongCreationFactory


@pytest.fixture(scope="function")
@pytest.mark.asyncio
async def beatles_song(db: AsyncSession):
    the_beatles_data = BandCreationFactory.build(name="The Beatles")
    the_beatles = await band_crud.create(db, obj_in=the_beatles_data.model_dump())
    song_data = SongCreationFactory.build(band_id=the_beatles.id)
    song = await song_crud.create(
        db,
        obj_in=song_data.model_dump(),
    )
    return song
