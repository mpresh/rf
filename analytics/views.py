from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404

def analytics(req):
    return render_to_response('analytics.html', {})
