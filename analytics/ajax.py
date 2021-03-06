from datetime import datetime, timedelta

from django.http import HttpResponse
import simplejson as json

from campaign.models import Campaign
from events.models import *
from fauth.models import *
from tauth.models import *


def analytics_date_range_reach(req):
    """Return data organized by date range."""
    dict = {}
    if "campaign" in req.GET:
        try:
            campaign = Campaign.objects.get(id=req.GET["campaign"])
            shares = Share.objects.filter(campaign=campaign.id)
        except Exception:
            dict["error"] = "Valid campaign id not provided."
            dict["status"] = 500
            return HttpResponse(json.dumps(dict))
    else:
        dict["error"] = "Must specify campaign."
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

    try:
        range_duration = int(range_duration)
    except Exception:
        dict["error"] = "range_duration must be an integer value."
        dict["status"] = 500
        return HttpResponse(json.dumps(dict))
    range_duration = range_duration + 1
    
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

    #column_list.append({"id" : "twitter", "label" : "Twitter", "type" : "number"})
    #column_list.append({"id" : "facebook", "label" : "Facebook", "type" : "number"})
    column_list.append({"id" : "total", "label" : "Total", "type" : "number"})
    data["cols"] = column_list
    
    bucket_dict = {}
    now = datetime.now()
    for val in range(0, range_duration):
        dt = now - timedelta(days=range_duration - val - 1)
        m = "0" + str(dt.month)
        d = "0" + str(dt.day)
        key = str(dt.year) + m[-2:] + d[-2:]
        bucket_dict[key] = {"twitter" : 0, "facebook" : 0, "datetime": dt}

    for share in shares:
        dt = share.created_at
        m = "0" + str(dt.month)
        d = "0" + str(dt.day)
        key = str(dt.year) + m[-2:] + d[-2:]
        if key in bucket_dict:
            if share.from_account_type == "F":
                bucket_dict[key]["facebook"] =  bucket_dict[key]["facebook"] + share.getReach()
            elif share.from_account_type == "T":
                bucket_dict[key]["twitter"] =  bucket_dict[key]["twitter"] + share.getReach()

    rows_list = []
    for key in sorted(bucket_dict.keys()):
        rows_list.append({"c" : [{"v" : str(key)[4:6] + "/" + str(key)[6:]},
                                # {"v" : bucket_dict[key]["twitter"]},
                                # {"v" : bucket_dict[key]["facebook"]}]})
                                 {"v" : bucket_dict[key]["twitter"] + bucket_dict[key]["facebook"]}]})
    data["rows"] = rows_list

    dict["status"] = 200
    dict["data"] = data
    dict["range_type_label"] = range_type_label
    print "DATE Returning DICT", dict
    return HttpResponse(json.dumps(dict))


def analytics_date_range_shares(req):
    """Return data organized by date range."""
    dict = {}
    if "campaign" in req.GET:
        try:
            campaign = Campaign.objects.get(id=req.GET["campaign"])
            shares = Share.objects.filter(campaign=campaign.id)
        except Exception:
            dict["error"] = "Valid Campaign id not provided."
            dict["status"] = 500
            return HttpResponse(json.dumps(dict))
    else:
        dict["error"] = "Must specify campaign."
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

    try:
        range_duration = int(range_duration)
    except Exception:
        dict["error"] = "range_duration must be an integer value."
        dict["status"] = 500
        return HttpResponse(json.dumps(dict))
    range_duration = range_duration + 1
    
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
    column_list.append({"id" : "facebook", "label" : "Facebook", "type" : "number"})
    #column_list.append({"id" : "total", "label" : "Total", "type" : "number"})
    data["cols"] = column_list
    
    bucket_dict = {}
    now = datetime.now()
    for val in range(0, range_duration):
        dt = now - timedelta(days=range_duration - val - 1)
        m = "0" + str(dt.month)
        d = "0" + str(dt.day)
        key = str(dt.year) + m[-2:] + d[-2:]
        bucket_dict[key] = {"twitter" : 0, "facebook" : 0, "datetime": dt}

    for share in shares:
        dt = share.created_at
        m = "0" + str(dt.month)
        d = "0" + str(dt.day)
        key = str(dt.year) + m[-2:] + d[-2:]
        if key in bucket_dict:
            if share.from_account_type == "F":
                bucket_dict[key]["facebook"] =  bucket_dict[key]["facebook"] + 1
            elif share.from_account_type == "T":
                bucket_dict[key]["twitter"] =  bucket_dict[key]["twitter"] + 1

    rows_list = []
    for key in sorted(bucket_dict.keys()):
        rows_list.append({"c" : [{"v" : str(key)[4:6] + "/" + str(key)[6:]},
                                 {"v" : bucket_dict[key]["twitter"]},
                                 {"v" : bucket_dict[key]["facebook"]},
                         #        {"v" : bucket_dict[key]["twitter"] + bucket_dict[key]["facebook"]}
                         ]})
    data["rows"] = rows_list

    dict["status"] = 200
    dict["data"] = data
    dict["range_type_label"] = range_type_label
    print "DATE Returning DICT", dict
    return HttpResponse(json.dumps(dict))


