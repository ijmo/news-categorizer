import requests


class RequestsHTTPClient:

    @staticmethod
    def html_getter():
        session = requests.Session()

        def http_get(url):
            return session.get(url).text
        return http_get
