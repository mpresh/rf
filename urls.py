from django.conf.urls.defaults import *
from django.conf import settings

from demo.views import *
from demo.auth.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
                       (r'^$', index),

                       # twitter authentication auth module
                       url(r'^info/?$', 'auth.views.info', name='auth_info'),
                       url(r'^login/?$', 'auth.views.login', name='auth_login'),
                       url(r'^login/callback/?$', 'auth.views.callback', name='auth_callback'),
                       url(r'^logout/?$', 'auth.views.logout', name='auth_logout'),


                       (r'^thanks/(?P<event_id>\d+)/$', event_thanks),
                       (r'^details/(?P<event_id>\d+)/$', event_details),
                       (r'^about/$', about),
                       (r'^list/$', event_list),
                       (r'^create/$', event_create),
                       (r'^register/$', event_register),
                       (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
                        {'document_root': settings.MEDIA_ROOT}),

                       #(r'^twitter/', include('twitter_app.urls')),
                       #(r'^event_home/$', event_home),
                       #url('^login/$', twitter_signin, name='login'),
                       #url('^return/$', twitter_return, name='return'),

                       (r'^admin/', include(admin.site.urls)),
)
