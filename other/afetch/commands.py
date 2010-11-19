import os
import sys

from twisted.internet import reactor, protocol, defer, task
from twisted.web import client
import time

import simplejson as json

# use local twitter lib                                                                                                                                                                                                                    
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../pylib")))
import settings
import oauth

from twittytwister import twitter

os.environ['DJANGO_SETTINGS_MODULE'] = "settings"
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from core.events.models import Event
from core.tauth.models import User
from django.conf import settings

def consumer():
    try: return consumer._consumer
    except AttributeError:
        consumer._consumer = oauth.OAuthConsumer(settings.TWITTERAUTH_KEY, 
                                                 settings.TWITTERAUTH_SECRET)
        return consumer._consumer

def token(oauth_token, oauth_token_secret):
    return oauth.OAuthToken(oauth_token, oauth_token_secret)

def fillUserInfo(user_data):
    """Fill In User Information."""
    print "Filling User Info", user_data
    user = User.objects.get(username=user_data.screen_name)
    user.profile_pic = user_data.profile_image_url
    user.name = user_data.name
    user.username = user_data.screen_name
    user.twitter_id = user_data.id
    user.save()

    print "Finished Filling In User Info", user.name
    return True

def gotUser(user_data):
    dict = {}
    dict["profile_image_url"] = user_data.profile_image_url
    dict["name"] = user_data.name
    dict["screen_name"] = user_data.screen_name
    dict["id"] = user_data.id

    return dict

def sentDM(result):
    print "DM SENT", result
    return result

def gotError(fail):
    print "There was an ERROR:", dir(fail)
    print "Fail:", fail

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

def done_dm(results, **kwargs):
    start = kwargs["start"]
    print "SUCCESS DONE", time.time() - start
    print "result!!!!", results

    p = kwargs["conn"]

    result_list = []
    for result in results:
        result_list.append(result[1])

    json_text = json.dumps(result_list) + "\n"

    print "json text", json_text
    p.transport.write(json_text)

    print "AND NOW HERE"
    p.connectionLost("done succesfully")

def get_twitter_user_info(**kwargs):
    """Get user info from twitter."""

    data = kwargs["data"]
    user_id = kwargs["username"]
    mc = kwargs["mc"]

    kwargs["start"] = time.time()
    d = twitter.Twitter(consumer=consumer(), 
                        token=token(data["oauth_token"],
                                    # BUG: info_user is undefined
                                    data["oauth_token_secret"])).show_user(info_user)
    d.addCallback(gotUser)
    d.addErrback(gotError)
    d.addCallback(done, **kwargs)

def get_twitter_user_list_info(**kwargs):
    """Get user info from twitter."""
    
    data = kwargs["data"]
    username = kwargs["username"]

    # get memcached
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

def send_dm_invites(**kwargs):
    """Send DM invites to users. """
    kwargs["start"] = time.time()
    data = kwargs["data"]
    #msg = data["msg"]

    deferred_list = []

    for (user, msg) in data["users"]:
        dm_deferred = twitter.Twitter(consumer=consumer(), 
                                      token=token(data["oauth_token"], 
                                                  data["oauth_token_secret"])).send_direct_message(msg,
                                                                                                   screen_name=user)

        print "here I am creating", user
        user_info_deferred = twitter.Twitter(consumer=consumer(), 
                                             token=token(data["oauth_token"],
                                                         data["oauth_token_secret"])).show_user(user)
        user_info_deferred.addCallback(fillUserInfo)

        dm_deferred.addCallback(sentDM)
        dm_deferred.addErrback(gotError)
        deferred_list.append(user_info_deferred)

    dl = defer.DeferredList(deferred_list)
    print "dl", dl
    dl.addCallback(done_dm, **kwargs)
    dl.addErrback(gotError)
    print "exiting this"

command_map = {"twitter_user_info" : get_twitter_user_info,
               "twitter_user_list_info" : get_twitter_user_list_info,
               "twitter_dm_users" : send_dm_invites}
