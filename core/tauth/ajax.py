from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponseServerError, HttpResponse
from django.core.urlresolvers import reverse
from pylib import oauth
from pylib.lazy import reverse
from utils import *
from models import User
from events.models import Event
from campaign.models import Campaign
from decorators import wants_user, needs_user
import simplejson as json
import urllib
from django.utils.functional import lazy
from pylib.util import handle_redirect_string
import re

reverse_lazy = lazy(reverse, unicode)


def check_twitter_logged_in(req):
    print "req CHECK TWITTER LOGGEED IN ", req
    if "user_id" in req.session:
        user = User.objects.get(id=req.session["user_id"])
        if user.oauth_token:
            return HttpResponse(json.dumps({"status": "1", "profile-img":user.profile_pic}))
    for key in req.session.keys():
        print "KEY", key, req.session[key]
    return HttpResponse(json.dumps({"status": "0"}))