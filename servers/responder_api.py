import requests
from requests.exceptions import HTTPError


class ResponderAPI():
    url = ""
    key = ""
    params = {}

    success = True
    error = ""
    response = {}

    def __init__(self, key, url, port):
        self.url = url
        self.port = port
        self.key = key

        self.params = {
            "auth_key": self.key,
        }

    def send_request(self):
        request = requests.get(self.url, params=self.params, port=self.port)

        try:
            request.raise_for_status()
        except HTTPError as e:
            self.success = False
            self.error = "Could not communicate with the server"
            print e
            return self

        self.response = request.json()
        return self
