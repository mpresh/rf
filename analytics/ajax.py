import simplejson as json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404

from events.models import *
from fauth.models import *
from tauth.models import *

def analytics_data(req):
    """Return json data for DataTable format"""
    dict = {}
    req.session["redirect"] = req.get_full_path()
    print "called analytics data"

    if "event" in req.GET:
        try:
            event = Event.objects.get(id=req.GET["event"])
            shares = Share.objects.filter(event=event.id)
        except Exception as e:
            dict["error"] = "Valid Event id not provided."
            dict["status"] = 500
            return HttpResponse(json.dumps(dict))


    data = {}
    column_list = []
    column_list.append({"id" : "name", "label" : "Name", "type" : "string"})
    column_list.append({"id" : "num_shares", "label" : "#Shares", "type" : "number"})
    column_list.append({"id" : "followers", "label" : "Followers", "type" : "number"})
    column_list.append({"id" : "reach", "label" : "reach", "type" : "reach"})
    data["cols"] = column_list


    rows_list = []
    for share in shares:
        print "share", share
        name = None
        if share.from_account_type == "F" and share.from_user_facebook:
            print share.from_user_facebook, "KAKA"
            fbuser = FBUser.objects.get(id=share.from_user_facebook.id)
            name = fbuser.name or fbuser.facebook_id
        #elif share.from_account_type == "T"::
        #    fbuser = User.objects.get(id=share.from_user_twitter)
        #    name = user.name
        print "name is", name
        if name:
            print "LALAL"
            rows_list.append({"c" : [{"v" : name}, 
                                     {"v" : 1},
                                     {"v" : share.reach},
                                     {"v" : 500}]})
    data["rows"] = rows_list


    dict["status"] = 200
    dict["data"] = data
    print "Returning DICT", dict
    return HttpResponse(json.dumps(dict))
