from fastapi_pagination import LimitOffsetPage
from sqlmodel.ext.asyncio.session import AsyncSession

from songs.crud import song_crud
from songs.models import Song, SongCreate


async def create(session: AsyncSession, song: SongCreate) -> Song:
    return await song_crud.create(session, obj_in=song)


async def get(session: AsyncSession, song_id: int) -> Song:
    return await song_crud.get(session, song_id)


async def get_all(session: AsyncSession) -> LimitOffsetPage[Song]:
    return await song_crud.paginate(session)
