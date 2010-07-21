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



#KEYS product_price 100
#KEYS product_description Best Toaster Ever!
#KEYS product_name Toaster
#KEYS product_url http://www.capitalfactory.com
#KEYS image 
#KEYS product_discount 50
#KEYS product_image 

def _create_business(campaign, req):
    return HttpResponse(json.dumps({}))    


#KEYS event_time_start 12:30 AM
#KEYS code JOHNCHOW1
#KEYS image 
#KEYS min_people 0
#KEYS promotion_time_end 12:30 PM
#KEYS event_url http://www.capitalfactory.com
#KEYS event_image 
#KEYS event_venue Mandalay Bay Convention Center
#KEYS event_description There will be open bar!
#KEYS promotion_date_end 06/16/2010
#KEYS percent 50
#KEYS event_lat 30.267153
#KEYS event_discount 50
#KEYS subdomain www
#KEYS event_time_end 12:30 PM
#KEYS max_people 0
#KEYS from_name John
#KEYS event_name BLOG WORLD 2010
#KEYS event_date_end 06/16/2010
#KEYS person_email 
#KEYS url_redeem www.product.com/redeem_discount
#KEYS event_price 100
#KEYS product_type event
#KEYS event_lng -97.7430608
#KEYS event_address Las Vegas, Nevada
#KEYS campaign_message Best Offer Ever, Sign Up Now!
#KEYS promotion_time_start 12:30 AM
#KEYS event_capacity 100
#KEYS promotion_date_start 06/16/2010
#KEYS event_date_start 06/16/2010

def _create_event(campaign, req):
    print "CREATING EVENT"

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
              percent=percent,
              code=code,
              from_name=from_name,
              subdomain=subdomain,
              campaign=campaign)
    e.save()

    if not os.path.exists(os.path.join(settings.ROOT_PATH, 'static/images/events/')):
        os.mzkdir(os.path.join(settings.ROOT_PATH, 'static/images/events'))
        
    if image:
        os.rename(os.path.join(settings.ROOT_PATH, 'static/images/tmp/' + str(user.id) + '_' + image),
                  os.path.join(settings.ROOT_PATH, 'static/images/event_logos/' + str(e.id)))
    else:
        shutil.copy(os.path.join(settings.ROOT_PATH, 'static/images/muse.png'),
                    os.path.join(settings.ROOT_PATH, 'static/images/events/' + str(e.id)))
        
    #return HttpResponseRedirect(reverse('event_thanks', kwargs={'event_id' : e.id}))
    return HttpResponse(json.dumps({}))   

def _create_product(campaign, req):
    return HttpResponse(json.dumps({}))    

def _create_hotel(campaign, req):
    return HttpResponse(json.dumps({}))    

def create_campaign(req):
    for key in req.POST:
        print "KEYS", key, req.POST[key]


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
