from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse_lazy


urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', {
        "template_name": 'quick_auth/login.html',

    }, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout')
)