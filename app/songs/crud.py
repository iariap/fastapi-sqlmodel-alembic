from base.crud import CRUDBase
from songs.models import Song, SongCreate, SongUpdate


class CRUDSong(CRUDBase[Song, SongCreate, SongUpdate]):
    ...


song_crud = CRUDSong(Song)
