from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from events.models import Event, Share
from tauth.models import User
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
from pylib import bitly, eventbrite

import urlparse

def create_discount(req):
    dict = {}
    percent = req.POST['percent']
    code = req.POST['code']
    username = req.POST['username']
    password = req.POST['password']
    eventid = req.POST['eventid']

    print "lal", settings.EVENTBRITE_API
    api = eventbrite.API(settings.EVENTBRITE_API, cache='.cache')
    try:
        discount = api.call('discount_new', user=username, password=password, percent_off=percent, code=code, event_id=eventid)
        print discount
    except Exception, e:
        print "there was a fail", e
    
    return HttpResponse(json.dumps(dict))

def update_discount(req):
    print "Creating discount", req
    dict = {}
    return HttpResponse(json.dumps(dict))

def discount_list(req):
    print "Creating discount", req
    dict = {}
    return HttpResponse(json.dumps(dict))
