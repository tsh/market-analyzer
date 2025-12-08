import yfinance as yf
from crawlers.sec.edgar import Edgar
from pprint import pprint as print

def low_pe():
    spy = yf.Ticker("SPY").info['trailingPE']
    baseline = spy * .8

    res = {}
    for ticker in Edgar.get_all_tickers():
        stock = yf.Ticker(ticker)
        tpe = stock.info['trailingPE']
        if tpe <= baseline:
            res[ticker] = tpe
            print(f'{ticker}: {tpe}')
    print(res)

low_pe()