from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^view/(?P<server_id>\d+)/$', 'servers.views.view_server'),
)
