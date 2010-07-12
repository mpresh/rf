import simplejson as json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404

from events.models import *
from fauth.models import *
from tauth.models import *

from datetime import datetime, timedelta

def analytics_date_range(req):
    """Return data organized by date range."""
    dict = {}
    if "event" in req.GET:
        try:
            event = Event.objects.get(id=req.GET["event"])
            shares = Share.objects.filter(event=event.id)
        except Exception as e:
            dict["error"] = "Valid Event id not provided."
            dict["status"] = 500
            return HttpResponse(json.dumps(dict))
    else:
        dict["error"] = "Must specify event."
        dict["status"] = 500
        return HttpResponse(json.dumps(dict))

    range_type_list = ["minutes", "hours", "days", "weeks", "months", "years"]
    if "range_type" in req.GET:
        if req.GET["range_type"] not in range_type_list:
            dict["error"] = "Valid range not provided."
            dict["status"] = 500
            return HttpResponse(json.dumps(dict))
        else:
            range_type = req.GET["range_type"]
    elif "range_type" in req.POST:
        if req.POST["range_type"] not in range_type_list:
            dict["error"] = "Valid range not provided."
            dict["status"] = 500
            return HttpResponse(json.dumps(dict))
        else:
            range_type = req.POST["range_type"]
    else:
        dict["error"] = "range_type not specfied."
        dict["status"] = 500
        return HttpResponse(json.dumps(dict))

    if "range_duration" in req.GET:
        range_duration = req.GET["range_duration"]
    elif "range_duration" in req.POST:
        range_duration = req.POST["range_duration"]
    else:
        dict["error"] = "range_duration not specfied."
        dict["status"] = 500
        return HttpResponse(json.dumps(dict))
    range_duration = range_duration + 1

    try:
        range_duration = int(range_duration)
    except Exception as e:
        dict["error"] = "range_duration must be an integer value."
        dict["status"] = 500
        return HttpResponse(json.dumps(dict))

    data = {}
    column_list = []
    range_type_label = ""
    if range_type == "minutes":
        range_type_label = "Minutes"
        column_list.append({"id" : "range_type", "label" : "Minutes", "type" : "string"})
    elif range_type == "hours":
        range_type_label = "Hours"
        column_list.append({"id" : "range_type", "label" : "Hours", "type" : "string"})    
    elif range_type == "days":
        range_type_label = "Days"
        column_list.append({"id" : "range_type", "label" : "Days", "type" : "string"})    
    elif range_type == "weeks":
        range_type_label = "Weeks"
        column_list.append({"id" : "range_type", "label" : "Weeks", "type" : "string"})    
    elif range_type == "months":
        range_type_label = "Months"
        column_list.append({"id" : "range_type", "label" : "Months", "type" : "string"})    
    elif range_type == "Years":
        range_type_label = "Years"
        column_list.append({"id" : "range_type", "label" : "Years", "type" : "string"})    
    else:
        dict["error"] = "Valid range_type not specfied."
        dict["status"] = 500
        return HttpResponse(json.dumps(dict))

    column_list.append({"id" : "twitter", "label" : "Twitter", "type" : "number"})
    column_list.append({"id" : "facebook", "label" : "Facebook!", "type" : "number"})
    column_list.append({"id" : "total", "label" : "Total", "type" : "number"})
    data["cols"] = column_list
    
    buckets_dict = {}
    now = datetime.now()
    for val in range(0, range_duration):
        dt = now - timedelta(days=range_duration - val)
        bucket_dict[str(dt.year) + str(dt.month) str(dt.day)] = {"twitter" : 0, "facebook" : 0, "datetime": dt}

    for share in shares:
        dt = share.created_at
        

    rows_list = []
    for date_val in range(0, range_duration):
        twitter_val = date_val
        facebook_val = date_val
        rows_list.append({"c" : [{"v" : str(date_val)},
                                 {"v" : twitter_val},
                                 {"v" : facebook_val},
                                 {"v" : twitter_val + facebook_val}]})
    data["rows"] = rows_list

    dict["status"] = 200
    dict["data"] = data
    dict["range_type_label"] = range_type_label
    print "DATE Returning DICT", dict
    return HttpResponse(json.dumps(dict))

def analytics_sources_pie(req):
    """Return json for DataTable pie Format totals."""

    dict = {}

    if "event" in req.GET:
        try:
            event = Event.objects.get(id=req.GET["event"])
            shares = Share.objects.filter(event=event.id)
        except Exception as e:
            dict["error"] = "Valid Event id not provided."
            dict["status"] = 500
            return HttpResponse(json.dumps(dict))
    else:
        dict["error"] = "Must specify event."
        dict["status"] = 500
        return HttpResponse(json.dumps(dict))

    data = {}
    column_list = []
    column_list.append({"id" : "network_type", "label" : "Network", "type" : "string"})
    column_list.append({"id" : "number_shares", "label" : "Number Shares", "type" : "number"})
    data["cols"] = column_list

    rows_list = []
    network_dict = {}
    for share in shares:
        print "Going through shares", share
        if share.from_account_type == "T":
            print "twitter"
            if "twitter" not in network_dict:
                network_dict["twitter"] = 1
            else:
                network_dict["twitter"] = network_dict["twitter"] + 1

        if share.from_account_type == "F":
            print "facebook"
            if "facebook" not in network_dict:
                network_dict["facebook"] = 1
            else:
                network_dict["facebook"] = network_dict["facebook"] + 1
    print "hello world"

    for key in network_dict.keys():
        rows_list.append({"c" : [{"v" : key},
                                 {"v" : network_dict[key]}]})
    
    data["rows"] = rows_list

    dict["status"] = 200
    dict["data"] = data
    print "Returning DICT", dict
    return HttpResponse(json.dumps(dict))


def analytics_data(req):
    """Return json data for DataTable format"""
    dict = {}

    if "event" in req.GET:
        try:
            event = Event.objects.get(id=req.GET["event"])
            shares = Share.objects.filter(event=event.id)
        except Exception as e:
            dict["error"] = "Valid Event id not provided."
            dict["status"] = 500
            return HttpResponse(json.dumps(dict))
    else:
        dict["error"] = "Must specify event."
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
