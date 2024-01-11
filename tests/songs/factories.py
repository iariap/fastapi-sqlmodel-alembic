from polyfactory.factories.pydantic_factory import ModelFactory

from app.songs.models import SongCreate


class SongCreationFactory(ModelFactory[SongCreate]):
    __model__ = SongCreate
