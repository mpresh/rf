from django.conf.urls.defaults import *
from django.conf import settings

# Comment/uncomment the next two lines to disable/enable admin, respectively.
from django.contrib import admin
admin.autodiscover()

# Base object to which patterns are added.
urlpatterns = patterns('',)

# Nonsense
urlpatterns = patterns('',
                       # url(r'^admin/', include(admin.site.urls)),
                       url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
                           {'document_root': settings.MEDIA_ROOT}, name="static"),
                       url(r'^manage/',  include('core.entities.urls')),
)

#
# Core URLS
#
urlpatterns += patterns('',
                        url(r'ajax/event_add_user/?$', 
                            'ajax.event_add_user', 
                            name='event_add_user'),

                        url(r'ajax/event_attendees/(?P<event_id>\d+)/?$', 
                            'ajax.event_attendees', 
                            name='event_attendees'),

                        url(r'ajax/event_friend_attendees/(?P<event_id>\d+)/?$', 
                            'ajax.event_friend_attendees', 
                            name='event_friend_attendees'),

                        url(r'ajax/event_friend_not_attendees/(?P<event_id>\d+)/?$', 
                            'ajax.event_friend_not_attendees', 
                            name='event_friend_not_attendees'),

                        url(r'ajax/event_not_going/(?P<event_id>\d+)/?$', 
                            'ajax.event_not_going', 
                            name='event_not_going'),

                        url(r'ajax/event_going/(?P<event_id>\d+)/?$', 
                            'ajax.event_going', 
                            name='event_going'),

                        url(r'ajax/campaign_going_twitter/(?P<campaign_id>\d+)/?$', 
                            'ajax.campaign_going_twitter', 
                            name='campaign_going_twitter'),
                        
                        url(r'ajax/event_tweet_invite/(?P<event_id>\d+)/?$', 
                            'ajax.event_tweet_invite', 
                            name='event_tweet_invite'),

                        url(r'ajax/campaign_tweet_invite/(?P<campaign_id>\d+)/?$', 
                            'ajax.campaign_tweet_invite', 
                            name='campaign_tweet_invite'),

                        # url(r'ajax/event_tweet_invite_dm/(?P<event_id>\d+)/?$', 
                        #     'ajax.event_tweet_invite_dm', 
                        #     name='event_tweet_invite_dm'),

                        url(r'upload_image/?$', 
                            'ajax.upload_image', 
                            name='upload_image'),
                        
                        ### miscellaneous
                        url(r'^map/?$', 'views.map', name='map'),
                        url(r'^test/?$', 'views.test', name='test'),
                        url(r'^test2/?$', 'views.test2', name='test2'),
                        url(r'^test3/?$', 'views.test3', name='test3'),
                        url(r'^test4/?$', 'views.test4', name='test4'),
                        url(r'^test5/?$', 'views.test5', name='test5'),
                        
                        # widget stuff
                        url(r'camp/widget/(?P<camp_id>\w+)/$', 
                            'views.campaign_widget', 
                            name='widget_id'),

                        url(r'camp/widget/$', 
                            'views.campaign_widget', 
                            name='widget'),
                        ##
                        
                        url(r'event_details/(?P<event_id>\d+)/$', 
                            'views.event_details', 
                            name='event_details'),

                        url(r'user_details/(?P<user_id>\d+)/$', 
                            'views.user_details', 
                            name='user_details'),

                        url(r'about/$', 'views.about', name='about'),
                        url(r'contact/$', 'views.contact', name='contact'),
                        url(r'jobs/$', 'views.jobs', name='jobs'),
                        url(r'howitworks/$', 'views.howitworks', name='howitworks'),
                        url(r'list/$', 'views.event_list', name='event_list'),
                        
                        url(r'create_campaign/$', 
                            'views.create_campaign', 
                            name='create_campaign'),

                        url(r'campaign_welcome/$', 
                            'views.campaign_created', 
                            name='campaign_created'),

                        url(r'create_campaign_ajax/$', 
                            'ajax_create.create_campaign', 
                            name='create_campaign_ajax'),

                        url(r'create_campaign_url_check/$', 
                            'ajax_create.create_campaign_url_check', 
                            name='create_campaign_url_check'),

                        url(r'send_details_email/$', 
                            'ajax_create.send_details_email', 
                            name='send_details_email'),
                        
                        url(r'campaign_page_preview/$', 
                            'views.campaign_page_preview', 
                            name='campaign_page_preview'),

                        url(r'camp/(?P<chash>\w{8}\w+)/$', 
                            'views.campaign_page', 
                            name='campaign_page'),

                        url(r'camp/(?P<camp_id>\w+)/$', 
                            'views.campaign_page', 
                            name='campaign_page_id'),
                        
                        url(r'camp/(?P<chash>\w{8}\w+)/admin/$', 
                            'views.campaign_admin', 
                            name='campaign_admin'),

                        url(r'camp/(?P<chash>\w{8}\w+)/update/$', 
                            'views.campaign_update', 
                            name='campaign_update'),

                        url(r'camp/(?P<chash>\w{8}\w+)/launch/$', 
                            'views.campaign_launch', 
                            name='campaign_launch'),

                        url(r'camp/(?P<chash>\w{8}\w+)/widget/$', 
                            'views.campaign_widget_page', 
                            name='campaign_widget_page'),

                        url(r'campaign_update_ajax/$', 
                            'ajax_create.campaign_update_ajax', 
                            name='campaign_update_ajax'),
                        )

