from django.db import models
from pylib import oauth
import re, httplib, simplejson
from simpz.tauth.models import User

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    event_date_time_start = models.DateTimeField('date time of event start', blank=True)
    event_date_time_end = models.DateTimeField('date time of event end', blank=True)
    capacity = models.IntegerField(blank=True)
    venue = models.CharField(max_length=100, blank=True)
    venue_address = models.CharField(max_length=300, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    lat = models.DecimalField(max_digits=10, decimal_places=4, blank=True)
    lng = models.DecimalField(max_digits=10, decimal_places=4, blank=True)
    url = models.URLField(verify_exists=True, blank=True)
    image = models.URLField(blank=True)
    organizer = models.ForeignKey(User, related_name="events_organized")
    attendees = models.ManyToManyField(User, related_name="events_going")
    attendees_maybe = models.ManyToManyField(User, related_name="events_maybe")

    def __unicode__(self):
        return "<Event: %s %s>" % (self.id, self.name)
   
class Invite(models.Model):
    message = models.CharField(max_length=140, default="")
    from_user = models.ForeignKey(User, related_name="made_invites")
    to_users = models.ManyToManyField(User, related_name="received_invites", null=True)
    event = models.ForeignKey(Event, related_name="invitations")
    from_invite = models.ForeignKey('self', related_name="invite_children", default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return "<Invite: %s>" % (self.id)

