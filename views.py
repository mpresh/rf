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

def test(request):
    return render_to_response('test.html', {})

def about(request):
    return render_to_response('about.html', {})

def event_list(request):
    all_events = Event.objects.all()
    return render_to_response('list.html', {"events":all_events})

def upload_image(req):
    user = User.objects.get(id=req.session["user_id"])
    cur_dir = os.path.dirname(__file__)

    if not os.path.exists(os.path.join(cur_dir, 'static/images/tmp')):
        os.mkdir(os.path.join(cur_dir, 'static/images/tmp'))
	
    f = req.FILES['image']
    destination = open(os.path.join(cur_dir, 
                                    'static/images/tmp/' + str(user.id) + "_" + f.name), 'wb+')
    for chunk in f.chunks():     
        destination.write(chunk)
    destination.close() 
    return HttpResponse(json.dumps({}))
    
def event_create(request):

    cur_dir = os.path.dirname(__file__)
    
    if "user_id" not in request.session:
        request.session["redirect"] = "/create"        
        return HttpResponseRedirect("/login")

    user = User.objects.get(id=request.session["user_id"])

    if "event_name" in request.POST and request.POST['event_name'] != "":
        ename = request.POST["event_name"]
        start_date = request.POST["event_date_start"]
        end_date = request.POST["event_date_end"]
        start_time = request.POST["event_time_start"]
        end_time = request.POST["event_time_end"]
        ecapacity = request.POST["event_capacity"]
        evenue = request.POST["event_venue"]
        eaddress = request.POST["event_address"]
        edescription = request.POST["event_description"]
        eurl = request.POST["event_url"]
        eprice = request.POST["event_price"]
        image = request.POST["event_image"]
        elat = request.POST["event_lat"]
        elng = request.POST["event_lng"]

        pemail = request.POST["person_email"]
        
        user = User.objects.get(id=request.session["user_id"])
        user.email = pemail
        user.save()

        import datetime
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

        return HttpResponseRedirect("/thanks/" + str(e.id))
	
    return render_to_response('create.html', {"user" : user, 
                                              "key": settings.GOOGLE_MAP_API,
                                              "zoom": 14})

def event_register(request):
    user = User.objects.get(id=req.session["user_id"])	
    return render_to_response('register.html', {"user" : user})

def event_thanks(request, event_id=""):
    if event_id:
        e = Event.objects.get(id=event_id)
        return render_to_response('thanks.html', {"event" : e})
    user = User.objects.get(id=req.session["user_id"])	
    return render_to_response('thanks.html', {"user" : user})

def index(req):
    if "user_id" not in req.session:
        req.session["redirect"] = "/"
        return render_to_response('index.html', {})

    user = User.objects.get(id=req.session["user_id"])	
    req.session["redirect"] = "/"

    return render_to_response('index.html', {"user" : user})

def event_details(req, event_id=""):
    req.session["redirect"] = "/event_details/" + event_id
    if event_id:
        e = Event.objects.get(id=event_id)
        print "DIR", dir(e), e.invitation.all()

        if "user_id" in req.session:
            user = User.objects.get(id=req.session["user_id"])
            print "User registered", dir(user)
            
            # provide information about friends that are attending with profile pic, name, twitter_name, twitter_id
            friends = user.get_friend_list()
            friends_list = []
            for u in e.attendees.all():
                if u.twitter_id in friends:
                    friends_list.append(u)
            return render_to_response('details.html', {"user" : user,
                                                       "event" : e,
                                                       "attendees":friends_list,
                                                       "invites" : e.invitation.all()})
	else:

            # provide people that are attending with profile pic, name, twitter_name, twitter_id
            return render_to_response('details.html', {"event" : e,
                                                       "attendees" : e.attendees.all(),
                                                       "invites" : e.invitation.all()})


    return render_to_response('details.html', {})

def map(request):
    return render_to_response('map.html', {"key": settings.GOOGLE_MAP_API,
                                           "zoom": 14})

def user_details(req):
    if "user_id" in req.session:
        user = User.objects.get(id=req.session["user_id"])	
        return render_to_response('user.html', {"user":user})
    else:
        return render_to_response('user.html')

