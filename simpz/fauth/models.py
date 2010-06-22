from django.db import models
from pylib import oauth
import re, httplib
import simplejson as json
<<<<<<< HEAD
=======
#from utils import *
>>>>>>> 49039fee52a8d739f5876a97f5a85fd59c2791f0
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

        access_token = models.CharField(max_length=100, default="", blank=True)

        def get_friends(self):
		data = urllib.urlopen("https://graph.facebook.com/" + 
				      str(self.facebook_id) + "/friends" 
				      "?access_token=" + self.access_token).read()
		data_dict = json.loads(data)
		print data_dict

        def get_info(self):
            pass

	def message(self, to="713879"):
		result = urllib.urlopen("https://graph.facebook.com/" + 
					str(to) + "/notes" 
					"?access_token=" + self.access_token +
					"&message=Testing!" +
					"&subject=Testing").read() 
		print result
	

	def fill_info(self):
		print "Filling info"
		data = urllib.urlopen("https://graph.facebook.com/" + 
				      str(self.facebook_id) + 
				      "?access_token=" + self.access_token).read()
		data_dict = json.loads(data)
		print data_dict
		self.name = data_dict["name"]
		
