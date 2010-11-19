from django.http import HttpResponse
from django.utils.functional import lazy
import simplejson as json

from models import User
from pylib.lazy import reverse
from pylib.util import *

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
