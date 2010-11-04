import urllib
import urlparse

from django.http import HttpResponse
import simplejson as json

from campaign.models import Campaign
from events.models import Share
from models import FBUser
from pylib import bitly


def campaign_facebook_update(req, campaign_id=""):
    """ Send feed update to facebook from user share. """

    fbuser = FBUser.objects.get(facebook_id=req.session["uid"])

    msg=req.GET["message"]
    if len(msg) > 125:
        msg = msg[:125]

    if "shash" in req.GET:
        parent_shash = req.GET["shash"]
    else:
        parent_shash = None

    if "parent_url" in req.GET:
        parent_url = req.GET["parent_url"]
        parent_url = urllib.unquote(parent_url)
        parent_url = parent_url.replace("#", "")
        parsed_url = urlparse.urlparse(parent_url)
        try:
            list_vals = parsed_url.query.split("&")
        except Exception:
            list_vals = parsed_url[3]
        dict = {}
        for val in list_vals:
            if val:
                k, v = val.split("=")
                dict[k] = v
        if "shash" in dict:
            parent_shash = dict["shash"][0]
    else:
        parent_url = None
        
    c=Campaign.objects.get(id=campaign_id)
    share = Share(message=msg,
                  campaign=c,
                  from_user_facebook=fbuser,
                  from_user_twitter=None,
                  from_account_type="F",
                  parent_shash=parent_shash,
                  reach=fbuser.num_friends()
                  )
    share.save()
    share.setHash()
    url = share.url(req, parent=parent_url)
    short_url = bitly.shorten(url)
    share.url_short = short_url
    msg = msg + " " + short_url

    share.save()
    fbuser.feed(message=msg)
    fbuser.campaign_interested.add(c.id)    

    dict = {}
    dict["status"] = "ok!"
    dict["url"] = short_url
    dict["msg"] = msg
    return HttpResponse(json.dumps(dict))


def update_feed(req):
    fbuser = FBUser.objects.get(facebook_id=req.session["uid"])
    fbuser.feed(message=req.GET["message"])

    dict = {}
    dict["status"] = "ok!"
    return HttpResponse(json.dumps(dict))


def message(req):
    if "uid" in req.session:
        fbuser = FBUser.objects.get(facebook_id=req.session["uid"])
        fbuser.message()

        dict = {}
        dict["status"] = "ok!"
        return HttpResponse(json.dumps(dict))
    else:
        dict = {}
        dict["status"] = "error"
        dict["message"] = "no user"
        return HttpResponse(json.dumps(dict))

def friends(req):
    if "uid" in req.session:
        fbuser = FBUser.objects.get(facebook_id=req.session["uid"])
        data = fbuser.friends()
        
        dict = {}
        dict["status"] = "ok!"
        dict["data"] = data
        return HttpResponse(json.dumps(dict))
    else:
        dict = {}
        dict["status"] = "error"
        dict["message"] = "no user"
        return HttpResponse(json.dumps(dict))


def facebook_logout(req):
    """facebook logout."""
    # remove all cookies and session keys
    for key in req.session.keys():
        del req.session[key]
    for key in req.COOKIES.keys():
        del req.COOKIES[key]
    dict = {}
    return HttpResponse(json.dumps(dict))

def facebook_check_logout(req):
    """facebook logout."""
    dict = {}
    if "uid" in req.session:
        fbuser = FBUser.objects.get(facebook_id=req.session["uid"])
        url = "https://graph.facebook.com/me?access_token=" + fbuser.access_token
        result = urllib.urlopen(url).read()
        my_info = json.loads(result)
        if "id" in my_info:
            return HttpResponse(json.dumps(dict))
        else:
            del req.session["uid"]

    return HttpResponse(json.dumps(dict))

def facebook_feed_test(req):
    dict = {}
    fbuser = FBUser.objects.get(facebook_id=req.session["uid"])
    fbuser.feed()
    return HttpResponse(json.dumps(dict))


def facebook_info_test(req):
    
    fbuser = FBUser.objects.get(facebook_id=req.session["uid"])
    url = "https://graph.facebook.com/me?access_token=" + fbuser.access_token
    result = urllib.urlopen(url).read()
    my_info = json.loads(result)
    dict = {}
    dict["data"] = my_info
    return HttpResponse(json.dumps(dict))

def facebook_sync_server(req):
    # get uid and access_token
    req.session["uid"] = req.GET["uid"]
    req.session["access_token"] = req.GET["access_token"]
    
    # get or create facebook user
    (user, create) = FBUser.objects.get_or_create(facebook_id=req.session['uid'])
    user.access_token = req.session["access_token"]
    user.save()
    
    if create:
        user.fill_info()
        user.save()
    
    return HttpResponse(json.dumps({}))

def check_facebook_logged_in(req):
    print "req CHECK FACEBOOK LOGGEED IN ", req
    for key in req.session.keys():
        print "KEY", key, req.session[key]    
        
    if "uid" in req.session:
        fbuser = FBUser.objects.get(facebook_id=req.session["uid"])
        try:
            fbuser.num_friends()
            return HttpResponse(json.dumps({"status": "1"}))
        except Exception:
            pass
                
    return HttpResponse(json.dumps({"status": "0"}))
    

