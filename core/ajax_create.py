import datetime
import os
import shutil
import urllib

from smtplib import SMTP

import simplejson as json
from django.http import HttpResponse
from django.conf import settings

from campaign.models import Campaign
from campaign.models import CampaignAttr
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from events.models import Event

def send_details_email(req):
    print "here I am"
    admin_url = req.POST["admin_url"]
    landing_url = req.POST["landing_url"]
    email = req.POST["email_address"]

    print "here"
    msg = MIMEMultipart()
    print "hellop"

    content = "Admin URL: " + admin_url + "\n"
    content += "Landing Page URL: " + landing_url
    msg = MIMEText(content)
    print "no"

    msg['Subject'] = "Campaign Details"
    msg["From"] = "RippleFunction<info@ripplefunction.com>"
    msg['To'] = email

    
    from_addr = 'info@ripplefunction.com'
    to_addrs = [email]
    print "do I get here"

    try:
        s = SMTP()
        s.connect('smtp.webfaction.com')
        s.login('mpresh','1564f867')
        s.sendmail(from_addr, to_addrs, msg.as_string())
        return HttpResponse(json.dumps({"status":200} ))    
    except:
        return HttpResponse(json.dumps({"status":500} ))    

def campaign_update_ajax(req):
    if ("chash" in req.GET):
        c = Campaign.objects.get(chash=req.GET["chash"])
    else:
        return HttpResponse(json.dumps({"status":500} ))    

    
    if "campaign_type" in req.POST:
        c.campaign_type = req.POST["campaign_type"]
    if "title" in req.POST:
        c.title = req.POST["title"]
    if "from_name" in req.POST:
        c.from_name = req.POST["title"]
    if "code" in req.POST:
        c.code = req.POST["code"]
    if "twitter_account" in req.POST:
        c.twitter_account = req.POST["twitter_account"]
    if "facebook_fan" in req.POST:
        c.facebook_fan = req.POST["facebook_fan"]
    
    if "max_people" in req.POST:
        c.max_people = req.POST["max_people"]
    if "min_people" in req.POST:
        c.min_people = req.POST["min_people"]
    if "percent" in req.POST:
        c.percent = req.POST["percent"]
    if "campaign_message" in req.POST:
        c.message = req.POST["campaign_message"]
    
    if "campaign_message_share" in req.POST:
        c.message_share = req.POST["campaign_message_share"]
    if "subdomain" in req.POST:
        c.subdomain = req.POST["subdomain"]
    if "url_redeem" in req.POST:
        print "REDEEEM", req.POST["url_redeem"]    
        c.url_redeem = req.POST["url_redeem"]    
    if "url" in req.POST:
        c.url = req.POST["url"]
    
    if "promotion_date_start" in req.POST and "promotion_time_start" in req.POST: 
        start_date = req.POST["promotion_date_start"]
        start_time = req.POST["promotion_time_start"]        
        start_dt = datetime.datetime.strptime(start_date.strip() + " " + start_time.strip(), 
                                              "%m/%d/%Y %I:%M %p")
        c.start_date_time = start_dt
    
    if "promotion_date_end" in req.POST and "promotion_time_end" in req.POST: 
    
        end_date = req.POST["promotion_date_end"]
        end_time = req.POST["promotion_time_end"]        
        end_dt = datetime.datetime.strptime(end_date.strip() + " " + end_time.strip(), 
                                              "%m/%d/%Y %I:%M %p")
        c.end_date_time = end_dt
    print "hi5"

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
        # BUG: user is undefined
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

    if req.POST['campaign_type'] == 'raffle':
        template_val = 0
        campaign_url_val = "http://i.bnet.com/blogs/verizon-prepping-the-ipad.jpg"
    elif req.POST['campaign_type'] == 'discount':
        campaign_url_val = campaign_url
        template_val = 2
    else:
        template_val = 0
        campaign_url_val = campaign_url
    

    c = Campaign(
        url=campaign_url,
        url_redeem=campaign_url_val,
        template=template_val
        )

    c.save()
    print "CAMPAIGN CREATE", c.page_views

    c.campaign_type = req.POST['campaign_type']
    c.save()

    c.setHash()
    create_attr(c, name='post', value='')
    create_attr(c, name='follow', value='')
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

def create_attr(campaign, name='', value=''):
    ca = CampaignAttr(
        name=name,
        value=value,
        campaign=campaign
        )

    ca.save()
    return

def del_all_attr(campaign):
    CampaignAttr.objects.filter(id=campaign.id).delete()
    return

