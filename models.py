from google.appengine.ext import db
from google.appengine.ext.db.polymodel import PolyModel
from referenced_property import ReferenceListProperty

class BaseModel(db.Model):
    @classmethod
    def get_or_create(cls, parent=None, **kwargs):
            query = cls.all()
            if parent:
                query.ancestor(parent)
            for kw in kwargs:
                query.filter("%s =" % kw, kwargs[kw])
            entity = query.get()
            if entity:
                created = False
            else:
                entity = cls(parent, **kwargs)
                entity.put()
                created = True
            return (entity, created)

    
class Network(BaseModel):
    title = db.StringProperty()

class Show(BaseModel):
    title = db.StringProperty()
    summary = db.StringProperty()
    network = db.ReferenceProperty(Network)




class Episode(BaseModel):

    show = db.ReferenceProperty(Show)
    title = db.StringProperty()
    summary = db.StringProperty()
    air_date = db.DateTimeProperty()
    season_number = db.IntegerProperty()
    episode_number = db.IntegerProperty()


class Track(BaseModel):
    episode = db.ReferenceProperty()
    title = db.StringProperty()
    artist = db.StringProperty()


class ArticleType(BaseModel):
    KEY_NAME = "%(title)s"

    title = db.StringProperty()



ARTICLE_TYPES = ("Review"
                "Feature",
                "Interview",
                "News",
                "One-liner",
                "Article",)
for article_type in ARTICLE_TYPES:
    a, created = ArticleType.get_or_create(title=article_type)

class Article(BaseModel):
    show = db.ReferenceProperty(Show, required=True)
    related_shows = ReferenceListProperty(Show)
    related_episodes = ReferenceListProperty(Episode)
    type = db.ReferenceProperty(ArticleType, required=True)
    title = db.StringProperty(required=True)
    body = db.StringProperty(required=True)
    publication_date = db.DateTimeProperty()
    exclusive = db.BooleanProperty(default=False)

abc, created = Network.get_or_create(title="ABC")
person_of_interest, created = Show.get_or_create(title="Person Of Interest", network=abc)