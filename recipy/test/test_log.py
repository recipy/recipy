import os
import unittest
import mock

from recipy.log import open_or_create_db, log_values, log_init


TEST_DB_PATH = os.path.expanduser('~/.recipy/test_recipyDB.json')


def open_or_create_test_db():
    return open_or_create_db(TEST_DB_PATH)


class TestLog(unittest.TestCase):
    def setUp(self):
        """ Invoke log_init with the test database, so as not to interfere with the regular database """
        with mock.patch('recipy.log.open_or_create_db', open_or_create_test_db):
            log_init()

    def test_log_values_single_dictionary(self):
        with mock.patch('recipy.log.open_or_create_db', open_or_create_test_db):
            log_values({'a': 1, 'b': 2})

        db = open_or_create_test_db()
        last_entry = db.all()[-1]

        self.assertIn('custom-values', last_entry)
        self.assertEquals(last_entry['custom-values'], {'a': 1, 'b': 2})

    def test_log_values_multiple_dictionaries(self):
        with mock.patch('recipy.log.open_or_create_db', open_or_create_test_db):
            log_values({'a': 1, 'b': 2})
            log_values({'a': 3, 'b': 4})
            log_values({'c': 5, 'd': 6})

        db = open_or_create_test_db()
        last_entry = db.all()[-1]

        self.assertIn('custom-values', last_entry)
        self.assertEquals(last_entry['custom-values'], {'a': 3, 'b': 4, 'c': 5, 'd': 6})

    def test_log_values_keyword_arguments(self):
        with mock.patch('recipy.log.open_or_create_db', open_or_create_test_db):
            log_values(cat=1, dog=2)

        db = open_or_create_test_db()
        last_entry = db.all()[-1]

        self.assertIn('custom-values', last_entry)
        self.assertEquals(last_entry['custom-values'], {'cat': 1, 'dog': 2})

    def test_log_values_dict_and_keyword_arguments(self):
        with mock.patch('recipy.log.open_or_create_db', open_or_create_test_db):
            log_values({'bananas': 3, 'pears': 4}, apples=1, oranges=2)

        db = open_or_create_test_db()
        last_entry = db.all()[-1]

        self.assertIn('custom-values', last_entry)
        self.assertEquals(last_entry['custom-values'], {'bananas': 3, 'pears': 4, 'apples':1, 'oranges':2})
