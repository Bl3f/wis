from django.http import HttpResponse

from django.shortcuts import render
from django.views.generic import ListView
import os
from web.settings import MEDIA_ROOT


def gallery_home(request, name):
    template_name = "gallery.html"

    context = dict()
    context["title"] = name

    context['img'] = os.listdir(MEDIA_ROOT + 'pic/base/')

    return render(request, template_name, context)

def home(request):
    template_name = "home.html"

    context = dict()
    context["title"] = "WIS - Welcome"

    return render(request, template_name, context)
