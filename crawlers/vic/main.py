import sys
from pathlib import Path

from bs4 import BeautifulSoup, SoupStrainer
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
URL_VIC_IDEAS = f'{URL_VIC}/ideas'




class Driver:
    def __init__(self):
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1200")
        # service = Service()
        # service.executable_path = '/lib/chromedriver'
        self.driver = webdriver.Chrome(options=options)

    def get(self, url, wait_selector: tuple, wait_timeout=6) -> str:
        self.driver.get(url)
        WebDriverWait(self.driver, wait_timeout).until(lambda drver: drver.find_element(*wait_selector).is_displayed())
        return self.driver.page_source

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()


class VICIdeasParser:
    def __init__(self, page_content: str):
        self.page_content = page_content

    def get_ideas_links(self) -> list:
        links = []
        for link in  BeautifulSoup(self.page_content, 'html.parser').find(id='ideas_body').find_all('a'):
            links.append(link.get('href'))
        return links


selector = (By.CSS_SELECTOR, "#ideas_body>.row")
with Driver() as d:
    content = d.get(URL_VIC_IDEAS, selector)
    vip = VICIdeasParser(content)
    links = vip.get_ideas_links()
    print(links)
