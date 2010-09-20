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

def frontpage(req):
    #req.session["redirect"] = req.get_full_path()  

    domain = req.META['HTTP_HOST'].split(".")[0]
    print "DOMAIN IS", domain

    if domain != "www" and domain != "ripplefunction":
        campaigns = Campaign.objects.filter(subdomain=domain)
        if len(list(campaigns)) > 0:
            campaign = list(campaigns)[-1]
            return HttpResponseRedirect(reverse('campaign_page_id', kwargs={'camp_id':campaign.id}))


    templates = ["frontpage.html", "frontpageCycle.html"]
    template = templates[0]
    if "t" in req.GET:
        t = req.GET["t"]
        try:
            template = templates[int(t)]
        except Exception:
            pass
    return render_to_response(template, {})


def googlehostedservice(req):
    return render_to_response('googlehostedservice.html', {})
