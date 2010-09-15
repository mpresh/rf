def sync_session_cookies(req):
    cookies = req.COOKIES
    print "COOKIES", cookies
    if "access_token" in cookies and 'access_token' not in req.session:
        req.session['access_token'] = cookies["access_token"]

    if "base_domain" in cookies and 'base_domain' not in req.session:
        req.session['base_domain']  = cookies["base_domain"]

    if "secret" in cookies and 'secret' not in req.session:
        req.session['secret'] = cookies["secret"]

    if "session_key" in cookies and 'session_key' not in req.session:
        req.session['session_key'] = cookies["session_key"]

    if "sessionid" in cookies and 'sessionid' not in req.session:
        req.session['sessionid'] = cookies["sessionid"]

    if "sig" in cookies and 'sig' not in req.session:
        req.session['sig'] = cookies["sig"]

    if "uid" in cookies and 'uid' not in req.session:
        req.session['uid'] = cookies["uid"]
