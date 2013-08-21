from django.shortcuts import render, get_object_or_404
from servers.models import Server, ServerCheck
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from ping import Ping


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
    servers_to_check = Server.objects.filter(check_status=True)
    for server in servers_to_check:
        server_log = ServerCheck.check_server(server)
        if server_log is not False:
            print "Checked Server"
        else:
            print "Leeway in action"

    return HttpResponse("")