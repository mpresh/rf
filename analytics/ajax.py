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
    column_list.append({"id" : "network", "label" : "Network", "type" : "string"})
    column_list.append({"id" : "num_shares", "label" : "#Shares", "type" : "number"})
    column_list.append({"id" : "followers", "label" : "Followers", "type" : "number"})
    column_list.append({"id" : "reach", "label" : "Reach", "type" : "number"})
    data["cols"] = column_list


    rows_list = []
    user_dict = {}
    for share in shares:
        name = None
        if share.from_account_type == "F" and share.from_user_facebook:
            fbuser = FBUser.objects.get(id=share.from_user_facebook.id)
            name = fbuser.name or fbuser.facebook_id
            network = "Facebook"
        elif share.from_account_type == "T":
            print "helloTT", share.from_user_twitter
            user = User.objects.get(id=share.from_user_twitter.id)
            print "USERttt", user.name
            name = user.name 
            network = "Twitter"

        name_id = name + network

        if name_id  not in user_dict:
            user_dict[name_id] = {"name":name, 
                                  "network":network, 
                                  "num":1, 
                                  "reach":share.reach, 
                                  "totalReach":share.totalReach()}
        else:
            user_dict[name_id]["num"] = user_dict[name_id]["num"] + 1
            user_dict[name_id]["reach"] = user_dict[name_id]["reach"] + share.reach
            user_dict[name_id]["totalReach"] = user_dict[name_id]["totalReach"] + share.totalReach()

    for name_id in user_dict.keys():
        rows_list.append({"c" : [{"v" : user_dict[name_id]["name"]}, 
                                 {"v" : user_dict[name_id]["network"]},
                                 {"v" : user_dict[name_id]["num"]},
                                 {"v" : int(float(user_dict[name_id]["reach"]) / float(user_dict[name_id]["num"]))},
                                 {"v" : int(float(user_dict[name_id]["totalReach"]) / float(user_dict[name_id]["num"]))}]})

    data["rows"] = rows_list

    dict["status"] = 200
    dict["data"] = data
    print "Returning DICT", dict
    return HttpResponse(json.dumps(dict))
