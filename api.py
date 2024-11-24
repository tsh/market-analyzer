import requests

import config


# TODO: 250 calls / day https://intelligence.financialmodelingprep.com/developer/docs#etf-holdings-etf-holdings

class AlphaVantage:
    # 25 per day
    def __int__(self):
        url = f'https://www.alphavantage.co/query?function=HISTORICAL_OPTIONS&symbol=IBM&apikey={config.ALPHA_VANTAGE_KEY}'
        r = requests.get(url)
        print(r.json())


# Seeking alpha
class SeekingAlpha:
    def __int__(self):
        url = "https://seeking-alpha.p.rapidapi.com/articles/v2/list"
        querystring = {"category": "stock-ideas::quick-picks"}
        headers = {
            "x-rapidapi-key": config.SEEKING_ALPHA_KEY,
            "x-rapidapi-host": "seeking-alpha.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers, params=querystring)
        print(response.json())


class PolygonIO:
    # USELESS for options
    # https://polygon.io/blog/how-to-read-a-stock-options-ticker
    def __int__(self):
        r = requests.get(f'https://api.polygon.io/v3/reference/options/contracts/O:SPY251219C00650000?apiKey={config.POLYGON_IO_KEY}')
        print(r.json())
