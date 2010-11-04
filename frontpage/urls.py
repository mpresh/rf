from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       url(r'^$', 'frontpage.views.frontpage', name='frontpage'),
                       url(r'^googlehostedservice.html/?$', 'frontpage.views.googlehostedservice', name='googlehostedservice'),
)
