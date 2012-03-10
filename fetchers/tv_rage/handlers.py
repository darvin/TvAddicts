from xml.etree.ElementTree import tostring
from google.appengine.api import taskqueue
import webapp2 as webapp
from libs.tvrage import api

from fetchers.tv_rage.urls import url_prefix, name_prefix

__author__ = 'darvin'



from libs.tvrage import feeds
feeds.TV_RAGE_API_KEY = "Fli3h0sNYIV0yyDWETv0"

CLASSIFICATION_ONLY = ("Scripted",)


#        schedule = feeds.full_schedule()
#        for day in schedule:
#            for time in day:
#                for show in time:
#                    x = show

class FetchSchedule(webapp.RequestHandler):
    def get(self, *args):
        shows = feeds.current_shows()
        for country in shows:
            for i, show in enumerate(country):
                showid = int(show.find("showid").text)
                #fixme lookup if show fully fetched
                taskqueue.add(url=webapp.uri_for(name_prefix+"show_task"),
                    params={'showid': showid})
                if i>10:
                    break


def get_date(node, key):
    try:
        return node.find(key).text
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

class ShowTask(webapp.RequestHandler):
    def post(self, *args):
        showid = int(self.request.get('showid'))
        show = feeds.showinfo(showid)
        classification = get_str(show, "classification")
        if classification not in CLASSIFICATION_ONLY:
            #fixme save show as fully fetched
            return

        show_title = get_str(show, "showname")
        origin_country = get_str(show, "origin_country")
        status = get_str(show, "status")

        summary = get_str(show, "summary")

        networks = [network.text for network in show.findall("network")]
        genres = [genre.text for genre in show.find("genres")]
        network = get_str(show, "network")

        seasons_number = get_int(show, "seasons")
        runtime = get_int(show, "runtime")
        started_date = get_date(show, "startdate")
        ended_date = get_date(show, "ended")

        taskqueue.add(url=webapp.uri_for(name_prefix+"episodes_list_task"),
            params={'showid': showid})



class SeasonTask(webapp.RequestHandler):
    def post(self, *args):
        pass

class EpisodeTask(webapp.RequestHandler):
    def post(self, *args):
        pass

class EpisodesListTask(webapp.RequestHandler):


    def post(self, *args):
        showid = int(self.request.get('showid'))
        episode_list = feeds.episode_list(showid).find("Episodelist")
        if episode_list is None:
            return
            #fixme mark as fully fetched
        for season in episode_list:
            for episode in season:
                self._parse_episode(episode, season)

    def _parse_episode(self, episode, season):

        episode_number_total = get_int( episode, "epnum")
        if season.tag=="Special":
            season_number = get_int(episode, "season")
            episode_number = -1
        else:
            season_number = season.attrib["no"]
            episode_number = get_int(episode, "seasonnum")
        rating = get_float(episode, "rating")
        airdate = get_date(episode, "airdate")
        title = get_str(episode, "title")
        epnum = get_int(episode, "epnum")
        summary = get_str(episode, "summary")
        screenshot_link = get_str(episode, "screencap")



