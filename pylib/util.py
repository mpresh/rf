# random utility functions
def handle_redirect_string(redirect_url, redirect_args_string):

    print "HANDLE_REDIRECT_STRING", redirect_url, redirect_args_string
    redirectargs_list = redirect_args_string.split("AND")
    redirect_string = ""
    args_dict = {}
    for param in redirectargs_list:
        (key, value) = param.split("EQUALS")
        args_dict[key] = value


    query_args_dict = {}
    if redirect_url.find("?") != -1:
        (url, query_string) = redirect_url.split("?")
        query_args = query_string.split("&")
        for arg in query_args:
            (key, value) = arg.split("=")
            query_args_dict[key] = value
    else:
        url = redirect_url 
        

    for key in args_dict.keys():
        query_args_dict[key] = args_dict[key]

    query_args_list = ["%s=%s" % (key, query_args_dict[key]) for key in query_args_dict.keys()]
    redirect = url + "?" + "&".join(query_args_list)

    print "REDIRECT STRING RETURNING", redirect
    return redirect
