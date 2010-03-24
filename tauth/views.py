from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponseServerError, HttpResponse
from django.core.urlresolvers import reverse
import oauth
from utils import *
from models import User
from decorators import wants_user, needs_user
import simplejson as json
import urllib

@needs_user('tauth_login')
def info(req):
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

@needs_user('tauth_login')
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
	print "HERE I AM"
	if 'redirect' not in req.session:
		req.session['redirect'] = "/tauth_info"

	if req.user: 
		redirect = req.session['redirect']
		del req.session["redirect"]
		return HttpResponseRedirect(redirect)

	token = get_unauthorized_token()
	req.session['token'] = token.to_string()

	return HttpResponseRedirect(get_authorization_url(token))

def callback(req):
	token = req.session.get('token', None)
	if not token:
		return render_to_response('callback.html', {
			'token': True
		})
	token = oauth.OAuthToken.from_string(token)

	if token.key != req.GET.get('oauth_token', 'no-token'):
		return render_to_response('callback.html', {
			'mismatch': True
		})
	token = get_authorized_token(token)

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
		print "AAAAA", info
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
		redirect = None

	if req.user is not None:
		req.user.oauth_token = ''
		req.user.oauth_token_secret = ''
		req.user.save()
	req.session.flush()

	if redirect:
		return HttpResponseRedirect(redirect)
	else:
		return render_to_response('logout.html', {})


"""
Below are json ajax functions that return information about friends.
"""
@needs_user('tauth_login')
def follow_list(req):
	user = User.objects.get(username=req.user.username)	
	return HttpResponse(json.dumps(user.get_follow_list()))

@needs_user('tauth_login')
def follower_list(req):
	user = User.objects.get(username=req.user.username)	
	return HttpResponse(json.dumps(user.get_follower_list()))

@needs_user('tauth_login')
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
			print "FRIEND", str(friend), url
			friend_obj = json.loads(urllib.urlopen(url).read())
			friends_dict[friend] = [friend_obj["name"], 
						friend_obj["profile_image_url"], 
						friend_obj["screen_name"]]

		return HttpResponse(json.dumps(friends_dict))
	
def maybe(req):
	"""
	Return a list of users maybe attending the event.
	If logged in, friends returned first.
	GET Parameter: event_id

	"""
