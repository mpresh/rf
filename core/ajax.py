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
from pylib import bitly
import urlparse

AFETCH_PORT = 5002
AFETCH_HOST = "localhost"


def upload_image(req):
    """Upload an image from client to server."""
    f = req.FILES[req.GET['file_name']]
    cid = req.GET['camp_id']
    image_purpose = req.GET['image_purpose']

    campaign = Campaign.objects.get(id=cid)
    destination_dir = os.path.join(settings.ROOT_PATH, 'static/images/campaign/logos/' + image_purpose + '/')
    if not os.path.exists(destination_dir):
        os.system("mkdir -p " + destination_dir)

    image_file = os.path.join(destination_dir, str(campaign.id))
    if os.path.exists(image_file):
        os.system("rm -f " + image_file)
    destination = open(image_file, 'wb+')
    
    for chunk in f.chunks():     
        destination.write(chunk)
    destination.close() 
    return HttpResponse(json.dumps({}))

def event_add_user(req):
    """Add user to event as attendee."""
    if "user_id" not in req.session:
        return HttpResponse("ERROR: User must be authenticated!")

    user = User.objects.get(id=req.session["user_id"])	

    dict = {}
    if "event_id" in req.POST:
        user.events_going.add(Event.objects.get(id=req.POST["event_id"]))
        dict = {}
        dict["status"] = "ok"
        return HttpResponse(json.dumps(attendees_list))
    
    dict["status"] = "error"
    dict["message"] = "event_id must be passed in POST"
    return HttpResponse(json.dumps(dict))

def event_attendees(req, event_id=""):
    """ 
    Retreive a list of users going to the event.
    Relevant information. Photo url, name.
    """

    if not event_id:
            return HttpResponse("ERROR: must provide event_id")
    event = Event.objects.get(id=event_id)
    
    attendees_list = []
    for person in event.attendees.all():
        attendees_list.append([person.profile_pic, person.name])

    return HttpResponse(json.dumps(attendees_list))

def event_friend_attendees(req, event_id=""):
    """
    Retreive friends that are going to the event.
    Relevant information includes: photo url, name.
    """

    dict = {}
    if "user_id" not in req.session:
        dict["status"] = "error"
        dict["message"] = "user must be authenticated"
        return HttpResponse(json.dumps(dict))

    if not event_id:
        dict["status"] = "error"
        dict["message"] = "must provide event_id"
        return HttpResponse(json.dumps(dict))

    event = Event.objects.get(id=event_id)
    user = User.objects.get(id=req.session["user_id"])	

    user_frineds_list = user.get_friend_list()
    
    event_friend_attendees = []

    for person in event.attendees.all():
        if person.twitter_id in user_friends_list:
            event_friend_attendees.append([person.profile_pic, person.name])

    return HttpResponse(json.dumps(event_friend_attendees))

def event_friend_not_attendees(req, event_id=""):
    """
    Retreive friends that are not going to the event.
    Phot url, name.
    """
    dict = {}
    if "user_id" not in req.session:
        dict["status"] = "error"
        dict["message"] = "User must be authenticated!"
        return HttpResponse(json.dumps(attendees_list))
    
    if not event_id:
        dict["status"] = "error"
        dict["message"] = "must provide event_id"
        return HttpResponse(json.dumps(attendees_list))

    event = Event.objects.get(id=event_id)
    user = User.objects.get(id=req.session["user_id"])

    friends_not_going_to_event = user.get_friends_not_attending_event(event)

    return HttpResponse(json.dumps(friends_not_going_to_event))
    
def event_not_going(req, event_id=""):
    """ Not goign to event."""
    if "user_id" not in req.session:
        return HttpResponse("ERROR: User must be authenticated!")

    event = Event.objects.get(id=event_id)
    user = User.objects.get(id=req.session["user_id"])	
    
    try:
        event.attendees.remove(user)
        user.events_going.remove(event)
    except:
        pass

    dict = {}
    dict["status"] = "ok"
    dict["message"] = "not going to event"
    return HttpResponse(json.dumps(dict))

def event_going(req, event_id=""):
    """ Going to event. """
    if "user_id" not in req.session:
        return HttpResponse("ERROR: User must be authenticated!")
    
    event = Event.objects.get(id=event_id)
    user = User.objects.get(id=req.session["user_id"])	
    user.events_going.add(event.id)    

    dict = {}
    dict["status"] = "ok"
    dict["message"] = "going to event"
    return HttpResponse(json.dumps(dict))

