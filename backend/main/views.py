from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site

def home(request):
    domain_url = request.scheme + "://" + get_current_site(request).domain
    context = {"domain_url": domain_url}
    return render(request, "home.html", context)
