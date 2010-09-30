from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
                       url(r'ajax/eventBrite/discount_list/?$', 'pos.brite.ajax.discount_list', name='ajax_eventbrite_discountlist'),
                       url(r'ajax/eventBrite/create_discount/?$', 'pos.brite.ajax.create_discount', name='ajax_eventbrite_create_discount'),
                       url(r'ajax/eventBrite/update_discount/?$', 'pos.brite.ajax.update_discount', name='ajax_eventbrite_update_discount'),
                       )
