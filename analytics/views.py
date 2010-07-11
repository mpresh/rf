from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404

from events.models import *
from fauth.models import *
from tauth.models import *

def analytics(req):
    dict = {}
    req.session["redirect"] = req.get_full_path()

    if "event" in req.GET:
        try:
            event = Event.objects.get(id=req.GET["event"])
            dict["event"] = event
            shares = Share.objects.filter(event=event.id)
            dict["shares"] = shares
        except Exception as e:
            pass

    if "user_id" in req.session:
        try:
            user = User.objects.get(id=req.GET["user_id"])
            dict["user"] = user
        except Exception as e:
            pass
        
    return render_to_response('analytics.html', dict)
