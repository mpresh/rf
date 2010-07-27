from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from events.models import Event, Share
from tauth.models import User
from models import FBUser
from campaign.models import Campaign
from django.conf import settings
import simplejson as json
import urllib
import os
import hashlib
import base64
import shutil
import socket
import datetime
import util
from pylib import bitly

def campaign_facebook_update(req, campaign_id=""):
    """ Send feed update to facebook from user share. """
    fbuser = FBUser.objects.get(facebook_id=req.session["uid"])

    msg=req.GET["message"]
    if len(msg) > 125:
        msg = msg[:125]

    if "shash" in req.GET:
        parent_shash = req.GET["shash"]
    else:
        parent_shash = None

    share = Share(message=msg,
                  campaign=Campaign.objects.get(id=campaign_id),
                  from_user_facebook=fbuser,
                  from_user_twitter=None,
                  from_account_type="F",
                  parent_shash=parent_shash,
                  reach=fbuser.num_friends()
                  )
    share.setHash()

    url = share.url(req)
    short_url = bitly.shorten(url)
    share.url_short = short_url
    msg = msg + " " + short_url

    share.save()
    fbuser.feed(message=msg)
    dict = {}
    dict["status"] = "ok!"
    dict["url"] = short_url
    dict["msg"] = msg
    return HttpResponse(json.dumps(dict))


def update_feed(req):
    fbuser = FBUser.objects.get(facebook_id=req.session["uid"])
    fbuser.feed(message=req.GET["message"])

    dict = {}
    dict["status"] = "ok!"
    return HttpResponse(json.dumps(dict))


def message(req):
    print "message"
    print "SESSION KEYS"
    for key in req.session.keys():
        print "KEY", key, req.session[key]

    if "uid" in req.session:
        fbuser = FBUser.objects.get(facebook_id=req.session["uid"])
        fbuser.message()

        dict = {}
        dict["status"] = "ok!"
        return HttpResponse(json.dumps(dict))
    else:
        dict = {}
        dict["status"] = "error"
        dict["message"] = "no user"
        return HttpResponse(json.dumps(dict))

def friends(req):
    if "uid" in req.session:
        fbuser = FBUser.objects.get(facebook_id=req.session["uid"])
        data = fbuser.friends()
        
        print "DAAAATAAAA", data
        #for friend in data:
        #    print item

        dict = {}
        dict["status"] = "ok!"
        dict["data"] = data
        return HttpResponse(json.dumps(dict))
    else:
        dict = {}
        dict["status"] = "error"
        dict["message"] = "no user"
        return HttpResponse(json.dumps(dict))
