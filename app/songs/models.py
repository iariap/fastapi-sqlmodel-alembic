from sqlmodel import Field, SQLModel
from typing import Optional

from base.models import TimestampModel, UUIDModel


class SongBase(SQLModel):
    name: str
    artist: str
    year: Optional[int] = None


class Song(SongBase, TimestampModel, UUIDModel, table=True):
    ...


class SongCreate(SongBase):
    pass


class SongUpdate(SongBase):
    pass
