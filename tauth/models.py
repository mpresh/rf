from django.db import models
import oauth
import re, httplib
import simplejson as json
from utils import *
import urllib
import time
import sys
import os
import socket

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
import settings

class User(models.Model):
	username = models.CharField(max_length=40)
	email = models.EmailField()
	name = models.CharField(max_length=100)
	profile_pic = models.CharField(max_length=100)
	twitter_id = models.CharField(max_length=20)
	url = models.URLField()

	oauth_token = models.CharField(max_length=200)
	oauth_token_secret = models.CharField(max_length=200)

	def validate(self):
		errors = []
		if self.username and not re.compile('^[a-zA-Z0-9_]{1,40}$').match( \
			self.username):
			errors += ['username']
		if self.email and not re.compile( \
			'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$').match( \
			self.email):
			errors += ['email']
		return errors

	# django.core.context_processors.auth assumes that an object attached
	# to request.user is always a django.contrib.auth.models.User, which
	# is completely broken but easy to work around
	def get_and_delete_messages(self): pass

	def token(self):
		return oauth.OAuthToken(self.oauth_token, self.oauth_token_secret)

	def is_authorized(self): return is_authorized(self.token())

	def tweet(self, status):
		return api(
			'https://twitter.com/statuses/update.json',
			self.token(),
			http_method='POST',
			status=status
		)

	def dm(self, status, to_person):
		return api(
			'https://twitter.com/statuses/update.json',
			self.token(),
			http_method='POST',
			status=status
		)

	def get_follow_list(self):
		return api(
			'http://api.twitter.com/1/friends/ids.json',
			self.token())

	def get_follower_list(self):
		return api(
			'http://api.twitter.com/1/followers/ids.json',
			self.token())

	def get_friend_list(self):
		follow = self.get_follow_list()
		followers = self.get_follower_list()
		print "Get Friend List follow", follow
		print "Get Friend List followers", followers
		return_val = [val for val in follow if val in followers]
		print "Friend Lsit", return_val
		return return_val

	def more_info(self, friends):
		friends = friends[0:8]
		friends_list = []
		for friend in friends:
			url = "http://api.twitter.com/1/users/show/" + str(friend) + ".json"
			print "FRIEND", str(friend), url
			friend_obj = json.loads(urllib.urlopen(url).read())
			friends_list.append(
				[friend,
				 friend_obj["name"], 
				 friend_obj["profile_image_url"], 
				 friend_obj["screen_name"]])
		return friends_list

	def get_friends_not_attending_event(self, event):
		"""
		Retreive friends that are not going to the event.
		Phot url, name.
		"""	
		user_friends_list = self.get_friend_list()
		event_attendees_list = event.attendees.all()
	
		friends_not_going_to_event = []
		
		# remove self from friend list
		if self.twitter_id in user_friends_list:
			user_friends_list.remove(self.twitter_id)

		for attendee in event_attendees_list:
			print "Attending", attendee.twitter_id
			if attendee.twitter_id in user_friends_list:
				user_friends_list.remove(attendee.twitter_id)
				
		print "user_firneds_list", user_friends_list
		dict = {}
		dict["cmd"] = "twitter_user_list_info"
		dict["username"] = self.username
		data = {}
		dict["data"] = data
		dict["data"]["oauth_token"] = self.oauth_token
		dict["data"]["oauth_token_secret"] = self.oauth_token_secret
		dict["data"]["users"] = user_friends_list
		to_send = json.dumps(dict) + "\n\r\n"
		
		port = 5002
		host = "localhost"

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((host, port))
		s.send(to_send)

		print "connection made", to_send
		buf = ""
		while 1:
			incoming = s.recv(1000)
			print "received ", incoming
			if not incoming:
				break
			buf += incoming
		s.close()
		
		print "result is", buf
		friends_not_going_to_event = json.loads(buf)
		return friends_not_going_to_event

