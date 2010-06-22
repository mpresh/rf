from django.db import models
from pylib import oauth
import re, httplib
import simplejson as json
#from utils import *
import urllib
import time
import sys
import os
import socket

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
import settings

class FBUser(models.Model):
    	username = models.CharField(max_length=40, default="")
	email = models.EmailField(default="", blank=True)
	name = models.CharField(max_length=100, default="", blank=True)
	profile_pic = models.CharField(max_length=100, default="", blank=True)
	facebook_id = models.CharField(max_length=20, default="", blank=True)
        auth_token = models.CharField(max_length=100, default="", blank=True)

        def get_friends(self):
            pass

        def get_info(self):
            pass
