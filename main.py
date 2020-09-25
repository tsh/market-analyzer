import os

import pandas as pd
import yfinance as yf
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.dates import datestr2num


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
        df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
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

if __name__ == '__main__':
    qqq = StockRepository('QQQ')
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.plot(qqq.history()['Date'], qqq.history()['Close'])
    plt.show()
