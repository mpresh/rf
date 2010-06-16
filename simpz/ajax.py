from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from events.models import Event, Invite
from tauth.models import User
from django.conf import settings
import simplejson as json
import urllib
import os
import hashlib
import base64
import shutil
import socket
import datetime

AFETCH_PORT = 5002
AFETCH_HOST = "localhost"


def upload_image(req):
    """Upload an image from the creation page onto server."""

    user = User.objects.get(id=req.session["user_id"])
    cur_dir = os.path.join(os.path.dirname(__file__), "..")

    if not os.path.exists(os.path.join(cur_dir, 'static/images/tmp')):
        os.mkdir(os.path.join(cur_dir, 'static/images/tmp'))
	
    f = req.FILES['image']
    destination = open(os.path.join(cur_dir, 
                                    'static/images/tmp/' + str(user.id) + "_" + f.name), 'wb+')
    for chunk in f.chunks():     
        destination.write(chunk)
    destination.close() 
    return HttpResponse(json.dumps({}))

def event_add_user(req):
    """Add user to event as attendee."""
    if "user_id" not in req.session:
        return HttpResponse("ERROR: User must be authenticated!")

    user = User.objects.get(id=req.session["user_id"])	

    if "event_id" in req.POST:
        user.events_going.add(req.POST["event_id"])
        return HttpResponse("User added to event")
    return HttpResponse("ERROR: event_id must be passed in POST")

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

    if "user_id" not in req.session:
        return HttpResponse("ERROR: User must be authenticated!")

    if not event_id:
            return HttpResponse("ERROR: must provide event_id")

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
    if "user_id" not in req.session:
        return HttpResponse("ERROR: User must be authenticated!")
    
    if not event_id:
        return HttpResponse("ERROR: must provide event_id")

    event = Event.objects.get(id=event_id)
    user = User.objects.get(id=req.session["user_id"])

    friends_not_going_to_event = user.get_friends_not_attending_event(event)
    print "HERE I AM", friends_not_going_to_event

    return HttpResponse(json.dumps(friends_not_going_to_event))
    
def event_not_going(req, event_id=""):
    """ Not goign to event."""
    if "user_id" not in req.session:
        return HttpResponse("ERROR: User must be authenticated!")

    print "NOT GOING!!!"
    event = Event.objects.get(id=event_id)
    user = User.objects.get(id=req.session["user_id"])	
    
    try:
        event.attendees.remove(user)
        user.events_going.remove(event)
    except:
        pass
    return HttpResponse("Succesfully Not Going to Event.")

def event_going(req, event_id=""):
    """ Going to event. """
    if "user_id" not in req.session:
        return HttpResponse("ERROR: User must be authenticated!")
    
    event = Event.objects.get(id=event_id)
    user = User.objects.get(id=req.session["user_id"])	
    user.events_going.add(event.id)    

    return HttpResponse("Succesfully Going to Event.")

def event_tweet_invite(req, event_id=""):
    """ Tweet out invite to everyone. """
    ret_obj = {}

    if "user_id" not in req.session:
        ret_obj["error"] = "User Must be Logged in."
        return HttpResponse(json.dumps(ret_obj))

    event = Event.objects.get(id=event_id)
    user = User.objects.get(id=req.session["user_id"])	

    url = req.GET['invite_url']
    if 'data' in req.GET and req.GET['data'].strip() != "":
        msg = url + req.GET['data']
    else:
        msg = url + ": Dicounted Invite to " + event.name

    if len(msg) > 140:
        msg = msg[:140]

    (u, c) = User.objects.get_or_create(username="DEFAULT")
    (invite, created) = Invite.objects.get_or_create(from_user=user,
                                                     to_user=u,
                                                     event=event)
    invite.message = msg
    invite.save()

    user.tweet(msg)
    ret_obj["msg"] = "Tweeted: " +  msg
    return HttpResponse(json.dumps(ret_obj))

def event_tweet_invite_dm(req, event_id=""):
    """ Send invite to one person."""
    ret_obj = {}

    if "user_id" not in req.session:
        ret_obj["error"] = "User Must be Logged in."
        return HttpResponse(json.dumps(ret_obj))

    event = Event.objects.get(id=event_id)
    user = User.objects.get(id=req.session["user_id"])	
    
    url = req.GET['invite_url']
    friends = req.GET['invited_friends'].split(",")
    
    if 'data' in req.GET and req.GET['data'].strip() != "":
        msg = req.GET['data']
    else:
        msg = ": Dicounted Invite to " + event.name

    # shorten message so that it fits into a tweet
    if len(msg) > 115:
        msg = msg[:115]
    msg = url + " " + msg

    # iterate over friends and create a friend User record for each if doesnt exist
    # create invite record for each
    new_friends = []
    for friend in friends:
        (u, created_user) = User.objects.get_or_create(username=friend)
        (invite, created_invite) = Invite.objects.get_or_create(from_user=user,
                                                                to_user=u,
                                                                event=event)
        invite.message = msg
        invite.save()

        if created_invite:
            new_friends.append(friend)

    dict = {}
    dict["cmd"] = "twitter_dm_users"
    dict["username"] = user.username

    data = {}
    data["oauth_token"] = user.oauth_token
    data["oauth_token_secret"] = user.oauth_token_secret
    data["users"] = new_friends
    data["msg"] = msg
    dict["data"] = data
    to_send = json.dumps(dict) + "\n\r\n"

    afetch_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    afetch_socket.connect((AFETCH_HOST, AFETCH_PORT))
    afetch_socket.send(to_send)

    buffer = ""
    while 1:
        incoming = afetch_socket.recv(1000)
        if not incoming:
            break
        buffer += incoming
    afetch_socket.close()

    ret_obj = {}
    ret_obj["ret"] = buffer
    ret_obj["msg"] = "Sent DM to " + " ".join(friends) +  " " + msg

    ret_val = json.dumps(ret_obj)
    return HttpResponse(ret_val)
