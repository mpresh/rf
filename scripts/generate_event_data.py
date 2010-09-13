# set up environment
import sys
import os
sys.path.append("..")
os.environ["DJANGO_SETTINGS_MODULE"] = "settings"

from django.db import models
from core.tauth.models import User
from core.fauth.models import FBUser
from core.campaign.models import Campaign
from core.events.models import Share

from optparse import OptionParser

from datetime import datetime, timedelta
import random

def parse_options():
    parser = OptionParser()
    parser.add_option("-c", "--campaign", dest="campaign", 
                      help="specify campaign id")
    parser.add_option("-t", "--type", dest="type", default="discount",
                      help="specify campaign type")
    parser.add_option("--coefficient", dest="coefficient", default=".1",
                      help="coefficient share value")
    parser.add_option("--days", dest="days", default=10,
                      help="for how many days to generate data")
    parser.add_option("--amp", dest="amp", default="1",
                      help="how much to amplify the shares.")

    (options, args) = parser.parse_args()
    return (options, args)

def create_share(created_at="",
                 campaign_id=1,
                 msg="This is a test.",
                 from_account_type="T",
                 from_user_twitter="1",
                 from_user_facebook=None,
                 ):


    if from_user_facebook:
        user = FBUser.objects.get(id=1)
        share = Share(message=msg,
                      campaign=campaign_id,
                      #campaign=Campaign.objects.get(id=campaign_id),
                      from_user_facebook=user,
                      from_account_type=from_account_type,
                      parent_shash=None,
                      reach=100
                      )
    else:
        user = User.objects.get(id=1)
        share = Share(message=msg,
                      campaign=campaign_id,
                      #campaign=Campaign.objects.get(id=campaign_id),
                      from_user_facebook=None,
                      from_user_twitter=user,
                      from_account_type=from_account_type,
                      parent_shash=None,
                      reach=100
                      )

    share.save()
    share.created_at = created_at
    share.setHash()
    #url = share.url(req)
    #short_url = bitly.shorten(url)
    #share.url_short = short_url
    share.save()    
    

def generate_data(c, options):
    now = datetime.now()
    start = now - timedelta(days=int(options.days))

    for day in range(0, int(options.days)):
        start = start + timedelta(days=1)

        for s in range(0, (day + 1) * int(options.amp)):
            print "Campaign", day, start
            create_share(created_at=start, campaign_id=c)
            create_share(created_at=start, campaign_id=c, from_account_type="F", from_user_facebook="1")



def main():
    (options, args) = parse_options()
    
    if options.campaign:
        c = Campaign.objects.get(id=options.campaign)
    else:
        c = Campaign()

    generate_data(c, options)
    

if __name__ == "__main__":
    main()
