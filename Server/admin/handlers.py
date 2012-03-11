## Admin views ##
from google.appengine.ext.db.djangoforms import forms
from libs import appengine_admin
from models import Show, Episode, Network, Country, Genre, Article, ArticleType, Track


class BaseAdmin(appengine_admin.ModelAdmin):
    customFormFields = None

    readonlyFields = ("updated", "created")
    def __init__(self):
        super(BaseAdmin, self).__init__()
        if self.customFormFields:
            for field_name, field in self.customFormFields.iteritems():
                self.AdminForm.base_fields[field_name] = field

class NetworkAdmin(BaseAdmin):
    model = Network
    listFields = ("title",)
    editFields = ("title",)

class CountryAdmin(BaseAdmin):
    model = Country
    listFields = ("title",)
    editFields = ("title",)

class GenreAdmin(BaseAdmin):
    model = Genre
    listFields = ("title",)
    editFields = ("title",)

class ArticleTypeAdmin(BaseAdmin):
    model = ArticleType
    listFields = ("title",)
    editFields = ("title",)



class ArticleAdmin(BaseAdmin):

    model = Article
    listFields = ("title",
                  "publication_date",
                  "show", "summary")
    editFields = ("title",
                  "publication_date",
                    "show",
                    "body",
                    "exclusive",
                    "summary",
                    "related_shows",
                    "related_episodes",
                    "type",)

    customFormFields = {
        "body":forms.CharField(widget=forms.Textarea)
    }


class ShowAdmin(BaseAdmin):
    model = Show
    listFields = ("title", "updated", "created")
    editFields = ("title", "summary")
    readonlyFields = ("updated", "created")

    customFormFields = {
        "summary":forms.CharField(widget=forms.Textarea)
    }


class EpisodeAdmin(BaseAdmin):
    model = Episode
    listFields = ("title", "updated", "created")
    editFields = ("title", "summary")
    readonlyFields = ("updated", "created")
    customFormFields = {
        "summary":forms.CharField(widget=forms.Textarea)
    }


class TrackAdmin(BaseAdmin):
    model = Track
    listFields = ( "title", "artist", "episode")
    editFields = ("episode", "title", "artist")

# Register to admin site
appengine_admin.register(ShowAdmin,
    EpisodeAdmin,
    ArticleAdmin,
    GenreAdmin,
    NetworkAdmin,
    CountryAdmin,
    ArticleTypeAdmin,
    TrackAdmin)