from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
                       #url(r'facebook_callback/$', 'facebook_auth.facebook_server_callback', name='facebook_callback'),
                       url(r'facebook_callback/$', 'fauth.facebook_auth.facebook_callback', name='facebook_callback'),
                       url(r'facebook_callback_test/$', 'fauth.facebook_auth.facebook_callback_test', name='facebook_callback_test'),
                       url(r'facebook_callback_ajax/$', 'fauth.facebook_auth.facebook_callback_ajax', name='facebook_callback_ajax'),
                       url(r'facebook_logout_callback/$', 'fauth.facebook_auth.facebook_logout_callback', name='facebook_logout_callback'),
                       url(r'ajax/facebook_update_feed/$', 'fauth.ajax.update_feed', name='facebook_update_feed'),
                       url(r'ajax/campaign_facebook_update/(?P<campaign_id>\d+)/?$', 'fauth.ajax.campaign_facebook_update', name='campaign_facebook_update'),
                       url(r'ajax/facebook_message/$', 'fauth.ajax.message', name='facebook_message'),
                       url(r'ajax/facebook_friends/$', 'fauth.ajax.friends', name='facebook_friends'),




                       # sample html page to test out the facebook login functionality
                       url(r'facebook_login_test/$', 'fauth.views.facebook_login_test', name='facebook_login_test'),

                       # redirect facebook ogin callback
                       url(r'facebook_login_callback/$', 'fauth.facebook_auth.facebook_login_callback', name='facebook_login_callback'),

                       # ajax call to logout
                       url(r'ajax/facebook_logout/$', 'fauth.ajax.facebook_logout', name='ajax_facebook_logout'),

                       # ajax call to check if facebook is logged expired and log out if it is
                       url(r'ajax/facebook_check_logout/$', 'fauth.ajax.facebook_check_logout', name='ajax_facebook_check_logout'),

                       # ajax call to post a test feed
                       url(r'ajax/facebook_info_test/$', 'fauth.ajax.facebook_info_test', name='ajax_facebook_info_test'),

                       # ajax call to get info
                       url(r'ajax/facebook_feed_test/$', 'fauth.ajax.facebook_feed_test', name='ajax_facebook_feed_test'),
                       )
