from django.http import HttpResponse, Http404

from django.shortcuts import render

import os.path

# View for the homepage
def home(request):
    template_name = "home.html"

    context = dict()
    context["title"] = "WIS - Accueil"

    return render(request, template_name, context)


# View for a personal gallery home page
def gallery_home(request, name):
    template_name = "gallery.html"

    if (int(name) > 2000): 
        raise Http404

    context = dict()
    context["title"] = name

    return render(request, template_name, context)