def analytics_sources_pie(req):
    """Return json for DataTable pie Format totals."""

    dict = {}

    if "campaign" in req.GET:
        try:
            campaign = Campaign.objects.get(id=req.GET["campaign"])
            shares = Share.objects.filter(campaign=campaign.id)
        except Exception:
            dict["error"] = "Valid Campaign id not provided."
            dict["status"] = 500
            return HttpResponse(json.dumps(dict))
    else:
        dict["error"] = "Must specify campaign."
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

    try:
        range_duration = int(range_duration)
    except Exception:
        dict["error"] = "range_duration must be an integer value."
        dict["status"] = 500
        return HttpResponse(json.dumps(dict))
    range_duration = range_duration + 1

    bucket_dict = {}
    now = datetime.now()
    for val in range(0, range_duration):
        dt = now - timedelta(days=range_duration - val - 1)
        m = "0" + str(dt.month)
        d = "0" + str(dt.day)
        key = str(dt.year) + m[-2:] + d[-2:]
        bucket_dict[key] = {"twitter" : 0, "facebook" : 0, "datetime": dt}

    
    network_dict = {}
    #for share in shares:
    #    if share.from_account_type == "T":
    #        if "twitter" not in network_dict:
    #            network_dict["twitter"] = 1
    #        else:
    #            network_dict["twitter"] = network_dict["twitter"] + 1
    #
    #    if share.from_account_type == "F":
    #        if "facebook" not in network_dict:
    #            network_dict["facebook"] = 1
    #        else:
    #            network_dict["facebook"] = network_dict["facebook"] + 1
    #
    #
    #total_facebook = 0
    #total_twitter = 0
    network_dict["facebook"] = 0
    network_dict["twitter"] = 0
    for share in shares:
        dt = share.created_at
        m = "0" + str(dt.month)
        d = "0" + str(dt.day)
        key = str(dt.year) + m[-2:] + d[-2:]
        if key in bucket_dict:
            if share.from_account_type == "F":
                network_dict["facebook"] = network_dict["facebook"] + 1
                bucket_dict[key]["facebook"] =  bucket_dict[key]["facebook"] + 1
            elif share.from_account_type == "T":
                network_dict["twitter"] = network_dict["twitter"] + 1
                bucket_dict[key]["twitter"] =  bucket_dict[key]["twitter"] + 1


    data = {}
    column_list = []
    column_list.append({"id" : "network_type", "label" : "Network", "type" : "string"})
    column_list.append({"id" : "number_shares", "label" : "Number Shares", "type" : "number"})
    data["cols"] = column_list

    rows_list = []
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
    if "campaign" in req.GET:
        try:
            campaign = Campaign.objects.get(id=req.GET["campaign"])
            shares = Share.objects.filter(campaign=campaign.id)
        except Exception:
            dict["error"] = "Valid Campaign id not provided."
            dict["status"] = 500
            return HttpResponse(json.dumps(dict))
    else:
        dict["error"] = "Must specify campaign."
        dict["status"] = 500
        return HttpResponse(json.dumps(dict))

    data = {}
    column_list = []
    column_list.append({"id" : "pic", "label" : "", "type" : "string"})
    column_list.append({"id" : "name", "label" : "Name", "type" : "string"})
    column_list.append({"id" : "page", "label" : "Link", "type" : "string"})
    column_list.append({"id" : "followers", "label" : "Followers", "type" : "number"})
    column_list.append({"id" : "reach", "label" : "Reach", "type" : "number"})
    column_list.append({"id" : "num_shares", "label" : "Shares", "type" : "number"})
    column_list.append({"id" : "child_num_retweets", "label" : "Re-Shares (Friend)", "type" : "number"})
    column_list.append({"id" : "total_num_retweets", "label" : "Re-Shares (Total)", "type" : "number"})
    column_list.append({"id" : "network", "label" : "Network", "type" : "string"})
    column_list.append({"id" : "clicks", "label" : "Clicks", "type" : "number"})

    data["cols"] = column_list

    rows_list = []
    user_dict = {}
    for share in shares:
        name = ""
        network = ""

        if share.from_account_type == "F":
            if not share.from_user_facebook:
                fbuser = FBUser.objects.get(id=1)
            else:
                fbuser = FBUser.objects.get(id=share.from_user_facebook.id)
            name = fbuser.name or fbuser.facebook_id
            network = "Facebook"
            page = "http://www.facebook.com/" + fbuser.username
            picture = "<img src='http://graph.facebook.com/" + fbuser.facebook_id + "/picture' />" 

        elif share.from_account_type == "T":
            user = User.objects.get(id=share.from_user_twitter.id)
            name = user.name 
            network = "Twitter"
            page = "http://twitter.com/" + user.username 
            picture = "<img src='" + user.profile_pic + "' />"

        name_id = str(name) + network
        if name_id  not in user_dict.keys():
            user_dict[name_id] = {"name":name, 
                                  "network":network, 
                                  "num":1, 
                                  "child_num_retweet":len(share.children()),
                                  "total_num_retweet":len(share.allOffspring()),
                                  "reach":share.getReach(), 
                                  "totalReach":share.totalReach(),
                                  "pic" : picture,
                                  "page" : page,
                                  "clicks" : share.page_views}
        else:
            user_dict[name_id]["num"] = user_dict[name_id]["num"] + 1
            user_dict[name_id]["child_num_retweet"] = user_dict[name_id]["child_num_retweet"] + len(share.children())
            user_dict[name_id]["total_num_retweet"] = user_dict[name_id]["total_num_retweet"] + len(share.allOffspring())
            user_dict[name_id]["reach"] = user_dict[name_id]["reach"] + share.getReach()
            user_dict[name_id]["totalReach"] = user_dict[name_id]["totalReach"] + share.totalReach()
            user_dict[name_id]["clicks"] = user_dict[name_id]["clicks"] + share.page_views


    # div_num is total number of shares by this user
    for name_id in user_dict.keys():
        if float(user_dict[name_id]["num"]) == 0:
            div_num = 1.0
        else:
            div_num = float(user_dict[name_id]["num"])


        rows_list.append({"c" : [{"v" : user_dict[name_id]["pic"], "p": {'className': 'userPic'}},
                                 {"v" : user_dict[name_id]["name"], "p": {'className': 'userName'}}, 
                                 {"v" : user_dict[name_id]["page"]},
                                 {"v" : int(float(user_dict[name_id]["reach"]) / div_num)},
                                 {"v" : int(float(user_dict[name_id]["totalReach"]) / div_num), "p": {'style': 'width: 90px;'}},
                                 {"v" : user_dict[name_id]["num"]},
                                 {"v" : user_dict[name_id]["child_num_retweet"], "p": {'style': 'width: 60px;'}},
                                 {"v" : user_dict[name_id]["total_num_retweet"], "p": {'style': 'width: 60px;'}},
                                 {"v" : user_dict[name_id]["network"]},
                                 {"v" : user_dict[name_id]["clicks"]},
        ]});
 

    data["rows"] = rows_list

    dict["status"] = 200
    dict["data"] = data
    print "Table Returning DICT", dict
    return HttpResponse(json.dumps(dict))
