from celery import task
from servers.models import Server, ServerCheck
from django.core.cache import cache
from django.conf import settings

LOCK_TIME = 60 * settings.LEEWAY_TIME

@task(name='servers.ping')
def ping():
    servers_to_check = Server.objects.filter(check_status=True)
    for server in servers_to_check:
        ServerCheck.check_server(server)
