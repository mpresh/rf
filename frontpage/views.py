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
    req.session["redirect"] = req.get_full_path()  

    domain = req.META['HTTP_HOST'].split(".")[0]
    print "DOMAIN IS", domain

    if domain != "www":
        campaigns = Campaign.objects.filter(subdomain=domain)
        campaign = list(campaigns)[-1]
        event = campaign.events.all()[0]
        return HttpResponseRedirect(reverse('event_blogvip_flow') + "?event=" + str(event.id))

    return render_to_response('frontpage.html', {})
