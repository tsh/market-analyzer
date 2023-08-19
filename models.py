from datetime import datetime
import os

import pandas as pd
import yfinance as yf
import requests

from config import DATA_DIR


class IBKRProvider:
    def __init__(self):
        resp = requests.get('https://localhost:5000/v1/api/portfolio/accounts/', verify=False)
        acc = resp.json()
        acc_id = acc[0]['accountId']
        positions = requests.get('https://localhost:5000/v1/api/portfolio/{accountId}/positions/{pageId}'.format(accountId=acc_id, pageId=0), verify=False)
        print(positions.json())

