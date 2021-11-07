import os

import pandas as pd
import yfinance as yf

from config import DATA_DIR


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

