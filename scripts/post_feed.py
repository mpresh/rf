import urllib
import httplib



def feed(to="me", message="Testing."):
    access_token = "374592118121|2.t2rEPwnPEoN3_12z2Cc1pA__.3600.1284652800-1809480|-uPxNO5W0DJkl4dUE-Rh9FU8Zqc"
    print "access_token", access_token
    #access_token = access_token.replace("%7C", "|")
    params = urllib.urlencode({'access_token' : access_token,
                               'message' : message})
    headers = {"Content-Type": "multipart/form-data",
               "Accept": "*/*",
               "Host": "graph.facebook.com"}
    headers = {}
    conn = httplib.HTTPSConnection("graph.facebook.com")
    print conn, dir(conn)
    conn.request("POST", "/me/feed", params, headers) 
    response = conn.getresponse()
    print "RESPONSE FEED", response.status, response.reason
    data = response.read()
    conn.close()
    print "DATA IS", data


def feed_post():
    access_token = "374592118121|2.t2rEPwnPEoN3_12z2Cc1pA__.3600.1284652800-1809480|-uPxNO5W0DJkl4dUE-Rh9FU8Zqc"
    message = "Testing."
    params = urllib.urlencode({'access_token' : access_token,
                               'message' : message})


    path = "/me/feed"
    result = urllib.urlopen("https://graph.facebook.com/" + path + "?" +
                          urllib.urlencode({}), params).read()
    print result

feed()
