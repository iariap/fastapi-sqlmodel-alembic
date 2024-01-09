from app.base.crud import GenericCRUD
from app.songs.models import Song, SongCreate, SongUpdate


class CRUDSong(GenericCRUD[Song, SongCreate, SongUpdate]):
    ...


song_crud = CRUDSong(Song)
