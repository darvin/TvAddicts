from StringIO import StringIO
from datetime import datetime
import urllib
from google.appengine.api import taskqueue, urlfetch
import logging
from google.appengine.api.datastore_errors import BadValueError
import webapp2 as webapp
from models import Show, Episode
from fetchers.tv_rage.urls import url_prefix, name_prefix
try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et




TV_RAGE_API_KEY = "Fli3h0sNYIV0yyDWETv0"

CLASSIFICATION_ONLY = ("Scripted",)


#        schedule = feeds.full_schedule()
#        for day in schedule:
#            for time in day:
#                for show in time:
#                    x = show


DATE_FORMATS = ("%Y-%m-%d", "%Y", "%b/%d/%Y")

def get_date(node, key):
    try:
        st = node.find(key).text
        if st is None:
            return None
        for format in DATE_FORMATS:
            try:
                return datetime.strptime(st, format).date()
            except ValueError:
                pass
    except AttributeError:
        return None

def get_str(node, key):
    try:
        return node.find(key).text
    except AttributeError:
        return None


def get_int(node, key):
    try:
        return int(node.find(key).text)
    except AttributeError:
        return None


def get_float(node, key):
    try:
        return float(node.find(key).text)
    except AttributeError:
        return None



class BaseFetcher(webapp.RedirectHandler):
    BASE_URL = 'http://services.tvrage.com/myfeeds/{feed}.php?{params}'
    FEED_NAME = None
    def build_url(self, params):
        prms = {"key": TV_RAGE_API_KEY}
        if params:
            prms.update(params)
        result = self.BASE_URL.format(feed=self.FEED_NAME,
            params=urllib.urlencode(prms))
        return result


    def handle_xml(self, result_xml):
        pass

    def __handle_result(self, rpc):
        result = rpc.get_result()
#        result = et.parse (StringIO(result.content))
#        root = result.getroot()
        root = et.fromstring(result.content)
        self.handle_xml(root)

    def __create_callback(self,rpc):
        return lambda: self.__handle_result(rpc)

    def make_request(self, params=None):
        rpc = urlfetch.create_rpc(deadline=20)
        rpc.callback = self.__create_callback(rpc)
        urlfetch.make_fetch_call(rpc, self.build_url(params))
        rpc.wait()

class FetchSchedule(BaseFetcher):
    FEED_NAME = "currentshows"

    def get(self, *args):
        self.make_request()

    def handle_xml(self, shows):
        for country in shows:
            for i, show in enumerate(country):
                showid = get_int(show, "showid")
                show_name = get_str(show, "showname")
                show, created = Show.get_or_create(title=show_name)
                if not show.fully_populated:
                    taskqueue.add(url=webapp.uri_for(name_prefix+"show_task"),
                        params={'showid': showid})
                if i>12:
                    break



class ShowTask(BaseFetcher):
    FEED_NAME = "showinfo"

    def post(self, *args):
        self.showid = showid = int(self.request.get('showid'))

        self.make_request({"sid":showid})


    def handle_xml(self, show):
        show_title = get_str(show, "showname")


        classification = get_str(show, "classification")

        show_obj = Show.get_by_title(show_title)
        try:
            show_obj.classification = classification
        except BadValueError:
            logging.critical("!!! classification {}".format(classification))
        if classification not in CLASSIFICATION_ONLY:
            show_obj.fully_populate()
            return



        show_obj.country = get_str(show, "origin_country")


        try:
            show_obj.status = get_str(show, "status")
        except BadValueError:
            logging.critical("!!! stats {}".format(get_str(show, "status")))

        show_obj.summary = get_str(show, "summary") or ""

        show_obj.networks = [network.text for network in show.findall("network")]
        show_obj.genres = [genre.text for genre in show.find("genres")]

        seasons_number = get_int(show, "seasons")
        show_obj.runtime = get_int(show, "runtime")
        show_obj.started_date = get_date(show, "startdate")
        show_obj.ended_date = get_date(show, "ended")

        show_obj.put()
        taskqueue.add(url=webapp.uri_for(name_prefix+"episodes_list_task"),
            params={'showid': self.showid})



class SeasonTask(webapp.RequestHandler):
    def post(self, *args):
        pass

class EpisodeTask(webapp.RequestHandler):
    def post(self, *args):
        pass

class EpisodesListTask(BaseFetcher):
    FEED_NAME = "episode_list"

    def post(self, *args):
        showid = int(self.request.get('showid'))
        self.make_request({"sid":showid})

    def handle_xml(self, feed):
        episode_list = feed.find("Episodelist")
        show_name = get_str(feed, "name")

        if episode_list is not None:
            show_obj = Show.get_by_title(show_name)

            for season in episode_list:
                for episode in season:
                    self._parse_episode(episode, season, show_obj)
            show_obj.fully_populate()


    def _parse_episode(self, episode, season, show):

        episode_number_total = get_int( episode, "epnum")
        if season.tag=="Special":
            season_number = get_int(episode, "season")
            episode_number = -1
        else:
            season_number = int(season.attrib["no"])
            episode_number = get_int(episode, "seasonnum")
        rating = get_float(episode, "rating")
        airdate = get_date(episode, "airdate")
        title = get_str(episode, "title")
        epnum = get_int(episode, "epnum")
        summary = get_str(episode, "summary") or ""
        screenshot_link = get_str(episode, "screencap")
        if episode_number!=-1:
            episode_obj, created = Episode.get_or_create(
                show=show, season_number=season_number, episode_number=episode_number)
        else:
            episode_obj, created = Episode.get_or_create(
                show=show, season_number=season_number, special=True, title=title)

        episode_obj.summary = summary
        episode_obj.screenshot_link = screenshot_link
        episode_obj.airdate = airdate
        episode_obj.rating = rating
        episode_obj.put()



