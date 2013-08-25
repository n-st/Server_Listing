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

    def __init__(self, url, api_key, api_hash):
        self.api_key = api_key
        self.api_hash = api_hash

        if not url.endswith('/'):
            url += '/'
        url += 'api/client/command.php'

        self.api_url = url

    def perform_request(self, **kwargs):
        request_data = urllib.urlencode({
            "key": self.api_key,
            "hash": self.api_hash,
            "action": "info",
        }.update(kwargs))
        request = urllib2.Request(self.api_url, request_data)
        request.add_header('User-agent', 'Mozilla/5.0')
        response = urllib2.urlopen(request)
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
        return False
