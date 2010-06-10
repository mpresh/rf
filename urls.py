from django.conf.urls.defaults import *
from django.conf import settings

from simpz.views import *
from simpz.tauth.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       #(r'^simpz/site_media/(?P<path>.*)$', 'django.views.static.serve',
                       #       {'document_root': settings.MEDIA_ROOT}),
                       (r'^simpz/',  include('simpz.simpz_urls'))
)
