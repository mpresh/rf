from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^simpz/',  include('core.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^analytics/', include('analytics.urls')),
                       url(r'^$', 'frontpage.views.frontpage', name='frontpage'),
                       url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
                           {'document_root': settings.MEDIA_ROOT}, name="static"),
)
