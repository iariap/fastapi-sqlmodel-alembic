import uuid

from app.songs.models import BandBase, SongBase


# band schemas
class BandCreate(BandBase):
    ...


class BandUpdate(BandBase):
    ...


class BandRead(BandBase):
    id: uuid.UUID


# song schemas
class SongRead(SongBase):
    band: BandRead


class SongCreate(SongBase):
    band_id: uuid.UUID


class SongUpdate(SongBase):
    ...
