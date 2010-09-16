import urllib
import httplib



def feed(to="me", message="Testing."):
    access_token = "374592118121|2.3kM3TxNrDodXdctbH6osTQ__.3600.1284681600-1809480|sBtcK40WJ_0s8hoaoEkaauSRxRw"
    params = urllib.urlencode({'access_token' : access_token,
                               'message' : message})
    headers = {"Content-Type": "multipart/form-data",
               "Accept": "*/*",
               "Host": "graph.facebook.com"}

    headers ={"Content-Type": "application/x-www-form-urlencoded",
              "Host": "graph.facebook.com",
              "Accept": "*/*"
        }

    conn = httplib.HTTPSConnection("graph.facebook.com")
    conn.set_debuglevel(3)
    conn.request("POST", "//me/feed?", params, headers) 
    print "connection", dir(conn)
    response = conn.getresponse()
    print response
    print "RESPONSE FEED", response.status, response.reason
    data = response.read()
    conn.close()
    print "DATA IS", data


def feed_post():
    access_token = "374592118121|2.3kM3TxNrDodXdctbH6osTQ__.3600.1284681600-1809480|sBtcK40WJ_0s8hoaoEkaauSRxRw"
    message = "Testing."
    params = urllib.urlencode({'access_token' : access_token,
                               'message' : message})
    httplib.HTTPConnection.debuglevel = 1
    print dir(urllib)
    path = "/me/feed"
    result = urllib.urlopen("https://graph.facebook.com/" + path + "?" +
                          urllib.urlencode({}), params).read()
    print result

feed()
