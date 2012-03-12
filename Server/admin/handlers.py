## Admin views ##
from libs.appengine_admin.djangoforms import forms
from libs import appengine_admin
from models import Show, Episode, Article, ArticleType, Track


class BaseAdmin(appengine_admin.ModelAdmin):
    customFormFields = None

    readonlyFields = ("updated", "created")
    def __init__(self):
        super(BaseAdmin, self).__init__()
        if self.customFormFields:
            for field_name, field in self.customFormFields.iteritems():
                self.AdminForm.base_fields[field_name] = field


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
    editFields = ("title",
                  "summary",
        "country",
        "genres",
        "networks",)
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
    ArticleTypeAdmin,
    TrackAdmin)