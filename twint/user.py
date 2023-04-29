import datetime
import logging as logme


class user:
    type = "user"

    def __init__(self):
        pass


User_formats = {"join_date": "%Y-%m-%d", "join_time": "%H:%M:%S %Z"}


def User(ur):
    logme.debug(__name__ + ":User")
    _usr = user()
    _usr.id = ur["id_str"]
    _usr.name = ur["name"]
    _usr.username = ur["screen_name"]
    _usr.bio = ur["description"]
    _usr.location = ur["location"]
    _usr.url = ur["url"]
    # parsing date to user-friendly format
    _dt = ur["created_at"]
    _dt = datetime.datetime.strptime(_dt, "%a %b %d %H:%M:%S %z %Y")
    # date is of the format year,
    _usr.join_date = _dt.strftime(User_formats["join_date"])
    _usr.join_time = _dt.strftime(User_formats["join_time"])

    # :type `int`
    _usr.tweets = int(ur["statuses_count"])
    _usr.following = int(ur["friends_count"])
    _usr.followers = int(ur["followers_count"])
    _usr.likes = int(ur["favourites_count"])
    _usr.media_count = int(ur["media_count"])

    _usr.is_private = ur["protected"]
    _usr.is_verified = ur["verified"]
    _usr.avatar = ur["profile_image_url_https"]
    _usr.background_image = ""
    # TODO : future implementation
    # legacy_extended_profile is also available in some cases which can be used to get DOB of user
    return _usr
