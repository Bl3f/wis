import os
from web.settings import MEDIA_ROOT

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import logout
from django.shortcuts import render
from django.shortcuts import redirect

from web.apps.gallery.models import *
from web.apps.gallery.forms import *


context = dict()
context['loginForm'] = AuthenticationForm()


def gallery_home(request, user, gallery_title):
    template_name = "gallery.html"

    owner_id = User.objects.get(username=user).pk
    gallery = Gallery.objects.get(title=gallery_title, owner_id=owner_id)

    context["gallery"] = gallery
    context["images"] = Image.objects.filter(gallery=gallery)

    return render(request, template_name, context)


def home(request):
    template_name = "home.html"

    context["title"] = "WIS - Welcome"
    context["searchForm"] = Search()

    return render(request, template_name, context)


def search(request):
    template_name = "gallery.html"

    return redirect("gallery/" + request.POST["gallery"])


def auth(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to a success page.
                context['auth'] = True
            else:
                context['auth'] = False
             # Return a 'disabled account' error message
        else:
            context['auth'] = False
        context['username'] = username

        return redirect(request.META['HTTP_REFERER'].replace(request.META["HTTP_ORIGIN"], ""))

    else:
        template_name = "login.html"

        context['auth'] = False

    return render(request, template_name, context)


def sign_out(request):

    logout(request)

    return redirect("/")  # home(request)


def register(request):

    template_name = "register.html"

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return redirect(home)
    else:
        context['form'] = UserCreationForm()
    return render(request, template_name, context)


def upload(request):

    template_name = "upload.html"
    
    if (request.method == "POST"):
        form = UploadImage(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # gallery_id = 1
            # title = request.POST['title']
            # description = request.POST['description']
            # owner_id = 2
            # uploaded = '2013-07-27 19:12'
    else:
        context['form'] = UploadImage()
    
    return render(request, template_name, context)
