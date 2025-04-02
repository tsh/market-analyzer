import os
import logging

logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    level=logging.DEBUG, encoding='utf-8')


PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))

DATABASE_DIR = os.path.join(PROJECT_DIR, 'data', 'db')
CRAWL_PAGES_DIR = os.path.join(PROJECT_DIR, 'data', 'crawled')

LIB_DIR = os.path.join(PROJECT_DIR, 'lib')

TG_TOKEN = os.environ['TG_TOKEN']

# ALPHA_VANTAGE_KEY = os.environ['ALPHA_VANTAGE_KEY']
# SEEKING_ALPHA_KEY = os.environ['SEEKING_ALPHA_KEY']
# POLYGON_IO_KEY = os.environ['POLYGON_IO_KEY']
# FMP_KEY = os.environ['FMP_KEY']  # financialmodelingprep.com
