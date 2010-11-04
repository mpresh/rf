import urlparse

from django.conf import settings
from django.http import HttpResponse
import simplejson as json

from pylib import eventbrite


def create_discount(req):
    dict = {}
    percent = req.POST['percent']
    code = req.POST['code']
    username = req.POST['username']
    password = req.POST['password']
    eventid = req.POST['eventid']

    print "lal", settings.EVENTBRITE_API
    api = eventbrite.API(settings.EVENTBRITE_API, cache='.cache')
    try:
        discount = api.call('discount_new', user=username, password=password, percent_off=percent, code=code, event_id=eventid)
        dict["data"] = discount
    except Exception, e:
        dict["data"] = e
    
    return HttpResponse(json.dumps(dict))

def update_discount(req):
    print "Creating discount", req
    dict = {}
    return HttpResponse(json.dumps(dict))

def discount_list(req):
    print "Creating discount", req
    dict = {}
    return HttpResponse(json.dumps(dict))
