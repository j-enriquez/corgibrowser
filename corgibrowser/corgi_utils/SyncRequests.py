import requests

class SyncRequests:
    def get_response(self, url):
        """Synchronous method to get a response using requests."""
        response = requests.get(url, timeout=5)
        return response.text, response.status_code