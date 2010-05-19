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

def done(result, **kwargs):
    start = kwargs["start"]
    print "SUCCESS DONE", time.time() - start

    p = kwargs["conn"]
    p.transport.write("DONE")
    p.connectionLost("done succesfully")

def done_list(results, **kwargs):
    start = kwargs["start"]
    print "SUCCESS DONE", time.time() - start

    mc_key = kwargs["mc_key"]
    mc = kwargs["mc"]
    p = kwargs["conn"]

    result_list = []
    for result in results:
        result_list.append(result[1])

    json_text = json.dumps(result_list) + "\n"

    p.transport.write(json_text)

    p.connectionLost("done succesfully")

    mc.set(mc_key, json_text, time=30)

def get_twitter_user_info(**kwargs):
    """Get user info from twitter."""

    data = kwargs["data"]
    user_id = kwargs["username"]
    mc = kwargs["mc"]

    kwargs["start"] = time.time()
    d = twitter.Twitter(consumer=consumer(), 
                        token=token(data["oauth_token"])).show_user(info_user)
    d.addCallback(gotUser)
    d.addErrback(gotError)
    d.addCallback(done, **kwargs)

def get_twitter_user_list_info(**kwargs):
    """Get user info from twitter."""
    
    data = kwargs["data"]
    username = kwargs["username"]
    mc = kwargs["mc"]

    kwargs["start"] = time.time()
    kwargs["mc_key"] = username + "twitter_user_list_info"

    value = mc.get(kwargs["mc_key"])
    if value:
        p = kwargs["conn"]
        p.transport.write(value)
        p.connectionLost("done succesfully")
        return

    deferred_list = []
    for user in data["users"]:
        d = twitter.Twitter(consumer=consumer(), 
                            token=token(data["oauth_token"], 
                                        data["oauth_token_secret"])).show_user(user)
        d.addCallback(gotUser)
        d.addErrback(gotError)
        deferred_list.append(d)

    dl = defer.DeferredList(deferred_list)
    dl.addCallback(done_list, **kwargs)

command_map = {"twitter_user_info" : get_twitter_user_info,
               "twitter_user_list_info" : get_twitter_user_list_info}
