from google.appengine.ext import db
from google.appengine.ext.db.polymodel import PolyModel
from referenced_property import ReferenceListProperty
from libs.aetycoon import *


ARTICLE_TYPE_CHOICES = (None, "Review"
                        "Feature",
                        "Interview",
                        "News",
                        "One-liner",
                        "Article",)
SHOW_STATUS_CHOICES = (None,
                       "Returning Series",
                       "Final Season",
                       "TBD/On The Bubble",
#                       "",
#                       "",
#                       "",
    )
SHOW_CLASSIFICATION_CHOICES = (None,
                               "Scripted",
                               "Talk Shows",
                               "Reality",
                               "News",
                               "Variety",
                               "Documentary",
                               "Animation",
                               "Mini-Series",
                               "Game Show",)


class BaseModel(db.Model):
    updated = db.DateTimeProperty(auto_now=True)
    created = db.DateTimeProperty(auto_now_add=True)

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

    def _set_referenced_list_property_create_objects(self, property_name, model, titles_list):
        result = []
        for title in titles_list:
            obj, created = model.get_or_create(title=title)
            result.append(obj)
        setattr(self, property_name, result)
    def _set_referenced_property_create_objects(self, property_name, model, title):
        obj, created = model.get_or_create(title=title)
        setattr(self, property_name, obj)


class PopulatedModel(BaseModel):
    fully_populated = db.BooleanProperty(default=False)

    @classmethod
    def get_by_title(cls, title):
        result = cls.all().filter('title =', title)
        if result.count()!= 1:
            x = result.count()
            raise NotImplementedError
        return result[0]

    def fully_populate(self):
        self.fully_populated = True
        self.put()


class Network(BaseModel):
    title = db.StringProperty()


class Country(BaseModel):
    title = db.StringProperty()


class Genre(BaseModel):
    title = db.StringProperty()


class Show(PopulatedModel):
    title = db.StringProperty()
    country = db.ReferenceProperty(Country)
    genres = ReferenceListProperty(Genre)
    status = ChoiceProperty(enumerate(SHOW_STATUS_CHOICES))
    classification = ChoiceProperty(enumerate(SHOW_CLASSIFICATION_CHOICES))
    summary = CompressedTextProperty(default="")
    networks = ReferenceListProperty(Network)
    runtime = db.IntegerProperty()
    started_date = db.DateProperty()
    ended_date = db.DateProperty()

    def set_genres(self, genres_lst):
        self._set_referenced_list_property_create_objects("genres", Genre, genres_lst)

    def set_country(self, country_title):
        self._set_referenced_property_create_objects("country", Country, country_title)

    def set_networks(self, networks_lst):
        self._set_referenced_list_property_create_objects("networks", Network, networks_lst)




class Episode(PopulatedModel):
    show = db.ReferenceProperty(Show)
    title = db.StringProperty()
    summary = CompressedTextProperty(default="")
    air_date = db.DateTimeProperty()
    season_number = db.IntegerProperty()
    special = db.BooleanProperty()
    episode_number = db.IntegerProperty()
    episode_number_total = db.IntegerProperty()
    screenshot_link = db.LinkProperty()
    rating = db.FloatProperty()


class Track(BaseModel):
    episode = db.ReferenceProperty(Episode)
    title = db.StringProperty()
    artist = db.StringProperty()


class Article(BaseModel):
    show = db.ReferenceProperty(Show, required=True)
    related_shows = ReferenceListProperty(Show)
    related_episodes = ReferenceListProperty(Episode)
    type = ChoiceProperty(enumerate(ARTICLE_TYPE_CHOICES))
    title = db.StringProperty(required=True)
    body = db.StringProperty(required=True)
    summary = db.StringProperty()
    publication_date = db.DateTimeProperty()
    exclusive = db.BooleanProperty(default=False)

