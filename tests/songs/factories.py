from polyfactory.factories.pydantic_factory import ModelFactory

from app.songs.schemas import BandCreate, SongCreate


class SongCreationFactory(ModelFactory[SongCreate]):
    __model__ = SongCreate


class BandCreationFactory(ModelFactory[BandCreate]):
    __model__ = BandCreate
