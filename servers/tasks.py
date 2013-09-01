from celery import task
from celery.utils.log import get_task_logger
from servers.models import Server, ServerCheck
from django.core.cache import cache
from django.conf import settings
from django.utils import timezone

LOCK_TIME = 60 * settings.LEEWAY_TIME
logger = get_task_logger(__name__)

@task(name='servers.ping')
def ping():
    servers_to_check = Server.objects.filter(check_status=True)
    for server in servers_to_check:
        server_key = '{0}-server-ping'.format(server.pk)
        if cache.get(server_key) is not None:
            logger.info("Server {0} still in cool down".format(server.pk))
            continue
        logger.info("Server {0} running ping...".format(server.pk))
        cache.add(server_key, 'true', LOCK_TIME)
        ServerCheck.check_server(server)


@task(name='servers.next_due_date')
def update_server_dates():
    servers_to_update = Server.objects.filter(next_due_date__lte=timezone.now().date())

    for server in servers_to_update:
        logger.info("Updating next due date of server {0}".format(server.pk))
        if server.billing_type == Server.MONTHLY:
            test_time = timezone.now().date().replace(day=server.purchased_at.day)
            if test_time <= timezone.now().date():
                if test_time.month == 12:
                    test_time = test_time.replace(month=1)
                else:
                    test_time = test_time.replace(month=test_time.month+1)
            server.next_due_date = test_time
            server.save()
        else:
            test_time = timezone.now().date().replace(day=server.purchased_at.day, month=server.purchased_at.month)
            if test_time <= timezone.now().date():
                test_time = test_time.replace(year=test_time.year+1)
            server.next_due_date = test_time
            server.save()
