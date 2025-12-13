import yfinance as yf

class MissingData(KeyError):
    pass

def is_crypto_related(stock: yf.Ticker) -> bool:
    return 'crypto' in stock.info['longBusinessSummary']

def is_low_pe(stock: yf.Ticker, base_pe: float) -> bool:
        try:
            tpe = stock.info['trailingPE']
        except KeyError as e:
            raise MissingData(e)
        return tpe <= base_pe

def is_positive_recommendation(stock: yf.Ticker) -> bool:
    df = stock.get_recommendations_summary()
    r = df.iloc[0]
    sbuy, buy, hold, sell, ssel = r['strongBuy'], r['buy'], r['hold'], r['sell'], r['strongSell']
    return (sbuy + buy) > (hold + sell + ssel)

def quarter_per(stock: yf.Ticker) -> float:
    last_year = stock.info['trailingPE'] # trailing 12 month
    df = stock.history()
    cur_market_price = df['Close'].iloc[-1]
    last_quarter = '2025-09-30'
    diluted_eps = stock.quarterly_financials.T['Diluted EPS'].dropna()[last_quarter]
    pe_ratio = cur_market_price / diluted_eps  # to large comparing to trailing from yf
    return pe_ratio
