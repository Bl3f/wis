import json
import os
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from web.settings import MEDIA_ROOT

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import logout
from django.shortcuts import render, render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt

from web.apps.gallery.models import *
from web.apps.gallery.forms import *

from web.apps.gallery.messages import *

from ajaxuploader.views import AjaxFileUploader

context = dict()
context['loginForm'] = UserForm()

import_uploader = AjaxFileUploader()

def gallery_home(request, user, gallery_slug):
    template_name = "gallery.html"

    request.session['gallery'] = gallery_slug
    request.session['gallery_owner'] = user

    owner_id = User.objects.get(username=user).pk
    gallery = Gallery.objects.get(slug_name=gallery_slug, owner_id=owner_id)

    context["gallery"] = gallery
    context["images"] = Image.objects.filter(gallery=gallery)

    return render(request, template_name, context)


def user_galleries(request, user):
    template_name = "user_galleries.html"

    context['isOwner'] = (user == str(request.user))

    context['galleries'] = Gallery.objects.filter(owner=User.objects.get(username=user))

    return render(request, template_name, context)


def home(request):
    template_name = "home.html"

    context["title"] = "WIS - Welcome"
    context["searchForm"] = SearchForm(json.dumps(Gallery.objects.get_galleries_with_slug()))

    return render(request, template_name, context)


@csrf_exempt
def search(request):
    gallery_to_go = dict(request.POST)

    data = {'redirect': "/gallery/{}/{}".format(gallery_to_go['owner'].pop(), gallery_to_go['slug'].pop())}

    return HttpResponse(json.dumps(data), mimetype='application/json')


def create_gallery(request):
    template_name = "create_gallery.html"

    form = GalleryForm(request.POST or None)

    if form.is_valid():
        data = form.cleaned_data
        new_gallery = Gallery(title=data['title'],
                              description=data['description'],
                              public=data['public'],
                              owner=request.user,
                              place=data['place'])
        new_gallery.save()
    else:
        context['form'] = form

    return render(request, template_name, context)


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

    form = UserCreationForm(request.POST or None)

    if form.is_valid():
        new_user = form.save()
        return redirect(home)
    else:
        context['form'] = form
    return render(request, template_name, context)


def upload(request):

    template_name = "upload.html"
    context['canUpload'] = False

    if str(request.user) == "AnonymousUser":
        context['msg'] = ERROR_NOTAUTH
    elif request.session['gallery_owner'] != str(request.user):
        context['msg'] = ERROR_PERM
    else:
        context['canUpload'] = True
        if request.method == "POST":
            form = UploadImage(request.POST, request.FILES)
            if form.is_valid():
                data = form.cleaned_data
                new_img = Image(path=request.FILES['img'],
                                description=data['description'],
                                place=data['place'],
                                gallery=Gallery.objects.get(slug_name=data['gallery_slug'],
                                                            owner=request.user),
                                owner=request.user)
                new_img.save()
            else:
                context['msg'] = "ERROR"
        else:
            if request.session['gallery'] is None:
                context['msg'] = "Error : no gallery"
            else:
                context['form'] = UploadImage(initial={'gallery_slug': request.session['gallery']})

    return render(request, template_name, context)


def ajax_upload(request):
    csrf_token = get_token(request)
    return render_to_response('startbis.html',
        {'csrf_token': csrf_token}, context_instance = RequestContext(request))


@csrf_exempt
def ajax(request):

    if request.method == 'POST':
        print request
        new_img = Image(path=request.FILES[u'files[]'],
                        description="Au matin je vis avec joie ...",
                        place="Ushuaia",
                        gallery=Gallery.objects.get(slug_name="freedom",),
                        owner=User.objects.get(username="estelle"))
        new_img.save()
        return HttpResponse(True)
    # return status to client
    
    return render(request, template_name, context)
    
