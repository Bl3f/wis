from django.http import HttpResponse

from django.shortcuts import render
from django.views.generic import ListView
import os
from web.settings import MEDIA_ROOT


def gallery_home(request, name):
    template_name = "gallery.html"

    context = dict()
    context["title"] = name

    context['img'] = my_list = []
    files = os.listdir(MEDIA_ROOT + 'pic/base/')
    context['img'] = files

    return render(request, template_name, context)

def home(request):
    template_name = "home.html"

    context = dict()
    context["title"] = "Hello World !"
    context["body"] = "<div id=\"testBox\"> Ahaha </div>"

    return render(request, template_name, context)
