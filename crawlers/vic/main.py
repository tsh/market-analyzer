import sys
from pathlib import Path

file = Path(__file__).resolve()
project_dir = file.parents[2]
sys.path.append(str(project_dir))

import config as cfg

url_vic = 'http://valueinvestorsclub.com'
url_vic_ideas = f'{url_vic}/ideas'


fname = 'file.html'
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By



# Configure Chrome options
options = Options()
options.add_argument("--headless=new")
options.add_argument("--window-size=1920,1200")

service = Service()
# service.executable_path = '/lib/chromedriver'

# Initialize the Chrome driver with the specified options

driver = webdriver.Chrome(options=options)
driver.get(url_vic_ideas)
selector = (By.CSS_SELECTOR, "#ideas_body>.row")
wait = WebDriverWait(driver, 10).until(lambda drvr: drvr.find_element(*selector).is_displayed())
# driver.get_screenshot_as_file('test.png')
#
# links = driver.find_element(By.CSS_SELECTOR, '#ideas_body').find_elements(By.TAG_NAME, 'a').get_attribute("href")
# print(links)
with open(fname, 'w') as f:
    f.write(driver.page_source)
# It's a good practice to close the driver when you're finished
# driver.quit()

# with open(fname, 'r') as f:
#     content = f.read()
#
# from bs4 import BeautifulSoup, SoupStrainer
#
# for link in  BeautifulSoup(content, 'html.parser').find(id='ideas_body').find_all('a'):
#     print(url_vic + link.get('href'))
