import pytest
import os

from IPython.testing.globalipapp import get_ipython

# For some reason numpy is already in sys.modules of the interactive shell
# fixture. This means numpy won't be patched, and therefore, can't be used for
# testing the magic. In an actual notebook, numpy can be patched.


@pytest.fixture
def notebook():
    ip = get_ipython()
    ip.magic('load_ext recipyCommon.magic')

    return ip


def test_magic_recipyOff_without_recipyOn(notebook):
    with pytest.warns(RuntimeWarning):
        notebook.run_line_magic(magic_name='recipyOff', line='')
