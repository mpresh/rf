from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from events.models import Event, Invite
from tauth.models import User
from models import FBUser
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


def facebook_callback(req):

    print "inside facebook callbacsk"
    cookies = req.COOKIES;
    print "COOKIES KEYS"
    for key in cookies.keys():
        print "KEY", key, cookies[key]
    if "access_token" in cookies:
        req.session['access_token'] = cookies["access_token"]
        req.session['base_domain']  = cookies["base_domain"]
        req.session['secret'] = cookies["secret"]
        req.session['session_key'] = cookies["session_key"]
        req.session['sessionid'] = cookies["sessionid"]
        req.session['sig'] = cookies["sig"]
        req.session['uid'] = cookies["uid"]

        (user, create) = FBUser.objects.get_or_create(facebook_id=req.session['uid'])
        user.access_token = req.session["access_token"]
        user.save()

        #if create:
        user.fill_info()
        user.friends()
        user.feed()

    print "SESSION KEYS"
    for key in req.session.keys():
        print "KEY", key, req.session[key]

    if "redirect" not in req.session:
        req.session["redirect"] = "/simpz/"
    return HttpResponseRedirect(req.session['redirect'])

def facebook_logout_callback(req):
    print "LOGOUT"
    del req.session['access_token']
    del req.session['base_domain']
    del req.session['secret']
    del req.session['session_key']
    del req.session['sessionid']
    del req.session['sig']
    del req.session['uid']

    return HttpResponseRedirect(req.session['redirect'])



def facebook_server_callback(req):
    print "FACEBOOK SERVER CALLBACK"

    if "code" in req.GET:
        code = req.GET['code']
        client_id = settings.FACEBOOK_API
        redirect_uri = "http://localhost:8000/simpz/facebook_callback"
        client_secret = settings.FACEBOOK_SECRET
        
        url = "https://graph.facebook.com/oauth/access_token?" + \
            "client_id=" + client_id + \
            "&redirect_uri=" + redirect_uri + \
            "&client_secret=" + client_secret + \
            "&code=" + code 

        print "URL IS ", url
        result =  urllib.urlopen(url).read()

        dict = {}
        params = result.split("&")
        for param in params:
            (key, value) = param.split("=")
            dict[key] = value

        return HttpResponse("RESULT " + str(dict))

    
