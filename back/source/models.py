import maya
from graphql import GraphQLError
from py2neo import Graph
from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom, Related, Label

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
        obj = cls.match(graph, _id).first()
        if obj is None:
            raise GraphQLError(f'"{_id}" has not been found')
        return obj

    def save(self):
        graph.push(self)


class User(BaseModel):
    __primarykey__ = 'username'

    username = Property()
    password = Property()

    email = Property()

    friends = Related('User', 'FRIENDS')
    playlists = RelatedTo('Playlist', 'CREATED')

    artists = RelatedTo('Artist', 'LISTENS')
    releases = RelatedTo('Release', 'LISTENS')

    def as_dict(self):
        return {
            'username': self.username,
            'email': self.email,
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


class Artist(BaseModel):
    collective = Label('Collective')
    performer = Label('Performer')
    composer = Label('Composer')

    name = Property()
    born = Property()
    died = Property()

    related = Related('Artist', 'RELATED_WITH')  # Member, OriginalMember, Tribute, Collaborator, etc

    listeners = RelatedFrom('User', 'LISTENS')

    compositions = RelatedTo('Composition', 'COMPOSED')
    tracks = RelatedTo('Track', 'RECORDED')
    releases = RelatedTo('Release', 'RECORDED')

    def as_dict(self):
        return {
            '_id': self.__primaryvalue__,
            'name': self.name,
            'born': self.born,
            'died': self.died,
        }


class Composition(BaseModel):
    aggregator = Label('Aggregator')
    items = RelatedTo('Composition', 'AGGREGATES')

    name = Property()
    started = Property()
    finished = Property()

    composers = RelatedFrom('Composer', 'COMPOSED')
    listeners = RelatedFrom('User', 'LISTENS')

    genres = RelatedTo('Genre', 'BELONGS_TO')
    tracks = RelatedTo('Track', 'RECORDED_ON')

    def as_dict(self):
        return {
            '_id': self.__primaryvalue__,
            'name': self.name,
            'started': self.started,
            'finished': self.finished,
        }


class Release(BaseModel):
    aggregator = Label('Aggregator')
    items = RelatedTo('Release', 'AGGREGATES')

    albumn = Label('Albumn')
    ep = Label('EP')
    single = Label('Single')
    live = Label('Live')
    compilation = Label('Compilation')

    name = Property()
    date = Property()
    label = Property()

    listeners = RelatedFrom('User', 'LISTENS')

    tracks = RelatedTo('Track', 'INCLUDES')

    def as_dict(self):
        return {
            '_id': self.__primaryvalue__,
            'name': self.name,
            'date': self.date,
            'label': self.label,
        }


class Track(BaseModel):
    aggregator = Label('Aggregator')
    items = RelatedTo('Track', 'AGGREGATES')

    name = Property()
    year = Property()

    playlists = RelatedFrom('Playlist', 'INCLUDES')
    artists = RelatedFrom('Artist', 'RECORDED')

    composition = RelatedFrom('Composition', 'RECORDED_ON')
    release = RelatedFrom('Release', 'INCLUDES')

    def as_dict(self):
        return {
            '_id': self.__primaryvalue__,
            'name': self.name,
            'year': self.year,
        }
