from django.shortcuts import render, get_object_or_404
from servers.models import Server, ServerCheck
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
import json


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
        ServerCheck.check_server(server)

    return HttpResponse("")


@login_required()
def update_server(request):
    response_data = {
        "success": True,
    }
    if request.method == "POST":
        if request.is_ajax():
            server = get_object_or_404(Server, pk=request.POST["server"])
            if server.solusapi is None:
                response_data = {"success": False}
            else:
                if request.POST["attribute"] == 'spec-bandwidth':
                    new_bandwidth = server.solusapi.update_bandwidth()
                    if new_bandwidth:
                        response_data["spec-bandwidth"] = new_bandwidth
                    else:
                        response_data = {"success": False}
                elif request.POST["attribute"] == 'spec-ram':
                    new_ram = server.solusapi.update_ram()
                    if new_ram:
                        response_data["spec-ram"] = new_ram
                    else:
                        response_data = {"success": False}
                elif request.POST["attribute"] == 'spec-hdd':
                    new_hdd = server.solusapi.update_hdd()
                    if new_hdd:
                        response_data["spec-hdd"] = new_hdd
                    else:
                        response_data = {"success": False}
                else:
                    response_data = {"success": False}
        else:
            response_data = {"success": False}
    else:
        response_data = {"success": False}

    return HttpResponse(json.dumps(response_data), content_type="application/json")
