from django.db import models

from core.tauth.models import User
from core.fauth.models import FBUser
import hashlib

class Campaign(models.Model):
    
    start_date_time = models.DateTimeField('date time of event start', blank=True, null=True)
    end_date_time = models.DateTimeField('date time of event start', blank=True, null=True)
    code = models.CharField(max_length=100)
    percent = models.IntegerField(blank=True)
    url = models.URLField(verify_exists=True, blank=True)
    chash = models.CharField(max_length=100, default="", null=True)
    admin_access_tusers = models.ManyToManyField(User, related_name="admin_access_campaign")
    admin_access_fusers = models.ManyToManyField(FBUser, related_name="admin_access_campaign")
    max_people = models.IntegerField(blank=True, default=0, null=True)
    min_people = models.IntegerField(blank=True, default=0, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=300)
    from_name = models.CharField(max_length=100)
    subdomain = models.CharField(max_length=50)
    campaign_type = models.CharField(max_length=50)
    
    def __unicode__(self):
        return "<Campaign: %s %s>" % (self.id, self.name)

    def getHash(self):
        """Gets chash for this campaign. If it's not set, compute it and then return it."""
        if self.chash:
            return self.chash
        else:
            self.setHash()
        return self.chash

    def setHash(self):
        """Computes and sets hash for current campaign."""
        chash_string = str(self.code) + str("CAMPAIGN") + str(self.created_at)
        chash = hashlib.sha1()
        chash.update(chash_string)
        
        self.chash = chash.hexdigest()
        self.save()

