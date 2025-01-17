import os

PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(PROJECT_DIR, 'data')
CRAWL_PAGES_DIR = os.path.join(DATA_DIR, 'crawled')
LIB_DIR = os.path.join(PROJECT_DIR, 'lib')

TG_TOKEN = os.environ['TG_TOKEN']

# ALPHA_VANTAGE_KEY = os.environ['ALPHA_VANTAGE_KEY']
# SEEKING_ALPHA_KEY = os.environ['SEEKING_ALPHA_KEY']
# POLYGON_IO_KEY = os.environ['POLYGON_IO_KEY']
# FMP_KEY = os.environ['FMP_KEY']  # financialmodelingprep.com
