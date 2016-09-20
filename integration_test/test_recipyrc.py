"""
Tests of recipy configuration, provided via 'recipyrc' configuration files.
"""

import os
import os.path
import shutil
import tempfile
import pytest

from .process import execute
from .environment import get_recipy_dir, get_recipydb, get_recipyrc

test_files = []  # pylint: disable=C0103
test_script = "run_numpy.py"  # pylint: disable=C0103
test_data = "run_numpy.dat"  # pylint: disable=C0103


def run_script():
    execute("python", [test_script])


def append_recipyrc_database(recipyrc, recipydb):
    with open(recipyrc, 'a') as f:
        f.write('[database]\n')
        f.write('path=' + recipydb + '\n')


def setup_module(module):
    """
    py.test-compliant setup function, run when module is loaded,
    creates TMP/run_numpy.py.

    :param functon: Test function
    :type function: function
    """
    global test_script, test_data
    test_script = os.path.join(tempfile.gettempdir(), "run_numpy.py")
    test_data = os.path.join(tempfile.gettempdir(), "run_numpy.dat")
    with open(test_script, "w") as f:
        f.write("import recipy")
        f.write("\n")
        f.write("import numpy as np")
        f.write("\n")
        f.write("data = np.array([list(range(4,8))])")
        f.write("\n")
        f.write("np.savetxt(" +
                str(test_data).__repr__() +
                ", data, delimiter=',')")
        f.write("\n")


def teardown_module(module):
    """
    py.test-compliant setup function, run when module is completed,
    deletes TMP/run_numpy.py and TMP/run_numpy.dat.

    :param functon: Test function
    :type function: function
    """
    if os.path.isfile(test_script):
        os.remove(test_script)
    if os.path.isfile(test_data):
        os.remove(test_data)


def setup_function(function):
    """
    py.test-compliant setup function, run before each test function,
    deletes ~/.recipy.

    :param functon: Test function
    :type function: function
    """
    global test_files
    recipy_dir = get_recipy_dir()
    if os.path.isdir(recipy_dir):
        shutil.rmtree(recipy_dir)
    os.mkdir(recipy_dir)
    test_files = []


def teardown_function(function):
    """
    py.test-compliant teardown function, run after each test function,
    deletes files in test_files.

    :param functon: Test function
    :type function: function
    """
    for test_file in test_files:
        if os.path.isfile(test_file):
            os.remove(test_file)


def test_default():
    """
    If neither .recipyrc, recipyrc nor ~/recipyrc exist then test that
    recipy uses its default configuration.
    """
    recipydb = get_recipydb()
    test_files.append(recipydb)
    run_script()
    assert os.path.isfile(recipydb), ("Expected to find " + recipydb)


@pytest.mark.parametrize("recipyrc", [
    get_recipyrc(),
    os.path.join(os.getcwd(), ".recipyrc"),
    os.path.join(os.getcwd(), "recipyrc")])
def test_local_recipyrc(recipyrc):
    """
    If ~/recipy/recipyrc, .recipy or recipyrc are present. then test
    that their configuration is used.

    :param recipyrc: recipyrc file
    :type recipyrc: str or unicode
    """
    test_files.append(recipyrc)
    recipydb = os.path.join(os.getcwd(), "recipyDB.json")
    test_files.append(recipydb)
    append_recipyrc_database(recipyrc, recipydb)
    run_script()
    assert os.path.isfile(recipydb), ("Expected to find " + recipydb)


@pytest.mark.parametrize("recipyrc_files", [
    (os.path.join(os.getcwd(), ".recipyrc"), get_recipyrc()),
    (os.path.join(os.getcwd(), "recipyrc"), get_recipyrc()),
    (os.path.join(os.getcwd(), "recipyrc"),
     os.path.join(os.getcwd(), ".recipyrc"))])
def test_local_recipyrc_precedence(recipyrc_files):
    """
    Test the following scenarios:

    * If both .recipyrc and ~/recipy/recipyrc are present then the
      former's configuration is used.
    * If both recipyrc and ~/recipy/recipyrc are present then the
      former's configuration is used.
    * If both recipyrc and .recipyrc are present then the former's
      configuration is used.

    :param recipyrc_files: two recipyrc files, the former of which is
     expected to take precedence
    :type recipyrc_files: tuple of (str or unicode, str or unicode)
    """
    (recipyrc, ignore_recipyrc) = recipyrc_files

    test_files.append(recipyrc)
    test_files.append(ignore_recipyrc)

    recipydb = os.path.join(os.getcwd(), "recipyDB.json")
    test_files.append(recipydb)
    append_recipyrc_database(recipyrc, recipydb)

    ignore_recipydb = os.path.join(os.getcwd(), "ignoreDB.json")
    test_files.append(ignore_recipydb)
    append_recipyrc_database(ignore_recipyrc, ignore_recipydb)

    run_script()
    assert os.path.isfile(recipydb), ("Expected to find " + recipydb)
    assert not os.path.isfile(ignore_recipydb),\
        ("Did not expect to find " + ignore_recipydb)
