from django.conf.urls.defaults import *
from django.conf import settings

#from views import *
#from fauth.facebook_auth import *
#from tauth.views import login

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'views.index', name='index'),
                       #
                       ## json / ajax calls
                       url(r'ajax/follow_list.json/?$', 'tauth.views.follow_list', name='follow_list'),
                       url(r'ajax/follower_list.json/?$', 'tauth.views.follower_list', name='follower_list'),
                       url(r'ajax/friend_list.json/?$', 'tauth.views.friend_list', name='friend_list'),
                       url(r'ajax/attendees.json/(?P<event_id>\d+)/?$', 'tauth.views.attendees', name='attendees_list'),
                       ###
                       url(r'ajax/event_add_user/?$', 'ajax.event_add_user', name='event_add_user'),
                       url(r'ajax/event_attendees/(?P<event_id>\d+)/?$', 'ajax.event_attendees', name='event_attendees'),
                       url(r'ajax/event_friend_attendees/(?P<event_id>\d+)/?$', 'ajax.event_friend_attendees', name='event_friend_attendees'),
                       url(r'ajax/event_friend_not_attendees/(?P<event_id>\d+)/?$', 'ajax.event_friend_not_attendees', name='event_friend_not_attendees'),
                       url(r'ajax/event_not_going/(?P<event_id>\d+)/?$', 'ajax.event_not_going', name='event_not_going'),
                       url(r'ajax/event_going/(?P<event_id>\d+)/?$', 'ajax.event_going', name='event_going'),
                       url(r'ajax/event_tweet_invite/(?P<event_id>\d+)/?$', 'ajax.event_tweet_invite', name='event_tweet_invite'),
                       url(r'ajax/event_tweet_invite_dm/(?P<event_id>\d+)/?$', 'ajax.event_tweet_invite_dm', name='event_tweet_invite_dm'),
                       url(r'upload_image/?$', 'ajax.upload_image', name='upload_image'),
                       ##
                       ### miscellaneous
                       url(r'map/?$', 'views.map', name='map'),
                       url(r'test/?$', 'views.test', name='test'),
                       url(r'test2/?$', 'views.test2', name='test2'),
                       url(r'test3/?$', 'views.test3', name='test3'),
                       ##
                       url(r'event_home/(?P<event_id>\d+)/?$', 'views.event_home', name='event_home'),                       
                       url(r'thanks/(?P<event_id>\d+)/$', 'views.event_thanks', name='event_thanks'),
                       url(r'event_details/(?P<event_id>\d+)/$', 'views.event_details', name='event_details'),
                       url(r'user_details/(?P<user_id>\d+)/$', 'views.user_details', name='user_details'),
                       url(r'about/$', 'views.about', name='about'),
                       url(r'list/$', 'views.event_list', name='event_list'),

                       url(r'create/$', 'views.event_create', name='event_create'),
                       url(r'campaign_welcome/$', 'views.campaign_created', name='campaign_created'),
                       url(r'create_campaign/$', 'ajax_create.create_campaign', name='create_campaign'),

                       url(r'camp/(?P<chash>\w{8}\w+)/$', 'views.campaign_page', name='campaign_page'),
                       url(r'camp/(?P<chash>\w{8}\w+)/admin/$', 'views.campaign_admin', name='campaign_admin'),
                       url(r'camp/(?P<chash>\w{8}\w+)/update/$', 'views.campaign_update', name='campaign_update'),

                       url(r'invite/(?P<invite_id>\d+)/$', 'views.invite', name='event_invite'),
                       #url(r'blogvip/(?P<invite_id>\d+)/$', 'views.blogvip', name='event_blogvip'),
                       url(r'be/?$', 'views.blogvip_flow', name='event_blogvip_flow'),
                       #
                       url(r'^',  include('fauth.urls')),
                       url(r'^',  include('tauth.urls')),

                       (r'site_media/(?P<path>.*)$', 'django.views.static.serve',
                              {'document_root': settings.MEDIA_ROOT}),
                       
)

