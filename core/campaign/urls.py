from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       url(r'ajax/ajax_select_winners/$', 'campaign.ajax.select_winners', name='ajax_select_winners'),
                       url(r'ajax/ajax_update_widget/$', 'campaign.ajax.ajax_update_widget', name='ajax_update_widget'),
                       )
