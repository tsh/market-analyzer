import requests


class Edgar:
    @staticmethod
    def get_all_tickers():
        url = 'https://www.sec.gov/files/company_tickers.json'
        resp = requests.get(url, headers = {'User-Agent': 'Market@private.com',
                                       'Accept': 'application/json',
                                       "Accept-Encoding": "gzip, deflate",
                                       })
        resp.raise_for_status()
        data = resp.json()
        for record in data.values():
            yield record['ticker']
