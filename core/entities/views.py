from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import *
from django.conf import settings

from models import AttributeType, Attribute, EntityType, Entity

def index(req):
    dict = {}
    dict['attributes'] = Attribute.objects.all()
    dict['attribute_types'] = AttributeType.objects.all()
    dict["entity_types"] = EntityType.objects.all()
    dict["entities"] = Entity.objects.all()
    return render_to_response('manage.html', dict)

def manage_entities(req):
    dict = {}
    dict["entities"] = Entity.objects.all()
    return render_to_response('entity_manage.html', dict)


def manage_entity_types(req):
    dict = {}
    dict["entity_types"] = EntityType.objects.all()
    return render_to_response('entity_type_manage.html', dict)

def manage_attributes(req):
    dict = {}
    dict['attributes'] = Attribute.objects.all()
    return render_to_response('attribute_manage.html', dict)

def manage_attribute_types(req):
    dict = {}
    #dict['attribute_types'] = AttributeType.objects.all()
    dict['items'] = AttributeType.objects.all()
    return render_to_response('attribute_type_manage.html', dict)
