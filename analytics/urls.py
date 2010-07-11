from django.conf.urls.defaults import *
from django.conf import settings

from analytics.views import *

urlpatterns = patterns('',
                       url(r'^$', 'analytics.views.analytics', name='analytics'),
                       url(r'ajax/analytics_data$', 'analytics.ajax.analytics_data', name='analytics_data'),
)
