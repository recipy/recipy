import unittest

from recipyGui.controller import search_database
from recipyCommon import utils


class TestController(unittest.TestCase):
    def setUp(self):
        self.db = utils.open_or_create_db()

    def test_search_database_with_None_query_returns_all(self):
        query = None

        results = search_database(self.db, query=query)

        self.assertEquals(results, self.db.all())

    def test_search_database_with_blank_query_returns_all(self):
        query = ''

        results = search_database(self.db, query=query)

        self.assertEquals(results, self.db.all())

    def test_search_database_with_colon_returns_some_results(self):
        query = ':'

        results = search_database(self.db, query=query)

        self.assertEquals(results, self.db.all())

    def test_search_database_with_nonexistent_result_returns_nothing(self):
        query = 'some_result_that_couldnt_possibly_exist_qwertyuiopoiuytrewq'

        results = search_database(self.db, query=query)

        self.assertEquals(results, [])

    # TODO: try to put in a test for windows style paths like 'C:/Users/blabla'
    # this is difficult to replicate in a test since it only seems to work from the gui entry form
