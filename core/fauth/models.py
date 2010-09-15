from django.db import models
from pylib import oauth
import re, httplib
import simplejson as json

import urllib, httplib
import time
import sys
import os
import socket
import re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
import settings

class FBUser(models.Model):
    	username = models.CharField(max_length=80, default="")
	email = models.EmailField(default="", blank=True)
	name = models.CharField(max_length=200, default="", blank=True)
	profile_pic = models.CharField(max_length=200, default="", blank=True)
	facebook_id = models.CharField(max_length=40, default="", blank=True)

        access_token = models.CharField(max_length=300, default="", blank=True)

	def __unicode__(self):
		return "<Facebook User: %s %s %s %s>" % (self.id, self.username, self.facebook_id, self.name)

	def get_profile_pic(self):
		#return "http://www.facebook.com/profile.php?id=%s" % (self.facebook_id)
		return "http://graph.facebook.com/%s/picture" % (self.facebook_id)

        def friends(self):
		print "grabbing friends data"
		data = urllib.urlopen("https://graph.facebook.com/" + 
				      str(self.facebook_id) + "/friends" 
				      "?access_token=" + self.access_token).read()
		#data_dict = json.loads(data)
		return data

	def num_friends(self):
		data = urllib.urlopen("https://graph.facebook.com/" + 
				      str(self.facebook_id) + "/friends"
                		      "?access_token=" + self.access_token).read()
		data_dict = json.loads(data)
		print "URL", "https://graph.facebook.com/" + str(self.facebook_id) + "/friends?access_token=" + self.access_token
		print "self.access_token", self.access_token
                print "DATA", data_dict
		return len(data_dict['data'])

	def num_friends_post(self):
                params = urllib.urlencode({'access_token' : self.access_token})
		headers = {"Content-Type": "multipart/form-data",
			   "Accept": "*/*"}
		conn = httplib.HTTPSConnection("graph.facebook.com")
		conn.request("POST", "/" + str(self.facebook_id) + "/friends", params, headers) 
		response = conn.getresponse()
                data = response.read()
		data_dict = json.loads(data)
		
                print "DATA", data_dict
		return len(data_dict['data'])

	def feed(self, to="me", message="Testing."):
		print "self.access_token", self.access_token
	        #self.access_token = "374592118121|2.L1AZSRgyEco_AAqk2KSIrg__.3600.1284566400-1809480|pftR96mozxCtTFolrUKzY7qK6ZU"
		self.access_token = self.access_token.replace("%7C", "|")
		params = urllib.urlencode({'access_token' : self.access_token,
					   'message' : message})
		headers = {"Content-Type": "multipart/form-data",
			   "Accept": "*/*"}
		print "PARAMS", params
		conn = httplib.HTTPSConnection("graph.facebook.com")
		conn.request("POST", "/" + str(to) + "/feed", params, headers) 
		response = conn.getresponse()
		print "RESPONSE FEED", response.status, response.reason
		data = response.read()
		conn.close()
		print "DATA IS", data
	

	def message(self, to="713879", message="Testing.", subject="subject"):
		self.access_token = self.access_token.replace("%7C", "|")
		params = urllib.urlencode({'access_token' : self.access_token,
					   'message' : message,
					   'subject' : subject})
		headers = {"Content-Type": "multipart/form-data",
			   "Accept": "*/*"}
		conn = httplib.HTTPSConnection("graph.facebook.com")
		conn.request("POST", "/" + str(to) + "/notes", params, headers) 
		response = conn.getresponse()
		print "RESPONSE", response.status, response.reason
		data = response.read()
		conn.close()

		print "DATA IS", data
	

	def fill_info(self):
		""" Fill in information about user synchronously."""
		print "Filling info", self.facebook_id, self.access_token
		data = urllib.urlopen("https://graph.facebook.com/" + 
				      str(self.facebook_id) + 
				      "?access_token=" + self.access_token).read()
		print "Returned value", data
		data_dict = json.loads(data)
		if "error" in data_dict:
			return

		if "name" in data_dict:
			self.name = data_dict["name"]
		if "email" in data_dict:
			self.email = data_dict["email"]
		if "link" in data_dict:
			try:
				link = data_dict["link"]
				mo = re.match(".*[/](.*?)$", link)
				if mo:
					self.username = mo.group(1)
			except:
				pass
		self.save()
