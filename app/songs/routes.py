from app.base.routers import GenericCrudRouter
from app.songs.models import Song
from app.songs.schemas import SongCreate, SongRead, SongUpdate

router = GenericCrudRouter(Song, SongRead, SongUpdate, SongCreate)
