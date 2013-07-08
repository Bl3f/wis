from django.http import HttpResponse

from django.shortcuts import render
from django.views.generic import ListView
import os
from web.settings import MEDIA_ROOT


class GalleryListView(ListView):
    context_object_name = "pics_gallery"
    template_name = "gallery.html"

    def get_queryset(self):
        self.my_list = []
        files = os.listdir(MEDIA_ROOT + 'pic/base/')
        self.my_list = files

    def get_context_data(self, **kwargs):
        context = super(GalleryListView, self).get_context_data(**kwargs)
        context['my_list'] = self.my_list
        return context


def hello_world(request):
    template_name = "home.html"

    context = dict()
    context["title"] = "Hello World !"
    context["body"] = "<div id=\"testBox\"> Ahaha </div>"

    return render(request, template_name, context)
