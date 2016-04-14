from nose.tools import assert_true, assert_false

from recipyCommon.tinydb_utils import listsearch


def test_listsearch_flat_list_match():
    q = 'test'
    l = ['test', '/test/test.csv']

    for item in l:
        msg = 'listsearch({}, {}) does not return true'.format(q, item)
        yield assert_true, listsearch(q, item), msg


def test_listsearch_flat_list_no_match():
    q = 'test'
    l = ['string', '/text/data.csv']

    for item in l:
        msg = 'listsearch({}, {}) does not return false'.format(q, item)
        yield assert_false, listsearch(q, item), msg


def test_listsearch_list_of_lists_match():
    q = 'string'
    l = [['string', 'hash-for-string'], ['/text/string.csv', 'another-hash'],
         ['blabla', 'string-in-hash']]

    for item in l:
        msg = 'listsearch({}, {}) does not return true'.format(q, item)
        yield assert_true, listsearch(q, item), msg


def test_listsearch_list_of_lists_no_match():
    q = 'test'
    l = [['string', 'hash-for-string'], ['/text/data.csv', 'another-hash']]

    for item in l:
        msg = 'listsearch({}, {}) does not return false'.format(q, item)
        yield assert_false, listsearch(q, item), msg
