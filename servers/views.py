from django.shortcuts import render, get_object_or_404
from servers.models import Server
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse


@login_required
def server_list(request):
    servers = Server.objects.all()
    return render(request, 'servers/server_listing.html', {
        "servers": servers
    })


@login_required
def view_server(request, server_id):
    server = get_object_or_404(Server, pk=server_id)
    return render(request, 'servers/server.html', {
        "server": server
    })


def ping_check(request):
    return HttpResponse("ping response")