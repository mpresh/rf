from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from events.models import Event, Share
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
import urlparse

def create_campaign(req):
    """ This is the default create campaign page."""
    dict = {}
    return render_to_response('create_campaign.html', dict)    

def campaign_widget(req, camp_id="1"):

    dict = {}
    if "overlay" in req.GET:
        dict["overlay"] = True
        if req.GET["overlay"] == "facebook":
            dict["overlayFacebook"] = True
        elif req.GET["overlay"] == "twitter":
            dict["overlayTwitter"] = True    
        elif req.GET["overlay"] == "true":
            dict["overlayTrue"] = True    

    # parent_url
    if "parent_url" in req.GET:
        parent_url = req.GET["parent_url"]
        dict["parent_url"] = parent_url
        #parent_url = urlparse.unquote(parent_url)
        
    try:
        campaign_id = int(req.GET["campaign"])
        campaign = Campaign.objects.get(id=campaign_id)
        dict["campaign"] = campaign
    except Exception:
        campaign = Campaign.objects.get(id=camp_id)
        dict["campaign"] = campaign

    # twitter user
    if "user_id" in req.session:
        user = User.objects.get(id=req.session["user_id"])	
        dict['user'] = user
    else:
        user = None
 
    req.session["redirect"] = reverse("facebook_login_test")
    host = "http://" + req.get_host()
    dict["host"] = host
    dict["facebook_app_id"] = settings.FACEBOOK_APP_ID
    dict["facebook_api"] = settings.FACEBOOK_API
    dict["redirect_uri"] = host + reverse("facebook_login_callback")
    dict["scope"] = "publish_stream"

    if "uid" in req.session:
        fbuser = FBUser.objects.get(facebook_id=req.session["uid"])
        dict["fbuser"] = fbuser

    print "WIDGET DICT", dict
    return render_to_response('widget.html', dict)    

def campaign_badge(req, camp_id="1"):
    campaign = Campaign.objects.get(id=camp_id)
    dict = {"campaign":campaign}

    if "overlay" in req.GET:
        dict["overlay"] = True
        if req.GET["overlay"] == "facebook":
            dict["overlayFacebook"] = True
        elif req.GET["overlay"] == "twitter":
            dict["overlayTwitter"] = True    
        elif req.GET["overlay"] == "true":
            dict["overlayTrue"] = True    

    # twitter user
    if "user_id" in req.session:
        user = User.objects.get(id=req.session["user_id"])	
        dict['user'] = user
    else:
        user = None
    
    # HACK: if the oauth cookie has expired, clean up the session
    #try:
    #    fbuser.num_friends()
    #except:
    #    del req.session['uid']
 
    req.session["redirect"] = reverse("facebook_login_test")
    host = "http://" + req.get_host()
    dict["host"] = host
    dict["facebook_app_id"] = settings.FACEBOOK_APP_ID
    dict["facebook_api"] = settings.FACEBOOK_API
    dict["redirect_uri"] = host + reverse("facebook_login_callback")
    dict["scope"] = "publish_stream"

    if "uid" in req.session:
        fbuser = FBUser.objects.get(facebook_id=req.session["uid"])
        dict["fbuser"] = fbuser

    print "BADGE DICT", dict
    return render_to_response('badge.html', dict)    

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

    req.session["redirect"] = reverse("facebook_login_test")
    host = "http://" + req.get_host()
    dict["host"] = host
    dict["facebook_app_id"] = settings.FACEBOOK_APP_ID
    dict["facebook_api"] = settings.FACEBOOK_API
    dict["redirect_uri"] = host + reverse("facebook_login_callback")
    dict["scope"] = "publish_stream"
    

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
        share = Share.objects.get(shash=dict["shash"])
        share.page_views = share.page_views + 1
        share.save()
        c.page_views_total = c.page_views_total + 1
    else:
        dict["shash"] = ""
        c.page_views = c.page_views + 1
        c.page_views_total = c.page_views_total + 1

    c.save()

    # twitter user
    if "user_id" in req.session:
        user = User.objects.get(id=req.session["user_id"])	
        dict['user'] = user
    else:
        user = None

    # facebook user
    if "uid" in req.session:
        fbuser = FBUser.objects.get(facebook_id=req.session["uid"])	
        dict['fbuser'] = fbuser
    else:
        fbuser = None
        dict["fbuser"] = ""
  
    templates = ['campaign_page2.html', 'campaign_page.html']
    try:
        template = templates[int(req.GET["t"])]
    except:
        template = 'campaign_page2.html'
        
    return render_to_response(template, dict)

