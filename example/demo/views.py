from django.shortcuts import render
from django.template import RequestContext


def homepage_v(request):
    return render(request, "homepage.html")
