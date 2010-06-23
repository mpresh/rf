from django.db import models
from pylib import oauth
import re, httplib
import simplejson as json

import urllib, httplib
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


	def feed(self, to="713879", message="Testing."):
		params = urllib.urlencode({'access_token' : self.access_token,
					   'message' : message})
		headers = {}
		conn = httplib.HTTPSConnection("graph.facebook.com")
		conn.request("POST", str(to) + "/feed", params, headers) 
		response = conn.getresponse()
		print "RESPONSE", response.status, response.reason
		data = response.read()
		conn.close()

		print "DATA IS", data


	def message(self, to="713879", message="Testing.", subject="subject"):
		params = urllib.urlencode({'access_token' : self.access_token,
					   'message' : message,
					   'subject' : subject})
		headers = {}
		conn = httplib.HTTPSConnection("graph.facebook.com")
		conn.request("POST", str(to) + "/notes", params, headers) 
		response = conn.getresponse()
		print "RESPONSE", response.status, response.reason
		data = response.read()
		conn.close()

		print "DATA IS", data
	

	def fill_info(self):
		""" Fill in information about user synchronously."""
		print "Filling info"
		data = urllib.urlopen("https://graph.facebook.com/" + 
				      str(self.facebook_id) + 
				      "?access_token=" + self.access_token).read()
		data_dict = json.loads(data)
		print data_dict
		self.name = data_dict["name"]
		
