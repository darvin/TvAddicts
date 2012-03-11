from libs import rest



routes = [(r'/rest/.*', rest.Dispatcher)]


# configure the rest dispatcher to know what prefix to expect on request urls
rest.Dispatcher.base_url = '/rest'

import models
# add all models from some other module, and/or...
rest.Dispatcher.add_models_from_module(models)

