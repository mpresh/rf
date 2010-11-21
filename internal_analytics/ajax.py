import re
from datetime import datetime, timedelta
from django.http import HttpResponse
import simplejson as json

from campaign.models import Campaign
from events.models import *
from fauth.models import *
from tauth.models import *

import analytics_util

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
    return HttpResponse(json.dumps(dict_vals))

def analytics_totalreach_pie(req):
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

    facebook_shares = shares.filter(from_account_type='F')
    temp_shares_facebook_reach = 0
    for fshare in facebook_shares:
        temp_shares_facebook_reach += fshare.reach
    network_dict["facebook"] = temp_shares_facebook_reach

    twitter_shares = shares.filter(from_account_type='T')
    temp_shares_twitter_reach = 0
    for tshare in twitter_shares:
        temp_shares_twitter_reach += tshare.reach
    network_dict["twitter"] = temp_shares_twitter_reach
    
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
    return HttpResponse(json.dumps(dict_vals))


def analytics_totalshares_line(req):
    dict_vals = {}
    SPLITS = 10

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

    shares = Share.objects.all()
    shares = shares.exclude(created_at__gte=end)
    shares = shares.exclude(created_at__lte=start)

    data = {}
    column_list = []
    column_list.append({"id" : "range_type", "label" : "Time", "type" : "string"})
    column_list.append({"id" : "twitter", "label" : "Twitter", "type" : "number"})
    column_list.append({"id" : "facebook", "label" : "Facebook", "type" : "number"})
    data["cols"] = column_list

    td = end - start
    diff_seconds = (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6 

    inc_diff = diff_seconds / SPLITS
    temp_end = start
    temp_start = start

    rows_list = []
    for incr in range(0, SPLITS):
        temp_shares = shares.exclude(created_at__lte=temp_start)
        temp_end = temp_start + timedelta(seconds=inc_diff)
        
        temp_shares = temp_shares.exclude(created_at__gte=temp_end)

        label = analytics_util.getChartLabel(temp_start, temp_end, SPLITS, start, end)

        temp_start = temp_end
        temp_shares_facebook = temp_shares.filter(from_account_type="F").count()
        temp_shares_twitter = temp_shares.filter(from_account_type="T").count()
        

        rows_list.append({"c" : [{"v" : label},
                                 {"v" : temp_shares_twitter},
                                 {"v" : temp_shares_facebook}]
                         })

        
    data["rows"] = rows_list
    dict_vals["status"] = 200
    dict_vals["data"] = data
    return HttpResponse(json.dumps(dict_vals))

def analytics_totalreach_line(req):
    dict_vals = {}
    SPLITS = 10

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

    shares = Share.objects.all()
    shares = shares.exclude(created_at__gte=end)
    shares = shares.exclude(created_at__lte=start)

    data = {}
    column_list = []
    column_list.append({"id" : "range_type", "label" : "Time", "type" : "string"})
    column_list.append({"id" : "twitter", "label" : "Twitter", "type" : "number"})
    column_list.append({"id" : "facebook", "label" : "Facebook", "type" : "number"})
    data["cols"] = column_list

    td = end - start
    diff_seconds = (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6 

    inc_diff = diff_seconds / SPLITS
    temp_end = start
    temp_start = start

    rows_list = []
    for incr in range(0, SPLITS):
        temp_shares = shares.exclude(created_at__lte=temp_start)
        temp_end = temp_start + timedelta(seconds=inc_diff)
        
        temp_shares = temp_shares.exclude(created_at__gte=temp_end)

        label = analytics_util.getChartLabel(temp_start, temp_end, SPLITS, start, end)

        temp_start = temp_end

        temp_shares_facebook = temp_shares.filter(from_account_type="F")
        temp_shares_facebook_reach = 0
        for share in temp_shares_facebook:
            temp_shares_facebook_reach += share.reach

        temp_shares_twitter = temp_shares.filter(from_account_type="T")
        temp_shares_twitter_reach = 0
        for share in temp_shares_twitter:
            temp_shares_twitter_reach += share.reach

        rows_list.append({"c" : [{"v" : label},
                                 {"v" : temp_shares_twitter_reach},
                                 {"v" : temp_shares_facebook_reach}]
                         })

        
    data["rows"] = rows_list
    dict_vals["status"] = 200
    dict_vals["data"] = data
    return HttpResponse(json.dumps(dict_vals))
    
def analytics_campaignscreated_line(req):

    dict_vals = {}
    SPLITS = 10

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

    data = {}
    column_list = []
    column_list.append({"id" : "range_type", "label" : "Time", "type" : "string"})
    column_list.append({"id" : "twitter", "label" : "Raffle", "type" : "number"})
    column_list.append({"id" : "facebook", "label" : "Discount", "type" : "number"})
    data["cols"] = column_list

    td = end - start
    diff_seconds = (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6 

    inc_diff = diff_seconds / SPLITS
    temp_end = start
    temp_start = start

    rows_list = []

    for incr in range(0, SPLITS):
        temp_camps = campaigns.exclude(created_at__lte=temp_start)
        temp_end = temp_start + timedelta(seconds=inc_diff)
        temp_camps = temp_camps.exclude(created_at__gte=temp_end)

        label = analytics_util.getChartLabel(temp_start, temp_end, SPLITS, start, end)

        temp_start = temp_end
        temp_camps_raffle = temp_camps.filter(campaign_type="raffle").count()
        temp_camps_discount = temp_camps.filter(campaign_type="discount").count()

        rows_list.append({"c" : [{"v" : label},
                                 {"v" : temp_camps_raffle},
                                 {"v" : temp_camps_discount}]
                         })

        
    data["rows"] = rows_list
    dict_vals["status"] = 200
    dict_vals["data"] = data
    return HttpResponse(json.dumps(dict_vals))
