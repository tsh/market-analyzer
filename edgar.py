import requests
import pandas as pd


class CIK:
    """https://sec.report/Ticker/AAPL"""
    pass


class CIK2Report:
    """
    https://www.sec.gov/edgar/sec-api-documentation
    https://data.sec.gov/submissions/CIK0000320193.json
    """
    pass

class Agent:
    """User-Agent: Sample Company Name AdminContact@<sample company domain>.com
    Accept-Encoding: gzip, deflate"""


headers = {'User-Agent': 'Market-Analyzer', 'Accept': 'application/json'}

class Recent:
    """
    Latest:
    https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&datea=&dateb=&company=&type=4&SIC=&State=&Country=&CIK=&owner=include&accno=&start=0&count=100
    or via RSS: https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&CIK=&type=&company=&dateb=&owner=include&start=0&count=40&output=atom
    """
    report = 4
    url = 'https://www.sec.gov/cgi-bin/browse-edgar'
    params ='action=getcurrent&datea=&dateb=&company=&type=4&SIC=&State=&Country=&CIK=&owner=include&accno=&start=0&count=100'
    r = requests.get(url, params=params, headers=headers)

class Daily:
    def __init__(self):
        url = 'https://www.sec.gov/Archives/edgar/daily-index/2022/QTR3/'


if __name__ == '__main__':
    t = pd.Timestamp(2022, 8, 11)
    print(t, t.quarter)
