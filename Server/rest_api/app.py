

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import urls

app = webapp.WSGIApplication(urls.routes,
                             debug=True)




def main():
    run_wsgi_app(app)

if __name__ == "__main__":
    main()