#
# Frontpage URLS
#
urlpatterns += patterns('',
                        url(r'^$', 'frontpage.views.frontpage', name='frontpage'),

                        url(r'^googlehostedservice.html/?$', 
                            'frontpage.views.googlehostedservice', 
                            name='googlehostedservice'),
                        )

#
# Analytics URLS
#
urlpatterns += patterns('',
                        url(r'^$', 
                            'analytics.views.analytics', 
                            name='analytics'),

                        url(r'ajax/analytics_data$', 
                            'analytics.ajax.analytics_data', 
                            name='analytics_data'),

                        url(r'ajax/analytics_sources_pie$', 
                            'analytics.ajax.analytics_sources_pie', 
                            name='analytics_sources_pie'),
                        
                        url(r'ajax/analytics_date_range_shares$', 
                            'analytics.ajax.analytics_date_range_shares', 
                            name='analytics_date_range_shares'),

                        url(r'ajax/analytics_date_range_reach$', 
                            'analytics.ajax.analytics_date_range_reach', 
                            name='analytics_date_range_reach'),

                        url(r'camp/(?P<chash>\w{8}\w+)/v/$', 
                            'analytics.views.analytics_chash',
                            name='campaign_analytics'),
                        )

#
# Facebook Authentication URLS
#
urlpatterns += patterns('',
                        # url(r'facebook_callback/$', 
                        #     'facebook_auth.facebook_server_callback', 
                        #     name='facebook_callback'),
                        
                       url(r'facebook_callback/$', 
                           'fauth.facebook_auth.facebook_callback', 
                           name='facebook_callback'),

                       url(r'facebook_callback_test/$', 
                           'fauth.facebook_auth.facebook_callback_test', 
                           name='facebook_callback_test'),

                       url(r'facebook_callback_ajax/$', 
                           'fauth.facebook_auth.facebook_callback_ajax', 
                           name='facebook_callback_ajax'),

                       url(r'facebook_logout_callback/$', 
                           'fauth.facebook_auth.facebook_logout_callback', 
                           name='facebook_logout_callback'),

                       url(r'ajax/facebook_update_feed/$', 
                           'fauth.ajax.update_feed', 
                           name='facebook_update_feed'),

                       url(r'ajax/campaign_facebook_update/(?P<campaign_id>\d+)/?$', 
                           'fauth.ajax.campaign_facebook_update', 
                           name='campaign_facebook_update'),

                       url(r'ajax/facebook_message/$', 
                           'fauth.ajax.message', 
                           name='facebook_message'),

                       url(r'ajax/facebook_friends/$', 
                           'fauth.ajax.friends', 
                           name='facebook_friends'),

                       # sample html page to test out the facebook login functionality
                       url(r'facebook_login_test/$', 
                           'fauth.views.facebook_login_test', 
                           name='facebook_login_test'),

                       # redirect facebook ogin callback
                       url(r'facebook_login_callback/$', 
                           'fauth.facebook_auth.facebook_login_callback', 
                           name='facebook_login_callback'),

                       # ajax call to logout
                       url(r'ajax/facebook_logout/$', 
                           'fauth.ajax.facebook_logout', 
                           name='ajax_facebook_logout'),

                       # ajax call to check if facebook is logged expired and 
                       # log out if it is
                       url(r'ajax/facebook_check_logout/$', 
                           'fauth.ajax.facebook_check_logout', 
                           name='ajax_facebook_check_logout'),

                       # ajax call to post a test feed
                       url(r'ajax/facebook_info_test/$', 
                           'fauth.ajax.facebook_info_test', 
                           name='ajax_facebook_info_test'),

                       # ajax call to get info
                       url(r'ajax/facebook_feed_test/$', 
                           'fauth.ajax.facebook_feed_test',
                           name='ajax_facebook_feed_test'),

                       # ajax call to sync session on client side with session on server
                       url(r'ajax/facebook_sync_server/$', 
                           'fauth.ajax.facebook_sync_server', 
                           name='ajax_facebook_sync_server'),
                       
                       # close return page
                       url(r'facebook_callback_close/$', 
                           'fauth.views.facebook_callback_close', 
                           name='facebook_callback_close'),

                       url(r'fauth/ajax/logged_in/?$', 
                           'fauth.ajax.check_facebook_logged_in', 
                           name='fauth_logged_in'),
                        )

