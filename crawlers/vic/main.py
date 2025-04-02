import sys
import os
from pathlib import Path
import json
import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import selenium.common.exceptions as excs
from tinydb import TinyDB, Query, where
from tinydb.storages import JSONStorage


from parsers import IdeaParser, VICIdeasParser, AuthorParser


file = Path(__file__).resolve()
project_dir = file.parents[2]
sys.path.append(str(project_dir))

import config as cfg

logger = logging.getLogger(__name__)

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


class CrawlManager:
    def __init__(self, domain):
        """
        Args:
            domain: what data are we parsing? vic, edgar, etc
                    Also used as prefix for db file, and parent dir for all pages in `data` directory
        """
        self.domain = domain
        self.db = TinyDB(os.path.join(cfg.DATABASE_DIR, f'{domain}_crawl_manager.json'))

    def save_content(self, url, content):
        fname = self.url_to_filename(url)
        with open(os.path.join(cfg.CRAWL_PAGES_DIR, self.domain, fname), 'w') as f:
            f.write(content)
        self.db.insert({'url': url,
                        'file_name': fname,
                        'is_parsed': False})

    @staticmethod
    def url_to_filename(url):
        name = url.split('/')[-1]
        return f"{name}.html"

    def get_not_parsed(self) -> list:
        return self.db.search(where('is_parsed') == False)



def download_pages(manager: CrawlManager):
    q = ['/idea/INMUNE_BIO_INC/3528803511']
    dlq = set()
    seen = set()
    counter = 0
    with Driver() as d:

        while q:
            url = q.pop()
            full_url = f'{URL_VIC}{url}'
            print(counter, url)
            try:
                content = d.get(full_url)
            except excs.InvalidArgumentException as e:
                dlq.add(url)

            manager.save_content(url, content)
            parsed = IdeaParser(content)
            parsed_urls = parsed.urls()

            for parsed_url in parsed_urls:
                if parsed_url in seen or parsed_url in dlq:
                    continue
                q.append(parsed_url)

            print(q)
            counter += 1
            if counter > 1:
                break


def parse_page(manager):
    manager = CrawlManager('vic')
    to_parse = manager.get_not_parsed()
    counter = 0
    while to_parse:
        if counter > 0:
            break
        record = to_parse.pop()
        with open(record.file_name) as f:
            content = ...
        counter +=1

if __name__ == '__main__':


