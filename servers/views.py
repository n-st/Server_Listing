from django.shortcuts import render
from servers.models import Server


def server_list(request):
    servers = Server.objects.all()
    return render(request, 'servers/server_listing.html', {
        "servers": servers
    })