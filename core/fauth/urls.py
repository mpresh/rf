from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
                       #url(r'facebook_callback/$', 'facebook_auth.facebook_server_callback', name='facebook_callback'),
                       url(r'facebook_callback/$', 'facebook_auth.facebook_callback', name='facebook_callback'),
                       url(r'facebook_logout_callback/$', 'facebook_auth.facebook_logout_callback', name='facebook_logout_callback'),
                       url(r'ajax/facebook_update_feed/$', 'ajax.update_feed', name='facebook_update_feed'),
                       url(r'ajax/event_facebook_update/(?P<event_id>\d+)/?$', 'ajax.event_facebook_update', name='event_facebook_update'),
                       url(r'ajax/facebook_message/$', 'ajax.message', name='facebook_message'),
                       url(r'ajax/facebook_friends/$', 'ajax.friends', name='facebook_friends'),
                       )
