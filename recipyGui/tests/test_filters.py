from nose.tools import assert_equal
from recipyGui import highlight

def test_highlight():
    """Test the highlight filter"""
    cases = [
        {'txt': 'test', 'q': None, 'out': 'test'},
        {'txt': 'test', 'q': 'test', 'out': '<mark class="no-side-padding">test</mark>'},
        {'txt': None, 'q': None, 'out': None}
    ]

    for c in cases:
        yield assert_equal, highlight(text=c['txt'], query=c['q']), c['out']
