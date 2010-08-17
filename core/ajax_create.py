from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
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
from pylib import bitly
import sys
from smtplib import SMTP
import re

def send_details_email(req):
    content = req.POST["content"]
    chash = req.POST["chash"]
    email = req.POST["email_address"]

    content = re.sub(r'<.*?>', '',content) 
    content = content.replace("&nbsp;", "") 
    from_addr = 'info@ripplefunction.com'
    to_addrs = [email]

    try:
        s = SMTP()
        s.connect('smtp.webfaction.com')
        s.login('mpresh','1564f867')
        s.sendmail(from_addr, to_addrs, content)
        return HttpResponse(json.dumps({"status":200} ))    
    except:
        return HttpResponse(json.dumps({"status":500} ))    

def campaign_update_ajax(req):
    if ("chash" in req.GET):
        c = Campaign.objects.get(chash=req.GET["chash"])
    else:
        return HttpResponse(json.dumps({"status":500} ))    

    title = req.POST["title"]
    from_name = req.POST["from_name"]
    code = req.POST["code"]
    max_people = req.POST["max_people"]        
    min_people = req.POST["min_people"]    
    percent = req.POST["percent"]

    start_date = req.POST["promotion_date_start"]
    start_time = req.POST["promotion_time_start"]
    end_date = req.POST["promotion_date_end"]
    end_time = req.POST["promotion_time_end"]

    start_dt = datetime.datetime.strptime(start_date.strip() + " " + start_time.strip(), 
                                          "%m/%d/%Y %I:%M %p")

    end_dt = datetime.datetime.strptime(end_date.strip() + " " + end_time.strip(), 
                                        "%m/%d/%Y %I:%M %p")   

    message_share = req.POST["campaign_message_share"]
    message = req.POST["campaign_message"]
    subdomain = req.POST["subdomain"]
    url_redeem = req.POST["url_redeem"]
    url = req.POST["url"]

    c.title = title
    c.from_name= from_name
    c.code = code
    c.max_people = max_people
    c.min_people = min_people
    c.percent = percent
    c.message = message
    c.message_share = message_share
    c.subdomain = subdomain
    c.url = url
    c.url_redeem = url_redeem

    c.save()
    return HttpResponse(json.dumps({"status" : 200}))    

def _create_business(campaign, req):
    return HttpResponse(json.dumps({}))    


def _create_event(campaign, req):

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
              campaign=campaign)

    e.save()
    e.setHash()
    
    if not os.path.exists(os.path.join(settings.ROOT_PATH, 'static/images/events/')):
        os.mzkdir(os.path.join(settings.ROOT_PATH, 'static/images/events'))
        
    if image:
        os.rename(os.path.join(settings.ROOT_PATH, 'static/images/tmp/' + str(user.id) + '_' + image),
                  os.path.join(settings.ROOT_PATH, 'static/images/event_logos/' + str(e.id)))
    else:
        shutil.copy(os.path.join(settings.ROOT_PATH, 'static/images/muse.png'),
                    os.path.join(settings.ROOT_PATH, 'static/images/events/' + str(e.id)))
        
    #return HttpResponseRedirect(reverse('event_thanks', kwargs={'event_id' : e.id}))
    return HttpResponse(json.dumps({"campaign_hash": campaign.chash}))   

def _create_product(campaign, req):
    return HttpResponse(json.dumps({}))    

def _create_hotel(campaign, req):
    return HttpResponse(json.dumps({}))    

def create_campaign_url_check(req):
    campaign_url = req.POST["url"]
    if not campaign_url.startswith("http://"):
        campaign_url = "http://" + campaign_url 

    try:
        obj = urllib.urlopen(campaign_url)
    except:
        return HttpResponse(json.dumps({"url": ""}))   

    try:
        status = obj.getcode()
        status_str = str(status)
    
        if status_str[0] == "2" or status_str[0] == 3:
            return HttpResponse(json.dumps({"url": campaign_url}))   
        else:
            
            return HttpResponse(json.dumps({"url": ""}))   
    except Exception:
        return HttpResponse(json.dumps({"url": campaign_url}))   

def create_campaign(req):
    campaign_url = req.POST["url"]
    if not campaign_url.startswith("http://"):
        campaign_url = "http://" + campaign_url

    start_dt = datetime.datetime.now()
    end_dt = datetime.datetime.now()

    c = Campaign(
        url=campaign_url,
        url_redeem=campaign_url,
        )

    c.save()
    c.setHash()
    return HttpResponse(json.dumps({"campaign_hash": c.chash}))

def create_campaign_original(req):

    if "campaign_type" not in req.POST:
        return HttpResponse(json.dumps({"status": "error"}))

    campaign_type = req.POST["campaign_type"]
    code = req.POST["code"]
    max_people = req.POST["max_people"]        
    min_people = req.POST["min_people"]    
    percent = req.POST["percent"]
    start_date = req.POST["promotion_date_start"]
    start_time = req.POST["promotion_time_start"]
    end_date = req.POST["promotion_date_end"]
    end_time = req.POST["promotion_time_end"]
    from_name = req.POST["from_name"]
    message = req.POST["campaign_message"]
    pemail = req.POST["person_email"]
    subdomain = req.POST["subdomain"]
    url = req.POST["url_redeem"]

    start_dt = datetime.datetime.strptime(start_date.strip() + " " + start_time.strip(), 
                                          "%m/%d/%Y %I:%M %p")
    end_dt = datetime.datetime.strptime(end_date.strip() + " " + end_time.strip(), 
                                        "%m/%d/%Y %I:%M %p")   

    c = Campaign(
        start_date_time=start_dt,
        end_date_time=end_dt,
        code=code,
        percent=percent,
        url=url,
        max_people=max_people,
        min_people=min_people,
        message=message,
        subdomain=subdomain,
        from_name=from_name,
        campaign_type=campaign_type
        )
    c.save()
    c.setHash()

    if campaign_type == "business":
        return _create_business(c, req)
    elif campaign_type == "hotel":
        return _create_hotel(c, req)
    elif campaign_type == "product":
        return _create_product(c, req)
    elif campaign_type == "event":
        return _create_event(c, req)
    return HttpResponse(json.dumps({}))
