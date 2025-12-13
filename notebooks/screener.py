import yfinance as yf
from pprint import pprint as print

from crawlers.sec.edgar import Edgar
from market.screeners import *

spy = yf.Ticker("SPY").info['trailingPE']
baseline = spy * .8

res = []
dlq = []
total = len(list(Edgar.get_all_tickers()))
processed = 0
for ticker in Edgar.get_all_tickers():
    stock = yf.Ticker(ticker)
    processed += 1
    if processed % 25 == 0:
        print(f'{processed} / {total}')
    try:
        if is_low_pe(stock, baseline) and is_crypto_related(stock) and is_positive_recommendation(stock):
            res.append(stock)
            print(res)
    except MissingData as e:
        dlq.append(ticker)
        if len(dlq) % 100 == 0:
            print(f'DLQ: {dlq}')
    except Exception as e:
        print(e)
        print(ticker)
print(len(dlq), dlq)
print('RESULTS: ')
print(res)

# https://github.com/dgunning/edgartools