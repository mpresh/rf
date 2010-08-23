from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
                       url(r'ajax/ajax_select_winners/$', 'campaign.ajax.select_winners', name='ajax_select_winners'),
                       )
