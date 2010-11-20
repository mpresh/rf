from django.conf import settings
from django.shortcuts import render_to_response

from campaign.models import Campaign
from create import *
from events.models import Event, Share
from tauth.models import User
from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required

# iframe embed in django page
def test5(req):
    return render_to_response('test5.html', {})

# iframe embed
def test4(req):
    return render_to_response('test4.html', {})

# javascript embed
def test3(req):
    return render_to_response('test3.html', {})

def test2(req):
    return render_to_response('test2.html', {})


def test(req):
    #req.session["redirect"] = req.get_full_path()  
    return render_to_response('test.html', {})

def about(req):
    return render_to_response('about.html', {})

def jobs(req):
    return render_to_response('jobs.html', {})

def contact(req):
    return render_to_response('contact.html', {})

def howitworks(req):
    return render_to_response('howitworks.html', {})

@login_required
def event_data(req):
    now = datetime.now()
    now = datetime(now.year, now.month, now.day)

    dict_vals = {}
    dict_vals['current'] = datetime.strftime(datetime.now(), "%m/%d/%Y")
    dict_vals['start'] = "01/01/2010"

    shares = Share.objects.all()
    dict_vals["total_shares"] = shares.count()
    
    day = now - timedelta(days=1)
    dict_vals["total_shares_last_day"] = shares.exclude(created_at__lte=day).count()

    week = now - timedelta(days=7)
    dict_vals["total_shares_last_week"] = shares.exclude(created_at__lte=week).count()

    month = now - timedelta(days=30)
    dict_vals["total_shares_last_month"] = shares.exclude(created_at__lte=month).count()


    campaigns = Campaign.objects.all()
    dict_vals["total_campaignscreated"] = campaigns.count()

    day = now - timedelta(days=1)
    dict_vals["total_campaignscreated_last_day"] = campaigns.exclude(created_at__lte=week).count()

    week = now - timedelta(days=7)
    dict_vals["total_campaignscreated_last_week"] = campaigns.exclude(created_at__lte=week).count()

    month = now - timedelta(days=30)
    dict_vals["total_campaignscreated_last_month"] = campaigns.exclude(created_at__lte=month).count()

    dict_vals['all'] = "01/01/2010"
    dict_vals['day'] = str(day.month) + "/" + str(day.day) + "/" + str(day.year)
    dict_vals['week'] = str(week.month) + "/" + str(week.day) + "/" + str(week.year)
    dict_vals['month'] = str(month.month) + "/" + str(month.day) + "/" + str(month.year)

    return render_to_response('data.html', dict_vals)


@login_required
def event_list(req):
    all_campaigns = Campaign.objects.all()
    return render_to_response('list.html', {"campaigns":all_campaigns})
    
def event_details(req, event_id=""):

    dict = {}
    if "user_id" in req.session:
        user = User.objects.get(id=req.session["user_id"])
        dict['user'] = user

    #req.session["redirect"] = req.get_full_path()
    if event_id:
        e = Event.objects.get(id=event_id)
        dict['event'] = e
        dict['invites'] = e.invitations.all()
        dict['attendees'] = e.attendees.all()
        dict['attendees_maybe'] = e.attendees_maybe.all()
            
        return render_to_response('details.html', dict)
	
    return render_to_response('details.html', dict)

def map(request):
    return render_to_response('map.html', {"key": settings.GOOGLE_MAP_API,
                                           "zoom": 14})

def user_details(req, user_id=""):
    #req.session["redirect"] = req.get_full_path()

    dict = {}
    if user_id:
        user = User.objects.get(id=user_id)	
        dict["user_info"] = user
        dict["events_going"] = user.events_going.all()
        dict["events_organized"] = user.events_organized.all()
        dict["received_invites"] = user.received_invites.all()
        dict["made_invites"] = user.made_invites.all()
        dict["events_maybe"] = user.events_maybe.all()

    if "user_id" in req.session:
        user = User.objects.get(id=req.session["user_id"])
	dict["user"] = user

    return render_to_response('user.html', dict)    

