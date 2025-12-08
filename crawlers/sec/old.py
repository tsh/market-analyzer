import datetime as dt
from enum import Enum
import os

import requests
import pandas as pd
# import feedparser
import gzip
import json
import shutil
import xml.etree.ElementTree as ET

import config


# RUN AS <from root dir> python3 -m path.to.this.file (dots)


class CIK:
    pass


class CikTicker:
    def __init__(self):
        self.CIK_TICKER_URL = 'https://www.sec.gov/files/company_tickers_exchange.json'
        self.CIK_TICKER_MAP_FILENAME = 'map_cik_ticker.json'
        self.CIK_TICKER_PATH = os.path.join(config.SEC_EDGAR_DATA_DIR, self.CIK_TICKER_MAP_FILENAME)
        self.CIK_IDX = 0
        self.NAME_IDX = 1
        self.TICKER_IDX = 2
        self.EXCHANGE_IDX = 3
        self.MUTUAL_FUNDS_URL = 'https://www.sec.gov/files/company_tickers_mf.json'
        self.MUTUAL_FUNDS_FILE_NAME = 'map_cik_mf.json'
        self.MUTUAL_FUNDS_PATH = os.path.join(config.SEC_EDGAR_DATA_DIR, self.MUTUAL_FUNDS_FILE_NAME)
        self.SERIES_ID_IDX = 1
        self.CLASS_ID_IDX = 2
        self.SYMBOL_IDX = 3

    def all_symbols_mutual_funds(self):
        """incl etfs"""
        return self._parse_file(self.MUTUAL_FUNDS_PATH, self.SYMBOL_IDX)

    def all_tickers_companies(self):
        return self._parse_file(self.CIK_TICKER_PATH, self.TICKER_IDX)

    def all_tickers(self):
        mf_symbols = self.all_symbols_mutual_funds()
        stock_tickers = self.all_tickers_companies()
        return mf_symbols + stock_tickers

    def _parse_file(self, fpath, field_index):
        with open(fpath, 'rt') as f:
            parsed = json.load(f)
        res = []
        for d in parsed['data']:
            res.append(d[field_index])
        return res

    def _download_cik_mapping(self):
        self._download(self.CIK_TICKER_URL, self.CIK_TICKER_PATH)

    def _download_mutual_funds_mapping(self):
        self._download(self.MUTUAL_FUNDS_URL, self.MUTUAL_FUNDS_PATH)

    def _download(self, frm: str, to_path: str):
        # TODO: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/If-Modified-Since
        headers = {'User-Agent': 'Market@private.com',
                   'Accept': 'application/json',
                   "Accept-Encoding": "gzip, deflate",
                   }
        with (requests.get(frm, headers=headers) as src, open(to_path, 'wt') as dst):
            src.raise_for_status()
            data = json.loads(src.content)
            json.dump(data, dst, indent=2)


class CIK2Report:
    """
    https://www.sec.gov/edgar/sec-api-documentation
    https://data.sec.gov/submissions/CIK0000320193.json
    """
    pass

class Agent:
    """User-Agent: Sample Company Name AdminContact@<sample company domain>.com
    Accept-Encoding: gzip, deflate"""


class RecentSubmissionAtomParser:
    def __init__(self, atom_data):
        self.raw_data = atom_data
        self.data = feedparser.parse(self.raw_data)

    @property
    def time(self):
        return datetime.fromisoformat(self.data.feed.updated)

    @property
    def entries(self) -> []:
        entries = []
        for entree in self.data.entries:
            entries.append({
                'title': entree['title']
            })
        return entries


class BucketRateLimiter:
    pass


class RecentSubmissionsAtom:
    """
    Latest:
    https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&datea=&dateb=&company=&type=4&SIC=&State=&Country=&CIK=&owner=include&accno=&start=0&count=100
    or archive https://www.sec.gov/Archives/edgar/Feed/2022/QTR3/
    RSS: updated every ten minutes Monday through Friday, 6am – 10pm EST
    """
    def __init__(self):
        self.headers = {'User-Agent': 'Market-Analyzer', 'Accept': 'application/json'}

    def parsers(self) -> [RecentSubmissionAtomParser]:
        url = 'https://www.sec.gov/cgi-bin/browse-edgar'
        start = 0
        count = 100
        while True:
            params = {
                'action': 'getcurrent',
                'type': 4,
                'owner': 'include',
                'start': start,
                'count': count,
                'output': 'atom'
            }
            r = requests.get(url, params=params, headers=self.headers)
            if r.ok:
                parser = RecentSubmissionAtomParser(r.content)
                yield parser
                start += count
            elif r.status_code == 503:
                print('No new record found for the date')
                break
            else:
                r.raise_for_status()


    def get_instruments(self) -> list:
        instruments = []
        for parser in self.parsers():
            for entree in parser.entries:
                instrument = entree['title'].lower()           
                instruments.append(instruments)
        return instruments


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


class Relationship(Enum):
    DIRECTOR = 'director'
    OFFICER = 'officer'
    TEN_PERCENT_OWNER = 'ten_percent_owner'
    OTHER = 'other'

class ParsingError(ValueError):
    pass

class Form4:
    def __init__(self, xml_data):
        from bs4 import BeautifulSoup
        self.soup = BeautifulSoup(xml_data, features='xml')

    def reporting_owner_relationship(self) -> Relationship:
        relationship = self.soup.find('reportingOwnerRelationship')
        for tag, rel in zip(['isDirector', 'isOfficer', 'isTenPercentOwner', 'isOther'],
                            [Relationship.DIRECTOR, Relationship.OFFICER, Relationship.TEN_PERCENT_OWNER, Relationship.OTHER]):
            if relationship.find(tag).get_text() == '1':
                return rel
        else:
            raise ParsingError('Relationship for the form can not be determined')


if __name__ == '__main__':
    url = 'https://www.sec.gov/cgi-bin/browse-edgar'
    # params = {
    #     'action': 'getcurrent',
    #     'type': 4,
    #     'owner': 'include',
    #     'start': 0,
    #     'count': 10,
    #     'output': 'atom'
    # }
    # r = requests.get(url, params=params, headers=headers)
    # r.raise_for_status()
    # # parse
    # import feedparser
    # feed = feedparser.parse(r.content)
    # submission = {}
    # for s in feed.entries:
    #     submission['link'] = s.link
    #     submission['title'] = s.title
    #     break
    # # submission page
    # r = requests.get(submission['link'], headers=headers)
    # r.raise_for_status()
    # from bs4 import BeautifulSoup
    # soup = BeautifulSoup(r.content, 'html')
    # report_links = []
    # for a in soup.find_all('a'):
    #     link = a.get('href')
    #     if link.startswith('/Archives') and link.endswith('.xml') and a.text.endswith('.xml'):
    #         report_links.append(link)
    # # get report
    # for report_link in report_links:
    #     r = requests.get('https://www.sec.gov' + report_link, headers=headers)
    #     r.raise_for_status()
    #
    # f4 = Form4(r.content)
    # print(r.content)
    # print(f4.reporting_owner_relationship())
