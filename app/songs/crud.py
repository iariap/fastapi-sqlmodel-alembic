from base.crud import GenericCRUD
from songs.models import Song, SongCreate, SongUpdate


class CRUDSong(GenericCRUD[Song, SongCreate, SongUpdate]):
    ...


song_crud = CRUDSong(Song)
