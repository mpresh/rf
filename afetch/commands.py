import os
import sys

from twisted.internet import reactor, protocol, defer, task
from twisted.web import client
import time

import simplejson as json

# use local twitter lib                                                                                                                                                                                                                    
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
import settings
import oauth

from twittytwister import twitter

def consumer():
    try: return consumer._consumer
    except AttributeError:
        consumer._consumer = oauth.OAuthConsumer(settings.TWITTERAUTH_KEY, 
                                                 settings.TWITTERAUTH_SECRET)
        return consumer._consumer

def token(oauth_token, oauth_token_secret):
    return oauth.OAuthToken(oauth_token, oauth_token_secret)

def gotUser(user_data):
    dict = {}
    dict["profile_image_url"] = user_data.profile_image_url
    dict["name"] = user_data.name
    dict["screen_name"] = user_data.screen_name
    dict["id"] = user_data.id

    return dict

def gotError(fail):
    print "There was a fail", fail

def done(result, start, **kwargs):
    print "SUCCESS DONE", time.time() - start

    p = kwargs["conn"]
    p.transport.write("DONE")
    p.connectionLost("done succesfully")

def done_list(results, start, **kwargs):
    print "SUCCESS DONE", time.time() - start

    p = kwargs["conn"]

    result_list = []
    for result in results:
        result_list.append(result[1])

    json_text = json.dumps(result_list) + "\n"

    p.transport.write(json_text)

    p.connectionLost("done succesfully")

def get_twitter_user_info(data, **kwargs):
    """Get user info from twitter."""
    username = "mpresh"
    password = "pilotpresh25"
    info_user = "mpresh"

    print "Data", data
    start = time.time()

    print "Getting User Info Twitter"
    d = twitter.Twitter(username, password).show_user(info_user)
    d.addCallback(gotUser)
    d.addErrback(gotError)
    d.addCallback(done, start, conn=kwargs["conn"])

def get_twitter_user_list_info(data, **kwargs):
    """Get user info from twitter."""
    username = "mpresh"
    password = "pilotpresh25"
    info_user = "mpresh"

    print "Data Twitter User List Info", data
    print "token", data["oauth_token"], data["oauth_token_secret"]

    start = time.time()
    print "Getting User Info Twitter"

    deferred_list = []
    for user in data["users"]:
        d = twitter.Twitter(consumer=consumer(), 
                            token=token(data["oauth_token"], 
                                        data["oauth_token_secret"])).show_user(user)
        d.addCallback(gotUser)
        d.addErrback(gotError)
        deferred_list.append(d)

    dl = defer.DeferredList(deferred_list)
    dl.addCallback(done_list, start, conn=kwargs["conn"])

command_map = {"twitter_user_info" : get_twitter_user_info,
               "twitter_user_list_info" : get_twitter_user_list_info}
