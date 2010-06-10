# Taken almost verbatim from Henrik Lied's django-twitter-oauth app
# http://github.com/henriklied/django-twitter-oauth

from django.conf import settings
from django.utils import simplejson as json
import oauth
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

	print "oauth request parameters", parameters
	c = consumer()
	print "Consumer is ", c, type(c) 
	req = oauth.OAuthRequest.from_consumer_and_token(
		consumer(), token=token, http_url=url,
		parameters=parameters, http_method=http_method
	)
	print "Signature method", signature_method
	req.sign_request(signature_method, consumer(), token)
	print "REQUEST", req, dir(req)
	print "HTTP_url", req.http_url, req.get_normalized_http_url(), req.to_url
	return req

def oauth_response(req):
	url = req.to_url()
	parameters = req.parameters
	print "URL", url, parameters
	connection().request(req.http_method, url)
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
	req.sign_request(signature_method, consumer(), token)
	return oauth.OAuthToken.from_string(oauth_response(req))

def api(url, token, http_method='GET', **kwargs):
	try:
		return json.loads(oauth_response(oauth_request(
			url, token, http_method=http_method, parameters=kwargs
		)))
	except Exception, e:
		print "Exception in API", e, dir(e)
	return None

def is_authorized(token):
	return api('https://twitter.com/account/verify_credentials.json',
		token)
