## Admin views ##
from libs import appengine_admin
from models import Show, Episode

class ShowAdmin(appengine_admin.ModelAdmin):
    model = Show
    listFields = ("title", "updated", "created")
    editFields = ("title", "summary")
    readonlyFields = ("updated", "created")


class EpisodeAdmin(appengine_admin.ModelAdmin):
    model = Episode
    listFields = ("title", "updated", "created")
    editFields = ("title", "summary")
    readonlyFields = ("updated", "created")

# Register to admin site
appengine_admin.register(ShowAdmin, EpisodeAdmin)