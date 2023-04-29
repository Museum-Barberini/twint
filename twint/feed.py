import time
from datetime import datetime
from rich import print

from bs4 import BeautifulSoup
from re import findall
from json import loads

import logging as logme

from .tweet import utc_to_local, Tweet_formats


class NoMoreTweetsException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


def Follow(response):

    follows = loads(response)
    print(follows["users"])
    follow = follows["users"]
    logme.debug(__name__ + ":Follow")
    soup = BeautifulSoup(response, "html.parser")
    cursor = follows["next_cursor_str"]

    return follow, cursor


# TODO: this won't be used by --profile-full anymore. if it isn't used anywhere else, perhaps remove this in future
def Mobile(response):
    logme.debug(__name__ + ":Mobile")
    soup = BeautifulSoup(response, "html.parser")
    tweets = soup.find_all("span", "metadata")
    max_id = soup.find_all("div", "w-button-more")
    try:
        max_id = findall(r'max_id=(.*?)">', str(max_id))[0]
    except Exception as e:
        logme.critical(__name__ + ":Mobile:" + str(e))

    return tweets, max_id


def MobileFav(response):
    from rich import print_json

    print(response)
    soup = BeautifulSoup(response, "html.parser")
    tweets = soup.find_all("table", "tweet")
    max_id = soup.find_all("div", "w-button-more")
    try:
        max_id = findall(r'max_id=(.*?)">', str(max_id))[0]
    except Exception as e:
        print(str(e) + " [x] feed.MobileFav")

    return tweets, max_id


def _get_cursor(response):
    try:
        next_cursor = response["timeline"]["instructions"][0]["addEntries"]["entries"][
            -1
        ]["content"]["operation"]["cursor"]["value"]
    except KeyError:
        # this is needed because after the first request location of cursor is changed
        next_cursor = response["timeline"]["instructions"][-1]["replaceEntry"]["entry"][
            "content"
        ]["operation"]["cursor"]["value"]
    return next_cursor


def Json(response):
    logme.debug(__name__ + ":Json")
    json_response = loads(response)
    html = json_response["items_html"]
    soup = BeautifulSoup(html, "html.parser")
    feed = soup.find_all("div", "tweet")
    return feed, json_response["min_position"]


def parse_tweets(config, response, last_cursor):
    logme.debug(__name__ + ":parse_tweets")
    response = loads(response)
    if len(response) == 0:
        msg = "No more data!"
        raise NoMoreTweetsException(msg)
    print(len(response))
    next_cursor = response[-1]["id_str"]
    if response[0]["id_str"] == last_cursor:
        response = response[1:]

    feed = []
    for timeline_entry in response:
        # this will handle the cases when the timeline entry is a tweet
        # if timeline_entry.get("id"):
        #     _id = timeline_entry["id"]
        # else:
        #     _id = None
        # if _id is None:
        #     raise ValueError("Unable to find ID of tweet in timeline.")
        # try:
        #     temp_obj = response["globalObjects"]["tweets"][_id]
        # except KeyError:
        #     logme.info("encountered a deleted tweet with id {}".format(_id))

        #     config.deleted.append(_id)
        #     continue
        # temp_obj["user_data"] = response["globalObjects"]["users"][
        #     temp_obj["user_id_str"]
        # ]
        # if "retweeted_status_id_str" in temp_obj:
        #     rt_id = temp_obj["retweeted_status_id_str"]
        #     _dt = response["globalObjects"]["tweets"][rt_id]["created_at"]
        #     _dt = datetime.strptime(_dt, "%a %b %d %H:%M:%S %z %Y")
        #     _dt = utc_to_local(_dt)
        #     _dt = str(_dt.strftime(Tweet_formats["datetime"]))
        #     temp_obj["retweet_data"] = {
        #         "user_rt_id": response["globalObjects"]["tweets"][rt_id][
        #             "user_id_str"
        #         ],
        #         "user_rt": response["globalObjects"]["tweets"][rt_id]["full_text"],
        #         "retweet_id": rt_id,
        #         "retweet_date": _dt,
        #     }
        # feed.append(temp_obj)
        feed.append(timeline_entry)
    return feed, next_cursor
