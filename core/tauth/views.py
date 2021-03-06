import re
import urlparse

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.utils.functional import lazy
import simplejson as json

from pylib import oauth
from pylib.lazy import reverse
from pylib.util import handle_redirect_string

from utils import *
from models import User
from campaign.models import Campaign
from decorators import wants_user, needs_user

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
	
	return render_to_response('info.html', {'user': req.user})



@wants_user
def login(req):
	host = "http://" + req.get_host()
	print "ENTERING LOGIN", req, "end login req"
	if 'redirect' not in req.session:
		req.session['redirect'] = host + str(reverse('facebook_callback_close'))
		
	if "popup" in req.GET:
		req.session['redirect'] = host + str(reverse('facebook_callback_close'))

	if "redirectArgs" in req.GET:
		print "calling handle_redirect_string", type(req.session["redirect"])
		req.session["redirect"] = handle_redirect_string(req.session["redirect"], req.GET["redirectArgs"])

	if req.user is not None:# and "oauth_token" in req.user:
		if req.user.oauth_token:
			print "USERAAA", req.user, req.user.oauth_token
		
			print req.user, "login redirect:", req.session['redirect']
			redirect = req.session['redirect']
			del req.session["redirect"]
			return HttpResponseRedirect(redirect)

	try:
		token = get_unauthorized_token()
	except:
		HttpResponseRedirect(reverse("tauth_login"))
	print "unauthorized token", token
	req.session['token'] = token.to_string()
	url_auth = get_authorization_url(token)


	print "Twitter url login is ", url_auth
	return HttpResponseRedirect(url_auth)

def callback(req):
	token = req.session.get('token', None)
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
	
	for key in req.session.keys():
		print "KEY CALLBACK", key, req.session[key]
	
	del req.session['redirect']
	if req.META["SERVER_NAME"].find("localhost") != -1:
		return HttpResponseRedirect(redirect)

	parsed_redirect = urlparse.urlparse(redirect)
	
	base_url = "http://" + req.META["SERVER_NAME"] + ":" + req.META["SERVER_PORT"]
	redirect = base_url + parsed_redirect.path
	if "refer_domain" in req.session and req.session["refer_domain"] != "wwww":
		redirect = redirect.replace("www", req.session["refer_domain"])
	print "REDIRECT", redirect

	return HttpResponseRedirect(redirect)

@wants_user
def logout(req):
	print "tauth_logout REQQQ", req
	if "redirect" in req.session:
		redirect = str(req.session["redirect"])
		del req.session["redirect"]
	else:
		redirect = str(reverse('facebook_callback_close'))
	
	if "popup" in req.GET:
		redirect = str(reverse('facebook_callback_close'))
	
	if "redirectArgs" in req.GET:
		redirect = handle_redirect_string(redirect, req.GET["redirectArgs"])
	
	if req.user is not None:
		req.user.oauth_token = ''
		req.user.oauth_token_secret = ''
		req.user.save()
		print "LOGOUT oauth_token", req.user.oauth_token
	
	if "user_id" in req.session:
		del req.session["user_id"]

	if "popup" in req.GET:
		    return HttpResponse(json.dumps({}))

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

