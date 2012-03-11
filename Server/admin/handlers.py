## Admin views ##
from libs import appengine_admin
from models import Show, Episode, Network, Country, Genre, Article


class BaseAdmin(appengine_admin.ModelAdmin):
    readonlyFields = ("updated", "created")


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
                    "summary",)

class ShowAdmin(BaseAdmin):
    model = Show
    listFields = ("title", "updated", "created")
    editFields = ("title", "summary")
    readonlyFields = ("updated", "created")


class EpisodeAdmin(BaseAdmin):
    model = Episode
    listFields = ("title", "updated", "created")
    editFields = ("title", "summary")
    readonlyFields = ("updated", "created")

# Register to admin site
appengine_admin.register(ShowAdmin,
    EpisodeAdmin,
    ArticleAdmin,
    GenreAdmin,
    NetworkAdmin,
    CountryAdmin)