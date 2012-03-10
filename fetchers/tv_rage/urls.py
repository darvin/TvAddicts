
handler_prefix = "fetchers.tv_rage.handlers."
url_prefix = r"/fetchers/tv_rage/"
name_prefix = "fetchers_tv_rage_"


routes = [
    (r"fetch_schedule", "FetchSchedule", "fetch_schedule"),
    (r"show_task", "ShowTask", "show_task"),
    (r"season_task", "SeasonTask", "season_task"),
    (r"episode_task", "EpisodeTask", "episode_task"),
    (r"episodes_list_task", "EpisodesListTask", "episodes_list_task"),
]
