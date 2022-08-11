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
    or archive https://www.sec.gov/Archives/edgar/Feed/2022/QTR3/
    """
    report = 4
    url = 'https://www.sec.gov/cgi-bin/browse-edgar'
    params ='action=getcurrent&datea=&dateb=&company=&type=4&SIC=&State=&Country=&CIK=&owner=include&accno=&start=0&count=100'
    r = requests.get(url, params=params, headers=headers)

class DailyArchive:
    @staticmethod
    def date_to_url(year, month, date):
        quarter = pd.Timestamp(year, month, date).quarter
        return f'https://www.sec.gov/Archives/edgar/daily-index/{year}/QTR{quarter}'

    @classmethod
    def get_url_forms_per_day(cls, year, month, date):
        url = cls.date_to_url(year, month, date)
        t = pd.Timestamp(year, month, date)
        filename = 'form.'+t.strftime('%Y%m%d')
        return url + '/' + filename + '.idx'

    def get_report_per_day(self, year, month, date):
        url = Daily.get_url_forms_per_day(year, month, date)
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.content
        return data

if __name__ == '__main__':
    d = Daily().get_report_per_day(2022, 8, 9)
    print(d)
