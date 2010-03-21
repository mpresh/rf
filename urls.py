from django.conf.urls.defaults import *
from django.conf import settings

from demo.views import *
from demo.tauth.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
                       (r'^$', index),

                       # twitter authentication auth module
                       url(r'^info/?$', 'tauth.views.info', name='tauth_info'),
                       url(r'^login/?$', 'tauth.views.login', name='tauth_login'),
                       url(r'^login/callback/?$', 'tauth.views.callback', name='tauth_callback'),
                       url(r'^logout/?$', 'tauth.views.logout', name='tauth_logout'),
                       url(r'^tauth_info/?$', 'tauth.views.tauth_info', name='tauth_info'),

                       # json 
                       url(r'^follow_list/?$', 'tauth.views.follow_list', name='follow_list'),
                       url(r'^follower_list/?$', 'tauth.views.follower_list', name='follower_list'),
                       url(r'^friend_list/?$', 'tauth.views.friend_list', name='friend_list'),

                       # 
                       url(r'^map/?$', 'views.map', name='map'),

                       # old
                       (r'^thanks/(?P<event_id>\d+)/$', event_thanks),
                       (r'^details/(?P<event_id>\d+)/$', event_details),
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
