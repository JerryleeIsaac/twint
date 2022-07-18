import datetime
import logging as logme


class user:
    type = "user"

    def __init__(self):
        pass


User_formats = {
    'join_date': '%Y-%m-%d',
    'join_time': '%H:%M:%S %Z'
}


# ur object must be a json from the endpoint https://api.twitter.com/graphql
def User(ur):
    logme.debug(__name__ + ':User')
    if 'data' not in ur and 'user' not in ur['data']:
        msg = 'malformed json! cannot be parsed to get user data'
        logme.fatal(msg)
        raise KeyError(msg)
    _usr = user()
    _usr.id = ur['data']['user']['rest_id']
    legacy_data = ur['data']['user']['legacy'] 

    _usr.name = legacy_data.get("name", "")
    _usr.username = legacy_data.get("screen_name", "")
    _usr.bio = legacy_data.get("description", "")
    _usr.location = legacy_data.get('location', "")
    _usr.url = legacy_data.get("url", "")
    # parsing date to user-friendly format
    _dt = legacy_data.get('created_at')
    _dt = datetime.datetime.strptime(_dt, '%a %b %d %H:%M:%S %z %Y')
    # date is of the format year,
    _usr.join_date = _dt.strftime(User_formats['join_date'])
    _usr.join_time = _dt.strftime(User_formats['join_time'])

    # :type `int`
    _usr.tweets = int(legacy_data.get('statuses_count'))
    _usr.following = int(ur['data']['user']['legacy']['friends_count'])
    _usr.followers = int(ur['data']['user']['legacy']['followers_count'])
    _usr.likes = int(ur['data']['user']['legacy']['favourites_count'])
    _usr.media_count = int(ur['data']['user']['legacy']['media_count'])

    _usr.is_private = legacy_data.get('protected', "")
    _usr.is_verified = legacy_data.get('verified', "")
    _usr.avatar = legacy_data.get('profile_image_url_https', "")
    _usr.background_image = legacy_data.get('profile_banner_url', "")
    # TODO : future implementation
    # legacy_extended_profile is also available in some cases which can be used to get DOB of user
    return _usr
