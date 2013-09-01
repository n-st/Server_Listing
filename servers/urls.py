from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^view/(?P<server_id>\d+)/$', 'servers.views.view_server'),
    url(r'^update/$', 'servers.views.update_server'),
    url(r'^solus_connect/$', 'servers.views.get_solus_data'),
    url(r'^responder_connect/$', 'servers.views.get_responder_data'),
    url(r'^update_ip/$', 'servers.views.update_ips'),
    url(r'^ping_check/$', 'servers.views.ping_check'),
)
