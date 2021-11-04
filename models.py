import os

import pandas as pd
import yfinance as yf

from config import DATA_DIR


class Calculator:
    def expected_return(self, future, current):
        return (future - current) / current


class Stock:
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
        df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
        return df

    def info(self):
        return self.ticker.info

    @property
    def quote_type(self):
        return self.raw_info['quoteType']

    def __str__(self):
        return 'stock: {}'.format(self.name)

