import pytest

from recipyCommon.tinydb_utils import listsearch


@pytest.mark.parametrize('item', ['test', '/test/test.csv'])
def test_listsearch_flat_list_match(item):
    q = 'test'

    msg = 'listsearch({}, {}) does not return true'.format(q, item)
    assert listsearch(q, item), msg


@pytest.mark.parametrize('item', ['string', '/text/data.csv'])
def test_listsearch_flat_list_no_match(item):
    q = 'test'

    msg = 'listsearch({}, {}) does not return false'.format(q, item)
    assert not listsearch(q, item), msg


@pytest.mark.parametrize('item', [['string', 'hash-for-string'],
                                  ['/text/string.csv', 'another-hash'],
                                  ['blabla', 'string-in-hash']])
def test_listsearch_list_of_lists_match(item):
    q = 'string'

    msg = 'listsearch({}, {}) does not return true'.format(q, item)
    assert listsearch(q, item), msg


@pytest.mark.parametrize('item', [['string', 'hash-for-string'],
                                  ['/text/data.csv', 'another-hash']])
def test_listsearch_list_of_lists_no_match(item):
    q = 'test'

    msg = 'listsearch({}, {}) does not return false'.format(q, item)
    assert not listsearch(q, item), msg


def test_listsearch_empty_item():
    item = []
    q = 'test'

    msg = 'listsearch fails when item=[]'

    assert not listsearch(q, item), msg


def test_listsearch_hash_is_none():
    item = [u'test.csv', None]
    q = 'test'

    msg = 'listsearch fails when hash is None'

    assert listsearch(q, item), msg
