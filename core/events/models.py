from django.db import models
from pylib import oauth
import re, httplib, simplejson
from core.tauth.models import User
from core.fauth.models import FBUser
from core.campaign.models import Campaign
import re
import hashlib
import urlparse
import urllib

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
    attendees = models.ManyToManyField(User, related_name="events_going")
    attendees_maybe = models.ManyToManyField(User, related_name="events_maybe")
    campaign = models.ForeignKey(Campaign, related_name="events", null=True)
    ehash = models.CharField(max_length=100, default="", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    organizer = models.ForeignKey(User, related_name="events_organized", null=True)

    def __unicode__(self):
        return "<Event: %s %s>" % (self.id, self.name)
   
    def getHash(self):
        """Gets ehash for this event. If it's not set, compute it and then return it."""
        if self.ehash:
            return self.ehash
        else:
            self.setHash()
        return self.ehash

    def setHash(self):
        """Computes and sets hash for current Event."""
        ehash_string = str(self.name) + str("EVENT") + str(self.created_at)
        ehash = hashlib.sha1()
        ehash.update(ehash_string)

        self.ehash = ehash.hexdigest()
        self.save()


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
    from_user_twitter = models.ForeignKey(User, related_name="made_invites_twitter", null=True)
    from_user_facebook = models.ForeignKey(FBUser, related_name="made_invites_facebook", null=True)
    event = models.ForeignKey(Event, related_name="invites", null=True)
    campaign = models.ForeignKey(Campaign, related_name="shares", null=True)
    from_invite = models.ForeignKey('self', related_name="child_invites", default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    url_full = models.URLField(default="", null=True)
    url_short = models.URLField(default="", null=True)
    shash = models.CharField(max_length=100, default="", null=True)
    parent_shash = models.CharField(max_length=100, default="", null=True)
    reach = models.IntegerField(blank=True, default=0)
    page_views = models.IntegerField(null=False, default=0)

    def __unicode__(self):
        return "<Share: %s %s>" % (self.id, self.getHash())

    def parent(self):
        if self.parent_shash is not None:
            return Share.objects.get(shash=self.parent_shash)
        return None

    def children(self):
        return Share.objects.filter(parent_shash=self.shash)

    def allOffspring(self):
        list_objs = []
        seen = {}
        seen[self.id] = True
        for obj in self.children():
            if obj.id not in seen:
                list_objs.extend(obj.allOffspringHelper(seen=seen))
        return list_objs

    def allOffspringHelper(self, seen={}):
        """ Returns all of the shares that originated here."""
        list_objs = [self]
        seen[self.id] = True
        for obj in self.children():
            if obj.id not in seen:
                print obj
                list_objs.extend(obj.allOffspringHelper(seen=seen))
        return list_objs

    def getReach(self):
        """Return reach"""
        if self.reach:
            return self.reach

        else:
            return 0
    
    def totalReach(self, seen={}):
        """ Returns all of the shares that originated here."""
        total = 0
        total = total + self.getReach()

        seen[self.id] = True
        for obj in self.children():
            if obj.id not in seen:
                total = total + obj.totalReach(seen=seen)
        return total

    def url(self, request, parent=""):
        """Returns the url for this share link."""
        
        if parent:
            parent = urllib.unquote(parent)
            parsed_url = urlparse.urlparse(parent)
            try:
                list_vals = parsed_url.query.split("&")
            except Exception:
                list_vals = parsed_url[3]
            dict = {}
            for val in list_vals:
                if val:
                    k, v = val.split("=")
                    dict[k] = v
            
            if "shash" not in dict:
                if parent.find("?") != -1:
                    parent = parent + "&shash=" + self.getHash()
                else:
                    parent = parent + "?shash=" + self.getHash()
            else:
                parent = re.sub("shash=[a-zA-Z0-9_-]+", "shash=" + self.getHash(), parent)

            url = parent
            return url

        if request.session["redirect"].find("shash=") != -1:
            path = re.sub("shash=[a-zA-Z0-9_-]+", "shash=" + self.getHash(), request.session["redirect"])
        else:
            if request.session["redirect"].find("?") != -1:
                path = re.sub("shash=[a-zA-Z0-9_-]+", "shash=" + self.getHash(), request.session["redirect"] + "&shash=12345")
            else:
                path = re.sub("shash=[a-zA-Z0-9_-]+", "shash=" + self.getHash(), request.session["redirect"] + "?shash=12345")

        path = re.sub("overlay=[a-zA-Z0-9_-]+[&]?", "", path)
        return "http://" + request.get_host() + path

    def referUrl(self, request):

        current_url = self.url(request)
        if "shash" in request.GET:
            refer_shah = request.GET["shah"]
            url = re.sub("shash=[a-zA-Z0-9_-]+", "shash=" + refer_shah, current_url)
        else:
            url = re.sub("[&]shash=[a-zA-Z0-9_-]+", "", current_url)
            url = re.sub("[?]shash=[a-zA-Z0-9_-]+", "", url)

        return url

    def getHash(self):
        """Gets hash for this event. If it's not set, compute it and then return it."""
        if self.shash:
            return self.shash
        else:
            self.setHash()
        return self.shash

    def setHash(self):
        """Computes and sets hash for current event."""
        if self.from_user_twitter is None:
            from_twitter = "None"
        else:
            from_twitter = str(self.from_user_twitter.id)

        if self.from_user_facebook is None:
            from_facebook = "None"
        else:
            from_facebook = str(self.from_user_facebook.id)

        share_string = str(self.from_account_type) + str(self.created_at) + from_twitter + from_facebook + str(self.from_user_facebook) + str(self.from_user_twitter)
        shash = hashlib.sha1()
        shash.update(share_string)

        self.shash = shash.hexdigest()
        self.save()
