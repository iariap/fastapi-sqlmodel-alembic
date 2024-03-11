import uuid

from sqlmodel import Field, Relationship, SQLModel

from app.base.models import SoftDeleteModel, TimestampModel, UUIDModel


# Band models
class BandBase(SQLModel):
    name: str


class Band(BandBase, TimestampModel, UUIDModel, SoftDeleteModel, table=True):
    songs: list["Song"] = Relationship(back_populates="band")


# Song models
class SongBase(SQLModel):
    name: str
    artist: str
    year: int | None = None


class Song(SongBase, TimestampModel, UUIDModel, SoftDeleteModel, table=True):
    band_id: uuid.UUID = Field(foreign_key="band.id")
    band: Band = Relationship(back_populates="songs")
