from django.shortcuts import render
import os
from web.settings import MEDIA_ROOT

from web.apps.gallery.models import *


def gallery_home(request, id):
    template_name = "gallery.html"

    gallery = Gallery.objects.get(pk=id)

    context = dict()
    context["gallery"] = gallery
    context["images"] = Image.objects.filter(gallery=gallery)

    return render(request, template_name, context)


def home(request):
    template_name = "home.html"

    context = dict()
    context["title"] = "WIS - Welcome"

    return render(request, template_name, context)
