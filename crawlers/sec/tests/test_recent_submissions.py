# import datetime
# import os
# from os.path import dirname
# import unittest
# import sys

# allow import from parent
# module_dir = dirname(dirname(os.path.abspath(__file__)))
# sys.path.append(module_dir)
# from edgar import RecentSubmissionAtomParser
#
#
# TESTS_DIR = os.path.dirname(os.path.realpath(__file__))
# DATA_DIR = os.path.join(TESTS_DIR, 'fixtures')
#
# class TestParseRecentSubmissions(unittest.TestCase):
#     def setUp(self):
#         with open(os.path.join(DATA_DIR, 'browse-edgar_recent.atom')) as f:
#             self.data = f.read()
#         self.parser = RecentSubmissionAtomParser(self.data)
#
#     def test_general(self):
#         assert self.parser.time.date() == datetime.date(2023, 1, 7)
#         assert len(self.parser.entries) == 10
#
#     def test_record(self):
#         assert 'Name1 lastname' in self.parser.entries[0]['title']
#
