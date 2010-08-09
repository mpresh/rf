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
from pylib.bitly import *

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

def campaign_page(req, chash="", camp_id=""):
    req.session["redirect"] = req.get_full_path()
    try:
        if chash:
            c = Campaign.objects.get(chash=chash)
        if camp_id:
            c = Campaign.objects.get(id=camp_id)
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

    # HACK: if the oauth cookie has expired, clean up the session
    try:
        fbuser.num_friends()
    except:
        if "access_token" in req.session:
            del req.session['access_token']
            del req.session['base_domain']
            del req.session['secret']
            del req.session['session_key']
            del req.session['sessionid']
            del req.session['sig']
            del req.session['uid']

        if "access_token" in req.COOKIES:
            del req.COOKIES['access_token']
            del req.COOKIES['base_domain']
            del req.COOKIES['secret']
            del req.COOKIES['session_key']
            del req.COOKIES['sessionid']
            del req.COOKIES['sig']
            del req.COOKIES['uid'] 
        del dict["fbuser"]
    
    #facebook_users = c.interested_facebook.all()
    #twitter_users = c.interested_twitter.all()

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
    host = "http://" + req.get_host()
    dict["host"] = host
    dict["campaign"] = c

    campaign_admin_url = host + reverse("campaign_admin", kwargs={'chash':c.chash})
    campaign_analytics_url = host + reverse("campaign_analytics", kwargs={'chash':c.chash})
    campaign_update_url = host + reverse("campaign_update", kwargs={'chash':c.chash})
    campaign_landing_url = host + reverse("campaign_page_id", kwargs={'camp_id':c.id})

    #print "Campaign Admin URL", campaign_admin_url
    #print "Campaign Analytics URL", campaign_analytics_url
    #print "Campaign Update URL", campaign_update_url
    #print "Campaign Landing URL", campaign_landing_url

    dict["admin_url"] = shorten(campaign_admin_url)
    dict["landing_url"] = shorten(campaign_landing_url)
    dict["analytics_url"] = shorten(campaign_analytics_url)
    dict["update_url"] = shorten(campaign_update_url)
    return render_to_response('campaign_admin.html', dict)

def campaign_update(req, chash=""):
    req.session["redirect"] = req.get_full_path()
    try:
        c = Campaign.objects.get(chash=chash)
    except:
        return render_to_response('404.html', {})

    dict = {}
    host = "http://" + req.get_host()
    dict["host"] = host
    dict["campaign"] = c
    campaign_admin_url = host + reverse("campaign_admin", kwargs={'chash':c.chash})
    
    if c.start_date_time:
        dict["start_date_label"] = c.start_date_time.strftime("%m/%d/%y")
        dict["start_time_label"] = c.start_date_time.strftime("%I:%M %p")
    else:
        now = datetime.datetime.now()
        dict["start_date_label"] = now.strftime("%m/%d/%y")
        dict["start_time_label"] = now.strftime("%I:%M %p")

    if c.end_date_time:
        dict["end_date_label"] = c.end_date_time.strftime("%m/%d/%y")
        dict["end_time_label"] = c.end_date_time.strftime("%I:%M %p")
    else:
        now = datetime.datetime.now()
        dict["end_date_label"] = now.strftime("%m/%d/%y")
        dict["end_time_label"] = now.strftime("%I:%M %p")

    dict["admin_url"] = shorten(campaign_admin_url)    

    return render_to_response('campaign_edit.html', dict)

def campaign_created(req):
    req.session["redirect"] = req.get_full_path()
    dict = {}
    host = "http://" + req.get_host()
    dict["host"] = host
    print "HOST IS", host
    
    
    if "chash" in req.GET:
        try:
            c = Campaign.objects.get(chash=req.GET["chash"])
            dict["campaign"] = c

            campaign_admin_url = host + reverse("campaign_admin", kwargs={'chash':c.chash})
            campaign_analytics_url = host + reverse("campaign_analytics", kwargs={'chash':c.chash})
            campaign_update_url = host + reverse("campaign_update", kwargs={'chash':c.chash})
            campaign_landing_url = host + reverse("campaign_page_id", kwargs={'camp_id':c.id})

            #print "Campaign Admin URL", campaign_admin_url
            #print "Campaign Analytics URL", campaign_analytics_url
            #print "Campaign Update URL", campaign_update_url
            #print "Campaign Landing URL", campaign_landing_url

            dict["admin_url"] = shorten(campaign_admin_url)
            dict["landing_url"] = shorten(campaign_landing_url)
            dict["analytics_url"] = shorten(campaign_analytics_url)
            dict["update_url"] = shorten(campaign_update_url)

            return render_to_response('campaign_created.html', dict)
        except:
            pass

    return render_to_response('404.html', {})
