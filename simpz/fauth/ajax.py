from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from events.models import Event, Invite
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

def update_feed(req):
    print "update feed"
    print "SESSION KEYS"
    for key in req.session.keys():
        print "KEY", key, req.session[key]

    fbuser = FBUser.objects.get(facebook_id=req.session["uid"])
    fbuser.feed()

    dict = {}
    dict["status"] = "ok!"
    return HttpResponse(json.dumps(dict))
