from django.conf.urls.defaults import *

from analytics.views import *

urlpatterns = patterns('',
                       url(r'^$', 'analytics.views.analytics', name='analytics'),
                       url(r'ajax/analytics_data$', 'analytics.ajax.analytics_data', name='analytics_data'),
                       url(r'ajax/analytics_sources_pie$', 'analytics.ajax.analytics_sources_pie', name='analytics_sources_pie'),
                       url(r'ajax/analytics_date_range_shares$', 'analytics.ajax.analytics_date_range_shares', name='analytics_date_range_shares'),
                       url(r'ajax/analytics_date_range_reach$', 'analytics.ajax.analytics_date_range_reach', name='analytics_date_range_reach'),
                       url(r'camp/(?P<chash>\w{8}\w+)/v/$', 'analytics.views.analytics_chash', name='campaign_analytics'),
)