def campaign_page_preview(req):
    if "url" in req.GET:
        c = Campaign(url=req.GET["url"], id=0)
        dict={}
        dict["campaign"] = c
        return render_to_response('campaign_page.html', dict)    
    else:
        return render_to_response('404.html', {})

def campaign_admin(req, chash=""):
    #req.session["redirect"] = req.get_full_path()
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
    campaign_launch_url = host + reverse("campaign_launch", kwargs={'chash':c.chash})
    campaign_widget_url = host + reverse("campaign_widget", kwargs={'chash':c.chash})

    dict["admin_url"] = shorten(campaign_admin_url)
    dict["landing_url"] = shorten(campaign_landing_url)
    dict["analytics_url"] = shorten(campaign_analytics_url)
    dict["update_url"] = shorten(campaign_update_url)
    dict["launch_url"] = shorten(campaign_launch_url)
    dict["widget_url"] = shorten(campaign_widget_url)

    return render_to_response('campaign_admin.html', dict)

def campaign_launch(req, chash=""):
    try:
        c = Campaign.objects.get(chash=chash)
    except:
        return render_to_response('404.html', {})

    dict = {}
    dict["campaign"] = c

    host = "http://" + req.get_host()
    dict["host"] = host
    campaign_admin_url = host + reverse("campaign_admin", kwargs={'chash':c.chash})
    dict["admin_url"] = shorten(campaign_admin_url)

    return render_to_response('campaign_launch.html', dict)

def campaign_widget_page(req, chash=""):
    try:
        c = Campaign.objects.get(chash=chash)
    except:
        return render_to_response('404.html', {})

    dict = {}
    dict["campaign"] = c

    host = "http://" + req.get_host()
    dict["host"] = host
    campaign_admin_url = host + reverse("campaign_admin", kwargs={'chash':c.chash})
    dict["admin_url"] = shorten(campaign_admin_url)

    return render_to_response('campaign_widget.html', dict)


def campaign_update(req, chash=""):
    #req.session["redirect"] = req.get_full_path()
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
        dict["start_date_label"] = c.start_date_time.strftime("%m/%d/%Y")
        dict["start_time_label"] = c.start_date_time.strftime("%I:%M %p")
    else:
        now = datetime.datetime.now()
        dict["start_date_label"] = now.strftime("%m/%d/%Y")
        dict["start_time_label"] = now.strftime("%I:%M %p")

    if c.end_date_time:
        dict["end_date_label"] = c.end_date_time.strftime("%m/%d/%Y")
        dict["end_time_label"] = c.end_date_time.strftime("%I:%M %p")
    else:
        now = datetime.datetime.now()
        dict["end_date_label"] = now.strftime("%m/%d/%Y")
        dict["end_time_label"] = now.strftime("%I:%M %p")

    dict["admin_url"] = shorten(campaign_admin_url)
    for attr_obj in c.attributes.all():
        dict[attr_obj.name] = True;

    return render_to_response('campaign_edit.html', dict)

def campaign_created(req):
    #req.session["redirect"] = req.get_full_path()
    dict = {}
    host = "http://" + req.get_host()
    dict["host"] = host
    
    if "chash" in req.GET:
        try:
            c = Campaign.objects.get(chash=req.GET["chash"])
            dict["campaign"] = c
            
            campaign_admin_url = host + reverse("campaign_admin", kwargs={'chash':c.chash})
            campaign_analytics_url = host + reverse("campaign_analytics", kwargs={'chash':c.chash})
            campaign_update_url = host + reverse("campaign_update", kwargs={'chash':c.chash})
            campaign_landing_url = host + reverse("campaign_page_id", kwargs={'camp_id':c.id})
            campaign_launch_url = host + reverse("campaign_launch", kwargs={'chash':c.chash})
            campaign_widget_url = host + reverse("campaign_widget", kwargs={'chash':c.chash})

            dict["admin_url"] = shorten(campaign_admin_url)
            dict["landing_url"] = shorten(campaign_landing_url)
            dict["analytics_url"] = shorten(campaign_analytics_url)
            dict["update_url"] = shorten(campaign_update_url)
            dict["launch_url"] = shorten(campaign_launch_url)
            dict["widget_url"] = shorten(campaign_widget_url)

            return render_to_response('campaign_created.html', dict)
        except:
            pass

    return render_to_response('404.html', {})