def event_home(req, event_id=""):
    req.session["redirect"] = "/event_home/" + event_id
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
    if "user_id" in req.session:
        user = User.objects.get(id=req.session["user_id"])	
        
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
            return render_to_response('event_home.html', {"event" : e,
                                                          "user" : user,
                                                          "going" : going,
                                                          "attendees" : e.attendees.all(),
                                                          "map_key" : settings.GOOGLE_MAP_API,
                                                          "invite_url" : invite_url,
                                                          "refer_user": refer_user})
        else:
            return render_to_response('event_home.html', {"user" : user,
                                                          "attendees": [],
                                                          "map_key" : settings.GOOGLE_MAP_API,
                                                          "refer_user": refer_user})

    # not logged in
    else:
        
        if e:
            return render_to_response('event_home.html', {"event" : e,
                                                          "attendees" : e.attendees.all(),
                                                          "map_key" : settings.GOOGLE_MAP_API,
                                                          "refer_user": refer_user})
        else:
            return render_to_response('event_home.html', {"map_key" : settings.GOOGLE_MAP_API,
                                                          "refer_user": refer_user})


def event_add_user(req):
    if "user_id" not in req.session:
        return HttpResponse("ERROR: User must be authenticated!")


    user = User.objects.get(id=req.session["user_id"])	
    #event = Event.objects.get(id=req.POST["event_id"])

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

    return HttpResponse(json.dumps(friends_not_going_to_event))
    

def event_invite_friend(req, event_id=""):
    """
    Invite friend to event.
    """
    if "user_id" not in req.session:
        return HttpResponse("ERROR: User must be authenticated!")

    if not event_id:
        return HttpResponse("ERROR: must provide event_id")

    event = Event.objects.get(id=event_id)
    user = User.objects.get(id=req.session["user_id"])	
            
    key = None
    if "friend_twitter_id" in req.GET:
        friend_twitter_id = req.GET["friend_twitter_id"]
        key = "friend_twitter_id"
    elif "friend_id" in req.GET:
        friend_id = req.GET["friend_id"]
        key = "friend_id"
    elif "friend_username" in req.GET:
        friend_username = req.GET["friend_username"]
        key = "friend_username"

    if not key:
        return HttpResponse("ERROR: user invite info not provided.")

    friend_obj = None
    
    try:
        if key == "friend_twitter_id":
            friend_obj = User.objects.get(twitter_id=friend_twitter_id)
        elif key == "friend_id":
            friend_obj = User.objects.get(id=friend_id)
        else:
            friend_obj = User.objects.get(username=friend_username)
    except:
        return HttpResponse("ERROR: user to invite does not exist.")


    try:
        Invite.objects.get(event=event.id,
                           from_user_id=user.id,
                           to_user_id=friend_obj.id)
        return HttpResponse("Error: this invite already exists.")
    except:
        pass


    i = Invite(message="come to my party",
               from_user_id=1,
               to_user_id=1,
               event_id=1)
    i.save()
    return HttpResponse("Succesfully Invited User.")


def event_not_going(req, event_id=""):
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
    if "user_id" not in req.session:
        return HttpResponse("ERROR: User must be authenticated!")
    
    event = Event.objects.get(id=event_id)
    user = User.objects.get(id=req.session["user_id"])	
    user.events_going.add(event.id)    

    return HttpResponse("Succesfully Going to Event.")

def event_tweet_invite(req, event_id=""):

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

    user.tweet(msg)
    ret_obj["msg"] = "Tweeted: " +  msg
    return HttpResponse(json.dumps(ret_obj))

def event_tweet_invite_dm(req, event_id=""):

    ret_obj = {}

    if "user_id" not in req.session:
        ret_obj["error"] = "User Must be Logged in."
        return HttpResponse(json.dumps(ret_obj))

    event = Event.objects.get(id=event_id)
    user = User.objects.get(id=req.session["user_id"])	
    
    url = req.GET['invite_url']
    friends = req.GET['invited_friends'].split(",")
    
    if 'data' in req.GET and req.GET['data'].strip() != "":
        msg = url + " " + req.GET['data']
    else:
        msg = url + ": Dicounted Invite to " + event.name

    if len(msg) > 140:
        msg = msg[:140]

    dict = {}
    dict["cmd"] = "twitter_dm_users"
    dict["username"] = user.username

    data = {}
    dict["data"] = data
    dict["data"]["oauth_token"] = user.oauth_token
    dict["data"]["oauth_token_secret"] = user.oauth_token_secret
    dict["data"]["users"] = friends
    dict["data"]["msg"] = msg
    to_send = json.dumps(dict) + "\n\r\n"

    print "TO SEND", to_send
		
    port = 5002
    host = "localhost"

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send(to_send)

    print "connection made", to_send
    buf = ""
    while 1:
        print "Waiting to receive"
        incoming = s.recv(1000)
        print "received ", incoming
        if not incoming:
            break
        buf += incoming
    s.close()

    print "connection closed"
    ret_obj = {}
    ret_obj["ret"] = buf
    ret_obj["msg"] = "Sent DM to " + " ".join(friends) +  " " + msg

    print "HEY THERE"
    ret_val = json.dumps(ret_obj)
    print "RETURN", ret_val
    return HttpResponse(ret_val)
