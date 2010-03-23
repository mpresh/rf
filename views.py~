from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from demo.events.models import Event
from demo.tauth.models import User
from django.conf import settings

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
        print "EVENT", e, dir(e)
        print "USER", u, dir(u), u.events_going, dir(u.events_going)
        #u.events_going.update(1)

        return render_to_response('details.html', {"event" : e})
    return render_to_response('details.html', {})

def map(request):
    return render_to_response('map.html', {"key": settings.GOOGLE_MAP_API,
                                           "zoom": 14})

def event_home(request, event_id=""):
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