def campaign_going_twitter(req, campaign_id=""):
    """ Going to event. """
    if "user_id" not in req.session:
        return HttpResponse("ERROR: User must be authenticated!")
    
    campaign = Campaign.objects.get(id=campaign_id)
    user = User.objects.get(id=req.session["user_id"])	
    user.campaign_interested.add(campaign.id)    

    dict = {}
    dict["status"] = "ok"
    dict["message"] = "going to event"
    return HttpResponse(json.dumps(dict))


def event_tweet_invite(req, event_id=""):
    """ Tweet out invite to everyone. """
    ret_obj = {}

    if "user_id" not in req.session:
        ret_obj["status"] = "error"
        ret_obj["message"] = "User Must be Logged in."
        return HttpResponse(json.dumps(ret_obj))

    user = User.objects.get(id=req.session["user_id"])	

    msg=req.GET["message"]
    if len(msg) > 125:
        msg = msg[:125]

    if "shash" in req.GET:
        parent_shash = req.GET["shash"]
    elif "shash" in req.POST:
        parent_shash = req.POST["shash"]
    else:
        parent_shash = None

    share = Share(message=msg,
                  event=Event.objects.get(id=event_id),
                  from_user_facebook=None,
                  from_user_twitter=user,
                  from_account_type="T",
                  parent_shash=parent_shash,
                  reach=user.get_num_follower_list()
                  )
    share.save()

    share.setHash()

    url = share.url(req)
    short_url = bitly.shorten(url)

    share.url_short = short_url
    msg = msg + " " + short_url

    share.save()
    user.tweet(msg)

    dict = {}
    dict["status"] = "ok!"
    dict["url"] = short_url
    dict["msg"] = msg
    return HttpResponse(json.dumps(dict))


def campaign_tweet_invite(req, campaign_id=""):
    """ Tweet out invite to everyone. """
    ret_obj = {}

    if "user_id" not in req.session:
        ret_obj["status"] = "error"
        ret_obj["message"] = "User Must be Logged in."
        return HttpResponse(json.dumps(ret_obj))

    user = User.objects.get(id=req.session["user_id"])	

    campaign=Campaign.objects.get(id=campaign_id)

    user.campaign_interested.add(campaign.id)    
    dict = tweet_wrapper(req, campaign_id)
    if dict["status"] == "ok!":
        user.follow(campaign.twitter_account)
        
    return HttpResponse(json.dumps(dict))
        

def get_discount_twitter(req, campaign_id=""):
    """ Get discount code via twitter login. """
    ret_obj = {}

    if "user_id" not in req.session:
        ret_obj["status"] = "error"
        ret_obj["message"] = "User Must be Logged in."
        return HttpResponse(json.dumps(ret_obj))

    user = User.objects.get(id=req.session["user_id"])	
    campaign=Campaign.objects.get(id=campaign_id)
    
    user.campaign_interested.add(campaign.id)    
    for attr_obj in campaign.attributes.all():
        if (attr_obj.name == "post"):
            dict = tweet_wrapper(req, campaign_id)
            if dict["status"] != "ok!":
                break
        if (attr_obj.name == "follow"):
            user.follow(campaign.twitter_account)

    return HttpResponse(json.dumps(dict))
        

def tweet_wrapper(req, campaign_id=""):
    user = User.objects.get(id=req.session["user_id"])	

    msg=req.GET["message"]
    if len(msg) > 125:
        msg = msg[:125]

    if "shash" in req.GET:
        parent_shash = req.GET["shash"]
    elif "shash" in req.POST:
        parent_shash = req.POST["shash"]
    else:
        parent_shash = None

    if "parent_url" in req.GET:
        parent_url = req.GET["parent_url"]
        parent_url = urllib.unquote(parent_url)
        parsed_url = urlparse.urlparse(parent_url)
        try:
            list_vals = parsed_url.query.split("&")
        except Exception:
            list_vals = parsed_url[4]
        print "parsed_url", parsed_url
        print "list vals", list_vals
        dict = {}
        for val in list_vals:
            if val:
                k, v = val.split("=")
                dict[k] = v
        if "shash" in dict:
            parent_shash = dict["shash"][0]
    else:
        parent_url = None

    share = Share(message=msg,
                  campaign=Campaign.objects.get(id=campaign_id),
                  from_user_facebook=None,
                  from_user_twitter=user,
                  from_account_type="T",
                  parent_shash=parent_shash,
                  reach=user.get_num_follower_list()
                  )

    
    share.save()

    share.setHash()
    url = share.url(req, parent=parent_url)
    short_url = bitly.shorten(url)
    share.url_short = short_url
    msg = msg + " " + short_url

    share.save()
    user.tweet(msg)

    dict = {}
    dict["status"] = "ok!"
    dict["url"] = short_url
    dict["msg"] = msg
    return (dict)



