from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from events.models import Event, Invite
from tauth.models import User
from fauth.models import FBUser
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

def test(req):
    req.session["redirect"] = "/simpz/test"        
    return render_to_response('test.html', {})

def about(req):
    req.session["redirect"] = "/simpz/about"        
    return render_to_response('about.html', {})

def event_list(req):
    req.session["redirect"] = "/simpz/list"        
    all_events = Event.objects.all()
    if "user_id" in req.session:
        user = User.objects.get(id=req.session["user_id"])
        return render_to_response('list.html', {"events":all_events,
                                                "user" : user})

    return render_to_response('list.html', {"events":all_events})
    
def event_create(req):
    cur_dir = os.path.join(os.path.dirname(__file__), "..")
    invite_url = util.get_invite_url(req)

    if "user_id" not in req.session:
        req.session["redirect"] = "/simpz/create"        
        return HttpResponseRedirect("/simpz/login")

    user = User.objects.get(id=req.session["user_id"])

    if "event_name" in req.POST and req.POST['event_name'] != "":
        ename = req.POST["event_name"]
        start_date = req.POST["event_date_start"]
        end_date = req.POST["event_date_end"]
        start_time = req.POST["event_time_start"]
        end_time = req.POST["event_time_end"]
        ecapacity = req.POST["event_capacity"]
        evenue = req.POST["event_venue"]
        eaddress = req.POST["event_address"]
        edescription = req.POST["event_description"]
        eurl = req.POST["event_url"]
        eprice = req.POST["event_price"]
        image = req.POST["event_image"]
        elat = req.POST["event_lat"]
        elng = req.POST["event_lng"]

        pemail = req.POST["person_email"]
        
        user = User.objects.get(id=req.session["user_id"])
        user.email = pemail
        user.save()

        start_dt = datetime.datetime.strptime(start_date.strip() + " " + start_time.strip(), 
                                     "%m/%d/%Y %I:%M %p")
        end_dt = datetime.datetime.strptime(end_date.strip() + " " + end_time.strip(), 
                                            "%m/%d/%Y %I:%M %p")

        e = Event(name=ename, 
                  description=edescription, 
                  event_date_time_start=start_dt,
                  event_date_time_end=end_dt,
                  capacity=ecapacity,
                  venue=evenue,
                  venue_address=eaddress,
                  organizer_id=user.id,
                  url=eurl,
                  price=eprice,
                  lat=elat,
                  lng=elng)
        e.save()

        if not os.path.exists(os.path.join(cur_dir, 'static/images/events/')):
            os.mkdir(os.path.join(cur_dir, 'static/images/events'))
			
        if image:
            os.rename(os.path.join(cur_dir, 'static/images/tmp/' + str(user.id) + '_' + image),
                  	os.path.join(cur_dir, 'static/images/events/' + str(e.id)))
        else:
          	shutil.copy(os.path.join(cur_dir, 'static/images/muse.png'),
                       os.path.join(cur_dir, 'static/images/events/' + str(e.id)))

        (u, c) = User.objects.get_or_create(username="DEFAULT")
        (invite, created) = Invite.objects.get_or_create(from_user=user,
                                                         event=e)
        invite.to_users.add(u)
        
        return HttpResponseRedirect("/simpz/thanks/" + str(invite.id))
	
    dict = {}
    dict["user"] = user
    dict["key"] = settings.GOOGLE_MAP_API
    dict["zoom"] = 14
    dict["invite_url"] = invite_url
    return render_to_response('create.html', dict)

def event_thanks(req, invite_id=""):
    req.session["redirect"] = "/simpz/thanks/" + invite_id        
    if "user_id" not in req.session:
        return HttpResponseRedirect("/simpz/login")

    dict = {}
    user = User.objects.get(id=req.session["user_id"])	
    dict["user"] = user

    if invite_id:
        invite = Invite.objects.get(id=invite_id)
        dict["invite"] = invite
        dict["from_user"] = User.objects.get(id=invite.from_user_id)
        dict["to_user"] = User.objects.get(id=invite.to_users.all()[0].id)
        dict["event"] = Event.objects.get(id=invite.event_id)

    if dict["from_user"].id != user.id:
        return HttpResponseRedirect("/simpz/")
    if dict["event"].organizer_id != user.id:
        return HttpResponseRedirect("/simpz/")

    dict["invite_url"] = util.get_invite_url(req) + str(invite.id)
    return render_to_response('thanks.html', dict)

def index(req):
    print "COOKIES", req.COOKIES
    print "KEYS....."
    for key in req.session.keys():
        print "KEY", key, req.session[key]

    dict = {}
    if "uid" in req.session:
        dict["facebook"] = req.session['uid']

    req.session["redirect"] = "/simpz/"        
    if "user_id" not in req.session:
        print "returning ", dict
        return render_to_response('index.html', dict)

    
    user = User.objects.get(id=req.session["user_id"])	
    req.session["redirect"] = "/simpz/"
    dict["user"] = user

    print dict
    return render_to_response('index.html', dict)

def event_details(req, event_id=""):

    dict = {}
    if "user_id" in req.session:
        user = User.objects.get(id=req.session["user_id"])
        dict['user'] = user

    req.session["redirect"] = "/simpz/event_details/" + event_id
    if event_id:
        e = Event.objects.get(id=event_id)
        dict['event'] = e
        dict['invites'] = e.invitations.all()
        dict['attendees'] = e.attendees.all()
        dict['attendees_maybe'] = e.attendees_maybe.all()
            
        invites = Invite.objects.filter(event=e.id)
        dict['invites'] = invites

        return render_to_response('details.html', dict)
	
    return render_to_response('details.html', dict)

