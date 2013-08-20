from django.shortcuts import render, get_object_or_404
from servers.models import Server


def server_list(request):
    servers = Server.objects.all()
    return render(request, 'servers/server_listing.html', {
        "servers": servers
    })


def view_server(request, server_id):
    server = get_object_or_404(Server, pk=server_id)
    return render(request, 'servers/server.html', {
        "server": server
    })