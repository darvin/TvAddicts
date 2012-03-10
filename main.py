import webapp2 as webapp
import urls


class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('Hello world!')

from libs import rest

app = webapp.WSGIApplication([('/', MainHandler),
             ('/rest/.*', rest.Dispatcher)]+urls.routes,
                             debug=True)

# configure the rest dispatcher to know what prefix to expect on request urls
rest.Dispatcher.base_url = '/rest'

import models
# add all models from some other module, and/or...
rest.Dispatcher.add_models_from_module(models)

