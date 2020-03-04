import maya
from graphql import GraphQLError
from py2neo import Graph
from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom, Related

from source import settings


graph = Graph(
    host=settings.NEO4J_HOST,
    port=settings.NEO4J_PORT,
    user=settings.NEO4J_USER,
    password=settings.NEO4J_PASSWORD,
)


class BaseModel(GraphObject):
    """
    Implements some basic functions to guarantee some standard functionality
    across all models. The main purpose here is also to compensate for some
    missing basic features that we expected from GraphObjects, and improve the
    way we interact with them.
    """

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    @classmethod
    def all(cls):
        return cls.match(graph)

    @classmethod
    def fetch(cls, _id = None):
        obj = cls.match(graph, _id).first
        if obj is None:
            raise GraphQLError(f'"{_id}" has not been found')
        return obj

    def save(self):
        graph.push(self)


class User(BaseModel):
    __primarykey__ = 'username'

    username = Property()
    password = Property()

    friends = Related('User', 'FRIENDS')
    playlists = RelatedTo('Playlist', 'CREATED')

    collectives = RelatedTo('Collective', 'LISTENS')
    composers = RelatedTo('Composer', 'LISTENS')
    performers = RelatedTo('Performer', 'LISTENS')
    releases = RelatedTo('Release', 'LISTENS')

    def as_dict(self):
        return {
            'username': self.username,
        }


class Playlist(BaseModel):
    name = Property()

    creators = RelatedFrom('User', 'CREATED')

    tracks = RelatedTo('Track', 'INCLUDES')

    def as_dict(self):
        return {
            '_id': self.__primaryvalue__,
            'name': self.name,
            'tracks': [track.as_dict() for track in self.tracks],
        }


class Genre(BaseModel):
    name = Property()

    ancestors = RelatedFrom('Genre', 'COMES_FROM')
    descendants = RelatedTo('Genre', 'INFLUENCED_ON')

    compositions = RelatedFrom('Composition', 'BELONGS_TO')
    releases = RelatedFrom('Release', 'BELONGS_TO')
    cycles = RelatedFrom('Cycle', 'BELONGS_TO')

    epoches = RelatedTo('Epoch', 'BELONGS_TO')

    def as_dict(self):
        return {
            '_id': self.__primaryvalue__,
            'name': self.name,
        }


class Epoch(BaseModel):
    name = Property()
    started = Property()
    ended = Property()

    ancestors = RelatedFrom('Epoch', 'COMES_FROM')
    descendants = RelatedTo('Epoch', 'INFLUENCED_ON')

    genres = RelatedFrom('Genre', 'BELONGS_TO')

    def as_dict(self):
        return {
            '_id': self.__primaryvalue__,
            'name': self.name,
            'started': self.started,
            'ended': self.ended,
        }


class Label(BaseModel):
    name = Property()

    tracks = RelatedTo('Track', 'RECORDED')
    releases = RelatedTo('Release', 'RECORDED')

    def as_dict(self):
        return {
            '_id': self.__primaryvalue__,
            'name': self.name,
        }


class Collective(BaseModel):
    name = Property()
    formed = Property()
    disbanded = Property()

    listeners = RelatedFrom('User', 'LISTENS')
    performers = RelatedFrom('Person', 'PLAYED_IN')

    tracks = RelatedTo('Track', 'RECORDED')
    releases = RelatedTo('Release', 'RECORDED')

    def as_dict(self):
        return {
            '_id': self.__primaryvalue__,
            'name': self.name,
        }


class Person(BaseModel):
    performer = Label('Performer')
    composer = Label('Composer')

    name = Property()
    born = Property()
    died = Property()

    collaborators = Related('Person', 'COLLABORATED_WITH')

    compositions = RelatedTo('Composition', 'COMPOSED')
    cycles = RelatedTo('Cycle', 'COMPOSED')

    tracks = RelatedTo('Track', 'RECORDED')
    releases = RelatedTo('Release', 'RECORDED')

    def as_dict(self):
        return {
            '_id': self.__primaryvalue__,
            'name': self.name,
            'born': self.born,
            'died': self.died,
        }


class Release(BaseModel):
    aggregator = Label('Aggregator')
    releases = RelatedTo('Release', 'AGGREGATES')

    albumn = Label('Albumn')
    ep = Label('EP')
    single = Label('Single')
    live = Label('Live')
    compillation = Label('Compillation')

    name = Property()
    year = Property()

    listeners = RelatedFrom('User', 'LISTENS')
    label = RelatedFrom('Label', 'RECORDED')
    performers = RelatedFrom('Person', 'RECORDED')
    collectives = RelatedFrom('Collective', 'RECORDED')

    genres = RelatedTo('Genre', 'BELONGS_TO')
    compositions = RelatedTo('Composition', 'INCLUDES')
    tracks = RelatedTo('Track', 'INCLUDES')

    def as_dict(self):
        return {
            '_id': self.__primaryvalue__,
            'name': self.name,
            'year': self.year,
        }


class Cycle(BaseModel):
    name = Property()
    started = Property()
    finished = Property()

    composers = RelatedFrom('Composer', 'COMPOSED')

    genres = RelatedTo('Genre', 'BELONGS_TO')
    compositions = RelatedTo('Composition', 'INCLUDES')

    def as_dict(self):
        return {
            '_id': self.__primaryvalue__,
            'name': self.name,
            'started': self.started,
            'finished': self.finished,
        }


class Composition(BaseModel):
    aggregator = Label('Aggregator')
    compositions = RelatedTo('Composition', 'AGGREGATES')

    name = Property()
    started = Property()
    finished = Property()

    cycle = RelatedFrom('Cycle', 'INCLUDES')
    composers = RelatedFrom('Person', 'COMPOSED')
    listeners = RelatedFrom('User', 'LISTENS')

    genres = RelatedTo('Genre', 'BELONGS_TO')
    tracks = RelatedTo('Track', 'RECORDED')

    def as_dict(self):
        return {
            '_id': self.__primaryvalue__,
            'name': self.name,
            'started': self.started,
            'finished': self.finished,
        }


class Track(BaseModel):
    aggregator = Label('Aggregator')
    tracks = RelatedTo('Track', 'AGGREGATES')

    name = Property()
    year = Property()

    playlist = RelatedFrom('Playlist', 'INCLUDES')
    label = RelatedFrom('Label', 'RECORDED')
    performers = RelatedFrom('Person', 'RECORDED')
    collectives = RelatedFrom('Collective', 'RECORDED')
    composition = RelatedFrom('Composition', 'RECORDED')

    def as_dict(self):
        return {
            '_id': self.__primaryvalue__,
            'name': self.name,
            'year': self.year,
        }
