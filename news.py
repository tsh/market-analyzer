import requests
from bs4 import BeautifulSoup


class Provider():
    URL = 'https://www.reddit.com/r/worldnews'

    def top_headers(self, amount=25):
        resp = requests.get(self.URL)
        resp.raise_for_status()
        return resp.text

