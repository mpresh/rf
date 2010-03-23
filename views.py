from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from demo.events.models import Event, Invite
from demo.tauth.models import User
from django.conf import settings
import simplejson as json

def about(request):
    return render_to_response('about.html', {})

def event_list(request):
    all_events = Event.objects.all()
    return render_to_response('list.html', {"events":all_events})

def event_create(request):

    if "user_id" not in request.session:
        request.session["redirect"] = "/create"
        return HttpResponseRedirect("/login")

    if "event_name" in request.POST and request.POST['event_name'] != "":
        ename = request.POST["event_name"]
        estart = request.POST["event_datetime_start"]
        eend = request.POST["event_datetime_end"]
        ecapacity = request.POST["event_capacity"]
        evenue = request.POST["event_venue"]
        eaddress = request.POST["event_address"]
        edescription = request.POST["event_description"]
        eurl = request.POST["event_url"]
        eprice = request.POST["event_price"]

        pemail = request.POST["person_email"]
        
        user = User.objects.get(id=request.session["user_id"])
        user.email = pemail
        user.save()

        import datetime
        e = Event(name=ename, 
                  description=edescription, 
                  event_date_time_start=datetime.datetime.now(),
                  event_date_time_end=datetime.datetime.now(),
                  capacity=ecapacity,
                  venue=evenue,
                  venue_address=eaddress,
                  organizer_id=user.id,
                  url=eurl,
                  price=eprice)
        e.save()

        return HttpResponseRedirect("/thanks/" + str(e.id))

    return render_to_response('create.html', {})

def event_register(request):
    return render_to_response('register.html', {})

def event_thanks(request, event_id=""):
    if event_id:
        e = Event.objects.get(id=event_id)
        return render_to_response('thanks.html', {"event" : e})
    return render_to_response('thanks.html', {})

def index(request):
    return render_to_response('index.html', {})

def event_details(request, event_id=""):
    if event_id:
        e = Event.objects.get(id=event_id)
        u = User.objects.get(id=1)
        #print "EVENT", e, dir(e)
        #print "USER", u, dir(u), u.events_going, dir(u.events_going)
        #print "made invite", type(u.made_invite), dir(u.made_invite)
        
        #i = Invite(message="come to my party",
        #           from_user_id=1,
        #           to_user_id=1,
        #           event_id=1)
        #i.save()
        #print "Users Invited", u.received_invite.all()
        #print "USER MADE Invite", u.made_invite.all()

        return render_to_response('details.html', {"event" : e})
    return render_to_response('details.html', {})

def map(request):
    return render_to_response('map.html', {"key": settings.GOOGLE_MAP_API,
                                           "zoom": 14})

def event_home(req, event_id=""):
    if event_id:
        e = Event.objects.get(id=event_id)
    else:
        e = None
        
    # logged in
    if "user_id" in req.session:
        user = User.objects.get(id=req.session["user_id"])	

        if e:
            return render_to_response('event_home.html', {"event" : e,
                                                          "user" : user})
        else:
            return render_to_response('event_home.html', {"user" : user})

    # not logged in
    else:
        
        if e:
            return render_to_response('event_home.html', {"event" : e})
        else:
            return render_to_response('event_home.html', {})


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

    user_frineds_list = user.get_friend_list()
    event_attendees_list = event.attendees.all()

    friends_not_going_to_event = []
    
    for person in event_attendees_list:
        user_friends_list.remove(person.twitter_id)

    for person in user_friends_list:
        url = "http://api.twitter.com/1/users/show/" + str(person) + ".json"
        friend_obj = json.loads(urllib.urlopen(url).read())
        friends_not_going_to_event.append([friend_obj["name"],
                                           friend_obj["profile_image_url"],
                                           friend_obj["screen_name"]])

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
