from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponseServerError, HttpResponse
from django.core.urlresolvers import reverse
from pylib import oauth
from utils import *
from models import User
from decorators import wants_user, needs_user
import simplejson as json
import urllib

@needs_user('/simpz/tauth_login')
def info(req):
	if 'POST' == req.method:
		req.user.email = req.POST['email']
		errors = []
		if not errors: req.user.save()
		return render_to_response('info.html', {
			'user': req.user,
			'errors': errors
		})

	return render_to_response('info.html', {'user': req.user})

@needs_user('/simpz/tauth_login')
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
	if 'redirect' not in req.session:
		req.session['redirect'] = "/simpz/"

	if "redirectArgs" in req.GET:
		redirectargs_list = req.GET["redirectArgs"].split("AND")
		redirect_string = ""
		for param in redirectargs_list:
			(key, value) = param.split("EQUALS")
			redirect_string += key + "=" + value + "&" 
		if redirect_string:
			redirect_string = redirect_string[:-1]

		if req.session["redirect"].find("?") != -1:
			req.session["redirect"] = req.session["redirect"] + "&" + redirect_string
		else:
			req.session["redirect"] = req.session["redirect"] + "?" + redirect_string

	if req.user: 
		print "login redirect:", req.session['redirect']
		redirect = req.session['redirect']
		del req.session["redirect"]
		return HttpResponseRedirect(redirect)
	token = get_unauthorized_token()
	print "unauthorized token", token
	req.session['token'] = token.to_string()
	url_auth = get_authorization_url(token)
	for key in req.session.keys():
		print "KEY LOGIN", key, req.session[key]

	print "url is ", url_auth
	return HttpResponseRedirect(url_auth)

def callback(req):
	print req.session.keys()
	for key in req.session.keys():
		print "KEY CALLBACK", key, req.session[key]
	token = req.session.get('token', None)
	#token = req.GET["oauth_token"]
	print "token is ", token
	if not token:
		print "am I here"
		return render_to_response('callback.html', {
			'token': True
		})

	print "this is problem", oauth.__file__
	token = oauth.OAuthToken.from_string(token)
	print "AM I HERE!!", token

	if token.key != req.GET.get('oauth_token', 'no-token'):
		return render_to_response('callback.html', {
			'mismatch': True
		})
	print "get authorized oken"
	token = get_authorized_token(token)

	print "TOKEN MATCHES", token
	# Actually login
	obj = is_authorized(token)
	if obj is None:
		return render_to_response('callback.html', {
			'username': True
		})

	try: user = User.objects.get(username=obj['screen_name'])
	except: user = User(username=obj['screen_name'])
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
	del req.session['redirect']
	return HttpResponseRedirect(redirect)

@wants_user
def logout(req):
	if "redirect" in req.session:
		redirect = req.session["redirect"]
		del req.session["redirect"]
	else:
		redirect = "/simpz/"

	if "redirectArgs" in req.GET:
		redirectargs_list = req.GET["redirectArgs"].split("AND")
		redirect_string = ""
		for param in redirectargs_list:
			(key, value) = param.split("EQUALS")
			redirect_string += key + "=" + value + "&" 
		if redirect_string:
			redirect_string = redirect_string[:-1]
		redirect = redirect + "?" + redirect_string

	if req.user is not None:
		req.user.oauth_token = ''
		req.user.oauth_token_secret = ''
		req.user.save()
	del req.session["user_id"]

	if redirect:
		return HttpResponseRedirect(redirect)
	else:
		return render_to_response('logout.html', {})


"""
Below are json ajax functions that return information about friends.
"""
@needs_user('/simpz/tauth_login')
def follow_list(req):
	user = User.objects.get(username=req.user.username)	
	return HttpResponse(json.dumps(user.get_follow_list()))

@needs_user('/simpz/tauth_login')
def follower_list(req):
	user = User.objects.get(username=req.user.username)	
	return HttpResponse(json.dumps(user.get_follower_list()))

@needs_user('/simpz/tauth_login')
def friend_list(req):
	user = User.objects.get(username=req.user.username)	
	return HttpResponse(json.dumps(user.get_friend_list()))

def attendees(req):
	"""
	Return a list of users attending the event.
	If logged in, friends returned first.
	GET Parameter: event_id
	
	"""
	
	if "user_id" in req.session:
		user = User.objects.get(id=req.session["user_id"])	
		friends = user.get_friend_list()

		friends_dict = {}
		for friend in friends:
			url = "http://api.twitter.com/1/users/show/" + str(friend) + ".json"
			friend_obj = json.loads(urllib.urlopen(url).read())
			friends_dict[friend] = [friend_obj["name"], 
						friend_obj["profile_image_url"], 
						friend_obj["screen_name"]]

		return HttpResponse(json.dumps(friends_dict))
	
