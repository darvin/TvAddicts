import os
# specify the name of your settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_settings'


from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from libs import appengine_admin
from handlers import *



app = webapp.WSGIApplication([
        (r'^(/admin)(.*)$', appengine_admin.Admin),
])


def main():
    run_wsgi_app(app)

if __name__ == "__main__":
    main()