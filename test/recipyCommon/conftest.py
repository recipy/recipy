import pytest

from IPython.testing.globalipapp import start_ipython


@pytest.fixture(scope='session')
def session_ip():
    return start_ipython()


@pytest.fixture(scope='function')
def notebook(session_ip):
    session_ip.magic('load_ext recipyCommon.magic')

    yield session_ip

    session_ip.run_line_magic(magic_name='unload_ext',
                              line='recipyCommon.magic')
    session_ip.run_line_magic(magic_name='reset', line='-f')
