import requests
from requests.exceptions import HTTPError, ConnectionError


def bytes_to_megs(value):
    return float(value) / 1048576.0


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

    def process_mem(self):
        keys = [key for key in self.response["mem"]]
        for key in keys:
            self.response["mem"][key + "_meg"] = bytes_to_megs(self.response["mem"][key])

    def process_hdd(self):
        keys = [key for key in self.response["disk"]]
        for key in keys:
            self.response["disk"][key + "_meg"] = bytes_to_megs(self.response["disk"][key])

    def send_request(self):
        try:
            request = requests.get(self.url, params=self.params)
            request.raise_for_status()
        except (HTTPError, ConnectionError):
            self.success = False
            self.error = "Could not communicate with the server"
            return self
        self.response = request.json()

        self.process_mem()
        self.process_hdd()

        return self
