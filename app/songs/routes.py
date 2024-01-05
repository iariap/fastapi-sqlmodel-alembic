from app.base.routers import GenericCrudRouter
from app.songs.models import Song, SongCreate, SongUpdate

router = GenericCrudRouter(Song, Song, SongUpdate, SongCreate)
