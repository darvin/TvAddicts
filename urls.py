from pprint import pprint
import webapp2 as webapp
from fetchers.tv_rage import urls as fetchers_tv_rage_urls


def _process_urls_module(urls_module):
    result = []
    for url_route in urls_module.routes:
        result.append(webapp.Route(urls_module.url_prefix+url_route[0],
                       handler=urls_module.handler_prefix+url_route[1],
                       name=urls_module.name_prefix+url_route[2]))
    return result


def _process_urls_modules(urls_modules):
    result = []
    for urls_module in urls_modules:
        result += _process_urls_module(urls_module)
    return result

routes = _process_urls_modules((fetchers_tv_rage_urls,))

