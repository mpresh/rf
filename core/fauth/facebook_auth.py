from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from events.models import Event
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
import fauth_utils
from pylib.util import handle_redirect_string

def facebook_login_callback(req):
    print "!!!FACEBOOK LOGIN CALLBACK", req
    
    try:
        code = req.GET["code"]
        #redirect = req.session["redirect"]
        print "CODE IS", code

        url = "https://graph.facebook.com/oauth/access_token?"
        url = url + "client_id=" + settings.FACEBOOK_API
        url = url + "&redirect_uri=" + "http://www.demo.com:8000/facebook_login_callback"
        url = url + "&client_secret=" + settings.FACEBOOK_SECRET
        url = url + "&code=" + code 

        print "URL IS", url
        result = urllib.urlopen(url).read()
        print "RETURNED RESULT", result
        list_of_values = result.split("&")
        values_dict = {}
        for value in list_of_values:
            (k, v) = value.split("=")
            values_dict[k] = v

        url = "https://graph.facebook.com/me?access_token=" + values_dict["access_token"]
        result = urllib.urlopen(url).read()
        
        my_info = json.loads(result)
        print "result", my_info

    except Exception as e:
        return render_to_response('facebook_login_callback.html', {"status":500})

    return render_to_response('facebook_login_callback.html', {"status":200})

def facebook_callback_test(req):
    print "FACEBOOK CALLBACK TEST", req
    return render_to_response('test3.html', {})

def facebook_callback(req):

    print "FACEBOOK CALLBACK", req
    for s in req.session.keys():
        print "SESSION", s, req.session[s]

    cookies = req.GET;
    fauth_utils.sync_session_cookies(req)

    for s in req.session.keys():
        print "SESSION", s, req.session[s]
    
    (user, create) = FBUser.objects.get_or_create(facebook_id=req.session['uid'])
    user.access_token = req.session["access_token"]
    user.save()
    user.fill_info()
    user.save()

    if "redirect" not in req.session:
        redirect = reverse('index')
    else:
        redirect = req.session['redirect']

    if "redirectArgs" in req.GET:
        redirect = handle_redirect_string(redirect, req.GET["redirectArgs"])

    return HttpResponseRedirect(redirect)

def facebook_callback_ajax(req):

    print "FACEBOOK CALLBACK AJAX", req
    for s in req.session.keys():
        print "SESSION", s, req.session[s]

    cookies = req.GET;
    print "hello world"
    fauth_utils.sync_session_cookies(req)

    for s in req.session.keys():
        print "SESSION", s, req.session[s]
    
    (user, create) = FBUser.objects.get_or_create(facebook_id=req.session['uid'])
    user.access_token = req.session["access_token"]
    user.save()
    user.fill_info()
    user.save()

    #if "redirect" not in req.session:
    #    redirect = reverse('index')
    #else:
    #    redirect = req.session['redirect']

    #if "redirectArgs" in req.GET:
    #    redirect = handle_redirect_string(redirect, req.GET["redirectArgs"])
    dict = {}

    return HttpResponse(json.dumps(dict))

def facebook_logout_callback(req):
    if "access_token" in req.session:
        del req.session['access_token']
        del req.session['base_domain']
        del req.session['secret']
        del req.session['session_key']
        del req.session['sessionid']
        del req.session['sig']
        del req.session['uid']

    if "access_token" in req.COOKIES:
        del req.COOKIES['access_token']
        del req.COOKIES['base_domain']
        del req.COOKIES['secret']
        del req.COOKIES['session_key']
        del req.COOKIES['sessionid']
        del req.COOKIES['sig']
        del req.COOKIES['uid']

    if "redirect" in req.session:
        redirect = req.session['redirect']

    if "redirectArgs" in req.GET:
        redirect = handle_redirect_string(redirect, req.GET["redirectArgs"])

    print "SESSION KEYS"
    for key in req.session.keys():
        print "KEY", key, req.session[key]

    print "COOKIES KEYS"
    for key in req.COOKIES.keys():
        print "KEY", key, req.COOKIES[key]
    print "redirecting logout", redirect
    return HttpResponseRedirect(redirect)


def facebook_server_callback(req):
    print "FACEBOOK SERVER CALLBACK"

    if "code" in req.GET:
        code = req.GET['code']
        client_id = settings.FACEBOOK_API
        redirect_uri = req.get_full_path() 
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

    
