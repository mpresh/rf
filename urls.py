from django.conf.urls.defaults import *
from django.conf import settings

from views import *
from tauth.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
                       #(r'^$', index),

                       # twitter authentication auth module
                       url(r'^info/?$', 'tauth.views.info', name='tauth_info'),
                       url(r'^login/?$', 'tauth.views.login', name='tauth_login'),
                       url(r'^login/callback/?$', 'tauth.views.callback', name='tauth_callback'),
                       url(r'^logout/?$', 'tauth.views.logout', name='tauth_logout'),
                       url(r'^tauth_info/?$', 'tauth.views.tauth_info', name='tauth_info2'),

                       # json / ajax calls
                       url(r'^ajax/follow_list.json/?$', 'tauth.views.follow_list', name='follow_list'),
                       url(r'^ajax/follower_list.json/?$', 'tauth.views.follower_list', name='follower_list'),
                       url(r'^ajax/friend_list.json/?$', 'tauth.views.friend_list', name='friend_list'),
                       url(r'^ajax/attendees.json/?$', 'tauth.views.attendees', name='attendees_list'),
                       url(r'^ajax/event_add_user/?$', 'views.event_add_user', name='event_add_user'),
                       url(r'^ajax/event_attendees/(?P<event_id>\d+)/?$', 'views.event_attendees', name='event_attendees'),
                       url(r'^ajax/event_friend_attendees/(?P<event_id>\d+)/?$', 'views.event_friend_attendees', name='event_friend_attendees'),
                       url(r'^ajax/event_friend_not_attendees/(?P<event_id>\d+)/?$', 'views.event_friend_not_attendees', name='event_friend_not_attendees'),

					
                       
                       
                       url(r'^ajax/event_not_going/(?P<event_id>\d+)/?$', 'views.event_not_going', name='event_not_going'),
                       url(r'^ajax/event_going/(?P<event_id>\d+)/?$', 'views.event_going', name='event_going'),
                       #url(r'^ajax/event_maybe_going/(?P<event_maybe_id>\d+)/?$', 'views.event_maybe_going', name='event_maybe_going'),
                       url(r'^ajax/event_invite/(?P<event_id>\d+)/?$', 'views.event_invite_friend', name='event_invite_friend'),


                       # miscellaneous
                       url(r'^map/?$', 'views.map', name='map'),
					   url(r'^test/?$', 'views.test', name='test'),
 					   url(r'^upload_image/?$', 'views.upload_image', name='upload-image'),
  
                       # old
                       (r'^thanks/(?P<event_id>\d+)/$', event_thanks),
                       (r'^details/(?P<event_id>\d+)/$', event_details),
                       (r'^user_details/$', user_details),
                       (r'^about/$', about),
                       (r'^list/$', event_list),
                       (r'^create/$', event_create),
                       (r'^register/$', event_register),
                       (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
                        {'document_root': settings.MEDIA_ROOT}),

                       #(r'^twitter/', include('twitter_app.urls')),
                       (r'^event_home/(?P<event_id>\d)/$', event_home),
                       #url('^login/$', twitter_signin, name='login'),
                       #url('^return/$', twitter_return, name='return'),
                       (r'^admin/', include(admin.site.urls)),
)
