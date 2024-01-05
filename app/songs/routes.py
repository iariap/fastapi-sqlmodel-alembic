from base.routers import GenericCrudRouter
from songs.models import Song, SongCreate, SongUpdate

router = GenericCrudRouter(Song, Song, SongUpdate, SongCreate)
