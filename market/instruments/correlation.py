
import os

import yfinance as yf

import config


class DownloadTickerData:
    @classmethod
    def download(cls, ticker):
        df = yf.download(
        tickers = [ticker],
        period = "50y",
        interval = "1d"
        )
        min_date = df.index[0].strftime('%Y-%m-%d')
        max_date = df.index[-1].strftime('%Y-%m-%d')
        filename = f'{ticker}_{min_date}_{max_date}_OHLC.parquet'
        path = os.path.join(config.INSTRUMENT_DATA_DIR, filename)
        df.to_parquet(path, compression='zstd')

# df['Close'].dropna().corr()