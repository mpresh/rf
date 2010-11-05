from django.http import HttpResponse
from django.shortcuts import render_to_response
import simplejson

# Utility functions
def handle_redirect_string(redirect_url, redirect_args_string):
    redirect_url = redirect_url.replace("fb_xd_fragment", "")
    redirect_args_string = redirect_args_string.replace("fb_xd_fragment", "")

    print "HANDLE_REDIRECT_STRING", redirect_url, redirect_args_string
    redirectargs_list = redirect_args_string.split("AND")
    args_dict = {}
    for param in redirectargs_list:
        (key, value) = param.split("EQUALS")
        args_dict[key] = value
    

    print "REDIRECT_URL", redirect_url
    query_args_dict = {}
    if redirect_url.find("?") != -1:
        (url, query_string) = redirect_url.split("?")
        query_args = query_string.split("&")
        print "QUERY ARGS", query_args
        for arg in query_args:
            if arg.strip():
                (key, value) = arg.split("=")
                query_args_dict[key] = value
    else:
        url = redirect_url 
        

    for key in args_dict.keys():
        query_args_dict[key] = args_dict[key]

    query_args_list = ["%s=%s" % (key, query_args_dict[key]) 
                       for key in query_args_dict.keys()]
    redirect = url + "?" + "&".join(query_args_list)

    print "REDIRECT STRING RETURNING", redirect
    return redirect

def render_template(template, **template_variables):
    """ Wrapper which makes rendering templates nicer."""
    return render_to_response(template, template_variables)

def json_response(**keys):
    """ Render error json. """
    return HttpResponse(simplejson.dumps(keys))
