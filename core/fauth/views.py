from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from events.models import Event
from tauth.models import User
from fauth.models import FBUser
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
from fauth import fauth_utils
from create import *

def facebook_login_test(req):
    #print req
    req.session["redirect"] = reverse("facebook_login_test")
    dict = {}
    host = "http://" + req.get_host()
    dict["facebook_app_id"] = settings.FACEBOOK_APP_ID
    dict["facebook_api"] = settings.FACEBOOK_API
    dict["redirect_uri"] = host + reverse("facebook_login_callback")
    dict["scope"] = "publish_stream"
    dict["scope"] = ""
    if "uid" in req.session:
        fbuser = FBUser.objects.get(facebook_id=req.session["uid"])
        dict["fbuser"] = fbuser
    return render_to_response('facebook_login_test.html', dict)
