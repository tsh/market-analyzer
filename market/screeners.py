import yfinance as yf
from crawlers.sec.edgar import Edgar
from pprint import pprint as print



def is_low_pe(stock: yf.Ticker, base_pe: float) -> bool:
        tpe = stock.info['trailingPE']
        return tpe <= base_pe

def is_crypto(stock: yf.Ticker) -> bool:
    return 'crypto' in stock.info['longBusinessSummary']

def is_positive_recommendation(stock: yf.Ticker) -> bool:
    df = stock.get_recommendations_summary()
    r = df.iloc[0]
    sbuy, buy, hold, sell, ssel = r['strongBuy'], r['buy'], r['hold'], r['sell'], r['strongSell']
    return (sbuy + buy) > (hold + sell + ssel)


msft = yf.Ticker('MSFT')
print(is_positive_recommendation(msft))

# spy = yf.Ticker("SPY").info['trailingPE']
# baseline = spy * .8
#
# for ticker in Edgar.get_all_tickers():
#     stock = yf.Ticker(ticker)
#     if is_low_pe(stock, baseline):
#         print(stock)
#         print(stock.info)
#         break
