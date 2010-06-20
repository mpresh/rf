from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from events.models import Event, Invite
from tauth.models import User
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
    print "\n\n\n\n\nFACEBOOK CALLBACK !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    print req
    cookies = req.COOKIES
    if "access_token" in cookies:
        req.session['access_token'] = cookies["access_token"]
        req.session['base_domain']  = cookies["base_domain"]
        req.session['secret'] = cookies["secret"]
        req.session['session_key'] = cookies["session_key"]
        req.session['sessionid'] = cookies["sessionid"]
        req.session['sig'] = cookies["sig"]
        req.session['uid'] = cookies["uid"]
    else:
        del req.session['access_token']
        del req.session['base_domain']
        del req.session['secret']
        del req.session['session_key']
        del req.session['sessionid']
        del req.session['sig']
        del req.session['uid']

    return HttpResponseRedirect(req.session['redirect'])
