from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import *

from core.events.models import *
from core.fauth.models import *
from core.tauth.models import *

def analytics(req):
    dict = {}
    req.session["redirect"] = req.get_full_path()

    if "event" in req.GET:
        try:
            event = Event.objects.get(id=req.GET["event"])
            dict["event"] = event
            shares = Share.objects.filter(event=event.id)
            dict["shares"] = shares
        except Exception:
            pass

    if "user_id" in req.session:
        try:
            user = User.objects.get(id=req.GET["user_id"])
            dict["user"] = user
        except Exception:
            pass
        
    return render_to_response('analytics.html', dict)
