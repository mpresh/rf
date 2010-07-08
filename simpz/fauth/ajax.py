from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from events.models import Event, Invite, Share
from tauth.models import User
from models import FBUser
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

def event_facebook_update(req, event_id=""):
    """ Send feed update to facebook from user share. """
    fbuser = FBUser.objects.get(facebook_id=req.session["uid"])
    #fbuser.feed(message=req.GET["message"])
    print "hello world2", event_id
    
    msg=req.GET["message"]
    if len(msg) > 125:
        msg = msg[:125]

    share = Share(message=msg,
                  event=Event.objects.get(id=event_id),
                  from_user_facebook=fbuser,
                  from_account_type="F"
                  )
    share.save()
    share.setHash()
    print "URL IS", share.url()
    print "URL IS", share.referUrl()

    dict = {}
    dict["status"] = "ok!"
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
