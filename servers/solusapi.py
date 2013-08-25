from xmltodict import parse
import urllib
import urllib2


class SolusAPI(object):

    api_key = ''
    api_hash = ''
    api_url = ''

    document = None
    success = False
    error = None

    GIGABYTES = 1073741824.0
    MEGABYTES = 1048576.0

    def __init__(self, url, api_key, api_hash):
        self.api_key = api_key
        self.api_hash = api_hash

        if not url.endswith('/'):
            url += '/'
        url += 'api/client/command.php'

        self.api_url = url

    def perform_request(self, **kwargs):

        params = dict(
            {
                "key": self.api_key,
                "hash": self.api_hash,
                "action": "info",
            }.items() + kwargs.items()
        )
        request_data = urllib.urlencode(params)
        request = urllib2.Request(self.api_url, request_data)
        request.add_header('User-agent', 'Mozilla/5.0')

        try:
            response = urllib2.urlopen(request)
        except urllib2.URLError:
            self.error = "Incorrect URL"
            self.success = False
            return False
        response_data = response.read()

        document = parse("<doc>" + response_data + "</doc>")

        document = document["doc"]
        self.document = None
        self.success = False

        if "status" in document:
            if document["status"] == "success":
                self.success = True
                self.document = document
                return True
            else:
                self.error = document["statusmsg"]
        else:
            self.error = 'Incorrect data format'
        return False

    def get_ips(self):
        if self.perform_request(ipaddr='true'):
            return self.document["ipaddr"].split(',')
        else:
            return False

    def get_status(self):
        if self.perform_request(action='status'):
            if self.document["vmstat"] == "online":
                return "online"
            return "offline"
        else:
            return False

    def get_hostname(self):
        if self.perform_request():
            return self.document["hostname"]
        return False

    def get_main_ip(self):
        if self.perform_request():
            return self.document["ipaddress"]
        return False

    def get_hdd(self, output_format=GIGABYTES):
        if self.perform_request(hdd='true'):
            hdd = self.document["hdd"]
            total, used, free, percent_used = hdd.split(',')

            total = float(total) / output_format
            used = float(used) / output_format
            free = float(free) / output_format

            return {
                "total": total,
                "used": used,
                "free": free,
                "percent": float(percent_used)
            }
        return False

    def get_memory(self, output_format=MEGABYTES):
        if self.perform_request(mem='true'):
            hdd = self.document["mem"]
            total, used, free, percent_used = hdd.split(',')

            total = float(total) / output_format
            used = float(used) / output_format
            free = float(free) / output_format

            return {
                "total": total,
                "used": used,
                "free": free,
                "percent": float(percent_used)
            }
        return False

    def get_bandwidth(self, output_format=GIGABYTES):
        if self.perform_request(bw='true'):
            hdd = self.document["bw"]
            total, used, free, percent_used = hdd.split(',')

            total = float(total) / output_format
            used = float(used) / output_format
            free = float(free) / output_format

            return {
                "total": total,
                "used": used,
                "free": free,
                "percent": float(percent_used)
            }
        return False
