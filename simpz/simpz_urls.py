from django.conf.urls.defaults import *
from django.conf import settings

from views import *
from tauth.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       (r'^$', index),

                       # twitter authentication auth module
                       url(r'info/?$', 'tauth.views.info', name='tauth_info'),
                       url(r'login/?$', 'tauth.views.login', name='tauth_login'),
                       url(r'login/callback/?$', 'tauth.views.callback', name='tauth_callback'),
                       url(r'logout/?$', 'tauth.views.logout', name='tauth_logout'),
                       url(r'tauth_info/?$', 'tauth.views.tauth_info', name='tauth_info2'),

                       # json / ajax calls
                       url(r'ajax/follow_list.json/?$', 'tauth.views.follow_list', name='follow_list'),
                       url(r'ajax/follower_list.json/?$', 'tauth.views.follower_list', name='follower_list'),
                       url(r'ajax/friend_list.json/?$', 'tauth.views.friend_list', name='friend_list'),
                       url(r'ajax/attendees.json/?$', 'tauth.views.attendees', name='attendees_list'),

                       url(r'ajax/event_add_user/?$', 'ajax.event_add_user', name='event_add_user'),
                       url(r'ajax/event_attendees/(?P<event_id>\d+)/?$', 'ajax.event_attendees', name='event_attendees'),
                       url(r'ajax/event_friend_attendees/(?P<event_id>\d+)/?$', 'ajax.event_friend_attendees', name='event_friend_attendees'),
                       url(r'ajax/event_friend_not_attendees/(?P<event_id>\d+)/?$', 'ajax.event_friend_not_attendees', name='event_friend_not_attendees'),
                       url(r'ajax/event_not_going/(?P<event_id>\d+)/?$', 'ajax.event_not_going', name='event_not_going'),
                       url(r'ajax/event_going/(?P<event_id>\d+)/?$', 'ajax.event_going', name='event_going'),
                       url(r'ajax/event_tweet_invite/(?P<event_id>\d+)/?$', 'ajax.event_tweet_invite', name='event_tweet_invite'),
                       url(r'ajax/event_tweet_invite_dm/(?P<event_id>\d+)/?$', 'ajax.event_tweet_invite_dm', name='event_tweet_invite_dm'),
                       url(r'upload_image/?$', 'ajax.upload_image', name='upload-image'),

                       # miscellaneous
                       url(r'map/?$', 'views.map', name='map'),
                       url(r'test/?$', 'views.test', name='test'),

                       url(r'event_home/(?P<event_id>\d)/?$', 'views.event_home', name='event_home'),                       
                       url(r'thanks/(?P<event_id>\d+)/$', 'views.event_thanks', name='event_thanks'),
                       url(r'event_details/(?P<event_id>\d+)/$', 'views.event_details', name='event_details'),
                       url(r'user_details/(?P<user_id>\d+)/$', 'views.user_details', name='user_details'),
                       url(r'about/$', 'views.about', name='about'),
                       url(r'list/$', 'views.event_list', name='event_list'),
                       url(r'create/$', 'views.event_create', name='event_create'),
                       url(r'invite/(?P<invite_id>\d+)/$', 'views.invite', name='event_invite'),
                       
                       
                       (r'site_media/(?P<path>.*)$', 'django.views.static.serve',
                              {'document_root': settings.MEDIA_ROOT}),
                       
)
