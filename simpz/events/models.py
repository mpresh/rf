from django.db import models
from pylib import oauth
import re, httplib, simplejson
from simpz.tauth.models import User
from simpz.fauth.models import FBUser
import re

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

class Share(models.Model):
    ACCOUNT_CHOICES = (
        ('F', 'Facebook'),
        ('T', 'Twitter'),
        ('E', 'Email'),
        ('L', 'LinkedIn'),
        ('N', 'None'),
    )
    message = models.CharField(max_length=140, default="")
    from_account_type = models.CharField(max_length=1, choices=ACCOUNT_CHOICES)
    from_user_twitter = models.ForeignKey(User, related_name="made_invites_twitter", default="", null=True)
    from_user_facebook = models.ForeignKey(FBUser, related_name="made_invites_facebook", default="", null=True)
    event = models.ForeignKey(Event, related_name="invites")
    from_invite = models.ForeignKey('self', related_name="child_invites", default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    #url_full = models.URLField(default="")
    #url_short = models.URLField(default="")
    hash = models.CharField(max_length=100, default="", null=True)

    def __unicode__(self):
        return "<Invite: %s>" % (self.id)

    def parent(self):
        return None

    def children(self):
        return None

    def allOffspring(self):
        return None

    def url(self, request):
        """Returns the url for this share link."""
        print dir(request)
        print request.get_full_path()
        print request.build_absolute_uri()
        print request.get_host()

        print request

        print "SESSION"
        for key in request.session.keys():
            print "%s  %s" % (key, request.session[key])

        path = re.sub("hash=[a-zA-Z0-9_-]+", "path=" + self.getHash(), request.session["redirect"] + "&path=12334355335")
        return request.get_host() + path

    def referUrl(self, request):
        return None

    def getHash(self):
        if self.hash:
            return self.hash

        else:
            setHash()

        return self.getHash()

    def setHash(self):
        self.hash = 0
        self.save()
