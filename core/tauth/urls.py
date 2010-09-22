from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',

                       # twitter authentication auth module
                       url(r'info/?$', 'tauth.views.info', name='tauth_info'),
                       url(r'login/?$', 'tauth.views.login', name='tauth_login'),
                       url(r'login/callback/?$', 'tauth.views.callback', name='tauth_callback'),
                       url(r'logout/?$', 'tauth.views.logout', name='tauth_logout'),
                       url(r'tauth_info/?$', 'tauth.views.tauth_info', name='tauth_info'),
                       url(r'tauth/ajax/logged_in/?$', 'tauth.ajax.check_twitter_logged_in', name='tauth_logged_in'),
                       )


