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
        if url.endswith('/'):
            url = url[:-1]
        self.url = url + str(port)
        self.key = key

        self.params = {
            "auth_key": self.key,
        }

    def get(self):
        request = requests.get(self.url, params=self.params)

        try:
            request.raise_for_status()
        except HTTPError:
            self.success = False
            self.error = "Could not communicate with the server"
            return self

        self.response = request.json()
