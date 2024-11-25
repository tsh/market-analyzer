import requests

import config


# TODO: 250 calls / day https://intelligence.financialmodelingprep.com/developer/docs#etf-holdings-etf-holdings

class AlphaVantage:
    # 25 per day
    def __init__(self):
        self.key = config.ALPHA_VANTAGE_KEY
        # url = f'https://www.alphavantage.co/query?function=HISTORICAL_OPTIONS&symbol=IBM&apikey={config.ALPHA_VANTAGE_KEY}'
        # r = requests.get(url)
        # print(r.json())

    def rsi(self, symbol, interval='weekly', time_period=30):
        url = f'https://www.alphavantage.co/query?function=RSI&symbol={symbol}&interval={interval}&time_period={time_period}&series_type=open&apikey={self.key}'
        r = requests.get(url)
        print(r.json())


# Seeking alpha
class SeekingAlpha:
    """
    Via rapidapi
    rate 5 / second
    limit 500 / month
    """
    def __init__(self):
        self.headers = {
            "x-rapidapi-key": config.SEEKING_ALPHA_KEY,
            "x-rapidapi-host": "seeking-alpha.p.rapidapi.com"
        }

    def get_articles(self, since: float) -> dict:
        url = "https://seeking-alpha.p.rapidapi.com/articles/v2/list"
        querystring = {"since": "1636693199", "size": "40", "number": "1", "category": "latest-articles"}
        response = requests.get(url, headers=self.headers, params=querystring)
        response.raise_for_status()
        return response.json()


class PolygonIO:
    # USELESS for options
    # https://polygon.io/blog/how-to-read-a-stock-options-ticker
    def __init__(self):
        r = requests.get(f'https://api.polygon.io/v3/reference/options/contracts/O:SPY251219C00650000?apiKey={config.POLYGON_IO_KEY}')
        print(r.json())
