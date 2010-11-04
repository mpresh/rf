from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response

from create import *
from fauth.models import FBUser

def facebook_login_test(req):
    #print req
    req.session["redirect"] = reverse("facebook_login_test")
    dict = {}
    host = "http://" + req.get_host()
    dict["facebook_app_id"] = settings.FACEBOOK_APP_ID
    dict["facebook_api"] = settings.FACEBOOK_API
    dict["redirect_uri"] = host + reverse("facebook_login_callback")
    dict["scope"] = "publish_stream"
    
    if "uid" in req.session:
        fbuser = FBUser.objects.get(facebook_id=req.session["uid"])
        dict["fbuser"] = fbuser
    return render_to_response('facebook_login_test.html', dict)


def facebook_callback_close(req):
    print "FACEBOOK CALLBACK CLOSE", req
    return render_to_response('facebook_close.html', {})
