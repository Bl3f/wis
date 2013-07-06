from django.conf.urls import patterns, url

urlpatterns = patterns('gallery.views',

    # Galleries url 
    url(r'^(?P<name>\d{4})$', 'gallery_home'),

)
