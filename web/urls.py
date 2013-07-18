from django.conf.urls import patterns, url, include
from django.conf import settings


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'web.apps.gallery.views.home'),
                       url(r'^gallery/', include('web.apps.gallery.urls')),

                       # Register view
                       url(r'^register', "web.apps.gallery.views.register"),

                       # Search view
                       url(r'^search$', "web.apps.gallery.views.search"),

                       # Login view
                       url(r'^login$', "web.apps.gallery.views.auth"),

                       # Logout view
                       url(r'^logout$', "web.apps.gallery.views.sign_out"),

                       # Upload view
                       url(r'^upload$', "web.apps.gallery.views.upload"),

                       # Examples:
                       # url(r'^$', 'web.views.home', name='home'),
                       # url(r'^web/', include('web.foo.urls')),

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
