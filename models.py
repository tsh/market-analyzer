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


class YahooProvider:
    def __init__(self):
        amzn = yf.Ticker("GOOG")
        # GET TODAYS DATE AND CONVERT IT TO A STRING WITH YYYY-MM-DD FORMAT (YFINANCE EXPECTS THAT FORMAT)
        # end_date = datetime.now().strftime('%Y-%m-%d')
        # amzn_hist = amzn.history(start='2022-01-01',end=end_date)
        print(amzn.recommendations)

class Stock:
    def __init__(self, name: str):
        self.name = name
        self.ticker = yf.Ticker(self.name)
        self.cache_file_path = os.path.join(DATA_DIR, self.name)

    def history(self):
        if os.path.exists(self.cache_file_path):
            df = pd.read_csv(self.cache_file_path)
        else:
            df = self.ticker.history(period='max')
            df.to_csv(self.cache_file_path)
        df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
        return df

    def ask(self):
        return self.ticker.get_info()['ask']

    def bid(self):
        return self.ticker.get_info()['bid']

    def expected_return(self, future, current):
        return (future - current) / current

    def __str__(self):
        return 'stock: {}'.format(self.name)


class Portfolio:
    pass

