import os

import pandas as pd
import yfinance as yf

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')


class StockRepository:
    def __init__(self, name: str):
        self.name = name
        self.ticker = yf.Ticker(self.name)
        self.cache_file_path = os.path.join(DATA_DIR, self.name)
        self.raw_info = self.info()

    def history(self):
        if os.path.exists(self.cache_file_path):
            df = pd.read_csv(self.cache_file_path)
        else:
            df = self.ticker.history(period='max')
            df.to_csv(self.cache_file_path)
        return df

    def info(self):
        return self.ticker.info

    @property
    def quote_type(self):
        return self.raw_info['quoteType']

    def __str__(self):
        return 'stock: {}'.format(self.name)


class Calculator:
    def expected_return(self, future, current):
        return (future - current) / current

qqq = StockRepository('QQQ')
print(qqq.quote_type)
