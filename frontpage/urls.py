from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

urlpatterns = patterns('',
                       url(r'^$', 'frontpage.views.frontpage', name='frontpage'),
                       url(r'^googlehostedservice.html/?$', 'frontpage.views.googlehostedservice', name='googlehostedservice'),
)
