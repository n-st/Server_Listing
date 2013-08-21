from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', {"template_name": 'quick_auth/login.html'}, name='login'),
)