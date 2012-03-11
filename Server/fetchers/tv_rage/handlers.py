from datetime import datetime
from xml.etree.ElementTree import tostring
from google.appengine.api import taskqueue
import logging
import webapp2 as webapp
from models import Show, Genre, Episode, Country
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


class FetchSchedule(webapp.RequestHandler):
    def get(self, *args):
        shows = feeds.current_shows()
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



class ShowTask(webapp.RequestHandler):
    def post(self, *args):
        showid = int(self.request.get('showid'))
        show = feeds.showinfo(showid)
        show_title = get_str(show, "showname")


        classification = get_str(show, "classification")

        show_obj = Show.get_by_title(show_title)
        show_obj.classification = classification
        if classification not in CLASSIFICATION_ONLY:
            show_obj.fully_populate()
            return



        show_obj.set_country(get_str(show, "origin_country"))



        show_obj.status = get_str(show, "status")

        show_obj.summary = get_str(show, "summary") or ""

        show_obj.set_networks([network.text for network in show.findall("network")])
        show_obj.set_genres([genre.text for genre in show.find("genres")])

        seasons_number = get_int(show, "seasons")
        show_obj.runtime = get_int(show, "runtime")
        show_obj.started_date = get_date(show, "startdate")
        show_obj.ended_date = get_date(show, "ended")

        show_obj.put()
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
        feed = feeds.episode_list(showid)
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
            season_number = season.attrib["no"]
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



