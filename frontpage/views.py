from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from campaign.models import Campaign


def frontpage(req):
    #req.session["redirect"] = req.get_full_path()  

    domain = req.META['HTTP_HOST'].split(".")[0]
    print "DOMAIN IS", domain

    if domain != "www" and domain != "ripplefunction":
        campaigns = Campaign.objects.filter(subdomain=domain)
        if len(list(campaigns)) > 0:
            campaign = list(campaigns)[-1]
            return HttpResponseRedirect(reverse('campaign_page_id', kwargs={'camp_id':campaign.id}))


    templates = ["frontpage.html", "frontpageCycle.html"]
    template = templates[0]
    if "t" in req.GET:
        t = req.GET["t"]
        try:
            template = templates[int(t)]
        except Exception:
            pass
    return render_to_response(template, {})


def googlehostedservice(req):
    return render_to_response('googlehostedservice.html', {})
