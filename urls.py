from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       (r'^simpz/',  include('simpz.simpz_urls')),
                       (r'^admin/', include(admin.site.urls)),
                       url(r'^$', 'frontpage.views.frontpage', name='frontpage'),
)
