from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponseServerError, HttpResponse
from django.core.urlresolvers import reverse
from pylib import oauth
from pylib.lazy import reverse
from utils import *
from models import User
from events.models import Event
from campaign.models import Campaign
from decorators import wants_user, needs_user
import simplejson as json
import urllib
from django.utils.functional import lazy
from pylib.util import handle_redirect_string
import re

reverse_lazy = lazy(reverse, unicode)

@needs_user(reverse('tauth_login'))
def info(req):
	pass
	if 'POST' == req.method:
		req.user.email = req.POST['email']
		errors = []
		if not errors: req.user.save()
		return render_to_response('info.html', {
			'user': req.user,
			'errors': errors
		})

	return render_to_response('info.html', {'user': req.user})

@needs_user(reverse('tauth_login'))
def tauth_info(req):
	if 'POST' == req.method:
		req.user.email = req.POST['email']
		#errors = req.user.validate()
		errors = []
		if not errors: req.user.save()
		return render_to_response('info.html', {
			'user': req.user,
			'errors': errors
		})
	
	user = User.objects.get(username=req.user.username)
	return render_to_response('info.html', {'user': req.user})



@wants_user
def login(req):
	print "ENTERING LOGIN"
	if 'redirect' not in req.session:
		req.session['redirect'] = str(reverse('index'))

	if "redirectArgs" in req.GET:
		print "calling handle_redirect_string", type(req.session["redirect"])
		req.session["redirect"] = handle_redirect_string(req.session["redirect"], req.GET["redirectArgs"])

	if req.user: 
		print "login redirect:", req.session['redirect']
		redirect = req.session['redirect']
		del req.session["redirect"]
		return HttpResponseRedirect(redirect)

	print "ABOUT TO: get_unauthorized_roken"
	try:
		token = get_unauthorized_token()
	except:
		HttpResponseRedirect(reverse("tauth_login"))
	print "unauthorized token", token
	req.session['token'] = token.to_string()
	url_auth = get_authorization_url(token)
	for key in req.session.keys():
		print "KEY LOGIN", key, req.session[key]

	#url_auth = url_auth + "&oauth_callback=" + urllib.quote("http://www.cnn.com")
	print "Twitter url login is ", url_auth

	return HttpResponseRedirect(url_auth)

def callback(req):
	token = req.session.get('token', None)
	#token = req.GET["oauth_token"]
	print "token is ", token
	if not token:
		print "TWITTER FAIL: NO TOKEN FOUND IN SESSION DURING CALLBACK"
		return HttpResponseRedirect(reverse('tauth_login'))

	token = oauth.OAuthToken.from_string(token)
	print "Token is  after oauth.OAuthToken.from_string(token)", token

	if token.key != req.GET.get('oauth_token', 'no-token'):
		print "TWITTER FAIL: token.key doesn't match oauth token. Login again."
		return HttpResponseRedirect(reverse('tauth_login'))

	print "get authorized token!", token
	token = get_authorized_token(token)
	print "RETURN FROM get_authorized_token", token

	if token is None:
		print "TWITTER FAIL: get_authorized_token(token) is None."
		return HttpResponseRedirect(reverse('tauth_login'))

	print "TOKEN MATCHES", token
	# Actually login
	obj = is_authorized(token)
	if obj is None:
		print "TWITTER FAIL: is_authorized(token) is None."
		return HttpResponseRedirect(reverse('tauth_login'))

	try: 
		user = User.objects.get(username=obj['screen_name'])
	except: 
		user = User(username=obj['screen_name'])
	user.oauth_token = token.key
	user.oauth_token_secret = token.secret
	user.save()
	req.session['user_id'] = user.id
	del req.session['token']

	if user.name == "":
		info = user.is_authorized()
		user.twitter_id = str(info["id"])
		user.name = str(info["name"])
		user.profile_pic = str(info["profile_image_url"])
		user.save()

	redirect = req.session["redirect"]
	
	print "REQUEST", req
	for key in req.session.keys():
		print "KEY CALLBACK", key, req.session[key]
	
	del req.session['redirect']
	if req.META["SERVER_NAME"].find("localhost") != -1:
		return HttpResponseRedirect(redirect)

	base_url = "http://" + req.META["SERVER_NAME"] + ":" + req.META["SERVER_PORT"]
	redirect = base_url + redirect
	if "refer_domain" in req.session and req.session["refer_domain"] != "wwww":
		redirect = redirect.replace("www", req.session["refer_domain"])
	print "REDIRECT", redirect

	return HttpResponseRedirect(redirect)

@wants_user
def logout(req):
	if "redirect" in req.session:
		redirect = str(req.session["redirect"])
		del req.session["redirect"]
	else:
		redirect = str(reverse('index'))

	print "REDIRECTS", redirect
	if "redirectArgs" in req.GET:
		redirect = handle_redirect_string(redirect, req.GET["redirectArgs"])

	if req.user is not None:
		req.user.oauth_token = ''
		req.user.oauth_token_secret = ''
		req.user.save()
	
	if "user_id" in req.session:
		del req.session["user_id"]

	if redirect:
		return HttpResponseRedirect(redirect)
	else:
		return render_to_response('logout.html', {})


"""
Below are json ajax functions that return information about friends.
"""
@needs_user(reverse('tauth_login'))
def follow_list(req):
	user = User.objects.get(username=req.user.username)	
	return HttpResponse(json.dumps(user.get_follow_list()))

@needs_user(reverse('tauth_login'))
def follower_list(req):
	user = User.objects.get(username=req.user.username)	
	return HttpResponse(json.dumps(user.get_follower_list()))

@needs_user(reverse('tauth_login'))
def friend_list(req):
	user = User.objects.get(username=req.user.username)	
	return HttpResponse(json.dumps(user.get_friend_list()))

def attendees(req, campaign_id=""):
	"""
	Return a list of users that are interested in teh campaign.
	If logged in, friends returned first.
	GET Parameter: event_id
	
	"""
	try:            
	    if campaign_id and campaign_id != "0":
	    	campaign = Campaign.objects.get(id=campaign_id)
	    	att_list = []	
	    	attendees_twitter = campaign.interested_twitter.all()
	    	for att in attendees_twitter:
	    		att_list.append([att.profile_pic, att.name, att.username, "twitter"])
	    	attendees_facebook = campaign.interested_facebook.all()
	    	for att in attendees_facebook:
	    		url = "http://graph.facebook.com/" + att.facebook_id + "/picture"
	    		#if not att.username:
	    		try:
	    			fid = re.match("http://graph.facebook.com/(\d+)/picture", url).group(1)
	    		except:
	    			fid = ""
	    		att_list.append([url, att.name, fid, "facebook"])
	    
	    		#else:
	    		#	att_list.append([url, att.name, att.username, "facebook"])
	    
	    	return HttpResponse(json.dumps(att_list))
	    else:
	    	return HttpResponse(json.dumps([]))
	except Exception as e:
		print e
