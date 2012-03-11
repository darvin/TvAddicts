import logging

import webapp2 as webapp


class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('Hello world!')



logging.getLogger().setLevel(logging.DEBUG)


import urls

app = webapp.WSGIApplication([('/', MainHandler),
             ]+urls.routes,
                             debug=True)
logging.getLogger().setLevel(logging.DEBUG)