#
# Twitter Authentication URLS
#
urlpatterns += patterns('',
                        url(r'ajax/follow_list.json/?$', 
                            'tauth.views.follow_list', 
                            name='follow_list'),

                        url(r'ajax/follower_list.json/?$', 
                            'tauth.views.follower_list', 
                            name='follower_list'),

                        url(r'ajax/friend_list.json/?$', 
                            'tauth.views.friend_list', 
                            name='friend_list'),

                        url(r'ajax/attendees.json/(?P<campaign_id>\d+)/?$', 
                            'tauth.views.attendees', 
                            name='attendees_list'),

                        url(r'info/?$', 
                            'tauth.views.info', 
                            name='tauth_info'),

                        url(r'login/?$', 
                            'tauth.views.login', 
                            name='tauth_login'),

                        url(r'login/callback/?$', 
                            'tauth.views.callback', 
                            name='tauth_callback'),

                       url(r'logout/?$', 
                           'tauth.views.logout', 
                           name='tauth_logout'),

                       url(r'tauth_info/?$', 
                           'tauth.views.tauth_info', 
                           name='tauth_info'),

                       url(r'tauth/ajax/logged_in/?$', 
                           'tauth.ajax.check_twitter_logged_in', 
                           name='tauth_logged_in'),
                        )

#
# Campaign URLS
#
urlpatterns += patterns('',
                        url(r'ajax/ajax_select_winners/$', 
                            'campaign.ajax.select_winners', 
                            name='ajax_select_winners'),

                        url(r'ajax/ajax_update_widget/$', 
                            'campaign.ajax.ajax_update_widget', 
                            name='ajax_update_widget'),
                        )

#
# Point-of-sale URLS
#
urlpatterns += patterns('',
                        url(r'ajax/eventBrite/discount_list/?$', 
                            'pos.brite.ajax.discount_list', 
                            name='ajax_eventbrite_discountlist'),

                        url(r'ajax/eventBrite/create_discount/?$', 
                            'pos.brite.ajax.create_discount', 
                            name='ajax_eventbrite_create_discount'),

                        url(r'ajax/eventBrite/update_discount/?$', 
                            'pos.brite.ajax.update_discount', 
                            name='ajax_eventbrite_update_discount'),
                        )
