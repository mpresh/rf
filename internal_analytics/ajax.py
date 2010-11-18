import re
from datetime import datetime, timedelta
from django.http import HttpResponse
import simplejson as json

from campaign.models import Campaign
from events.models import *
from fauth.models import *
from tauth.models import *

def analytics_totalshares_pie(req):
    """Return json for DataTable pie Format totals."""

    dict_vals = {}
    date_regex = "\d\d/\d\d/\d\d\d\d"
    try:
        mo = re.match(date_regex, req.GET['end'])
        if mo != None:
            (month, day, year) = req.GET['end'].split('/')
            end = datetime(int(year),int(month),int(day))
    except:
        today = datetime.now()
        end = datetime(today.year,today.month,today.day)    

    end = end + timedelta(days=1)

    try:
        mo = re.match(date_regex, req.GET['start'])
        if mo != None:
            (month, day, year) = req.GET['start'].split('/')
            start = datetime(int(year),int(month),int(day))
    except:
        start = datetime('2010','01','01')

    shares = Share.objects.all()
    shares = shares.exclude(created_at__gte=end)
    shares = shares.exclude(created_at__lte=start)
    
    network_dict = {}
    network_dict["facebook"] = shares.filter(from_account_type='F').count()
    network_dict["twitter"] = shares.filter(from_account_type='T').count()
    
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

    dict_vals["status"] = 200
    dict_vals["data"] = data
    print "Returning DICT", dict_vals
    return HttpResponse(json.dumps(dict_vals))


def analytics_campaignscreated_pie(req):
    """Return json for DataTable pie Format totals."""

    dict_vals = {}
    date_regex = "\d\d/\d\d/\d\d\d\d"
    try:
        mo = re.match(date_regex, req.GET['end'])
        if mo != None:
            (month, day, year) = req.GET['end'].split('/')
            end = datetime(int(year),int(month),int(day))
        end
    except:
        today = datetime.now()
        end = datetime(today.year,today.month,today.day)    

    end = end + timedelta(days=1)

    try:
        mo = re.match(date_regex, req.GET['start'])
        if mo != None:
            (month, day, year) = req.GET['start'].split('/')
            start = datetime(int(year),int(month),int(day))
        start
    except:
        start = datetime('2010','01','01')

    campaigns = Campaign.objects.all()
    campaigns = campaigns.exclude(created_at__gte=end)
    campaigns = campaigns.exclude(created_at__lte=start)
    network_dict = {}
    network_dict["raffle"] = campaigns.filter(campaign_type='raffle').count()
    network_dict["discount"] = campaigns.filter(campaign_type='discount').count()

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

    dict_vals["status"] = 200
    dict_vals["data"] = data
    print "Returning DICT", dict_vals
    return HttpResponse(json.dumps(dict_vals))


def analytics_totalshares_line(req):
    dict_vals = {}
    return HttpResponse(json.dumps(dict_vals))
    
def analytics_campaignscreated_line(req):
    dict_vals = {}
    return HttpResponse(json.dumps(dict_vals))
