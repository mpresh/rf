from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from events.models import Event
from tauth.models import User
from fauth.models import FBUser
from campaign.models import Campaign
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

def create_campaign(req):
    return render_to_response('create_campaign.html', dict)    

def event_create(req):
    dict = {}
    invite_url = util.get_invite_url(req)
    req.session["redirect"] = req.get_full_path()        

    #if "user_id" not in req.session:
    #    return HttpResponseRedirect(reverse('tauth_login'))

    user = None
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
        code = req.POST["code"]
        percent = req.POST["percent"]
        from_name = req.POST["from_name"]
        subdomain = req.POST["subdomain"]

        pemail = req.POST["person_email"]
        
        if "user_id" in req.session:
            user = User.objects.get(id=req.session["user_id"])
            dict["user"] = user
            if pemail:
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
                  url=eurl,
                  price=eprice,
                  lat=elat,
                  lng=elng,
                  percent=percent,
                  code=code,
                  from_name=from_name,
                  subdomain=subdomain)
        
        if user:
            print "AM I HERE"
            e.organizer_id=user.id,
        e.save()

        

        if not os.path.exists(os.path.join(settings.ROOT_PATH, 'static/images/events/')):
            os.mkdir(os.path.join(settings.ROOT_PATH, 'static/images/events'))
			
        if image:
            os.rename(os.path.join(settings.ROOT_PATH, 'static/images/tmp/' + str(user.id) + '_' + image),
                  	os.path.join(settings.ROOT_PATH, 'static/images/event_logos/' + str(e.id)))
        else:
          	shutil.copy(os.path.join(settings.ROOT_PATH, 'static/images/muse.png'),
                       os.path.join(settings.ROOT_PATH, 'static/images/events/' + str(e.id)))
        
        return HttpResponseRedirect(reverse('event_thanks', kwargs={'event_id' : e.id}))
	
    
    dict["key"] = settings.GOOGLE_MAP_API
    dict["zoom"] = 8
    dict["invite_url"] = invite_url
    return render_to_response('create.html', dict)

def event_thanks(req, event_id=""):
    req.session["redirect"] = req.get_full_path()
    
    dict = {}
    if "user_id" in req.session:
        user = User.objects.get(id=req.session["user_id"])	
        dict["user"] = user

    if event_id:
        dict["event"] = Event.objects.get(id=event_id)

    return render_to_response('thanks.html', dict)

def campaign_page(req, chash=""):
    req.session["redirect"] = req.get_full_path()
    try:
        c = Campaign.objects.get(chash=chash)
    except:
        return render_to_response('404.html', {})
    dict = {}
    dict["campaign"] = c
    dict["fbappid"] = settings.FACEBOOK_APP_ID

    if "overlay" in req.GET:
        dict["overlay"] = True
        if req.GET["overlay"] == "facebook":
            dict["overlayFacebook"] = True
        elif req.GET["overlay"] == "twitter":
            dict["overlayTwitter"] = True    
        elif req.GET["overlay"] == "true":
            dict["overlayTrue"] = True    

    if "shash" in req.GET:
        dict["shash"] = req.GET["shash"]
    else:
        dict["shash"] = ""

    # twitter user
    if "user_id" in req.session:
        user = User.objects.get(id=req.session["user_id"])	
        dict['user'] = user
    else:
        user = None

    # facebook user
    if "uid" in req.session:
        print "FBUSER ID", req.session["uid"]
        fbuser = FBUser.objects.get(facebook_id=req.session["uid"])	
        dict['fbuser'] = fbuser
    elif "uid" in req.COOKIES:
        fauth_utils.sync_session_cookies(req)
        fbuser = FBUser.objects.get(facebook_id=req.COOKIES["uid"])	
        dict['fbuser'] = fbuser
    else:
        fbuser = None
        dict["fbuser"] = ""

    return render_to_response('campaign_page.html', dict)

def campaign_page_preview(req):
    if "url" in req.GET:
        c = Campaign(url=req.GET["url"], id=0)
        dict={}
        dict["campaign"] = c
        return render_to_response('campaign_page.html', dict)    
    else:
        return render_to_response('404.html', {})

def campaign_admin(req, chash=""):
    req.session["redirect"] = req.get_full_path()
    try:
        c = Campaign.objects.get(chash=chash)
    except:
        return render_to_response('404.html', {})

    dict = {}
    dict["host"] = "http://" + req.get_host()
    dict["campaign"] = c
    return render_to_response('campaign_admin.html', dict)

def campaign_update(req, chash=""):
    req.session["redirect"] = req.get_full_path()
    try:
        c = Campaign.objects.get(chash=chash)
    except:
        return render_to_response('404.html', {})

    dict = {}
    dict["host"] = "http://" + req.get_host()
    dict["campaign"] = c
    return render_to_response('campaign_edit.html', dict)

def campaign_created(req):
    req.session["redirect"] = req.get_full_path()
    dict = {}
    dict["host"] = "http://" + req.get_host()
    if "chash" in req.GET:
        try:
            c = Campaign.objects.get(chash=req.GET["chash"])
            dict["campaign"] = c
            if c.campaign_type == "event":
                dict["event"] = c.events.all()[0]
            return render_to_response('campaign_created.html', dict)
        except:
            pass

    return render_to_response('404.html', {})
