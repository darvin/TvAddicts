from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import admin
import appengine_admin

application = webapp.WSGIApplication([
        # Admin pages
        (r'^(/admin)(.*)$', appengine_admin.Admin),
    ], debug = True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
