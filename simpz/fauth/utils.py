def sync_session_cookies(req):
    cookies = req.COOKIES
    if "access_token" in cookies and 'access_token' not in req.session:
        req.session['access_token'] = cookies["access_token"]
        req.session['base_domain']  = cookies["base_domain"]
        req.session['secret'] = cookies["secret"]
        req.session['session_key'] = cookies["session_key"]
        req.session['sessionid'] = cookies["sessionid"]
        req.session['sig'] = cookies["sig"]
        req.session['uid'] = cookies["uid"]
