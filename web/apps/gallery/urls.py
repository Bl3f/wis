from django.conf.urls import patterns, url
from web.apps.gallery.views import *


urlpatterns = patterns('web.apps.gallery.views',
                       # Galleries url
                       url(r'^(?P<user>[-A-Za-z0-9_]+)/(?P<gallery_title>(.+))$', gallery_home),
                       )
