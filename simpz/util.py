def get_invite_url(req):
    # getting the right path
    invite_url = req.build_absolute_uri() 
    return invite_url
    start = invite_url.find("?")
    if start != -1:
        invite_url = invite_url[:start]
    path = req.get_full_path()
    start = path.find("?")
    if start != -1:
        path = path[:start]
    invite_url = invite_url.strip("/")
    if path[-1] == "/":
        path = path[:-1]

    invite_url = invite_url[:len(path) * -1] + "/simpz/invite/"
    return invite_url
