import yfinance as yf
from utils.specification import AbstractSpecification

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

# def pe_yahoo(stock: yf.Ticker) -> float:
#     try:
#         tpe = stock.info['trailingPE']
#     except KeyError as e:
#         raise MissingData(e)
#     return tpe
#
# def eps_yahoo(stock: yf.Ticker) -> float:
#     try:
#         tpe = stock.info['epsTrailingTwelveMonths']
#     except KeyError as e:
#         raise MissingData(e)
#     return tpe
#
#
# def quarter_per(stock: yf.Ticker) -> float:
#     last_year = stock.info['trailingPE'] # trailing 12 month
#     df = stock.history()
#     cur_market_price = df['Close'].iloc[-1]
#     last_quarter = '2025-09-30'
#     diluted_eps = stock.quarterly_financials.T['Diluted EPS'].dropna()[last_quarter]
#     pe_ratio = cur_market_price / diluted_eps  # to large comparing to trailing from yf
#     return pe_ratio
#
#
# def edgar_diluted_eps(ticker):
#     from edgar import Company, set_identity
#     set_identity("your.email@exa9mple.com")
#     company = Company(ticker)
#     latest_10k = company.get_filings(form="10-K").latest()
#     filling_year = latest_10k.to_dict()['filing_date'].year
#     financials = latest_10k.obj().financials
#     df = financials.get_income_statement().to_dataframe()
#     diluted_eps = float(df.loc['Diluted'][str(filling_year)].iloc[0])
#     return diluted_eps
#
# def edgar_diluted_pe(stock: yf.Ticker):
#     current_price = stock.history(period="1d")['Close'].iloc[-1]
#     eps = edgar_diluted_eps(stock.ticker)
#     pe = current_price / eps
#     return pe

if __name__ == '__main__':
    stock = yf.Ticker('MSFT')
    import ipdb;ipdb.set_trace()