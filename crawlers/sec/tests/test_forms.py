# import os
# import unittest
#
# from edgar import Form4, Relationship
#
# TESTS_DIR = os.path.dirname(os.path.realpath(__file__))
# DATA_DIR = os.path.join(TESTS_DIR, 'fixtures')


# class Form4TestCase(unittest.TestCase):
#     def setUp(self):
#         with open(os.path.join(DATA_DIR, 'mcvt.xml')) as f:
#             self.mcvt = f.read()
#         self.form4 = Form4(self.mcvt)
#
#     def test_is_director(self):
#         self.assertEqual(self.form4.reporting_owner_relationship(), Relationship.DIRECTOR)
