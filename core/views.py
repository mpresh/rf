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

def test3(req):
    return render_to_response('test3.html', {})

def test2(req):
    return render_to_response('test2.html', {})


def test(req):
    #req.session["redirect"] = req.get_full_path()  
    return render_to_response('test.html', {})

def about(req):
    return render_to_response('about.html', {})

def contact(req):
    return render_to_response('contact.html', {})

def howitworks(req):
    return render_to_response('howitworks.html', {})

def event_list(req):
    #req.session["redirect"] = req.get_full_path()  
    all_campaigns = Campaign.objects.all()
    if "user_id" in req.session:
        user = User.objects.get(id=req.session["user_id"])
        return render_to_response('list.html', {"campaigns":all_campaigns,
                                                "user" : user})

    return render_to_response('list.html', {"campaigns":all_campaigns})
    
def event_details(req, event_id=""):

    dict = {}
    if "user_id" in req.session:
        user = User.objects.get(id=req.session["user_id"])
        dict['user'] = user

    #req.session["redirect"] = req.get_full_path()
    if event_id:
        e = Event.objects.get(id=event_id)
        dict['event'] = e
        dict['invites'] = e.invitations.all()
        dict['attendees'] = e.attendees.all()
        dict['attendees_maybe'] = e.attendees_maybe.all()
            
        return render_to_response('details.html', dict)
	
    return render_to_response('details.html', dict)

def map(request):
    return render_to_response('map.html', {"key": settings.GOOGLE_MAP_API,
                                           "zoom": 14})

def user_details(req, user_id=""):
    #req.session["redirect"] = req.get_full_path()

    dict = {}
    if user_id:
        user = User.objects.get(id=user_id)	
        dict["user_info"] = user
        dict["events_going"] = user.events_going.all()
        dict["events_organized"] = user.events_organized.all()
        dict["received_invites"] = user.received_invites.all()
        dict["made_invites"] = user.made_invites.all()
        dict["events_maybe"] = user.events_maybe.all()

    if "user_id" in req.session:
        user = User.objects.get(id=req.session["user_id"])
	dict["user"] = user

    return render_to_response('user.html', dict)    

