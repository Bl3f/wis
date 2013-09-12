from django.conf.urls import patterns, url, include
from django.conf import settings


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'wis.apps.gallery.views.home'),
                       url(r'^gallery/', include('wis.apps.gallery.urls')),

                       # Register view
                       url(r'^register', "wis.apps.gallery.views.register"),

                       # Search view
                       url(r'^search$', "wis.apps.gallery.views.search"),

                       # Login view
                       url(r'^login$', "wis.apps.gallery.views.auth"),

                       # Logout view
                       url(r'^logout$', "wis.apps.gallery.views.sign_out"),

                       # Upload view
                       # url(r'^upload$', "wis.apps.gallery.views.upload"),

                       # Creation of a new gallery view
                       url(r'^creation$', "wis.apps.gallery.views.create_gallery"),

                       # For the Django Jquery Upload
                       url(r'^upload$', 'wis.apps.gallery.views.ajax_upload'),

                       # Edit photos description
                       url(r'^edit$', 'wis.apps.gallery.views.edit_descriptions'),

                       # Delete a picture
                       url(r'^delete/(?P<obj_type>[-A-Za-z0-9_]+)/(?P<obj_id>[-A-Za-z0-9_]+)$',
                           'wis.apps.gallery.views.delete_obj', name="delete"),

                       # Check username availability view
                       url(r'^checkUser/(?P<username>(.+))$$', "wis.apps.gallery.views.check_user_availability"),

                       # Examples:
                       # url(r'^$', 'wis.views.home', name='home'),
                       # url(r'^wis/', include('wis.foo.urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       # url(r'^admin/', include(admin.site.urls)),
                       )


if settings.DEBUG:
    urlpatterns += patterns('',
                            url(r'^data/(?P<path>.*)$', 'django.views.static.serve', {
                                'document_root': settings.MEDIA_ROOT,
                                }),
                            url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
                                'document_root': settings.STATIC_ROOT,
                                }),
                            )
