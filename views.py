from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from demo.events.models import Event, Organizer, Attendee
from django.conf import settings

def about(request):
    return render_to_response('about.html', {})

def event_list(request):
    all_events = Event.objects.all()
    return render_to_response('list.html', {"events":all_events})

def event_create(request):
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

        pfname = request.POST["person_fname"]
        plname = request.POST["person_lname"]
        pemail = request.POST["person_email"]
        ptwitter = request.POST["person_twitter"]

        p = Organizer(fname=pfname,
                      lname=plname,
                      email=pemail, 
                      twitter=ptwitter)
        p.save()

        import datetime
        e = Event(name=ename, 
                  description=edescription, 
                  event_date_time_start=datetime.datetime.now(),
                  event_date_time_end=datetime.datetime.now(),
                  capacity=ecapacity,
                  venue=evenue,
                  venue_address=eaddress,
                  organizer_id=p.id,
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
        return render_to_response('details.html', {"event" : e})
    return render_to_response('details.html', {})

def map(request):
    return render_to_response('map.html', {"key": settings.GOOGLE_MAP_API,
                                           "zoom": 14})

def event_home(request, event_id=""):
    if event_id:
        e = Event.objects.get(id=event_id)
        return render_to_response('event_home.html', {"event" : e})
    else:
        return render_to_response('event_home.html', {})
