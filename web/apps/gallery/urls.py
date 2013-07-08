from django.conf.urls import patterns, url
from  web.apps.gallery.views import *

urlpatterns = patterns('web.apps.gallery.views',

    # Galleries url 
#    url(r'^$', GalleryListView.as_view))
    url(r'^(?P<name>\d{4})$', gallery_home),

)
