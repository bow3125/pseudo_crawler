from django.conf.urls import patterns, include, url
from notice import views
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pseudo_crawler.views.home', name='home'),
    # url(r'^pseudo_crawler/', include('pseudo_crawler.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    (r'^$', views.search_form),
    (r'^search/$', views.search),
)
