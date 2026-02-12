import os
import json

import yfinance as yf
from utils.specification import AbstractSpecification
from config import YAHOO_CACHE_TICKERS

class MissingData(KeyError):
    pass


class IsPositiveReccommendation(AbstractSpecification):
    def is_satisfied_by(self, stock: yf.Ticker):
        df = stock.get_recommendations_summary()
        r = df.iloc[0]
        sbuy, buy, hold, sell, ssel = r['strongBuy'], r['buy'], r['hold'], r['sell'], r['strongSell']
        return (sbuy + buy) > (hold + sell + ssel)


class IsCryptoRelated(AbstractSpecification):
    def is_satisfied_by(self, stock: yf.Ticker):
        return 'crypto' in stock.info['longBusinessSummary']


class IsLowPE(AbstractSpecification):
    def __init__(self, base_pe):
        self.base_pe = base_pe

    def is_satisfied_by(self, stock_pe: float):
            return stock_pe <= self.base_pe

class TickerCachedProxy:
    CACHE_DIR = YAHOO_CACHE_TICKERS
    CACHED_TICKERS = set(os.listdir(CACHE_DIR))

    def __init__(self, ticker: str):
        self._yf_ticker = yf.Ticker(ticker)

    @property
    def info(self):
        if self._yf_ticker.ticker in self.CACHED_TICKERS:
            return json.load(os.path.join(self.CACHE_DIR, self._yf_ticker.ticker))
        else:
            d = self._yf_ticker.info
            with open(os.path.join(self.CACHE_DIR, self._yf_ticker.ticker) + '.json', 'w') as f:
                json.dump(d, f)
            return d

    def trailing_pe(self) -> float:
        try:
            tpe = self.info['trailingPE']
        except KeyError as e:
            raise MissingData(e)
        return tpe

    def trailing_eps_twelve_months(self) -> float:
        try:
            tpe = self.info['epsTrailingTwelveMonths']
        except KeyError as e:
            raise MissingData(e)
        return tpe

if __name__ == '__main__':
    stock = TickerCachedProxy('MSFT')
    print(stock.trailing_pe())