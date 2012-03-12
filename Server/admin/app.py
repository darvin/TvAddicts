from django_legacy_setup import setup_legacy_django_compatibility

setup_legacy_django_compatibility()


#from google.appengine.ext.webapp.util import run_wsgi_app
from libs import appengine_admin
from handlers import *
from google.appengine.ext import webapp


app = webapp.WSGIApplication([
        (r'^(/admin)(.*)$', appengine_admin.Admin),
])

