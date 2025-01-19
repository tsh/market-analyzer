import sys
from datetime import datetime
from pathlib import Path

from bs4 import BeautifulSoup, SoupStrainer
import dateutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

file = Path(__file__).resolve()
project_dir = file.parents[2]
sys.path.append(str(project_dir))

import config as cfg

URL_VIC = 'http://valueinvestorsclub.com'




class Driver:
    def __init__(self):
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1200")
        # service = Service()
        # service.executable_path = '/lib/chromedriver'
        self.driver = webdriver.Chrome(options=options)

    def get(self, url, wait_selector: tuple=None, wait_timeout=6) -> str:
        self.driver.get(url)
        if wait_selector:
            WebDriverWait(self.driver, wait_timeout).until(lambda drver: drver.find_element(*wait_selector).is_displayed())
        return self.driver.page_source

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()


class Parser:
    def __init__(self, page_content: str):
        self.page_content = page_content
        self.soup = BeautifulSoup(self.page_content, 'html.parser')

    def urls(self) -> set:
        to_exclude = {'/login', '/signup', None, '/idea/apply', '/'}
        prefix_to_avoid = ['#', 'http', '/help']
        urls = set()
        for a in self.soup.find_all('a'):
            url = a.get('href')
            if url in to_exclude or any(map(url.startswith, prefix_to_avoid)):
                continue
            urls.add(url)
        return urls


class VICIdeasParser(Parser):
    def get_ideas_links(self) -> list:
        links = []
        for link in  self.soup.find(id='ideas_body').find_all('a'):
            links.append(link.get('href'))
        return links


class IdeaParser(Parser):
    def get_author_url(self) -> str:
        return self.soup.find('div', attrs={'class': 'idea_by'}).find('a').get('href')

    def get_publication_date(self) -> datetime:
        raw_text = self.soup.find('div', attrs={'class': 'idea_by'}).find('div').text
        text = raw_text[:-3]  # cut "by " from date
        return dateutil.parser.parse(text)

    def get_idea_description(self) -> str:
        return self.soup.find(attrs={'id':'description'}).text

    def get_ticker(self) -> str:
        raise NotImplementedError

    def get_conclusion(self) -> str:
        # class different at every page
        raw_text = self.soup.find_all('p', attrs={'class': 'MsoNormal'})
        if not raw_text:
            pass
        raise NotImplementedError


class AuthorParser(Parser):
    pass


with Driver() as d:
    url_idea = f'{URL_VIC}/idea/INMUNE_BIO_INC/3528803511'
    content = d.get(url_idea)
    parsed = IdeaParser(content)
    print(parsed.urls())


# with Driver() as d:
#     url_vic_ideas = f'{URL_VIC}/ideas'
#     selector = (By.CSS_SELECTOR, "#ideas_body>.row")
#     content = d.get(url_vic_ideas, selector)
#     vip = VICIdeasParser(content)
#     links = vip.get_ideas_links()
#     print(links)
