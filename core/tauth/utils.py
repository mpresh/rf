# Taken almost verbatim from Henrik Lied's django-twitter-oauth app
# http://github.com/henriklied/django-twitter-oauth

from django.conf import settings
from django.utils import simplejson as json
from pylib import oauth
import httplib

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

	c = consumer()
	req = oauth.OAuthRequest.from_consumer_and_token(
		consumer(), token=token, http_url=url,
		parameters=parameters, http_method=http_method
	)
	req.sign_request(signature_method, consumer(), token)
	return req

def oauth_response(req):
	url = req.to_url()
	parameters = req.parameters
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
