from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
                       (r'^simpz/',  include('simpz.simpz_urls'))
)
