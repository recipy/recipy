from nose.tools import assert_equal

from recipyCommon import libraryversions
from recipy.__init__ import __version__


def test_get_version_recipy():
    assert_equal(libraryversions.get_version('recipy'), 'recipy v{}'.format(__version__))


def test_get_version_unknown_library():
    assert_equal(libraryversions.get_version('unknown'), 'unknown v?')
