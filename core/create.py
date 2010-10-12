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
import re

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

    # check to see if there is a css file for widget of this campaign
    destination_dir = os.path.join(settings.ROOT_PATH, 'static/css/widget/')
    if not os.path.exists(destination_dir):
        os.system("mkdir -p " + destination_dir)
    css_file = os.path.join(destination_dir, 'style_' + str(campaign.id) + '.css')
    if os.path.exists(css_file):
        dict['css'] = True

    # check to see if there is custom widget text
    destination_dir = os.path.join(settings.ROOT_PATH, 'static/css/widget/text')
    if not os.path.exists(destination_dir):
        os.system("mkdir -p " + destination_dir)
    text_file = os.path.join(destination_dir, 'text_' + str(campaign.id) + '.html')
    if os.path.exists(text_file):
        dict['html'] = open(text_file).read()

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
    print "REQUEST IS", req
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
        #print "AAAA SHASH", share.page_views
        share.page_views = share.page_views + 1
        share.save()
        c.page_views_total = c.page_views_total + 1
    else:
        dict["shash"] = ""
        c.page_views = c.page_views + 1
        c.page_views_total = c.page_views_total + 1
        #print "NO SHASH", c.page_views, c.page_views_total

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

    templates = ['campaign_admin.html', 'campaign_admin2.html']
    try:
        template = templates[int(req.GET["t"])]
    except:
        template = 'campaign_admin.html'

    if template == "campaign_admin2.html":
        campaign_admin_url = host + reverse("campaign_admin", kwargs={'chash':c.chash}) + "?type=raw"
        campaign_analytics_url = host + reverse("campaign_analytics", kwargs={'chash':c.chash}) + "?type=raw"
        campaign_update_url = host + reverse("campaign_update", kwargs={'chash':c.chash}) + "?type=raw"
        campaign_landing_url = host + reverse("campaign_page_id", kwargs={'camp_id':c.id}) + "?type=raw"
        campaign_launch_url = host + reverse("campaign_launch", kwargs={'chash':c.chash}) + "?type=raw"
        campaign_widget_url = host + reverse("campaign_widget_page", kwargs={'chash':c.chash}) + "?type=raw"
    else:
        campaign_admin_url = host + reverse("campaign_admin", kwargs={'chash':c.chash})
        campaign_analytics_url = host + reverse("campaign_analytics", kwargs={'chash':c.chash})
        campaign_update_url = host + reverse("campaign_update", kwargs={'chash':c.chash})
        campaign_landing_url = host + reverse("campaign_page_id", kwargs={'camp_id':c.id})
        campaign_launch_url = host + reverse("campaign_launch", kwargs={'chash':c.chash})
        campaign_widget_url = host + reverse("campaign_widget_page", kwargs={'chash':c.chash})

    print "HERE I AM", campaign_update_url
    dict["admin_url"] = shorten(campaign_admin_url)
    dict["landing_url"] = shorten(campaign_landing_url)
    dict["analytics_url"] = shorten(campaign_analytics_url)
    dict["update_url"] = shorten(campaign_update_url)
    dict["launch_url"] = shorten(campaign_launch_url)
    dict["widget_url"] = shorten(campaign_widget_url)

    return render_to_response(template, dict)

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
        campaign = Campaign.objects.get(chash=chash)
    except:
        return render_to_response('404.html', {})

    dict = {}
    dict["campaign"] = campaign

    host = "http://" + req.get_host()
    dict["host"] = host
    campaign_admin_url = host + reverse("campaign_admin", kwargs={'chash':campaign.chash})
    dict["admin_url"] = shorten(campaign_admin_url)

    # check to see if there is a css file for widget of this campaign
    dict["headercolor"] = "#F2F2F2"
    dict["footercolor"] = "#FFFFFF"
    dict["platformcolor"] = "#FFFFFF"
    destination_dir = os.path.join(settings.ROOT_PATH, 'static/css/widget/')
    if not os.path.exists(destination_dir):
        os.system("mkdir -p " + destination_dir)
    css_file = os.path.join(destination_dir, 'style_' + str(campaign.id) + '.css')
    if os.path.exists(css_file):
        css = open(css_file).read()
        mo = re.search("badge-header\s*?{background-color[:]\s*?([#0-9a-zA-Z]+)", css)
        if mo:
            dict["headercolor"] = mo.group(1)
        mo = re.search("badge-footer\s*?{background-color[:]\s*?([#0-9a-zA-Z]+)", css)
        if mo:
            dict["footercolor"] = mo.group(1)
        mo = re.search("ripple-badge-wrapper\s*?{background-color[:]\s*?([#0-9a-zA-Z]+)", css)
        if mo:
            dict["platformcolor"] = mo.group(1)

    # check to see if there is custom widget text
    destination_dir = os.path.join(settings.ROOT_PATH, 'static/css/widget/text')
    if not os.path.exists(destination_dir):
        os.system("mkdir -p " + destination_dir)
    text_file = os.path.join(destination_dir, 'text_' + str(campaign.id) + '.html')
    if os.path.exists(text_file):
        dict['html'] = open(text_file).read()

    template = "campaign_widget.html"
    try:
        if req.GET["type"] == "raw":
            (prefix, suffix) = template.split(".")
            template = prefix + "_raw" + "." + suffix
            dict["raw"] = True
    except:
        template = 'campaign_widget.html'

    return render_to_response(template, dict)


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

    templates = ['campaign_edit.html']
    try:
        template = templates[int(req.GET["t"])]
    except:
        template = 'campaign_edit.html'
        
    try:
        if req.GET["type"] == "raw":
            (prefix, suffix) = template.split(".")
            template = prefix + "_raw" + "." + suffix
            dict["raw"] = True
    except:
        template = 'campaign_edit.html'

    return render_to_response(template, dict)

def campaign_created(req):
    #req.session["redirect"] = req.get_full_path()
    dict = {}
    host = "http://" + req.get_host()
    dict["host"] = host
    
    if "chash" in req.GET:
        try:
            c = Campaign.objects.get(chash=req.GET["chash"])
            dict["campaign"] = c
            return HttpResponseRedirect(reverse('campaign_admin', kwargs={'chash':req.GET['chash']}))

            campaign_admin_url = host + reverse("campaign_admin", kwargs={'chash':c.chash})
            campaign_analytics_url = host + reverse("campaign_analytics", kwargs={'chash':c.chash})
            campaign_update_url = host + reverse("campaign_update", kwargs={'chash':c.chash})
            campaign_landing_url = host + reverse("campaign_page_id", kwargs={'camp_id':c.id})
            campaign_launch_url = host + reverse("campaign_launch", kwargs={'chash':c.chash})
            campaign_widget_url = host + reverse("campaign_widget_page", kwargs={'chash':c.chash})

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
