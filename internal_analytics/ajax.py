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

    try:
        customer_id = int(req.GET["customer_id"])
    except:
        customer_id = None


    print "customer_id", customer_id
    shares = Share.objects.all()
    print shares.count()

    if customer_id:
        shares = shares.filter(campaign=customer_id)

    shares = shares.exclude(created_at__gte=end)
    shares = shares.exclude(created_at__lte=start)
    
    network_dict = {}
    network_dict["facebook"] = shares.filter(from_account_type='F')
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

    try:
        customer_id = req.GET["customer_id"] 
    except:
        customer_id = None

    shares = Share.objects.all()

    if customer_id:
        shares = shares.filter(campaign=customer_id)

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

    try:
        customer_id = req.GET["customer_id"] 
    except:
        customer_id = None

    campaigns = Campaign.objects.all()

    if customer_id:
        campaigns = campaigns.filter(id=customer_id)

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

    try:
        customer_id = req.GET["customer_id"] 
    except:
        customer_id = None

    shares = Share.objects.all()

    if customer_id:
        shares = shares.filter(campaign=customer_id)

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

    try:
        customer_id = req.GET["customer_id"] 
    except:
        customer_id = None

    shares = Share.objects.all()

    if customer_id:
        shares = shares.filter(campaign=customer_id)

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

    try:
        customer_id = req.GET["customer_id"] 
    except:
        customer_id = None

    campaigns = Campaign.objects.all()

    if customer_id:
        campaigns = campaigns.filter(campaign=customer_id)

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

def analytics_clicks_reshares_bar(req):

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

    try:
        data_type = req.GET['data_type']
    except:
        data_type = "total"

    try:
        abs_per = req.GET['abs_per']
    except:
        abs_per = "absolute"

    try:
        customer_id = req.GET["customer_id"] 
    except:
        customer_id = None

    shares = Share.objects.all()

    if customer_id:
        shares = shares.filter(campaign=customer_id)

    shares = shares.exclude(created_at__gte=end)
    shares = shares.exclude(created_at__lte=start)

    data = {}
    column_list = []
    column_list.append({"id" : "range_type", "label" : "Time", "type" : "string"})
    if abs_per == "absolute":
        column_list.append({"id" : "shares", "label" : "Shares", "type" : "number"})
        column_list.append({"id" : "clicks", "label" : "Clicks", "type" : "number"})
        column_list.append({"id" : "reshares", "label" : "Reshares", "type" : "number"})
    else:
        column_list.append({"id" : "clicks_percent", "label" : "Clicks_percent", "type" : "number"})
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
        temp_shares_facebook_clicks = 0
        temp_shares_facebook_count = temp_shares_facebook.count()

        temp_reshares_facebook = 0
        for share in temp_shares_facebook:
            temp_shares_facebook_reach += share.reach
            temp_shares_facebook_clicks += share.page_views
            temp_reshares_facebook += share.children().count()

        temp_shares_twitter = temp_shares.filter(from_account_type="T")
        temp_shares_twitter_reach = 0
        temp_shares_twitter_clicks = 0
        temp_shares_twitter_count = temp_shares_twitter.count()

        temp_reshares_twitter = 0
        
        for share in temp_shares_twitter:
            temp_shares_twitter_reach += share.reach
            temp_shares_twitter_clicks += share.page_views
            temp_reshares_twitter += share.children().count()

        if data_type == "total":
            reach = temp_shares_twitter_reach + temp_shares_facebook_reach
            clicks = temp_shares_twitter_clicks + temp_shares_facebook_clicks
            shares_count = temp_shares_twitter_count + temp_shares_facebook_count
            reshares = temp_reshares_twitter + temp_reshares_facebook
            
            if clicks == 0:
                clicks_percentage = 0
            else:
                clicks_percentage = clicks / (reach * 1.0) 

        elif data_type == "twitter":
            reach = temp_shares_twitter_reach
            clicks = temp_shares_twitter_clicks
            shares_count = temp_shares_twitter_count
            reshares = temp_reshares_twitter

            if clicks == 0:
                clicks_percentage = 0
            else:
                clicks_percentage = clicks / (reach * 1.0) 
        else:
            reach = temp_shares_facebook_reach
            clicks = temp_shares_facebook_clicks
            shares_count = temp_shares_facebook_count
            reshares = temp_reshares_facebook

            if clicks == 0:
                clicks_percentage = 0
            else:
                clicks_percentage = clicks / (reach * 1.0)
    

        if abs_per == "absolute":
            rows_list.append({"c" : [{"v" : label},
                                     {"v" : shares_count},
                                     {"v" : clicks},
                                     {"v" : reshares}]
                         })
        else:
            rows_list.append({"c" : [{"v" : label},
                                     {"v" : clicks_percentage}]
                         })

        
    data["rows"] = rows_list
    dict_vals["status"] = 200
    dict_vals["data"] = data
    return HttpResponse(json.dumps(dict_vals))

def analytics_percent_share_data(req):
    
    dict_vals = {}

    try:
        customer_id = req.GET["customer_id"] 
    except:
        customer_id = None

    campaigns = Campaign.objects.all()    
    total_page_views = 0
    top_page_views = 0

    for camp in campaigns:
        total_page_views += camp.page_views_total
        top_page_views += camp.page_views

    shares = Share.objects.all()    

    if customer_id:
        shares = shares.filter(campaign=customer_id)

    twitter_page_views = 0
    facebook_page_views = 0
    
    facebook_shares = 0
    twitter_shares = 0
    top_shares = 0
    for share in shares:
        parent = share.parent()
        if parent is None:
            top_shares += 1
        elif parent.from_account_type == "T":
            twitter_shares += 1
        elif parent.from_account_type == "F":
            facebook_shares += 1

        if share.from_account_type == "T":
            twitter_page_views += share.page_views
        elif share.from_account_type == "F":
            facebook_page_views += share.page_views
    
    dict_vals["status"] = 200
    dict_vals["top_page_views_val"] = top_page_views
    dict_vals["twitter_page_views_val"] = twitter_page_views
    dict_vals["facebook_page_views_val"] = facebook_page_views

    dict_vals["top_shares_val"] = top_shares
    dict_vals["twitter_shares_val"] = twitter_shares
    dict_vals["facebook_shares_val"] = facebook_shares

    dict_vals["top_percent"] = (top_shares * 1.0) / top_page_views
    dict_vals["twitter_percent"] = (twitter_shares * 1.0) / twitter_page_views
    dict_vals["facebook_percent"] = (facebook_shares * 1.0) / facebook_page_views
    print "VALS", dict_vals
    return HttpResponse(json.dumps(dict_vals))
