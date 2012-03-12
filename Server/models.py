from google.appengine.ext import db
from libs.appengine_admin.db_extensions import ManyToManyProperty
from libs.aetycoon import *


SHOW_STATUS_CHOICES = (None,
                       "Returning Series",
                       "Final Season",
                       "TBD/On The Bubble",
                       "New Series",
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
                               "Game Show",
                               "Sports",)


class BaseModel(db.Model):
    title = db.StringProperty()

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

    def __unicode__(self):
        if self.title:
            return self.title
        else:
            return "{}: {}".format(self.__class__.__name__, self.key())

    def __str__(self):
        return unicode(self)


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




class Show(PopulatedModel):
    country = db.StringProperty()
    genres = db.StringListProperty(default=None)
    networks = db.StringListProperty(default=None)

    status = ChoiceProperty(enumerate(SHOW_STATUS_CHOICES))
    classification = ChoiceProperty(enumerate(SHOW_CLASSIFICATION_CHOICES))
    summary = CompressedTextProperty(default="")
    runtime = db.IntegerProperty()
    started_date = db.DateProperty()
    ended_date = db.DateProperty()





class Episode(PopulatedModel):
    show = db.ReferenceProperty(Show)
    summary = CompressedTextProperty(default="")
    air_date = db.DateTimeProperty()
    season_number = db.IntegerProperty()
    special = db.BooleanProperty()
    episode_number = db.IntegerProperty()
    episode_number_total = db.IntegerProperty()
    screenshot_link = db.LinkProperty()
    rating = db.FloatProperty()

    def __unicode__(self):
        return "{show}: {episode_title}".format(show=self.show, episode_title=self.title)


class Track(BaseModel):
    episode = db.ReferenceProperty(Episode)
    artist = db.StringProperty()

    def __unicode__(self):
        return "{artist} - {title} ({episode})".format(
            episode=self.episode, artist=self.artist, title=self.title)



class ArticleType(BaseModel):
    pass

class Article(BaseModel):
    show = db.ReferenceProperty(Show, required=True)
    related_shows = ManyToManyProperty(Show)
    related_episodes = ManyToManyProperty(Episode)
    type = db.ReferenceProperty(ArticleType)
    body = CompressedTextProperty()
    summary = db.StringProperty()
    publication_date = db.DateTimeProperty()
    exclusive = db.BooleanProperty(default=False)

