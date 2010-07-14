from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponseServerError, HttpResponse
from django.core.urlresolvers import reverse
from pylib import oauth
from pylib.lazy import reverse
from utils import *
from models import User
from events.models import Event
from decorators import wants_user, needs_user
import simplejson as json
import urllib
from django.utils.functional import lazy
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
	pass
	if 'redirect' not in req.session:
		req.session['redirect'] = reverse('index')

	if "redirectArgs" in req.GET:
		redirectargs_list = req.GET["redirectArgs"].split("AND")
		redirect_string = ""
		for param in redirectargs_list:
			(key, value) = param.split("EQUALS")
			redirect_string += key + "=" + value + "&" 
		if redirect_string:
			redirect_string = redirect_string[:-1]

		if req.session["redirect"].find("?") != -1:
			if req.session["redirect"].find(redirect_string) == -1:
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
	token = req.session.get('token', None)
	#token = req.GET["oauth_token"]
	print "token is ", token
	if not token:
		print "am I here"
		return render_to_response('callback.html', {
			'token': True
		})

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
		redirect = req.session["redirect"]
		del req.session["redirect"]
	else:
		redirect = reverse('index')

	if "redirectArgs" in req.GET:
		redirectargs_list = req.GET["redirectArgs"].split("AND")
		redirect_string = ""
		for param in redirectargs_list:
			(key, value) = param.split("EQUALS")
			redirect_string += key + "=" + value + "&" 
		if redirect_string:
			redirect_string = redirect_string[:-1]
		if redirect.find("?") != -1:
			if redirect(redirect_string) == -1:
				redirect = redirect + "&" + redirect_string
		else:
			redirect = redirect + "?" + redirect_string

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

def attendees(req, event_id=""):
	"""
	Return a list of users attending the event.
	If logged in, friends returned first.
	GET Parameter: event_id
	
	"""
	if event_id:
		event = Event.objects.get(id=event_id)
		att_list = []	
		attendees = event.attendees.all()
		for att in attendees:
			att_list.append([att.profile_pic, att.name, att.username])
		return HttpResponse(json.dumps(att_list))
	else:
		return HttpResponse(json.dumps([]))

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
	
