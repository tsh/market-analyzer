import yfinance as yf

class MissingData(KeyError):
    pass

def is_crypto_related(stock: yf.Ticker) -> bool:
    return 'crypto' in stock.info['longBusinessSummary']

def is_low_pe(stock_pe: float, base_pe: float) -> bool:
        return stock_pe <= base_pe

def pe_yahoo(stock: yf.Ticker) -> float:
    try:
        tpe = stock.info['trailingPE']
    except KeyError as e:
        raise MissingData(e)
    return tpe

def eps_yahoo(stock: yf.Ticker) -> float:
    try:
        tpe = stock.info['epsTrailingTwelveMonths']
    except KeyError as e:
        raise MissingData(e)
    return tpe

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


def edgar_diluted_eps(ticker):
    from edgar import Company, set_identity
    set_identity("your.email@exa9mple.com")
    company = Company(ticker)
    latest_10k = company.get_filings(form="10-K").latest()
    filling_year = latest_10k.to_dict()['filing_date'].year
    financials = latest_10k.obj().financials
    df = financials.get_income_statement().to_dataframe()
    diluted_eps = float(df.loc['Diluted'][str(filling_year)].iloc[0])
    return diluted_eps

def edgar_diluted_pe(stock: yf.Ticker):
    current_price = stock.history(period="1d")['Close'].iloc[-1]
    eps = edgar_diluted_eps(stock.ticker)
    pe = current_price / eps
    return pe

