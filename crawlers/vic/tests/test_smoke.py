import os

import pytest

# from crawlers.vic.driver import SeleniumDriver
# from crawlers.vic.parsers import IdeaParser

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

URL_VIC = 'http://valueinvestorsclub.com'
IDEA_URL = 'idea/INMUNE_BIO_INC/3528803511'

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time

from pathlib import Path
home = Path.home()
profile = f'{home}/.config/google-chrome'  # MAKE DYNAMIC

url = f'{URL_VIC}/{IDEA_URL}'
options = Options()
# options.add_argument("--headless=new")
options.add_argument("--window-size=1920,1200")
# options.add_argument(f"--user-data-dir={profile}")
# options.add_argument(r'--profile-directory=Default') #e.g. Profile 3
import undetected_chromedriver as uc
driver = uc.Chrome(headless=False,use_subprocess=False)
# driver = webdriver.Chrome(options=options)
driver.get(f'{URL_VIC}/login')
time.sleep(4)
driver.find_elements(by=By.XPATH ,value='/html/body/div/div[1]/form/div[2]/input')[0].send_keys('tsh')
driver.find_elements(by=By.XPATH ,value='/html/body/div/div[1]/form/div[3]/input')[0].send_keys()  # TODO: add me
time.sleep(20)
driver.get(url)
time.sleep(3)
with open('page.html', 'w') as f:
    f.write(driver.page_source)



# @pytest.mark.smoke
# def test_vic_idea_get_ticker():
#     url = f'{URL_VIC}/{IDEA_URL}'
#     with SeleniumDriver() as d:
#         content = d.get(url)
#     parsed = IdeaParser(content)
#     parsed_urls = parsed.urls()
#     print('test', parsed_urls)
# 


