from django.conf.urls import patterns, url
from  web.apps.gallery.views import *

urlpatterns = patterns('web.apps.gallery.views',

    # Galleries url 
#    url(r'^$', GalleryListView.as_view))
    url(r'^(?P<name>[-A-Za-z0-9_]+)$', gallery_home),

)
