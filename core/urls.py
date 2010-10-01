from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       #
                       ## json / ajax calls
                       url(r'ajax/follow_list.json/?$', 'tauth.views.follow_list', name='follow_list'),
                       url(r'ajax/follower_list.json/?$', 'tauth.views.follower_list', name='follower_list'),
                       url(r'ajax/friend_list.json/?$', 'tauth.views.friend_list', name='friend_list'),
                       url(r'ajax/attendees.json/(?P<campaign_id>\d+)/?$', 'tauth.views.attendees', name='attendees_list'),
                       ###
                       url(r'ajax/event_add_user/?$', 'ajax.event_add_user', name='event_add_user'),
                       url(r'ajax/event_attendees/(?P<event_id>\d+)/?$', 'ajax.event_attendees', name='event_attendees'),
                       url(r'ajax/event_friend_attendees/(?P<event_id>\d+)/?$', 'ajax.event_friend_attendees', name='event_friend_attendees'),
                       url(r'ajax/event_friend_not_attendees/(?P<event_id>\d+)/?$', 'ajax.event_friend_not_attendees', name='event_friend_not_attendees'),
                       url(r'ajax/event_not_going/(?P<event_id>\d+)/?$', 'ajax.event_not_going', name='event_not_going'),
                       url(r'ajax/event_going/(?P<event_id>\d+)/?$', 'ajax.event_going', name='event_going'),
                       url(r'ajax/campaign_going_twitter/(?P<campaign_id>\d+)/?$', 'ajax.campaign_going_twitter', name='campaign_going_twitter'),

                       url(r'ajax/event_tweet_invite/(?P<event_id>\d+)/?$', 'ajax.event_tweet_invite', name='event_tweet_invite'),
                       url(r'ajax/campaign_tweet_invite/(?P<campaign_id>\d+)/?$', 'ajax.campaign_tweet_invite', name='campaign_tweet_invite'),
                       #url(r'ajax/event_tweet_invite_dm/(?P<event_id>\d+)/?$', 'ajax.event_tweet_invite_dm', name='event_tweet_invite_dm'),
                       url(r'upload_image/?$', 'ajax.upload_image', name='upload_image'),
                       ##

                       #
                       url(r'^',  include('fauth.urls')),
                       url(r'^',  include('tauth.urls')),
                       url(r'^',  include('campaign.urls')),
                       url(r'^',  include('pos.urls')),

                       ### miscellaneous
                       url(r'^map/?$', 'views.map', name='map'),
                       url(r'^test/?$', 'views.test', name='test'),
                       url(r'^test2/?$', 'views.test2', name='test2'),
                       url(r'^test3/?$', 'views.test3', name='test3'),
                       url(r'^test4/?$', 'views.test4', name='test4'),
                       url(r'^test5/?$', 'views.test5', name='test5'),

                       # widget stuff
                       url(r'camp/badge/(?P<camp_id>\w+)/$', 'views.campaign_badge', name='badge_id'),
                       url(r'camp/widget/(?P<camp_id>\w+)/$', 'views.campaign_widget', name='widget_id'),
                       url(r'camp/badge/$', 'views.campaign_badge', name='badge'),
                       url(r'camp/widget/$', 'views.campaign_widget', name='widget'),
                       ##

                       url(r'event_details/(?P<event_id>\d+)/$', 'views.event_details', name='event_details'),
                       url(r'user_details/(?P<user_id>\d+)/$', 'views.user_details', name='user_details'),
                       url(r'about/$', 'views.about', name='about'),
                       url(r'contact/$', 'views.contact', name='contact'),
                       url(r'jobs/$', 'views.jobs', name='jobs'),
                       url(r'howitworks/$', 'views.howitworks', name='howitworks'),
                       url(r'list/$', 'views.event_list', name='event_list'),

                       url(r'create_campaign/$', 'views.create_campaign', name='create_campaign'),
                       url(r'campaign_welcome/$', 'views.campaign_created', name='campaign_created'),
                       url(r'create_campaign_ajax/$', 'ajax_create.create_campaign', name='create_campaign_ajax'),
                       url(r'create_campaign_url_check/$', 'ajax_create.create_campaign_url_check', name='create_campaign_url_check'),
                       url(r'send_details_email/$', 'ajax_create.send_details_email', name='send_details_email'),

                       url(r'campaign_page_preview/$', 'views.campaign_page_preview', name='campaign_page_preview'),
                       url(r'camp/(?P<chash>\w{8}\w+)/$', 'views.campaign_page', name='campaign_page'),
                       url(r'camp/(?P<camp_id>\w+)/$', 'views.campaign_page', name='campaign_page_id'),

                       url(r'camp/(?P<chash>\w{8}\w+)/admin/$', 'views.campaign_admin', name='campaign_admin'),
                       url(r'camp/(?P<chash>\w{8}\w+)/update/$', 'views.campaign_update', name='campaign_update'),
                       url(r'camp/(?P<chash>\w{8}\w+)/launch/$', 'views.campaign_launch', name='campaign_launch'),
                       url(r'camp/(?P<chash>\w{8}\w+)/widget/$', 'views.campaign_widget_page', name='campaign_widget_page'),
                       url(r'campaign_update_ajax/$', 'ajax_create.campaign_update_ajax', name='campaign_update_ajax'),


                       (r'site_media/(?P<path>.*)$', 'django.views.static.serve',
                              {'document_root': settings.MEDIA_ROOT}),
                       
)

