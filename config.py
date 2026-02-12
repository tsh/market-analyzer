import os
import logging

# logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
#                     level=logging.DEBUG, encoding='utf-8')


PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))

DATA_DIR = os.path.join(PROJECT_DIR, 'data')
DATABASE_DIR = os.path.join(DATA_DIR, 'db')
CRAWL_PAGES_DIR = os.path.join(DATA_DIR, 'crawled')
SEC_EDGAR_DATA_DIR = os.path.join(DATA_DIR, 'sec_edgar')
INSTRUMENT_DATA_DIR = os.path.join(DATA_DIR, 'instruments')
YAHOO_CACHE_TICKERS = os.path.join(DATA_DIR, 'yahoo_cache', 'tickers')

LIB_DIR = os.path.join(PROJECT_DIR, 'lib')


# ALPHA_VANTAGE_KEY = os.environ['ALPHA_VANTAGE_KEY']
# SEEKING_ALPHA_KEY = os.environ['SEEKING_ALPHA_KEY']
# POLYGON_IO_KEY = os.environ['POLYGON_IO_KEY']
# FMP_KEY = os.environ['FMP_KEY']  # financialmodelingprep.com