def map(request):
    return render_to_response('map.html', {"key": settings.GOOGLE_MAP_API,
                                           "zoom": 14})

def user_details(req, user_id=""):
    req.session["redirect"] = "/simpz/user_details/" + user_id

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

def invite(req, invite_id):
    req.session["redirect"] = "/simpz/invite/" + invite_id
    invite = None
    if invite_id:
        try:
            invite = Invite.objects.get(id=invite_id)
        except ObjectDoesNotExist:
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
        print "TO USERS", to_users
        to_user_ids = [u.id for u in to_users]
        to_user_usernames = [u.username for u in to_users]

        print to_user_ids, to_user_usernames
        if user.id not in to_user_ids and "DEFAULT" not in to_user_usernames: 
            return HttpResponseRedirect("/simpz/event_home/" + str(dict["event"].id) + "/")

        going = False
        for event in user.events_going.all():
            if event.id == dict["event"].id:
                going = True

        dict['going'] = going
        
    return render_to_response('invite.html', dict)

def blogvip(req, invite_id):
    for key in req.GET.keys():
        print "KEY GET", key, req.GET[key]

    for key in req.session.keys():
        print "KEY SESSION", key, req.session[key]

    for key in req.COOKIES.keys():
        print "KEY COOKIE", key, req.COOKIES[key]

    req.session["redirect"] = "/simpz/blogvip/" + invite_id
    invite = None
    if invite_id:
        try:
            invite = Invite.objects.get(id=invite_id)
        except ObjectDoesNotExist:
            invite = None

    dict = {}
    if "overlay" in req.GET:
        dict["overlay"] = True

    if "user_id" in req.session:
        user = User.objects.get(id=req.session["user_id"])	
        dict['user'] = user
    else:
        user = None

    if "uid" in req.session:
        print "FBUSER ID", req.session["uid"]
        fbuser = FBUser.objects.get(facebook_id=req.session["uid"])	
        dict['fbuser'] = fbuser
    elif "uid" in req.COOKIES:
        print "calling sync from blogvip"
        fauth_utils.sync_session_cookies(req)
        print "FBUSER ID", req.COOKIES["uid"]
        fbuser = FBUser.objects.get(facebook_id=req.COOKIES["uid"])	
        dict['fbuser'] = fbuser
    else:
        fbuser = None

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
        print "TO USERS", to_users
        to_user_ids = [u.id for u in to_users]
        to_user_usernames = [u.username for u in to_users]

        print to_user_ids, to_user_usernames
        if user.id not in to_user_ids and "DEFAULT" not in to_user_usernames: 
            return HttpResponseRedirect("/simpz/event_home/" + str(dict["event"].id) + "/")

        going = False
        for event in user.events_going.all():
            if event.id == dict["event"].id:
                going = True

        dict['going'] = going
        
    return render_to_response('blogvip.html', dict)

def blogvip_flow(req, invite_id):
    req.session["redirect"] = "/simpz/blogvip_flow/" + invite_id
    invite = None
    if invite_id:
        try:
            invite = Invite.objects.get(id=invite_id)
        except ObjectDoesNotExist:
            invite = None

    dict = {}
    if "overlay" in req.GET:
        dict["overlay"] = True

    if "user_id" in req.session:
        user = User.objects.get(id=req.session["user_id"])	
        dict['user'] = user
    else:
        user = None



    if "uid" in req.session:
        print "FBUSER ID", req.session["uid"]
        fbuser = FBUser.objects.get(facebook_id=req.session["uid"])	
        dict['fbuser'] = fbuser
    elif "uid" in req.COOKIES:
        print "calling sync from blogvip"
        fauth_utils.sync_session_cookies(req)
        print "FBUSER ID", req.COOKIES["uid"]
        fbuser = FBUser.objects.get(facebook_id=req.COOKIES["uid"])	
        dict['fbuser'] = fbuser
    else:
        fbuser = None

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
        print "TO USERS", to_users
        to_user_ids = [u.id for u in to_users]
        to_user_usernames = [u.username for u in to_users]

        print to_user_ids, to_user_usernames
        if user.id not in to_user_ids and "DEFAULT" not in to_user_usernames: 
            return HttpResponseRedirect("/simpz/event_home/" + str(dict["event"].id) + "/")

        going = False
        for event in user.events_going.all():
            if event.id == dict["event"].id:
                going = True

        dict['going'] = going
        
    return render_to_response('blogvip_flow.html', dict)


def event_home(req, event_id=""):
    req.session["redirect"] = "/simpz/event_home/" + event_id
    if event_id:
        e = Event.objects.get(id=event_id)
    else:
        e = None
    
    #if 'refer' in req.GET:
    #    refer_username = base64.b64decode(req.GET['refer'])
    #    refer_user = User.objects.get(username=refer_username)	
    #else:
    #    refer_user = None

    # logged in
    e.num_attendees = len(e.attendees.all())
    e.spots_left = e.capacity - e.num_attendees
    e.discount_price = e.price / 2
    e.time = e.event_date_time_start.strftime("%A, %B %d, %Y @ %I:%M %p %Z")

    invites = e.invitations.all()
    invite = invites[0]
    # redirect to invite
    return HttpResponseRedirect("/simpz/invite/" + str(invite.id) + "/")

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
            #dict['invite_id'] = Invite.objects.get(event_id=e.id, from_user_id=user.id)
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

