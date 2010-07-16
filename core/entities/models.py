from django.db import models
from pylib import oauth
import re, httplib, simplejson
from core.tauth.models import User
from core.fauth.models import FBUser
import re
import hashlib


# describes the entity type
class EntityType(models.Model):
    name = models.CharField(max_length=200)
    
    
    def __unicode__(self):
        return "<EntityType: %s %s %s>" % (self.id, self., self.name)

class Entity(models.Model):
    type = models.CharField(max_length=200)       # this can be an event, promotion, any kind of campaign.
    name = models.CharField(max_length=200)       # title of entity

    def __unicode__(self):
        return "<Entity: %s %s %s>" % (self.id, self.type, self.name)



class AttributeType(models.Model):
    name = models.CharField(max_lengt=100)
    allowed_values = models.CharField(max_length=100)

class Attribute(models.Model):
    type = models.CharField(max_lengt=100)
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=200)


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


   
