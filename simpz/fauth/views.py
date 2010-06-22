from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponseServerError, HttpResponse
from django.core.urlresolvers import reverse
from pylib import oauth
from models import FBUser
#from decorators import wants_user, needs_user
import simplejson as json
import urllib
