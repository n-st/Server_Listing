import requests
from requests.exceptions import HTTPError, ConnectionError


class ResponderAPI():
    url = ""
    key = ""
    params = {}

    success = True
    error = ""
    response = {}

    def __init__(self, key, url, port):
        self.url = "http://{0}:{1}".format(url, str(port))
        self.port = port
        self.key = key

        self.params = {
            "auth_key": self.key,
        }

    def send_request(self):
        try:
            request = requests.get(self.url, params=self.params)
            request.raise_for_status()
        except (HTTPError, ConnectionError):
            self.success = False
            self.error = "Could not communicate with the server"
            return self
        self.response = request.json()
        return self
