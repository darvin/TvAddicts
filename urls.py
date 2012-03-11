from pprint import pprint
import webapp2 as webapp
from fetchers.tv_rage import urls as fetchers_tv_rage_urls

def _process_urls_module(urls_module):
    result = []
    for url_route in urls_module.routes:
        url_prefix = getattr(urls_module, "url_prefix", "")
        name_prefix = getattr(urls_module, "name_prefix", "")
        if hasattr(urls_module, "handler_prefix"):
            handler = urls_module.handler_prefix+url_route[1]
        else :
            handler = url_route[1]
        if len(url_route)>2:
            name = name_prefix+url_route[2]
        else:
            name = None
        result.append(webapp.Route(url_prefix+url_route[0],
                       handler=handler, name=name))
    return result


def _process_urls_modules(urls_modules):
    result = []
    for urls_module in urls_modules:
        result += _process_urls_module(urls_module)
    return result

routes = _process_urls_modules((fetchers_tv_rage_urls,
    ))

print


