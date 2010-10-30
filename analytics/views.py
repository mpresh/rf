from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import *
from django.conf import settings

from core.events.models import *
from core.fauth.models import *
from core.tauth.models import *
from core.campaign.models import Campaign

def analytics(req):
    data_tallies = {}
    data_tallies["fbappid"] = settings.FACEBOOK_APP_ID
    #req.session["redirect"] = req.get_full_path()

    shares = Share.objects.all()
    data_tallies["total_shares"] = len(shares)
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
    
    data_tallies["total_facebook_shares"] = total_facebook_shares
    data_tallies["total_twitter_shares"] = total_twitter_shares
    data_tallies["total_facebook_reach"] = total_facebook_reach
    data_tallies["total_twitter_reach"] = total_twitter_reach
    data_tallies["total_reach"] = total_twitter_reach + total_facebook_reach


    if "event" in req.GET:
        try:
            event = Event.objects.get(id=req.GET["event"])
            data_tallies["event"] = event
            shares = Share.objects.filter(event=event.id)
            data_tallies["shares"] = shares
        except Exception:
            return render_to_response('404.html', {})

    if "chash" in req.GET:
        try:
            camp = Campain.objects.get(chash=req.GET["chash"])
            event = camp.events.all()[0]
            data_tallies["event"] = event
            shares = Share.objects.filter(event=event.id)
            data_tallies["shares"] = shares
        except Exception:
            return render_to_response('404.html', {})

    if "user_id" in req.session:
        try:
            user = User.objects.get(id=req.GET["user_id"])
            data_tallies["user"] = user
        except Exception:
            pass

    template = "analytics.html"

    try:
        if req.GET["type"] == "raw":
            (prefix, suffix) = template.split(".")
            template = prefix + "_raw" + "." + suffix
            data_tallies["raw"] = True
    except:
        template = 'analytics.html'

        
    return render_to_response(template, data_tallies)


def analytics_chash(req, chash=""):
    data_tallies = {}
    data_tallies["fbappid"] = settings.FACEBOOK_APP_ID
    #req.session["redirect"] = req.get_full_path()


    try:
        c = Campaign.objects.get(chash=chash)
        shares = Share.objects.filter(campaign=c.id) 
        data_tallies["shares"] = shares
        data_tallies["campaign"] = c
    except Exception:
        return render_to_response('404.html', {})

    data_tallies["total_shares"] = len(shares)
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
    

    data_tallies["total_facebook_shares"] = total_facebook_shares
    data_tallies["total_twitter_shares"] = total_twitter_shares
    data_tallies["total_facebook_reach"] = total_facebook_reach
    data_tallies["total_twitter_reach"] = total_twitter_reach
    data_tallies["total_reach"] = total_twitter_reach + total_facebook_reach


    if "user_id" in req.session:
        try:
            user = User.objects.get(id=req.GET["user_id"])
            data_tallies["user"] = user
        except Exception:
            pass


    template = "analytics.html"

    try:
        if req.GET["type"] == "raw":
            (prefix, suffix) = template.split(".")
            template = prefix + "_raw" + "." + suffix
            data_tallies["raw"] = True
    except:
        template = 'analytics.html'
        
    return render_to_response(template, data_tallies)
