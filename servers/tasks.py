from celery import task
from celery.utils.log import get_task_logger
from servers.models import Server, ServerCheck
from django.core.cache import cache
from django.conf import settings

LOCK_TIME = 60 * settings.LEEWAY_TIME
logger = get_task_logger(__name__)

@task(name='servers.ping')
def ping():
    servers_to_check = Server.objects.filter(check_status=True)
    for server in servers_to_check:
        server_key = '{0}-server-ping'.format(server.pk)
        if cache.get(server_key) is not None:
            logger.debug("Server {0} still in cool down".format(server.pk))
            continue
        logger.debug("Server {0} running ping...".format(server.pk))
        cache.add(server_key, 'true', LOCK_TIME)
        ServerCheck.check_server(server)
