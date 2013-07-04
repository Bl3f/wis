from django.http import HttpResponse

from django.shortcuts import render

import os.path

def hello_world(request):
    template_name = "helloWorld.html"

    context = dict()
    context["title"] = "Hello World !"
    context["body"] = "<div id=\"testBox\"> Ahaha </div>"

    return render(request, template_name, context)
