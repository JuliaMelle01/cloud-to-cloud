import requests

class RESTConnection:
    """
        ...
    """

    def __init__(self, user, password):
        self.api_url = "http://localhost:3000/lua/rest/v2/get/interface/data.lua?ifid=4"
        self.user = user
        self.password = password

    #"curl -s -u admin:admin_julia

    def get_data(self):
        response = requests.get(self.api_url, auth=requests.auth.HTTPBasicAuth(self.user, self.password)).json()
        if response["rc"]:
            raise UnboundLocalError()
        response = self.extract_parameters(response["rsp"])
        return response

    def extract_parameters(self, json):
        bytes = json["bytes"]
        ifid = json["ifid"]
        bytes_upload = json["bytes_upload"]
        bytes_download = json["bytes_download"]
        localtime = json["localtime"]
        return bytes


class TrafficCapture:

    def __init__(self):
        self.data = 0

    def update_data(self, bytes):
        self.data += bytes