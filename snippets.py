from datetime import datetime
import os

import pandas as pd
import yfinance as yf
import requests

import requests
from bs4 import BeautifulSoup


class Provider():
    URL = 'https://www.reddit.com/r/worldnews'

    def top_headers(self, amount=25):
        resp = requests.get(self.URL)
        resp.raise_for_status()
        return resp.text

class IBKRProvider:
    def __init__(self):
        resp = requests.get('https://localhost:5000/v1/api/portfolio/accounts/', verify=False)
        acc = resp.json()
        acc_id = acc[0]['accountId']
        positions = requests.get('https://localhost:5000/v1/api/portfolio/{accountId}/positions/{pageId}'.format(accountId=acc_id, pageId=0), verify=False)
        print(positions.json())





import matplotlib.pyplot as plt
class GUI():
    def display(self, stock):
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.plot(stock.history()['Date'], stock.history()['Close'])
        plt.show()



