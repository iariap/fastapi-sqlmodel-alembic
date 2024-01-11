from sqlmodel import SQLModel

from app.base.models import SoftDeleteModel, TimestampModel, UUIDModel


class SongBase(SQLModel):
    name: str
    artist: str
    year: int | None = None


class Song(SongBase, TimestampModel, UUIDModel, SoftDeleteModel, table=True):
    ...


class SongCreate(SongBase):
    pass


class SongUpdate(SongBase):
    pass
