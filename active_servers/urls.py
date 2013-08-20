from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'active_servers.views.home', name='home'),
    # url(r'^active_servers/', include('active_servers.foo.urls')),

    url(r'^$', 'servers.views.server_list'),
    url(r'^server/', include('servers.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
