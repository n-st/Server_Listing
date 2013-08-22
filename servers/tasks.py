from celery import task
from servers.models import Server, ServerCheck

@task(name='servers.ping')
def ping():
    servers_to_check = Server.objects.filter(check_status=True)
    for server in servers_to_check:
        ServerCheck.check_server(server)
