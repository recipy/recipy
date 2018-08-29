import pytest

from IPython.testing.globalipapp import start_ipython


@pytest.fixture(scope='session')
def session_ip():
    return start_ipython()


@pytest.fixture(scope='function')
def notebook(session_ip):
    session_ip.magic('load_ext recipyCommon.magic')
    # Set notebook name to speed up running the tests
    session_ip.run_cell(raw_cell='recipyNotebookName="test_notebook.ipynb"')

    yield session_ip

    session_ip.run_line_magic(magic_name='unload_ext',
                              line='recipyCommon.magic')
    session_ip.run_line_magic(magic_name='reset', line='-f')
