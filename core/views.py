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
    
def index(req):
    return render_to_response('index.html', {})

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

def invite(req):
    #req.session["redirect"] = req.get_full_path()
    invite = None
    
    dict = {}
    if "user_id" in req.session:
        user = User.objects.get(id=req.session["user_id"])	
        dict['user'] = user
    else:
        user = None

    if not invite:
        return render_to_response('404.html', dict)
    
    dict["event"] = Event.objects.get(id=invite.event_id)
    dict['invite_url'] = util.get_invite_url(req)    
    dict["from_user"] = User.objects.get(id=invite.from_user_id)
    dict["to_user"] = User.objects.get(id=invite.to_users.all()[0].id)
    dict["attendees"] = invite.event.attendees.all()
    dict["map_key"]  = settings.GOOGLE_MAP_API    
    dict["created_at"]  = invite.created_at
    dict["msg"]  = invite.message
    dict['invite_id'] = invite_id

    if user:
        # if this invite is not for you, don't show page
        to_users = invite.to_users.all()
        to_user_ids = [u.id for u in to_users]
        to_user_usernames = [u.username for u in to_users]

        if user.id not in to_user_ids and "DEFAULT" not in to_user_usernames: 
            return HttpResponseRedirect(reverse("event_home", kwargs={"event_id":dict["event"].id}))

        going = False
        for event in user.events_going.all():
            if event.id == dict["event"].id:
                going = True

        dict['going'] = going
        
    return render_to_response('invite.html', dict)

def blogvip_flow(req):
    """ Request handler for blogger discount page."""
    req.session["refer_domain"] = req.META['HTTP_HOST'].split(".")[0]
    invite = None
    event = None
    
    if "event" in req.GET:
        event_id = req.GET["event"]
        #req.session["redirect"] = req.get_full_path()

        try:
            event = Event.objects.get(id=event_id)
            campaign = event.campaign
        except ObjectDoesNotExist:
            event = None
    elif "ehash" in req.GET:
        ehash = req.GET["ehash"]
        #req.session["redirect"] = req.get_full_path()

        try:
            event = Event.objects.get(ehash=ehash)
            campaign = event.campaign
        except ObjectDoesNotExist:
            event = None


    dict = {}
    dict["fbappid"] = settings.FACEBOOK_APP_ID
    
    if "overlay" in req.GET:
        dict["overlay"] = True
        if req.GET["overlay"] == "facebook":
            dict["overlayFacebook"] = True
        elif req.GET["overlay"] == "twitter":
            dict["overlayTwitter"] = True    
        elif req.GET["overlay"] == "true":
            dict["overlayTrue"] = True    


    if "shash" in req.GET:
        dict["shash"] = req.GET["shash"]
    else:
        dict["shash"] = ""

    # twitter user
    if "user_id" in req.session:
        user = User.objects.get(id=req.session["user_id"])	
        dict['user'] = user
    else:
        user = None

    # facebook user
    if "uid" in req.session:
        fbuser = FBUser.objects.get(facebook_id=req.session["uid"])	
        dict['fbuser'] = fbuser
    elif "uid" in req.COOKIES:
        fauth_utils.sync_session_cookies(req)
        fbuser = FBUser.objects.get(facebook_id=req.COOKIES["uid"])	
        dict['fbuser'] = fbuser
    else:
        fbuser = None
        dict["fbuser"] = ""

    if not event:
        return render_to_response('404.html', dict)
    
    dict["event"] = event
    dict["campaign"] = campaign 
    dict['invite_url'] = util.get_invite_url(req)    
    dict["attendees"] = event.attendees.all()
    dict["map_key"]  = settings.GOOGLE_MAP_API    

    event_start = event.event_date_time_start
    event_end = event.event_date_time_end
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    start_month = months[event_start.month]
    end_month = months[event_end.month]
    if start_month == end_month:
        if str(event_start.day) == str(event_end.day):
            dict["date_label"] = "%s %s" % (start_month, str(event_start.day))
        else:
            dict["date_label"] = "%s %s - %s " % (start_month, str(event_start.day), str(event_end.day))
    else:
        dict["date_label"] = "%s %s - %s %s " % (start_month + str(event_start.day), end_month, str(event_end.day))

    dict["time_label"] = event_start.strftime("%I:%M %p %Z").strip("0")

    for image_type in ['.png', '.gif', 'jpg', '.jpeg', ""]:
        if os.path.exists(os.path.join(settings.ROOT_PATH, 'static/images/event_logos/' + str(event.id) + image_type)):
            dict["logo"] = str(event.id) + image_type
            
    if os.path.exists(os.path.join(settings.ROOT_PATH, 'static/css/event_css/' + str(event.id) + ".css")):
        dict["css"] = str(event.id) + ".css"


    template_path = os.path.join(os.path.dirname(__file__), 'templates/event_templates/' + str(event.id) + ".html")
    if os.path.exists(template_path):
        return render_to_response(str(event.id) + '.html', dict)
    else:
        return render_to_response("blogvip_flow.html", dict)

def event_home(req, event_id=""):
    #req.session["redirect"] = req.get_full_path()
    if event_id:
        e = Event.objects.get(id=event_id)
    else:
        e = None
    
    # logged in
    e.num_attendees = len(e.attendees.all())
    e.spots_left = e.capacity - e.num_attendees
    e.discount_price = e.price / 2
    e.time = e.event_date_time_start.strftime("%A, %B %d, %Y @ %I:%M %p %Z")

    invites = e.invitations.all()
    invite = invites[0]
    # redirect to invite
    return HttpResponseRedirect(reverse('event_invite', kwargs={"invite_id":invite.id}))

    dict = {}
    dict['event'] = e
    dict["map_key"]  = settings.GOOGLE_MAP_API
    #dict["refer_user"] = refer_user
    dict['attendees'] = []

    if "user_id" in req.session:
        user = User.objects.get(id=req.session["user_id"])	
        dict['user'] = user

        if e:
            going = False
            for event in user.events_going.all():
                if event.id == e.id:
                    going = True

            invite_url = util.get_invite_url(req)

            #if invite_url.find("?") == -1:
            #    invite_url = invite_url + "?"
            #invite_url = invite_url + "&refer=" + base64.b64encode(user.username)
            dict['going'] = going
            dict['attendees'] = e.attendees.all()
            dict['invite_url'] = invite_url
            return render_to_response('invite.html', dict) 
                                      
        else:
            return render_to_response('invite.html', dict)
                                                          
    # not logged in
    else:
        
        if e:
            dict["attendees"] = e.attendees.all()
            return render_to_response('invite.html', dict)                                
        else:
            return render_to_response('invite.html', dict)

