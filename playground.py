# import requests
#
url_vic = 'http://valueinvestorsclub.com'
url_vic_ideas = f'{url_vic}/ideas'

url_wsb = 'https://www.reddit.com/r/wallstreetbets/'
#
# resp = requests.get(url)
# resp.raise_for_status()
# print(resp.content)
# print('==============================\n')
#

fname = 'file.html'
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By



# Configure Chrome options
# options = Options()
# options.add_argument("--headless=new")
# options.add_argument("--window-size=1920,1200")
# 
# service = Service()
# service.executable_path = '/lib/chromedriver'
# 
# # Initialize the Chrome driver with the specified options
# 
# driver = webdriver.Chrome(options=options)
# driver.get(url_vic_ideas)
# ideas = driver.find_element(By.CSS_SELECTOR, "#ideas_body>.row")
# 
# WebDriverWait(driver, 5).until(lambda x: ideas.is_displayed() )
# 
# links = ideas.find_elements(By.TAG_NAME, 'a')
# with open(fname, 'w') as f:
#     f.write(driver.page_source)
# It's a good practice to close the driver when you're finished
# driver.quit()

with open(fname, 'r') as f:
    content = f.read()

from bs4 import BeautifulSoup, SoupStrainer

for link in  BeautifulSoup(content, 'html.parser').find(id='ideas_body').find_all('a'):
    print(url_vic + link.get('href'))
