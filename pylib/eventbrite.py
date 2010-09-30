"""
Eventbrite api

"""

__author__    = "Josh Toft <josh@fwix.com>"
__copyright__ = "Copyright 2010 Fwix, Inc."
__license__   = "MIT"

import md5
import urllib

import httplib2
import simplejson

__all__ = ['APIError', 'API']

class APIError(Exception):
    pass

class API:
    def __init__(self, app_key, server='www.eventbrite.com', cache=None):
        """Create a new Eventbrite API client instance.
        If you don't have an application key, you can request one:
        http://www.eventbrite.com/api/key/"""
        self.app_key = app_key
        self.server = server
        self.http = httplib2.Http(cache)

    def call(self, method, **args):
        "Call the Eventbrite API's METHOD with ARGS."
        # Build up the request
        args['app_key'] = self.app_key
        if hasattr(self, 'user_key'):
            args['user'] = self.user
            args['user_key'] = self.user_key
        args = urllib.urlencode(args)
        url = "http://%s/json/%s?%s" % (self.server, method, args)

        # Make the request
        response, content = self.http.request(url, "GET")

        # Handle the response
        status = int(response['status'])
        if status == 200:
            try:
                return simplejson.loads(content)
            except ValueError:
                raise APIError("Unable to parse API response!")
        elif status == 404:
            raise APIError("Method not found: %s" % method)
        else:
            raise APIError("Non-200 HTTP response status: %s" % response['status'])

