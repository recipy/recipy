import pytest

from recipyGui import highlight


@pytest.mark.parametrize("c,expected", [
    ({'txt': 'test', 'q': None}, 'test'),
    ({'txt': 'test', 'q': 'test'},
     '<mark class="no-side-padding">test</mark>'),
    ({'txt': None, 'q': None}, 'None'),
])
def test_highlight(c, expected):
    """Test the highlight filter"""

    assert highlight(text=c['txt'], query=c['q']) == expected
