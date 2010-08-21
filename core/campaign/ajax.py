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
    print "SELECT WINNERS", req
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
        number = int(req.GET["number"])
    except:
        number = 1

    random.seed(time.time())
    print "NUMBER SHARES", len(shares)

    dict = {}
    dict["winners"] = []

    return HttpResponse(json.dumps({}))    
