import os
from os.path import dirname
import unittest
import sys

# allow import from parent
module_dir = dirname(dirname(os.path.abspath(__file__)))
sys.path.append(module_dir)
from edgar import RecentSubmissionParser


TESTS_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(TESTS_DIR, 'data')

class TestParseRecentSubmissions(unittest.TestCase):
    def setUp(self):
        with open(os.path.join(DATA_DIR, 'browse-edgar_recent.atom')) as f:
            self.data = f.read()
        self.parser = RecentSubmissionParser(self.data)

    def test_(self):
        pass

