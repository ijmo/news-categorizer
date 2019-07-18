import requests


class RequestsHTTPClient:

    def __init__(self):
        self.session = requests.Session()

    def get(self, url):
        return self.session.get(url).text
