from django.db import models
from pylib import oauth
import re, httplib, simplejson
from core.tauth.models import User
from core.fauth.models import FBUser
import re
import hashlib


class AttributeType(models.Model):
    name = models.CharField(max_length=100, default="STRING")
    allowed_values = models.CharField(max_length=100, null=True)

    def __unicode__(self):
        return "<AttributeType: %s %s %s>" % (self.id, self.name)

class Attribute(models.Model):
    type = models.ForeignKey(AttributeType)
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=200, default="")

    def __unicode__(self):
        return "<Attribute: %s %s %s>" % (self.id, self.name, self.value)

class EntityType(models.Model):
    name = models.CharField(max_length=200)
    required_fields = models.ManyToManyField(AttributeType, blank=True, related_name="entities_require")
    allowed_fields = models.ManyToManyField(AttributeType, blank=True, related_name="entities_allow")
    
    def __unicode__(self):
        return "<EntityType: %s %s %s>" % (self.id, self.name)

class Entity(models.Model):
    type = models.ForeignKey(EntityType)         # this can be an event, promotion, any kind of campaign.
    name = models.CharField(max_length=200)       # title of entity

    fields = models.ManyToManyField(Attribute, blank=True)

    def __unicode__(self):
        return "<Entity: %s %s %s>" % (self.id, self.type, self.name)

    def getValue(self, key):
        pass

    def setValue(self, key, value):
        pass
    
    def getKeys(self):
        pass

    def getDict(self):
        """ Return Dict of key value pairs."""
        pass


#    event_date_time_start = models.DateTimeField('date time of event start', blank=True)
#    event_date_time_end = models.DateTimeField('date time of event end', blank=True)
#    capacity = models.IntegerField(blank=True)
#    venue = models.CharField(max_length=100, blank=True)
#    venue_address = models.CharField(max_length=300, blank=True)
#    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
#    lat = models.DecimalField(max_digits=10, decimal_places=4, blank=True)
#    lng = models.DecimalField(max_digits=10, decimal_places=4, blank=True)
#    url = models.URLField(verify_exists=True, blank=True)
#    image = models.URLField(blank=True)
#    organizer = models.ForeignKey(User, related_name="events_organized")
#    attendees = models.ManyToManyField(User, related_name="events_going")
#    attendees_maybe = models.ManyToManyField(User, related_name="events_maybe")
#   
