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

        return HttpResponseRedirect("/simpz/thanks/" + str(e.id))
	
    return render_to_response('create.html', {"user" : user, 
                                              "key": settings.GOOGLE_MAP_API,
                                              "zoom": 14})

def event_thanks(req, event_id=""):
    req.session["redirect"] = "/simpz/thanks"        
    if event_id:
        e = Event.objects.get(id=event_id)
        return render_to_response('thanks.html', {"event" : e})
    user = User.objects.get(id=req.session["user_id"])	
    return render_to_response('thanks.html', {"user" : user})

def index(req):
    req.session["redirect"] = "/simpz/"        
    if "user_id" not in req.session:
        req.session["redirect"] = "/simpz/"
        return render_to_response('index.html', {})

    user = User.objects.get(id=req.session["user_id"])	
    req.session["redirect"] = "/simpz/"

    return render_to_response('index.html', {"user" : user})

def event_details(req, event_id=""):

    dict = {}
    if "user_id" in req.session:
        user = User.objects.get(id=req.session["user_id"])
        dict['user'] = user

    req.session["redirect"] = "/simpz/event_details/" + event_id
    if event_id:
        e = Event.objects.get(id=event_id)
        dict['event'] = e
        dict['invites'] = e.invitation.all()
        dict['attendess'] = e.attendees.all()
            
        invites = Invite.objects.filter(event=e.id)
        dict['invites'] = invites

        return render_to_response('details.html', dict)
	
    return render_to_response('details.html', dict)

def map(request):
    return render_to_response('map.html', {"key": settings.GOOGLE_MAP_API,
                                           "zoom": 14})

def user_details(req, user_id=""):
    req.session["redirect"] = "/simpz/user_details/" + user_id

    if user_id:
        user = User.objects.get(id=user_id)	
        return render_to_response('user.html', {"user":user})

    if "user_id" in req.session:
        user = User.objects.get(id=req.session["user_id"])	
        return render_to_response('user.html', {"user":user})
    else:
        return render_to_response('user.html')

def event_home(req, event_id=""):
    req.session["redirect"] = "/simpz/event_home/" + event_id
    if event_id:
        e = Event.objects.get(id=event_id)
    else:
        e = None
    
    if 'refer' in req.GET:
        refer_username = base64.b64decode(req.GET['refer'])
        refer_user = User.objects.get(username=refer_username)	
    else:
        refer_user = None

    # logged in
    e.num_attendees = len(e.attendees.all())
    e.spots_left = e.capacity - e.num_attendees
    e.discount_price = e.price / 2
    e.time = e.event_date_time_start.strftime("%A, %B %d, %Y @ %I:%M %p %Z")

    dict = {}
    dict['event'] = e
    dict["map_key"]  = settings.GOOGLE_MAP_API
    dict["refer_user"] = refer_user
    dict['attendees'] = []

    if "user_id" in req.session:
        user = User.objects.get(id=req.session["user_id"])	
        dict['user'] = user

        if e:
            going = False
            for event in user.events_going.all():
                if event.id == e.id:
                    going = True

            invite_url = req.build_absolute_uri() 
            if invite_url.find("?") == -1:
                invite_url = invite_url + "?"
            #invite_url = invite_url + "&refer=" + hashlib.sha1(user.name + e.name).hexdigest()[:8]
            invite_url = invite_url + "&refer=" + base64.b64encode(user.username)
            dict['going'] = going
            dict['attendees'] = e.attendees.all()
            dict['invite_url'] = invite_url
            return render_to_response('event_home.html', dict) 
                                      
        else:
            return render_to_response('event_home.html', dict)
                                                          
    # not logged in
    else:
        
        if e:
            dict["attendees"] = e.attendees.all()
            return render_to_response('event_home.html', dict)                                
        else:
            return render_to_response('event_home.html', dict)

