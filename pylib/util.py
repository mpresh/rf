import httplib
import simplejson

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils import simplejson as json

from pylib import oauth

# Utility functions
def handle_redirect_string(redirect_url, redirect_args_string):
    redirect_url = redirect_url.replace("fb_xd_fragment", "")
    redirect_args_string = redirect_args_string.replace("fb_xd_fragment", "")

    print "HANDLE_REDIRECT_STRING", redirect_url, redirect_args_string
    redirectargs_list = redirect_args_string.split("AND")
    args_dict = {}
    for param in redirectargs_list:
        (key, value) = param.split("EQUALS")
        args_dict[key] = value
    

    print "REDIRECT_URL", redirect_url
    query_args_dict = {}
    if redirect_url.find("?") != -1:
        (url, query_string) = redirect_url.split("?")
        query_args = query_string.split("&")
        print "QUERY ARGS", query_args
        for arg in query_args:
            if arg.strip():
                (key, value) = arg.split("=")
                query_args_dict[key] = value
    else:
        url = redirect_url 
        

    for key in args_dict.keys():
        query_args_dict[key] = args_dict[key]

    query_args_list = ["%s=%s" % (key, query_args_dict[key]) 
                       for key in query_args_dict.keys()]
    redirect = url + "?" + "&".join(query_args_list)

    print "REDIRECT STRING RETURNING", redirect
    return redirect

def render_template(template, **template_variables):
    """ Wrapper which makes rendering templates nicer."""
    return render_to_response(template, template_variables)

def json_response(**keys):
    """ Render error json. """
    return HttpResponse(simplejson.dumps(keys))

def get_invite_url(req):
    # getting the right path
    invite_url = req.build_absolute_uri() 
    return invite_url
    start = invite_url.find("?")
    if start != -1:
        invite_url = invite_url[:start]
    path = req.get_full_path()
    start = path.find("?")
    if start != -1:
        path = path[:start]
    invite_url = invite_url.strip("/")
    if path[-1] == "/":
        path = path[:-1]

    invite_url = invite_url[:len(path) * -1] + reverse('event_invite', kwargs={'event_id':''})
    return invite_url

def sync_session_cookies(req):
    cookies = req.COOKIES
    if "access_token" in cookies and 'access_token' not in req.session:
        req.session['access_token'] = cookies["access_token"]
        req.session['base_domain']  = cookies["base_domain"]
        req.session['secret'] = cookies["secret"]
        req.session['session_key'] = cookies["session_key"]
        req.session['sessionid'] = cookies["sessionid"]
        req.session['sig'] = cookies["sig"]
        req.session['uid'] = cookies["uid"]

def sync_session_cookies_v2(req):
    cookies = req.COOKIES
    print "COOKIES", cookies
    if "access_token" in cookies and 'access_token' not in req.session:
        req.session['access_token'] = cookies["access_token"]

    if "base_domain" in cookies and 'base_domain' not in req.session:
        req.session['base_domain']  = cookies["base_domain"]

    if "secret" in cookies and 'secret' not in req.session:
        req.session['secret'] = cookies["secret"]

    if "session_key" in cookies and 'session_key' not in req.session:
        req.session['session_key'] = cookies["session_key"]

    if "sessionid" in cookies and 'sessionid' not in req.session:
        req.session['sessionid'] = cookies["sessionid"]

    if "sig" in cookies and 'sig' not in req.session:
        req.session['sig'] = cookies["sig"]

    if "uid" in cookies and 'uid' not in req.session:
        req.session['uid'] = cookies["uid"]

# Taken almost verbatim from Henrik Lied's django-twitter-oauth app
# http://github.com/henriklied/django-twitter-oauth

signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()

TWITTERAUTH_KEY = getattr(settings, 'TWITTERAUTH_KEY', 'OH HAI')
TWITTERAUTH_SECRET = getattr(settings, 'TWITTERAUTH_SECRET', 'OH NOES')

def consumer():
	try: return consumer._consumer
	except AttributeError:
		consumer._consumer = oauth.OAuthConsumer(TWITTERAUTH_KEY, TWITTERAUTH_SECRET)
		return consumer._consumer

def connection():
	try: return connection._connection
	except AttributeError:
		connection._connection = httplib.HTTPSConnection('twitter.com')
		return connection._connection

def oauth_request(
	url,
	token,
	parameters=None,
	signature_method=signature_method,
	http_method='GET'
):

	req = oauth.OAuthRequest.from_consumer_and_token(
		consumer(), token=token, http_url=url,
		parameters=parameters, http_method=http_method
	)
	req.sign_request(signature_method, consumer(), token)
	return req

def oauth_response(req):
	url = req.to_url()
	conn = connection()
	conn.request(req.http_method, url)
	return connection().getresponse().read()

def get_unauthorized_token(signature_method=signature_method):
	req = oauth.OAuthRequest.from_consumer_and_token(
		consumer(), http_url='https://twitter.com/oauth/request_token'
	)
	req.sign_request(signature_method, consumer(), None)
	return oauth.OAuthToken.from_string(oauth_response(req))

def get_authorization_url(token, signature_method=signature_method):
	req = oauth.OAuthRequest.from_consumer_and_token(
		consumer(), token=token,
		http_url='http://twitter.com/oauth/authorize'
	)
	req.sign_request(signature_method, consumer(), token)
	return req.to_url()

def get_authorized_token(token, signature_method=signature_method):
	req = oauth.OAuthRequest.from_consumer_and_token(
		consumer(), token=token,
		http_url='https://twitter.com/oauth/access_token'
	)
	print "func: tauth.get_authorized_token"
	req.sign_request(signature_method, consumer(), token)
	print "func: tauth.get_authorized_token after req.sign", req
	resp = oauth_response(req)
	print "func: tauth.get_authorized_token after RESPONSE", resp
	
	try:
		ret = oauth.OAuthToken.from_string(resp)
		print "func: tauth.get_authorized_token after RETURN", ret
		return ret 
	except:
		return None

def api(url, token, http_method='GET', **kwargs):
	try:
                oauth_req = oauth_request(
			url, token, http_method=http_method, parameters=kwargs
		)
		request_val = oauth_response(oauth_req)		
		return json.loads(request_val)
	except Exception, e:
		print "Exception in API", e, dir(e)
	return None

def is_authorized(token):
	return api('https://twitter.com/account/verify_credentials.json',
		token)
