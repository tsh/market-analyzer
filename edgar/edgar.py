from enum import Enum

import requests
import pandas as pd
import xml.etree.ElementTree as ET


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

class RecentSubmissionParser:
    """
    Latest:
    https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&datea=&dateb=&company=&type=4&SIC=&State=&Country=&CIK=&owner=include&accno=&start=0&count=100
    or archive https://www.sec.gov/Archives/edgar/Feed/2022/QTR3/
    RSS: updated every ten minutes Monday through Friday, 6am – 10pm EST
    """
    def __init__(self, atom_data):
        self.raw_data = atom_data
        self.data = feedparser.parse(self.raw_data)


class RecentSubmissions:
    @classmethod
    def get_recent(cls):
        url = 'https://www.sec.gov/cgi-bin/browse-edgar'
        params = {
            'action': 'getcurrent',
            'type': 4,
            'owner': 'include',
            'start': 0,
            'count': 10,
            'output': 'atom'
        }
        r = requests.get(url, params=params, headers=headers)
        r.raise_for_status()
        import feedparser
        feed = feedparser.parse(r.content)


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
    params = {
        'action': 'getcurrent',
        'type': 4,
        'owner': 'include',
        'start': 0,
        'count': 10,
        'output': 'atom'
    }
    r = requests.get(url, params=params, headers=headers)
    r.raise_for_status()
    # parse
    import feedparser
    feed = feedparser.parse(r.content)
    submission = {}
    for s in feed.entries:
        submission['link'] = s.link
        submission['title'] = s.title
        break
    # submission page
    r = requests.get(submission['link'], headers=headers)
    r.raise_for_status()
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(r.content, 'html')
    report_links = []
    for a in soup.find_all('a'):
        link = a.get('href')
        if link.startswith('/Archives') and link.endswith('.xml') and a.text.endswith('.xml'):
            report_links.append(link)
    # get report
    for report_link in report_links:
        r = requests.get('https://www.sec.gov' + report_link, headers=headers)
        r.raise_for_status()

    f4 = Form4(r.content)
    print(r.content)
    print(f4.reporting_owner_relationship())
