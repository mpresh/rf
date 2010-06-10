from django.db import models
from pylib import oauth
import re, httplib, simplejson
from simpz.tauth.models import User

#class Organizer(models.Model):
#    fname = models.CharField(max_length=50)
#    lname = models.CharField(max_length=50)
#    email = models.EmailField()
#    twitter = models.CharField(max_length=50, default="")
#    #events = models.ManyToManyField('Event', related_name="organizers")

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    event_date_time_start = models.DateTimeField('date time of event start')
    event_date_time_end = models.DateTimeField('date time of event end')
    capacity = models.IntegerField()
    venue = models.CharField(max_length=100)
    venue_address = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    lat = models.DecimalField(max_digits=10, decimal_places=4)
    lng = models.DecimalField(max_digits=10, decimal_places=4)
    url = models.URLField(verify_exists=True)
    image = models.URLField()
    organizer = models.ForeignKey(User, related_name="event_organized")
    attendees = models.ManyToManyField(User, related_name="events_going")
    attendees_maybe = models.ManyToManyField(User, related_name="events_maybe")
   
class Invite(models.Model):
    message = models.CharField(max_length=140)
    from_user = models.ForeignKey(User, related_name="made_invite")
    to_user = models.ForeignKey(User, related_name="received_invite")
    event = models.ForeignKey(Event, related_name="invitation")
    created_at = models.DateTimeField(auto_now_add=True)


#class Attendee(models.Model):
#    fname = models.CharField(max_length=50)
#    lname = models.CharField(max_length=50)
#    email = models.EmailField()
#    twitter = models.CharField(max_length=50, default="")
