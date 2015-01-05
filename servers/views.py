from django.shortcuts import render, get_object_or_404
from servers.models import Server, ServerCheck
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.template.loader import render_to_string
from django.template.defaultfilters import filesizeformat
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
                        response_data["spec-bandwidth"] = filesizeformat(new_bandwidth)
                    else:
                        response_data = {"success": False}
                elif request.POST["attribute"] == 'spec-ram':
                    new_ram = server.solusapi.update_ram()
                    if new_ram:
                        response_data["spec-ram"] = filesizeformat(new_ram)
                    else:
                        response_data = {"success": False}
                elif request.POST["attribute"] == 'spec-hdd':
                    new_hdd = server.solusapi.update_hdd()
                    if new_hdd:
                        response_data["spec-hdd"] = filesizeformat(new_hdd)
                    else:
                        response_data = {"success": False}
                else:
                    response_data = {"success": False}
        else:
            response_data = {"success": False}
    else:
        response_data = {"success": False}

    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required()
def get_solus_data(request):
    response_data = {
        "success": True,
    }
    if request.method == "POST":
        if request.is_ajax():
            server = get_object_or_404(Server, pk=request.POST["server"])
            if server.solusapi is None:
                response_data = {"success": False}
            else:
                api = server.solusapi.get_raw_api()
                if api.get_all(output_bw=api.BYTES, output_mem=api.BYTES, output_hdd=api.BYTES):
                    response_data['bw'] = api.bw
                    response_data['mem'] = api.ram
                    response_data['hdd'] = api.hdd
                    response_data['html'] = render_to_string('servers/solus_response.html', {
                        "bandwidth": api.bw,
                        "memory": api.ram,
                        "hdd": api.hdd
                    })
                else:
                    response_data = {"success": False}
        else:
            response_data = {"success": False}
    else:
        response_data = {"success": False}

    return HttpResponse(json.dumps(response_data), content_type="application/json")


def update_ips(request):
    response_data = {
        "success": True,
    }
    if request.method == "POST":
        if request.is_ajax():
            server = get_object_or_404(Server, pk=request.POST["server"])
            if server.solusapi is None:
                response_data = {"success": False}
            else:
                updated = server.solusapi.update_ip_list()
                if updated:
                    response_data['ips'] = render_to_string('servers/server_extra_ip.html', {
                        "server": server,
                    })
                else:
                    response_data = {"success": False}
        else:
            response_data = {"success": False}
    else:
        response_data = {"success": False}

    return HttpResponse(json.dumps(response_data), content_type="application/json")


def get_responder_data(request):
    response_data = {
        "success": True,
    }
    if request.method == "POST":
        if request.is_ajax():
            server = get_object_or_404(Server, pk=request.POST["server"])
            if server.responderapi is None:
                response_data = {"success": False}
            else:
                api = server.responderapi.get_responder_data()
                if api.success:
                    response_data['html'] = render_to_string('servers/responder_response.html', {
                        "data": api.response,
                    })
                else:
                    response_data = {"success": False}
        else:
            response_data = {"success": False}
    else:
        response_data = {"success": False}

    return HttpResponse(json.dumps(response_data), content_type="application/json")
