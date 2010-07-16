from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import *

from core.events.models import *
from core.fauth.models import *
from core.tauth.models import *

def analytics(req):
    dict = {}
    req.session["redirect"] = req.get_full_path()

    shares = Share.objects.all()
    dict["total_shares"] = len(shares)
    total_facebook_shares = 0
    total_twitter_shares = 0
    total_twitter_reach = 0
    total_facebook_reach = 0
    for share in shares:
        if share.from_account_type == "F":
            total_facebook_shares = total_facebook_shares + 1
            if not share.parent_shash:
                total_facebook_reach = total_facebook_reach + share.totalReach()
                
        elif share.from_account_type == "T":
            total_twitter_shares = total_twitter_shares + 1
            if not share.parent_shash:
                total_twitter_reach = total_twitter_reach + share.totalReach()
                

    dict["total_facebook_shares"] = total_facebook_shares
    dict["total_twitter_shares"] = total_twitter_shares
    dict["total_facebook_reach"] = total_facebook_reach
    dict["total_twitter_reach"] = total_twitter_reach
    dict["total_reach"] = total_twitter_reach + total_facebook_reach


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
