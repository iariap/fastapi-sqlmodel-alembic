from app.base.crud import GenericCRUD
from app.songs.models import Band, Song
from app.songs.schemas import BandCreate, BandUpdate, SongCreate, SongUpdate


class CRUDSong(GenericCRUD[Song, SongCreate, SongUpdate]):
    ...


class CRUDBand(GenericCRUD[Band, BandCreate, BandUpdate]):
    ...


song_crud = CRUDSong(Song)
band_crud = CRUDBand(Band)
