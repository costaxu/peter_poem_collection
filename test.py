import collection
import constants
import unittest


class test_collection(unittest.TestCase):
    def setUp(self):
        print("___________________________________init unit test____________________________________________________")

    def tearDown(self):
        print("___________________________________done______________________________________________________________")

    def test_fetch_works(self):
        collection.fetch_works(constants.member_id, 1)

