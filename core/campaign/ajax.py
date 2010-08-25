from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from events.models import Event, Share
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
from pylib import bitly
import sys
from smtplib import SMTP
import re
import time
import random

def select_winners(req):
    if "campaign" in req.GET:
        try:
            campaign = Campaign.objects.get(id=req.GET["campaign"])
            shares = Share.objects.filter(campaign=campaign.id)
        except Exception:
            dict["error"] = "Valid campaign id not provided."
            dict["status"] = 500
            return HttpResponse(json.dumps(dict))
    else:
        dict["error"] = "Must specify campaign."
        dict["status"] = 500
        return HttpResponse(json.dumps(dict))

    try:
        total_number = int(req.GET["total_number"])
    except:
        total_number = 1

    try:
        number = int(req.GET["number"])
    except:
        number = total_number

    try:
        current_number = int(req.GET["current_number"])
    except:
        current_number = 0

    try:
        exclude = eval(req.GET["exclude"])
    except:
        exclude = []

    print "total_number=%s  number=%s  current_number=%s" % (total_number, number, current_number) 

    random.seed(time.time())

    shares = list(shares)
    dict = {}
    dict["winners"] = []
    while (((current_number + len(dict["winners"])) < number) and len(shares) > 0):
        print "total_number=%s  number=%s  current_number=%s" % (total_number, number, current_number) 
        randSelection = random.randint(0, len(shares) - 1)
        selectedShare = shares.pop(randSelection)
        if selectedShare.from_account_type == "F":
            fbuser = selectedShare.from_user_facebook
            user = {}
            user["type"] = "facebook"
            user["name"] = fbuser.name
            user["profile_pic"] = fbuser.get_profile_pic()
            user["username"] = fbuser.username
            user["id"] = fbuser.facebook_id
        elif selectedShare.from_account_type == "T":
            tuser = selectedShare.from_user_twitter
            user = {}
            user["type"] = "twitter"
            user["name"] = tuser.name
            user["profile_pic"] = tuser.profile_pic
            user["username"] = tuser.username
            user["id"] = tuser.twitter_id
        else:
            user = None
      
        key = (user["type"] + "_" + user["id"]) 
        print key, exclude
        if  key not in exclude:
            dict["winners"].append(user)
            exclude.append(key)
        
    dict["exclude"] = exclude;
    # number of winners is less than requested number of winners
    if (current_number + len(dict["winners"])) < number:
        dict["status"] = 501
        total_number = current_number + len(dict["winners"])
        dict["message"] = "No more valid winners at this time. Total winners %s." % (str(total_number))
    else:
        # number of winners matches the requested number of winners
        dict["status"] = 200

    print "Winners Dict", dict
    return HttpResponse(json.dumps(dict))    