import urllib
import simplejson as json
from django.conf import settings

def shorten(long_url, login="mpresh", format="json"):
    url = "http://api.bit.ly/v3/shorten"
    params = urllib.urlencode({"longUrl" : long_url,
                               "login" : login,
                               "format" : format, 
                               "apiKey" : settings.BITLY_API,
                               })
    f = urllib.urlopen(url, params)
    json_dict = json.loads(f.read())
    if json_dict["status_code"] == 200:
        return json_dict["data"]["url"]
    else:
        return None
